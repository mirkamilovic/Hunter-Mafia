# -*- coding: utf-8 -*-
"""
payments_idempotent.py — Telegram Stars to'lovlari uchun idempotent + atomik qatlam.

B bosqich (xavfsizlik). Bu modul ATAYLAB telebot'ga bog'liq EMAS: faqat sqlite3 va
standart kutubxona. Botning asosiy fayli unga oddiy ma'lumotlar (charge_id, summa,
payload) uzatadi, modul esa DB bilan ishlaydi.

Asosiy kafolatlar
-----------------
1. IDEMPOTENCY. Har bir to'lov Telegram bergan `telegram_payment_charge_id` bo'yicha
   `payments` jadvalida YAGONA (UNIQUE) qator sifatida qayd etiladi. Bir xil
   charge_id ikkinchi marta kelsa — hech narsa berilmaydi.
2. ATOMIKLIK. "Mahsulot/balansni berish" + "to'lovni 'granted' deb belgilash" +
   (oyning homiysi hisobi, referal bonus) BITTA SQLite tranzaksiyasida bajariladi.
   Xatolikda hammasi ROLLBACK bo'ladi; to'lov qatori 'received' holatida qoladi
   (to'lov YO'QOLMAYDI) va keyin qayta uriniladi (`retry_pending`).
3. ESKI BAZALAR. Migratsiya faqat `CREATE TABLE/INDEX IF NOT EXISTS` va
   `INSERT OR IGNORE` ishlatadi. Hech narsa DROP/DELETE/qayta yaratilmaydi.
4. Telegram tasdiqlamagan to'lov hech qachon berilmaydi: berish FAQAT
   `successful_payment` xabaridan keyin; pre-checkout esa alohida `validate_precheckout`
   orqali tekshiriladi va xato bo'lsa ok=False qaytariladi (fail-closed).

Eslatma: grant mantiqi (balans, ELITE, ism uslubi/rangi, geroy, kosmetika) bu yerda
bitta tranzaksiya ichida SQL bilan qayta bajariladi, chunki botdagi eski funksiyalar
(add_balance, grant_elite_days, ...) har biri alohida `commit()` qiladi va
tranzaksiyaga o'ralmaydi.
"""
import json
import logging
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Collection, Dict, Mapping, Optional, Tuple

_log = logging.getLogger("payments_idempotent")

SCHEMA_KEY = "payments_schema_v1"
MAX_ATTEMPTS = 5

# to'lov holatlari
ST_RECEIVED = "received"        # qayd etildi, hali berilmadi (yoki berish xato berdi — qayta uriniladi)
ST_GRANTED = "granted"          # berildi (atomik)
ST_REVIEW = "needs_review"      # to'lov bor, lekin avtomatik berib bo'lmaydi (qo'lda hal qilinadi)
ST_REFUNDED = "refunded"        # owner /refund qildi
ST_LEGACY = "legacy"            # eski `last_charge_*` yozuvidan ko'chirilgan (qayta berilmaydi)
ST_REJECTED = "rejected"        # noto'g'ri to'lov (valyuta/summa/identifikator yo'q)

_FINAL = {ST_GRANTED, ST_REVIEW, ST_REFUNDED, ST_LEGACY, ST_REJECTED}


class PayloadError(ValueError):
    """invoice_payload noto'g'ri yoki noma'lum."""


class NeedsReview(Exception):
    """To'lov haqiqiy, lekin avtomatik berib bo'lmaydi — qo'lda hal qilish kerak."""


# ------------------------------------------------------------------ payload
def _int(s: str, what: str) -> int:
    if not isinstance(s, str) or not s.isdigit() or len(s) > 18:
        raise PayloadError(f"{what} butun son emas")
    return int(s)


def parse_payload(payload: Any) -> Dict[str, Any]:
    """`kind_uid_...` formatini qat'iy tahlil qiladi.
    MUHIM: kalitlarda '_' bo'lishi mumkin (bold_serif, double_struck, sans_bold) —
    shuning uchun uchinchi qism `split("_", 2)` bilan olinadi. (Eski kodda
    `_, a, b = payload.split("_")` bunday kalitlarda ValueError berib, to'lovni
    yo'qotardi.)"""
    if not isinstance(payload, str) or not payload or len(payload) > 128:
        raise PayloadError("payload bo'sh yoki juda uzun")
    kind, _, rest = payload.partition("_")
    if kind in ("namestyle", "namecolor", "herobuy"):
        uid_s, sep, key = rest.partition("_")
        if not sep or not key:
            raise PayloadError("kalit yo'q")
        return {"kind": kind, "uid": _int(uid_s, "uid"), "key": key}
    if kind in ("hc", "diamondbuy", "dollarbuy"):
        uid_s, sep, qty_s = rest.partition("_")
        if not sep:
            raise PayloadError("miqdor yo'q")
        qty = _int(qty_s, "qty")
        if qty <= 0:
            raise PayloadError("qty > 0 bo'lishi kerak")
        return {"kind": kind, "uid": _int(uid_s, "uid"), "qty": qty}
    if kind == "elitepay":
        uid_s, sep, days_s = rest.partition("_")
        if not sep:
            raise PayloadError("kun yo'q")
        days = _int(days_s, "days")
        if days <= 0:
            raise PayloadError("days > 0 bo'lishi kerak")
        return {"kind": kind, "uid": _int(uid_s, "uid"), "days": days}
    if kind == "elitegift":
        parts = rest.split("_")
        if len(parts) != 3:
            raise PayloadError("elitegift 3 qismli bo'lishi kerak")
        days = _int(parts[2], "days")
        if days <= 0:
            raise PayloadError("days > 0 bo'lishi kerak")
        return {"kind": kind, "uid": _int(parts[0], "buyer"), "target": _int(parts[1], "target"), "days": days}
    if kind == "herolv":
        uid_s, sep, lvl_s = rest.partition("_")
        if not sep:
            raise PayloadError("daraja yo'q")
        return {"kind": kind, "uid": _int(uid_s, "uid"), "level": _int(lvl_s, "level")}
    if kind == "cosmetic":
        return {"kind": kind, "uid": None, "cosmetic_id": _int(rest, "cosmetic_id")}
    raise PayloadError(f"noma'lum to'lov turi: {kind!r}")


# ------------------------------------------------------------------ config / result
@dataclass
class PaymentConfig:
    """Bot tomonidan beriladigan qaramliklar (narxlar va kataloglar bitta joyda — botda — qoladi)."""
    expected_stars: Callable[[Dict[str, Any]], Optional[int]]
    """parsed payload -> kerakli Stars narxi; None = payload yaroqsiz (qty chegarasi, noma'lum kalit...)."""
    name_styles: Mapping[str, int] = field(default_factory=dict)      # key -> kunlar
    name_colors: Mapping[str, int] = field(default_factory=dict)      # key -> kunlar
    hero_keys: Collection[str] = field(default_factory=set)
    hero_max_level: int = 3
    hero_compensation: Callable[[str, Optional[str], Optional[int]], int] = lambda kind, hero_key, level: 0
    """(kind 'herobuy'|'herolv', hero_key, level) -> qaytariladigan 💎 (0 = yo'q)."""
    referral_bonus: Any = 0   # int YOKI callable() -> int (botda konstanta keyinroq e'lon qilinadi)
    require_payer_match: bool = True
    now: Callable[[], float] = time.time


@dataclass
class PaymentResult:
    status: str                         # granted | duplicate | pending | needs_review | rejected
    charge_id: Optional[str] = None
    db_status: Optional[str] = None
    newly_granted: bool = False         # FAQAT shu chaqiruv berdimi (xabar yuborish shartiga)
    kind: Optional[str] = None
    uid: Optional[int] = None
    info: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


# ------------------------------------------------------------------ store
_DDL = (
    """CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        charge_id TEXT NOT NULL UNIQUE,
        provider_charge_id TEXT,
        user_id INTEGER NOT NULL,
        kind TEXT,
        payload TEXT NOT NULL DEFAULT '',
        currency TEXT,
        amount INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 0,
        error TEXT,
        note TEXT,
        received_at REAL NOT NULL,
        granted_at REAL,
        updated_at REAL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_payments_user ON payments(user_id, id)",
    "CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status)",
)


class PaymentStore:
    def __init__(self, conn: sqlite3.Connection, lock, cfg: PaymentConfig):
        self.conn = conn
        self.lock = lock if lock is not None else threading.RLock()
        self.cfg = cfg

    # -------------------------------------------------------------- migration
    def migrate(self) -> Dict[str, Any]:
        """Qo'shimcha (additive) migratsiya. Mavjud jadval/ma'lumotlarga TEGMAYDI.
        1) payments jadvali + indekslar (IF NOT EXISTS)
        2) eski `bot_settings.last_charge_<uid>` yozuvlarini 'legacy' sifatida ko'chiradi
           (INSERT OR IGNORE) — shu charge_id qayta kelsa, qayta berilmaydi."""
        with self.lock:
            self._begin()
            try:
                for ddl in _DDL:
                    self.conn.execute(ddl)
                copied = 0
                has_settings = self.conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='bot_settings'").fetchone()
                if has_settings:
                    rows = self.conn.execute(
                        "SELECT key, value FROM bot_settings WHERE key LIKE 'last\\_charge\\_%' ESCAPE '\\'").fetchall()
                    now = self.cfg.now()
                    for key, value in rows:
                        uid_s = key[len("last_charge_"):]
                        if not value or not uid_s.lstrip("-").isdigit():
                            continue
                        cur = self.conn.execute(
                            "INSERT OR IGNORE INTO payments (charge_id, user_id, kind, payload, currency, amount, "
                            "status, note, received_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (str(value), int(uid_s), "legacy", "", "XTR", 0, ST_LEGACY,
                             "bot_settings.last_charge_* dan ko'chirildi", now, now))
                        copied += cur.rowcount
                self.conn.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES (?, ?)",
                                  (SCHEMA_KEY, "1")) if has_settings else None
                self.conn.commit()
                return {"ok": True, "legacy_copied": copied}
            except Exception:
                self.conn.rollback()
                raise

    # -------------------------------------------------------------- tx helpers
    def _begin(self):
        if self.conn.in_transaction:
            # db_lock ostida hamma commit qiladi; ochiq tranzaksiya bo'lsa — uni yopamiz
            # (botdagi mavjud xatti-harakat bilan bir xil), keyin toza BEGIN.
            self.conn.commit()
        self.conn.execute("BEGIN IMMEDIATE")

    def get(self, charge_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            cur = self.conn.execute("SELECT * FROM payments WHERE charge_id=?", (charge_id,))
            row = cur.fetchone()
            if not row:
                return None
            return dict(zip([d[0] for d in cur.description], row))

    # -------------------------------------------------------------- pre-checkout
    def validate_precheckout(self, *, payer_id: int, currency: str, total_amount: int,
                             payload: Any) -> Tuple[bool, Optional[str]]:
        """Faqat tekshiradi, DB'ga YOZMAYDI. (True, None) yoki (False, foydalanuvchiga xabar).
        Istisno bo'lsa — chaqiruvchi fail-closed (ok=False) qilishi kerak."""
        try:
            p = parse_payload(payload)
        except PayloadError:
            return False, "To'lov ma'lumoti noto'g'ri. Iltimos, xaridni qaytadan boshlang."
        if currency != "XTR":
            return False, "Faqat Telegram Stars (XTR) qabul qilinadi."
        if not isinstance(total_amount, int) or total_amount <= 0:
            return False, "To'lov summasi noto'g'ri."
        uid = p.get("uid")
        if self.cfg.require_payer_match and uid is not None and uid != payer_id:
            return False, "Bu to'lov havolasi boshqa foydalanuvchi uchun yaratilgan."
        kind = p["kind"]
        with self.lock:
            if not self._user_exists(payer_id):
                return False, "Avval botda /start bosing."
            if kind == "cosmetic":
                row = self.conn.execute(
                    "SELECT price, currency, stock, sold, active FROM cosmetics WHERE id=?",
                    (p["cosmetic_id"],)).fetchone()
                if not row:
                    return False, "Bunday kosmetika topilmadi."
                price, cur_, stock, sold, active = row
                if not active or sold >= stock:
                    return False, "Bu buyum sotuvdan tugagan."
                if cur_ != "stars":
                    return False, "Bu buyum Stars bilan sotilmaydi."
                if self.conn.execute("SELECT 1 FROM user_cosmetics WHERE user_id=? AND cosmetic_id=?",
                                     (payer_id, p["cosmetic_id"])).fetchone():
                    return False, "Bu buyum sizda allaqachon bor."
                if total_amount < price:
                    return False, "Narx o'zgargan. Xaridni qaytadan boshlang."
                return True, None
            expected = self.cfg.expected_stars(p)
            if expected is None:
                return False, "Bunday mahsulot mavjud emas yoki miqdor noto'g'ri."
            if total_amount < expected:
                return False, "Narx o'zgargan. Xaridni qaytadan boshlang."
            if kind == "namestyle" and p["key"] not in self.cfg.name_styles:
                return False, "Bunday ism uslubi yo'q."
            if kind == "namecolor" and p["key"] not in self.cfg.name_colors:
                return False, "Bunday ism rangi yo'q."
            if kind == "elitegift" and not self._user_exists(p["target"]):
                return False, "Sovg'a oluvchi botda topilmadi."
            if kind == "herobuy":
                if p["key"] not in self.cfg.hero_keys:
                    return False, "Bunday geroy yo'q."
                if self.conn.execute("SELECT 1 FROM heroes WHERE user_id=?", (payer_id,)).fetchone():
                    return False, "Sizda allaqachon geroy bor."
            if kind == "herolv":
                row = self.conn.execute("SELECT level FROM heroes WHERE user_id=?", (payer_id,)).fetchone()
                if not row or row[0] != p["level"] - 1 or p["level"] > self.cfg.hero_max_level:
                    return False, "Geroy darajasi o'zgargan. Qaytadan urinib ko'ring."
            return True, None

    def _user_exists(self, uid: int) -> bool:
        return self.conn.execute("SELECT 1 FROM users WHERE user_id=?", (uid,)).fetchone() is not None

    # -------------------------------------------------------------- successful payment
    def process_successful_payment(self, *, charge_id: Any, payer_id: int, currency: str,
                                   total_amount: int, payload: Any,
                                   provider_charge_id: Optional[str] = None) -> PaymentResult:
        """Telegram `successful_payment` xabari uchun. Idempotent va atomik."""
        if not isinstance(charge_id, str) or not charge_id.strip():
            # Identifikatorsiz to'lovni dedupe qilib bo'lmaydi — hech narsa BERILMAYDI.
            return PaymentResult("rejected", None, error="charge_id yo'q")
        charge_id = charge_id.strip()
        now = self.cfg.now()
        # 1-bosqich: qayd etish (UNIQUE). Alohida tranzaksiya — to'lov har qanday holatda saqlanadi.
        with self.lock:
            self._begin()
            try:
                kind = None
                try:
                    kind = parse_payload(payload)["kind"]
                except PayloadError:
                    pass
                cur = self.conn.execute(
                    "INSERT OR IGNORE INTO payments (charge_id, provider_charge_id, user_id, kind, payload, "
                    "currency, amount, status, received_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (charge_id, provider_charge_id, int(payer_id), kind, str(payload or "")[:128],
                     currency, int(total_amount or 0), ST_RECEIVED, now, now))
                self.conn.commit()
                is_new = cur.rowcount > 0
            except Exception:
                self.conn.rollback()
                raise
        row = self.get(charge_id)
        if row and row["status"] in _FINAL:
            return PaymentResult("duplicate", charge_id, row["status"], False, row.get("kind"), row["user_id"])
        return self._apply(charge_id, payer_id, currency, total_amount, payload, is_new)

    def retry_pending(self, limit: int = 50) -> list:
        """'received' holatida qolgan (berish xato bergan) to'lovlarni qayta uradi. Natijalar ro'yxati."""
        with self.lock:
            rows = self.conn.execute(
                "SELECT charge_id, user_id, currency, amount, payload FROM payments "
                "WHERE status=? AND attempts<? ORDER BY id LIMIT ?", (ST_RECEIVED, MAX_ATTEMPTS, limit)).fetchall()
        out = []
        for charge_id, uid, currency, amount, payload in rows:
            out.append(self._apply(charge_id, uid, currency, amount, payload, False))
        return out

    def mark_refunded(self, charge_id: str) -> bool:
        with self.lock:
            self._begin()
            try:
                cur = self.conn.execute(
                    "UPDATE payments SET status=?, updated_at=? WHERE charge_id=? AND status<>?",
                    (ST_REFUNDED, self.cfg.now(), charge_id, ST_REFUNDED))
                self.conn.commit()
                return cur.rowcount > 0
            except Exception:
                self.conn.rollback()
                raise

    def latest_charge_for(self, uid: int) -> Optional[str]:
        with self.lock:
            row = self.conn.execute(
                "SELECT charge_id FROM payments WHERE user_id=? AND status IN (?,?,?,?) ORDER BY id DESC LIMIT 1",
                (uid, ST_GRANTED, ST_REVIEW, ST_RECEIVED, ST_LEGACY)).fetchone()
            return row[0] if row else None

    # -------------------------------------------------------------- 2-bosqich: atomik berish
    def _apply(self, charge_id, payer_id, currency, total_amount, payload, is_new) -> PaymentResult:
        info: Dict[str, Any] = {}
        p: Dict[str, Any] = {}
        with self.lock:
            self._begin()
            try:
                # "da'vo" — faqat 'received' bo'lsa. Parallel/takroriy chaqiruv bu yerda to'xtaydi.
                claim = self.conn.execute(
                    "UPDATE payments SET status=?, granted_at=?, updated_at=? WHERE charge_id=? AND status=?",
                    (ST_GRANTED, self.cfg.now(), self.cfg.now(), charge_id, ST_RECEIVED))
                if claim.rowcount != 1:
                    self.conn.rollback()
                    row = self.get(charge_id)
                    return PaymentResult("duplicate", charge_id, row and row["status"], False,
                                         row and row.get("kind"), row and row["user_id"])
                p = parse_payload(payload)               # PayloadError -> pastda
                self._check_amount(p, currency, total_amount, payer_id)
                self._grant(p, payer_id, info)
                self._track_monthly_spend(payer_id, total_amount)
                inviter = self._referral_bonus(payer_id)
                if inviter is not None:
                    info["referral_inviter"] = inviter
                self.conn.commit()
                return PaymentResult("granted", charge_id, ST_GRANTED, True, p["kind"], payer_id, info)
            except (NeedsReview, PayloadError) as e:
                self.conn.rollback()
                return self._park(charge_id, ST_REVIEW, str(e), p, payer_id)
            except Exception as e:  # noqa: BLE001 — har qanday xato: ROLLBACK + qayta urinish uchun saqlash
                self.conn.rollback()
                _log.exception("to'lovni berishda xato (charge_id=%s)", charge_id)
                return self._record_failure(charge_id, repr(e), p, payer_id)

    def _park(self, charge_id, status, reason, p, payer_id=None) -> PaymentResult:
        self._begin()
        try:
            self.conn.execute("UPDATE payments SET status=?, error=?, attempts=attempts+1, updated_at=? "
                              "WHERE charge_id=?", (status, reason[:300], self.cfg.now(), charge_id))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return PaymentResult("needs_review", charge_id, status, False, p.get("kind"), payer_id, error=reason)

    def _record_failure(self, charge_id, err, p, payer_id=None) -> PaymentResult:
        self._begin()
        try:
            self.conn.execute("UPDATE payments SET attempts=attempts+1, error=?, updated_at=? WHERE charge_id=?",
                              (err[:300], self.cfg.now(), charge_id))
            attempts = self.conn.execute("SELECT attempts FROM payments WHERE charge_id=?", (charge_id,)).fetchone()[0]
            if attempts >= MAX_ATTEMPTS:
                self.conn.execute("UPDATE payments SET status=? WHERE charge_id=?", (ST_REVIEW, charge_id))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        status = "needs_review" if attempts >= MAX_ATTEMPTS else "pending"
        return PaymentResult(status, charge_id, ST_REVIEW if status == "needs_review" else ST_RECEIVED,
                             False, p.get("kind"), payer_id, error=err)

    # -------------------------------------------------------------- grant (tranzaksiya ichida, commit YO'Q)
    def _check_amount(self, p, currency, total_amount, payer_id):
        if currency != "XTR":
            raise NeedsReview(f"valyuta XTR emas: {currency!r}")
        if not isinstance(total_amount, int) or total_amount <= 0:
            raise NeedsReview(f"summa noto'g'ri: {total_amount!r}")
        uid = p.get("uid")
        if self.cfg.require_payer_match and uid is not None and uid != payer_id:
            raise NeedsReview("to'lovchi payload egasi bilan mos emas")
        if p["kind"] == "cosmetic":
            row = self.conn.execute("SELECT price FROM cosmetics WHERE id=?", (p["cosmetic_id"],)).fetchone()
            expected = row[0] if row else None
        else:
            expected = self.cfg.expected_stars(p)
        if expected is None:
            raise NeedsReview("mahsulot/miqdor yaroqsiz")
        if total_amount < expected:
            raise NeedsReview(f"kam to'langan: {total_amount} < {expected}")

    def _add_balance(self, uid, *, dollar=0, diamond=0, coin=0):
        cur = self.conn.execute(
            "UPDATE users SET dollar=MAX(0,dollar+?), diamond=MAX(0,diamond+?), coin=MAX(0,coin+?) WHERE user_id=?",
            (dollar, diamond, coin, uid))
        if cur.rowcount != 1:
            raise NeedsReview(f"foydalanuvchi {uid} bazada yo'q")

    def _charges(self, uid) -> dict:
        row = self.conn.execute("SELECT charges FROM users WHERE user_id=?", (uid,)).fetchone()
        if row is None:
            raise NeedsReview(f"foydalanuvchi {uid} bazada yo'q")
        raw = row[0]
        if raw in (None, ""):
            return {}
        try:
            val = json.loads(raw)
        except Exception as e:
            raise RuntimeError(f"charges JSON buzuq (uid={uid}): {e}") from e
        if not isinstance(val, dict):
            raise RuntimeError(f"charges dict emas (uid={uid})")
        return val

    def _set_charges(self, uid, ch):
        self.conn.execute("UPDATE users SET charges=? WHERE user_id=?", (json.dumps(ch), uid))

    def _grant_elite(self, uid, days) -> float:
        ch = self._charges(uid)
        now = self.cfg.now()
        cur_until = ch.get("vip_until", 0) or 0
        base = cur_until if cur_until and cur_until > now else now
        ch["vip_until"] = base + days * 86400
        self._set_charges(uid, ch)
        return ch["vip_until"]

    def _grant_timed(self, uid, field_name, key, days):
        ch = self._charges(uid)
        now = self.cfg.now()
        until = ch.get(field_name + "_until", 0) or 0
        base = until if (ch.get(field_name) == key and until > now) else now
        ch[field_name] = key
        ch[field_name + "_until"] = base + days * 86400
        self._set_charges(uid, ch)
        return ch[field_name + "_until"]

    def _grant(self, p, payer_id, info):
        kind = p["kind"]
        info["kind"] = kind
        if kind == "hc":
            self._add_balance(p["uid"], coin=p["qty"]); info.update(uid=p["uid"], qty=p["qty"])
        elif kind == "diamondbuy":
            self._add_balance(p["uid"], diamond=p["qty"]); info.update(uid=p["uid"], qty=p["qty"])
        elif kind == "dollarbuy":
            self._add_balance(p["uid"], dollar=p["qty"]); info.update(uid=p["uid"], qty=p["qty"])
        elif kind == "elitepay":
            info.update(uid=p["uid"], days=p["days"], new_until=self._grant_elite(p["uid"], p["days"]))
        elif kind == "elitegift":
            info.update(uid=p["uid"], buyer=p["uid"], target=p["target"], days=p["days"],
                        new_until=self._grant_elite(p["target"], p["days"]))
        elif kind == "namestyle":
            if p["key"] not in self.cfg.name_styles:
                raise NeedsReview(f"ism uslubi topilmadi: {p['key']}")
            days = self.cfg.name_styles[p["key"]]
            self._grant_timed(p["uid"], "name_style", p["key"], days)
            info.update(uid=p["uid"], key=p["key"], days=days)
        elif kind == "namecolor":
            if p["key"] not in self.cfg.name_colors:
                raise NeedsReview(f"ism rangi topilmadi: {p['key']}")
            days = self.cfg.name_colors[p["key"]]
            self._grant_timed(p["uid"], "name_color", p["key"], days)
            info.update(uid=p["uid"], key=p["key"], days=days)
        elif kind == "herobuy":
            if p["key"] not in self.cfg.hero_keys:
                raise NeedsReview(f"geroy topilmadi: {p['key']}")
            cur = self.conn.execute(
                "INSERT OR IGNORE INTO heroes (user_id, hero_key, level, acquired_at) VALUES (?,?,1,?)",
                (p["uid"], p["key"], self.cfg.now()))
            info.update(uid=p["uid"], key=p["key"])
            if cur.rowcount > 0:
                info["hero_granted"] = True
            else:
                comp = int(self.cfg.hero_compensation("herobuy", p["key"], None) or 0)
                if comp:
                    self._add_balance(p["uid"], diamond=comp)
                info.update(hero_granted=False, compensation=comp)
        elif kind == "herolv":
            row = self.conn.execute("SELECT hero_key, level FROM heroes WHERE user_id=?", (p["uid"],)).fetchone()
            new_level = p["level"]
            info.update(uid=p["uid"], level=new_level)
            if row and row[1] == new_level - 1 and new_level <= self.cfg.hero_max_level:
                cur = self.conn.execute("UPDATE heroes SET level=? WHERE user_id=? AND level=?",
                                        (new_level, p["uid"], new_level - 1))
                if cur.rowcount != 1:
                    raise RuntimeError("geroy darajasi parallel o'zgardi")
                info["level_granted"] = True
            else:
                comp = 0
                if row and new_level in (2, 3):
                    comp = int(self.cfg.hero_compensation("herolv", row[0], new_level) or 0)
                if comp:
                    self._add_balance(p["uid"], diamond=comp)
                info.update(level_granted=False, compensation=comp)
        elif kind == "cosmetic":
            cid = p["cosmetic_id"]
            row = self.conn.execute("SELECT name, emoji, stock, sold, active FROM cosmetics WHERE id=?", (cid,)).fetchone()
            if not row:
                raise NeedsReview("kosmetika topilmadi")
            name, emoji, stock, sold, active = row
            if not active or sold >= stock:
                raise NeedsReview("kosmetika tugagan (sold_out) — to'lov qaytarilishi kerak")
            if not self._user_exists(payer_id):
                raise NeedsReview(f"foydalanuvchi {payer_id} bazada yo'q")
            cur = self.conn.execute(
                "INSERT OR IGNORE INTO user_cosmetics (user_id, cosmetic_id, purchased_at) VALUES (?,?,?)",
                (payer_id, cid, time.strftime("%Y-%m-%d %H:%M", time.localtime(self.cfg.now()))))
            if cur.rowcount == 0:
                raise NeedsReview("kosmetika allaqachon sotib olingan — to'lov qaytarilishi kerak")
            cur = self.conn.execute("UPDATE cosmetics SET sold=sold+1 WHERE id=? AND sold<stock", (cid,))
            if cur.rowcount != 1:
                raise NeedsReview("kosmetika tugagan (sold_out) — to'lov qaytarilishi kerak")
            info.update(uid=payer_id, name=name, emoji=emoji)
        else:  # parse_payload allaqachon cheklagan, lekin himoya uchun
            raise NeedsReview(f"noma'lum tur: {kind}")

    def _table_exists(self, name) -> bool:
        return self.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None

    def _track_monthly_spend(self, uid, stars):
        if not stars or not self._table_exists("monthly_spend"):
            return
        ym = time.strftime("%Y-%m", time.localtime(self.cfg.now()))
        self.conn.execute(
            "INSERT INTO monthly_spend (user_id, ym, stars) VALUES (?,?,?) "
            "ON CONFLICT(user_id, ym) DO UPDATE SET stars = stars + excluded.stars", (uid, ym, int(stars)))

    def _referral_bonus(self, payer_uid) -> Optional[int]:
        bonus = self.cfg.referral_bonus() if callable(self.cfg.referral_bonus) else self.cfg.referral_bonus
        if not bonus or not self._table_exists("referrals"):
            return None
        row = self.conn.execute(
            "SELECT inviter_id FROM referrals WHERE invitee_id=? AND COALESCE(first_purchase_paid,0)=0",
            (payer_uid,)).fetchone()
        if not row:
            return None
        inviter = row[0]
        self.conn.execute("UPDATE referrals SET first_purchase_paid=1 WHERE invitee_id=?", (payer_uid,))
        self.conn.execute("UPDATE users SET diamond=MAX(0,diamond+?) WHERE user_id=?",
                          (int(bonus), inviter))
        return inviter
