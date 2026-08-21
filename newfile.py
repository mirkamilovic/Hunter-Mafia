# -*- coding: utf-8 -*-
"""
================================================================================
 HUNTER MAFIA — TO'LIQ VERSIYA v4 (pyTelegramBotAPI / telebot, sinxron)
================================================================================

YANGI (v4):
    - Boshlang'ich balans endi 0$ / 0💎 (avval 5000$/100💎 edi). Bu FAQAT yangi
      ro'yxatdan o'tadigan foydalanuvchilarga tegishli — mavjud foydalanuvchilarning
      SQLite bazasidagi balansi, inventari, o'ynagan o'yinlari va boshqa barcha
      ma'lumotlari kodni yangilashda TO'LIQ saqlanib qoladi (baza fayli o'chirilmaydi,
      jadval faqat CREATE TABLE IF NOT EXISTS orqali tekshiriladi).
    - Tun (night) uzunligi: 45 soniya.
    - Kun (day) uzunligi: jami 90 soniya — birinchi 30 soniya muhokama, so'ng
      ovoz berish tugmalari DM orqali yuboriladi va yana 60 soniya ovoz berish davom etadi.
    - 🕵️ Har bir o'yinchiga o'yin boshida shaxsiy maxfiy missiya beriladi (qoshimchakod1/4).
    - 🎲 Kunduzi 15% ehtimol bilan kutilmagan random event chiqishi mumkin (qoshimchakod1/4).
    - 🎁 Promo-kod tizimi: /promo_create (admin), /promo (foydalanuvchi) (qoshimchakod8).
    - 🎉 Sovg'a tarqatish tizimi: /tarqatish (qoshimchakod6, aiogram'dan telebot'ga moslashtirildi).
    - 😅 Duelda yutqazganlarga hazil-mutoyiba xabari yuboriladi (qoshimchakod9).

YANGI (v3): DO'KONDAGI HAR BIR BUYUM HAQIQIY ISHLAYDI + TELEGRAM STARS ORQALI
HUNTER COIN SOTIB OLISH TIZIMI.

MUHIM ESLATMA (Stars haqida):
    Telegram Stars orqali qilingan to'lovlar AVTOMATIK RAVISHDA botni
    BotFather orqali ro'yxatdan o'tkazgan hisobning Stars balansiga tushadi.
    Bu Telegramning o'z tizimi — botning kodi orqali pulni "boshqa odamga
    yo'naltirish" imkoni yo'q va kerak ham emas: agar bot @Mirkamilovic
    hisobida yaratilgan bo'lsa, barcha Stars avtomatik o'sha yerga tushadi.
    Bot faqat to'lovni qabul qiladi va foydalanuvchi hisobiga Hunter Coin
    qo'shadi — pastda shu jarayon to'liq ishlaydigan holda yozilgan.

DO'KONDAGI BARCHA 27 TA BUYUM ENDI HAQIQIY TA'SIRGA EGA:
    - 🎽 Himoya jileti / 🎭 Temir niqob / 🛡 Imunitet qalqoni → shield (o'limdan asraydi)
    - 📜 Soxta Hujjat → Komissar tekshirsa "Tinch aholi" ko'rsatadi
    - 🥽 Tungi ko'zoynak → tundan keyin qaysi rollar faol bo'lganini DM orqali ko'rsatadi
    - ✉️ Tushunarsiz xat → mafiya sizni nishonga olsa, hujum tasodifiy boshqa odamga burilib ketadi
    - 🧪 Zaharli flakon → /zahar buyrug'i orqali birovni zaharlaysiz (doktor qutqarmasa, tunda o'ladi)
    - 📍 GPS Mayak → /gps buyrug'i orqali birovning tirik/o'lganligini bilib olasiz
    - 💳 VIP Litsenziya / 🔮 Sehrli tumor / 🏦 Bank foizi → kunlik bonusni ko'paytiradi
    - ⚔️ Olmos Qilich → duelda 65% g'alaba imkoniyati beradi
    - 🟡 Oltin o'q → mafiyaning o'ldirish urinishi himoya/davolashni chetlab o'tadi
    - 📡 Maxfiy radar → /qayta_tanlash orqali o'z rolingizni qayta tasodifiy tanlaydi
    - ⚡️ Tezkor jonlanish → o'lish arafasida qo'shimcha jon beradi
    - 🎭 Barcha rollarni tanlash huquqi → /rolni_tanla <rol> orqali xohlagan rolni tanlaysiz
    - 🏛 Klan litsenziyasi → /klan <nomi> orqali klan ochish huquqini beradi
    - 👤 Shadow status → reytingda (/top) yashirin bo'lasiz
    - 🗡 Afsonaviy qotil nishoni / 🛡 Cheksiz duel qalqoni → duelda doim g'olib chiqasiz
    - 👁 Kuzatish ko'zi → kunduzi kim kimga ovoz berganini DM orqali to'liq ko'rasiz
    - 🏦/💳/🔮 → kunlik bonus multiplikatori (x2)
    - 🦊 Cheksiz omad tulki tumori → barcha pul yutuqlaringiz x3 bo'ladi
    - 👑 Hukmdor toj / 🖼 Mifik ramka / 🐉 Qirol unvoni → profilda ko'rinadigan maqom belgilari
    - ⚡️ Admin privilegiyasi (1 kun) → 24 soat davomida /NewGame va h.k. buyruqlarni bera olasiz
"""

import telebot
from telebot import types
import sqlite3
import random
import threading
import time
import json
import os

# ================================================================================
#  ASOSIY SOZLAMALAR
# ================================================================================

TOKEN = os.environ.get("HUNTER_MAFIA_TOKEN", "8826679011:AAGWEPGy-AKO9Nqp1KjLMurDWMNu2ApA5Fo")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

BOT_USERNAME = None
OWNER_USERNAME = "Mirkamilovic"

MIN_PLAYERS = 3
CORE_ROLE_THRESHOLD = 7

# --- YANGILANGAN VAQT SOZLAMALARI ---
# 🌙 Tun uzunligi (soniya)
NIGHT_SECONDS = 45
# ☀️ Kun (kunduzgi bosqich) umumiy uzunligi (soniya) — muhokama + ovoz berish
DAY_TOTAL_SECONDS = 90
# 💬 Kun boshlangandan keyin ovoz berish tugmalari nechi soniyadan so'ng chiqishi
DAY_DISCUSSION_SECONDS = 30
# 🗳 Ovoz berish davomiyligi (soniya) — ovoz tugmalari chiqqandan keyin
DAY_VOTE_SECONDS = DAY_TOTAL_SECONDS - DAY_DISCUSSION_SECONDS
LAST_WORDS_SECONDS = 30

WIN_REWARD = 70
LOSE_REWARD = 20

HC_STAR_RATE = 5    # 5 ⭐️ Stars = 1 🪙 Hunter Coin

NIGHT_PHOTO = "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1000&auto=format&fit=crop"
DAY_PHOTO = "https://images.unsplash.com/photo-1465101162946-4377e57745c3?q=80&w=1000&auto=format&fit=crop"
MAIN_PHOTO = "https://images.unsplash.com/photo-1514565131-fce0801e5785?q=80&w=1000&auto=format&fit=crop"


# ================================================================================
#  MA'LUMOTLAR BAZASI (SQLite)
# ================================================================================

conn = sqlite3.connect("hunter_mafia.db", check_same_thread=False)
db_lock = threading.RLock()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    dollar INTEGER DEFAULT 0,
    diamond INTEGER DEFAULT 0,
    coin INTEGER DEFAULT 0,
    games INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    shield INTEGER DEFAULT 0,
    inventory TEXT DEFAULT '[]',
    married_to INTEGER DEFAULT 0,
    last_bonus_date TEXT DEFAULT ''
)
""")
# eski bazalarda "charges" ustuni bo'lmasligi mumkin — xavfsiz qo'shamiz
try:
    cur.execute("ALTER TABLE users ADD COLUMN charges TEXT DEFAULT '{}'")
    conn.commit()
except sqlite3.OperationalError:
    pass

# YANGI (qo'shimcha kodlar orqali qo'shildi): duel statistikasi va ban tizimi uchun ustunlar
for _col, _default in (("duel_wins", "0"), ("duel_losses", "0"), ("banned", "0")):
    try:
        cur.execute(f"ALTER TABLE users ADD COLUMN {_col} INTEGER DEFAULT {_default}")
        conn.commit()
    except sqlite3.OperationalError:
        pass

cur.execute("""
CREATE TABLE IF NOT EXISTS known_groups (
    chat_id INTEGER PRIMARY KEY,
    title TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS bot_settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS clans (
    owner_id INTEGER PRIMARY KEY,
    name TEXT
)
""")
# --- YANGI (qoshimchakod8.py "Promo-kod Yaratish" g'oyasi asosida) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS promo_codes (
    code TEXT PRIMARY KEY,
    dollar INTEGER DEFAULT 0,
    diamond INTEGER DEFAULT 0,
    coin INTEGER DEFAULT 0,
    max_uses INTEGER DEFAULT 1,
    used_count INTEGER DEFAULT 0
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS promo_redemptions (
    code TEXT,
    user_id INTEGER,
    PRIMARY KEY (code, user_id)
)
""")
conn.commit()

USER_COLS = ["user_id", "name", "dollar", "diamond", "coin", "games", "wins",
             "shield", "inventory", "married_to", "last_bonus_date", "charges",
             "duel_wins", "duel_losses", "banned"]


def get_user_row(uid, name=None):
    with db_lock:
        cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO users (user_id, name) VALUES (?,?)", (uid, name or str(uid)))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
            row = cur.fetchone()
        elif name and row[1] != name:
            cur.execute("UPDATE users SET name=? WHERE user_id=?", (name, uid))
            conn.commit()
            row = list(row)
            row[1] = name
            row = tuple(row)
        return row


def user_dict(uid, name=None):
    row = get_user_row(uid, name)
    d = dict(zip(USER_COLS, row))
    if d.get("charges") is None:
        d["charges"] = "{}"
    if d.get("duel_wins") is None:
        d["duel_wins"] = 0
    if d.get("duel_losses") is None:
        d["duel_losses"] = 0
    if d.get("banned") is None:
        d["banned"] = 0
    return d


def update_user(uid, **fields):
    with db_lock:
        keys = ", ".join(f"{k}=?" for k in fields)
        vals = list(fields.values()) + [uid]
        cur.execute(f"UPDATE users SET {keys} WHERE user_id=?", vals)
        conn.commit()


def add_balance(uid, dollar=0, diamond=0, coin=0):
    u = user_dict(uid)
    update_user(
        uid,
        dollar=max(0, u["dollar"] + dollar),
        diamond=max(0, u["diamond"] + diamond),
        coin=max(0, u["coin"] + coin),
    )


def add_inventory_item(uid, item_name):
    u = user_dict(uid)
    inv = json.loads(u["inventory"])
    inv.append(item_name)
    update_user(uid, inventory=json.dumps(inv))


def add_shield(uid, n=1):
    u = user_dict(uid)
    update_user(uid, shield=u["shield"] + n)


def consume_shield(uid):
    u = user_dict(uid)
    if u["shield"] > 0:
        update_user(uid, shield=u["shield"] - 1)
        return True
    return False


# ---- "charges" (jangovar effektlar) tizimi — har bir do'kon buyumi shu orqali ishlaydi ----

def get_charges(uid):
    u = user_dict(uid)
    try:
        return json.loads(u.get("charges") or "{}")
    except Exception:
        return {}


def set_charges(uid, ch):
    update_user(uid, charges=json.dumps(ch))


def add_charge(uid, key, n=1):
    ch = get_charges(uid)
    ch[key] = ch.get(key, 0) + n
    set_charges(uid, ch)


def use_charge(uid, key, n=1):
    ch = get_charges(uid)
    if ch.get(key, 0) >= n:
        ch[key] -= n
        set_charges(uid, ch)
        return True
    return False


def set_charge_value(uid, key, value):
    ch = get_charges(uid)
    ch[key] = value
    set_charges(uid, ch)


def luck_mult(uid):
    """🦊 Cheksiz omad tulki tumori — barcha pul yutuqlarini ko'paytiradi."""
    return get_charges(uid).get("luck_mult", 1)


def bonus_mult(uid):
    """💳/🔮/🏦 — kunlik bonusni ko'paytiradi."""
    return get_charges(uid).get("bonus_mult", 1)


def add_known_group(chat_id, title):
    with db_lock:
        cur.execute("INSERT OR REPLACE INTO known_groups (chat_id, title) VALUES (?,?)", (chat_id, title))
        conn.commit()


def remove_known_group(chat_id):
    with db_lock:
        cur.execute("DELETE FROM known_groups WHERE chat_id=?", (chat_id,))
        conn.commit()


def list_known_groups():
    with db_lock:
        cur.execute("SELECT chat_id, title FROM known_groups")
        return cur.fetchall()


def get_setting(key):
    with db_lock:
        cur.execute("SELECT value FROM bot_settings WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else None


def set_setting(key, value):
    with db_lock:
        cur.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES (?,?)", (key, str(value)))
        conn.commit()


def get_top_players(limit=10):
    """👑 Qirol unvoni egalari tepada chiqadi, 👤 Shadow statusidagilar reytingdan yashiriladi."""
    with db_lock:
        cur.execute("SELECT name, wins, dollar, charges FROM users ORDER BY wins DESC, dollar DESC LIMIT 200")
        rows = cur.fetchall()
    normal, qirol = [], []
    for name, wins, dollar, charges_json in rows:
        try:
            ch = json.loads(charges_json or "{}")
        except Exception:
            ch = {}
        if ch.get("shadow", 0):
            continue
        entry = (name, wins, dollar, bool(ch.get("qirol", 0)))
        (qirol if entry[3] else normal).append(entry)
    return (qirol + normal)[:limit]


# ================================================================================
#  BOT YARATUVCHISINI ANIQLASH
# ================================================================================

_owner_id_raw = get_setting("owner_id")
OWNER_ID = int(_owner_id_raw) if _owner_id_raw else None


def is_owner(user_id):
    return OWNER_ID is not None and user_id == OWNER_ID


def maybe_capture_owner(tg_user):
    global OWNER_ID
    if OWNER_ID is not None or tg_user is None:
        return
    if tg_user.username and tg_user.username.lower() == OWNER_USERNAME.lower():
        OWNER_ID = tg_user.id
        set_setting("owner_id", OWNER_ID)


def is_banned(uid):
    return bool(user_dict(uid).get("banned"))


def ban_user(uid):
    update_user(uid, banned=1)


def unban_user(uid):
    update_user(uid, banned=0)


def record_duel_result(winner_id, loser_id):
    """qoshimchakod4.py g'oyasi asosida — endi haqiqiy SQLite bazasida saqlanadi."""
    w = user_dict(winner_id)
    l = user_dict(loser_id)
    update_user(winner_id, duel_wins=w["duel_wins"] + 1)
    update_user(loser_id, duel_losses=l["duel_losses"] + 1)


def get_partner_name(uid):
    """qoshimchakod3.py / qoshimchakod6.py g'oyasi — married_to ustuni asosida haqiqiy holat."""
    u = user_dict(uid)
    partner_id = u.get("married_to") or 0
    if not partner_id:
        return None
    return user_dict(partner_id)["name"]


def is_group_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


def is_authorized(message):
    """O'yin boshqaruv buyruqlari uchun: guruh admini, bot yaratuvchisi,
    yoki ⚡️ Admin privilegiyasi (1 kun) buyumi faol bo'lgan foydalanuvchi."""
    uid = message.from_user.id
    if is_owner(uid):
        return True
    ch = get_charges(uid)
    until = ch.get("temp_admin_until", 0)
    if until and time.time() < until:
        return True
    if message.chat.type in ("group", "supergroup"):
        return is_group_admin(message.chat.id, uid)
    return False


# ================================================================================
#  28 TA ROL
# ================================================================================

# ================================================================================
#  MAXFIY MISSIYALAR VA RANDOM EVENTLAR
#  (qoshimchakod1.py va qoshimchakod4.py g'oyalari asosida, telebot/SQLite uslubiga moslashtirildi)
# ================================================================================

SECRET_MISSIONS = [
    "Kunduzgi muhokamada birinchi bo'lib fikr bildir.",
    "Ovoz berish jarayonida hech kimga ovoz bermaslikka harakat qil.",
    "Tunda shifokor seni davolashiga erish (so'zsiz ishora bilan).",
    "Kimdir bilan bir xil shubhali fikrni qo'llab-quvvatla.",
    "Kunduzgi muhokamada jami 3 martadan ko'p gapirma.",
    "Ovoz berishda o'zingga ovoz ber.",
    "Tungi fazo boshlanishidan oldin guruhda 'Xayrli tun' deb yoz.",
    "Hech kim shubha qilmagan tinch aholidan birini himoya qil.",
    "Muhokama vaqtida kimningdir xatosini hammaga ko'rsat.",
    "Ovoz berishda oxirgi bo'lib ovoz ber.",
    "Bugungi o'yinda biron marta ham 'Men tinch aholiman' deb yozma.",
    "Tunda ovoz berishda mafiya tanlagan insonga qarshi ovoz ber.",
    "O'yin davomida bitta emojidan faqat 5 marta foydalan.",
    "Boshqalarning fikriga qo'shilib, 'Men ham shunday o'ylayman' deb yoz.",
    "Kunduzgi bosqichda mutlaqo jim o'tir va ovoz berishgacha gapirma.",
]

RANDOM_EVENTS = [
    "⚡️ Chaqmoq chaqdi! Tunda hamma bir-birining ovozini eshita olmaydi (Klinik sukunat).",
    "💰 Omadli daqiqa! Barcha tirik o'yinchilarga +50$ bonus taqdim etildi.",
    "🔀 Sirli tuman! Bugun kimningdir roli hech kimga ma'lum bo'lmaydi.",
    "🔍 Taqdir hukmi! Bugungi kunduzgi ovoz berishda hech kim o'lmaydi, lekin hamma shubhali deb topiladi.",
    "🌪 Bo'ron boshlandi! Bugungi tunda barcha maxsus qobiliyatlar 50% kuchsizroq ishlaydi.",
    "🎁 Sirli sovg'a qutisi topildi! Tasodifiy bitta o'yinchiga +100$ tushdi.",
    "📢 Shov-shuv! Guruh bo'ylab kimdir shubhali gap tarqatdi — hamma bir-biriga qarab qoldi.",
    "🕯 Sokinlik kuni! Bugun kunduzi ovoz berish 15 soniyaga qisqartirildi.",
]


ROLES_INFO = {
    "Don 🎩": "Mafia guruhining rahbari. Kechasi sheriklari bilan birga qaysi o'yinchini yo'q qilishni hal qiladi.",
    "Komissar 🕵️‍♂️": "Tinch aholining bosh himoyachisi. Kechasi har bir o'yinchini tekshiradi yoki o'ldiradi.",
    "Doktor 👨‍⚕️": "Kechasi o'yinchilarni davolaydi. Mafia yoki qotildan jabrlangan odamni qutqara oladi.",
    "Tinch aholi 👨‍👩‍👧‍👦": "Maxsus qobiliyati yo'q, lekin kunduzi ovoz berish yo'li bilan mafiyalarni aniqlaydi.",
    "Mafia 🕶": "Donning yaqin yordamchisi. Tunda Don bilan birgalikda qurbon tanlaydi.",
    "Qotil 🗡": "Mustaqil qotil. O'z qurbonini tunlari yashirincha pichoqlaydi.",
    "Manyak 🔪": "Hech kimga bo'ysunmaydigan shafqatsiz qotil. Kechasi istalgan odamga hujum qiladi.",
    "Serjant 👮‍♂️": "Komissarning yordamchisi. Komissar vafot etsa uning vazifasini bajarishni boshlaydi.",
    "Advokat ⚖️": "Mafia a'zosi yoki boshqalarni sud jarayonida yoki tekshiruvda himoya qiladi.",
    "Fohisha 💋": "Kechasi biron o'yinchining oldiga borib, uning tungi qobiliyatidan foydalanishiga to'sqinlik qiladi.",
    "Terrorist 💣": "Agar uni kunduzi o'yinchi osib o'ldirmoqchi bo'lishsa, o'zi bilan birga tanlagan odamini ham portlatib ketadi.",
    "Mergan 🏹": "Aniq nishonga oladi. O'z navbatida dushmanga o'q uzib, uni yo'q qilishi mumkin.",
    "Varvar 🪓": "Juda baquvvat jangchi. Unga qilingan ayrim hujumlarga qarshilik ko'rsata oladi.",
    "Sadoqatli yordamchi 🤝": "Boshqa asosiy o'yinchiga sodiq xizmat qiladi va uning jonini saqlab qolishga yordam beradi.",
    "Snayper 🎯": "Uzoq masofadan turib dushmanni aniq poylaydi va o'ldiradi.",
    "O'g'ri 🥷": "Kechasi boshqa o'yinchilarning pulini yoki buyumlarini o'g'irlab ketadi.",
    "Sehrgar 🧙‍♂️": "Sehrli kuchlar yordamida o'yin jarayonini o'zgartirishi mumkin.",
    "Sehrgar yordamchisi 🪄": "Sehrgarga yordam beradi va sehrli kuchlarni kuchaytiradi.",
    "Arvoh 👻": "O'lgandan keyin ham o'yinda qolib, tiriklarga sirli imo-ishoralar beradi.",
    "Sudya 👨‍⚖️": "Kunduzgi ovoz berish jarayonida hal qiluvchi ovozga ega yoki hukmni o'zgartira oladi.",
    "Provokator 🗣": "O'yinchilarni janjallashtirib, ularni bir-biriga qarshi ovoz berishga majbur qiladi.",
    "General 🎖": "Harbiy taktikani qo'llab, o'z jamoasiga qo'shimcha himoya taqdim etadi.",
    "Josus 🕵️": "Boshqa guruhlarning yashirin sirlari va rejalarini poylab eshitib keladi.",
    "Bomj 🧟‍♂️": "Kechalari ko'chada yashirin yurib, tasodifan boshqalarning sirli harakatlarini ko'rib qoladi.",
    "Arxitektor 📐": "O'yin davomida himoya binolari yoki to'siqlar qurish qobiliyatiga ega.",
    "Telba 🤪": "Oldindan bashorat qilib bo'lmaydigan harakatlar qiladi, uning o'yinini topish qiyin.",
    "Qorovul 🔦": "Kechasi o'z obyektini yoki tanlagan o'yinchini qo'riqlab, hujumlardan saqlaydi.",
    "Beshikdagi bola 👶": "O'yin boshida unga tegishib bo'lmaydi, maxsus himoyaga ega kenja qahramon.",
}

ALL_ROLES = list(ROLES_INFO.keys())
CORE_ROLES = ["Don 🎩", "Komissar 🕵️‍♂️", "Doktor 👨‍⚕️"]

MAFIA_ROLES = {"Don 🎩", "Mafia 🕶"}
INDEPENDENT_ROLES = {
    "Qotil 🗡", "Manyak 🔪", "Terrorist 💣", "O'g'ri 🥷", "Sehrgar 🧙‍♂️",
    "Sehrgar yordamchisi 🪄", "Telba 🤪", "Bomj 🧟‍♂️", "Provokator 🗣",
}


def team_of(role):
    if role in MAFIA_ROLES:
        return "mafia"
    if role in INDEPENDENT_ROLES:
        return "independent"
    return "town"


def mafia_count_for(n):
    if n <= 7:
        return 1
    elif n <= 12:
        return 2
    elif n <= 16:
        return 3
    else:
        return max(3, n // 5)


# ================================================================================
#  HAZIL / SO'ZLAR RO'YXATLARI
# ================================================================================

DEAD_FUNNY_WORDS = [
    "Xafa bo'lmanglar, narigi dunyoda Wi-Fi yaxshi ekan! 😎",
    "Men shunchaki tush ko'ryapman, uyg'otmanglar... 😴",
    "Kallam ishlamay qoldi, shef aybdor! 🧟‍♂️",
    "Pazandalar, menda endi ishtaha yo'q! 🍲",
    "O'lding demang, shunchaki afk bo'ldim kiberkatakda! 🎮",
    "Kechirasizlar, tormozim ishlamay qoldi! 🚗💥",
    "G'olib bo'lsanglar menga ham ulush chiqarasizlarmi? 🪙",
    "Ruhim guruhda qoladi, xavotir olmanglar! 👻",
    "Men o'lmadim, shunchaki taktik chekinish qildim! 🏃‍♂️",
    "Keyingi safar tirik qolsam, do'konni yulib olaman! 🛒",
]

DUEL_REJECT_JOKES = [
    "⚔️ Raqib qo'rqib qochib ketdi, ishtoni ho'l bo'lib qolgan shekilli! 🏃‍♂️💨",
    "⚔️ Duel bekor qilindi: Raqib onasidan ruxsat so'rolmadi! 🍼😂",
    "⚔️ Men kasalman, oyim nonushtaga chaqiryaptilar deb jangdan qochdi! 🍳",
    "⚔️ Qurol tanlashda raqib qoshiqni tanladi va qo'rqib yig'lab yubordi! 🥄😭",
]

GIFT_JOKES = [
    "😂 Xasislik qiladigan odam yo'q ekan bu guruhda!",
    "🎉 Mana bu saxiylik-ku, hammaga o'rnak bo'ladigan!",
    "🤑 Pulingiz omadli bo'lsin, faqat ortiqcha isrof qilmang!",
]

# 😂 Duelda yutqazganlarga DM orqali yuboriladigan hazil xabarlar
# (qoshimchakod9.py g'oyasi asosida qo'shildi)
DEFEAT_JOKES = [
    "Bugun yutqazdingiz, lekin xafa bo'lmang, klaviaturada mag'lubiyat tugmasi ham kerak-ku! 😉",
    "Mag'lubiyat — bu g'alabaning shogirdi. Ertaga ustozingizni xursand qilasiz! 🚀",
    "Yutqazish ham san'at! Faqat bu safargi asaringiz biroz qora rangda chiqdi. 🎨",
    "Tinchlaning, hatto professional chempionlar ham bir vaqtlar boshlang'ich bo'lishgan (faqat tezroq o'lishmasdi). 🐢",
    "Internet tezligingiz yoki omadingiz bugun dam olayotgan ekan. Keyingi safar uyg'otib qo'yamiz! ⚡",
    "Siz yutqazmadingiz, shunchaki raqibga g'alaba sovg'a qildingiz. Saxiylik ham fazilat! 🤝",
    "Mag'lubiyat bu — to'xtash emas, bu tezroq uxlagani ketish uchun bahona! 🛌",
    "Bot sizga qarab jilmaydi va dedi: 'Keyingi safar albatta eplaysiz... balki'. 🤖",
    "G'alaba yaqin edi, lekin u boshqa manzilga adashib ketdi shekilli. 🚎",
    "Xafa bo'lmang! Hatto eng yaxshi qahramonlar ham birinchi qismda adashib o'lib qolishadi. 🎬",
    "Afsuski, bu safar klaviatura siz tomonda emas edi. Omadni boshqa kunga rejalashtiramiz! 📅",
    "Mag'lubiyat achchiq, lekin uning ustidan kulish — shirin! Keyingi safar qasos olamiz. ⚔️",
    "O'yin tugadi, lekin sizning xarizmangiz o'zgarmadi. O'zingizni bosib oling! 😎",
    "Mag'lubiyat qahramonlarni toblaydi (yoki g'azablantiradi). Siz qaysi birisiz? 🔥",
    "Bugun qismat sizni tanlamadi, lekin keyingi jangda barchasi boshqacha bo'lishi aniq! 🌟",
    "Yutqazish bu — mag'lubiyat emas, bu 'Tajriba' degan yangi darajani ochish! 📈",
    "Xotirjam bo'ling, botlar ham xato qiladi, lekin siz bugun ulardan biroz oldinda edingiz. ☕",
]

MARRIAGE_ACCEPT_JOKES = [
    "💍 Tabriklaymiz! Endi bir yostiqqa bosh qo'yib, kechasi qaysi serialni ko'rishni talashasizlar! 📺😂",
    "💍 Baxtiyor oila qurildi! Birinchi janjal qachon bo'lishiga stavka qabul qilamiz! 💸🍿",
]

MARRIAGE_REJECT_JOKES = [
    "💍 'Mening oyim senga o'xshagan kelin/kuyovni yoqtirmaydi' deb rad etdi! 🧓❌",
    "💍 Kechirasan, men hali kareraga e'tibor qaratmoqchiman (pitsa yeyishga)! 🍕🏃‍♂️",
]


# ================================================================================
#  DO'KON MAHSULOTLARI — HAR BIRI HAQIQIY "mode" GA EGA
# ================================================================================
# mode turlari:
#   shield          -> DB "shield" ustuniga +1 (o'limdan bir marta asraydi)
#   instant_dollar   -> darhol dollar beradi (luck_mult bilan ko'payadi)
#   charge           -> "charges" json ichida sanoq (bir martalik ishlatiladi)
#   multiplier       -> charges ichida ko'paytiruvchi (eng kattasi saqlanadi)
#   expiry           -> charges ichida tugash vaqti (soniya, Unix timestamp)
#   permanent_flag   -> charges ichida doimiy belgi (1 = faol)

SHOP_DOLLAR = {
    "himoya":   {"name": "🎽 Himoya jileti", "price": 200, "currency": "dollar", "mode": "shield",
                 "desc": "O'yin paytida o'lishdan 1 marta himoya qiladi."},
    "hujjat":   {"name": "📜 Soxta Hujjat", "price": 350, "currency": "dollar", "mode": "charge", "charge_key": "fake_doc",
                 "desc": "Komissar sizni tekshirsa, 'Tinch aholi' bo'lib ko'rinasiz."},
    "aptechka": {"name": "🩹 Kichik Aptechka", "price": 150, "currency": "dollar", "mode": "instant_dollar", "range": (100, 100),
                 "desc": "Darhol +100$ beradi."},
    "kozoynak": {"name": "🥽 Tungi ko'zoynak", "price": 500, "currency": "dollar", "mode": "charge", "charge_key": "night_vision",
                 "desc": "Tundan keyin qaysi rollar faol bo'lganini shaxsiy xabarda ko'rasiz."},
    "xat":      {"name": "✉️ Tushunarsiz xat", "price": 100, "currency": "dollar", "mode": "charge", "charge_key": "confuse",
                 "desc": "Mafiya sizni nishonga olsa, hujum tasodifiy boshqa odamga burilib ketadi."},
    "sumka":    {"name": "💼 Shubhali sumka", "price": 450, "currency": "dollar", "mode": "instant_dollar", "range": (50, 300),
                 "desc": "Ichidan tasodifiy 50$-300$ chiqadi."},
    "niqob":    {"name": "🎭 Temir niqob", "price": 600, "currency": "dollar", "mode": "shield",
                 "desc": "O'yin paytida o'lishdan 1 marta himoya qiladi (qo'shimcha)."},
    "zahar":    {"name": "🧪 Zaharli flakon", "price": 800, "currency": "dollar", "mode": "charge", "charge_key": "poison",
                 "desc": "/zahar buyrug'i orqali (reply) birovni zaharlash imkonini beradi."},
    "gps":      {"name": "📍 GPS Mayak", "price": 900, "currency": "dollar", "mode": "charge", "charge_key": "gps",
                 "desc": "/gps buyrug'i orqali (reply) birovning tirik/o'lganligini bilib olasiz."},
    "vip":      {"name": "💳 VIP Litsenziya", "price": 1000, "currency": "dollar", "mode": "multiplier",
                 "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    # --- YANGI MAHSULOTLAR (qoshimchakod8.py g'oyasi asosida qo'shildi) ---
    "energy":   {"name": "⚡️ Energiya ichimligi", "price": 120, "currency": "dollar", "mode": "instant_dollar", "range": (150, 150),
                 "desc": "O'yin davomida tezkor harakat va +150$ mukofot beradi."},
    "tutun":    {"name": "💣 Tutunli bomba", "price": 280, "currency": "dollar", "mode": "charge", "charge_key": "smoke_bomb",
                 "desc": "Xavfli vaziyatda izingizni yo'qotib, dushmandan yashiringan bo'lasiz."},
    "zar":      {"name": "🎲 Sehrli Zarlar", "price": 320, "currency": "dollar", "mode": "instant_dollar", "range": (50, 1000),
                 "desc": "Ochilganda tasodifiy $50 dan $1000 gacha yutuq keltiradi."},
    "fonar":    {"name": "🔦 Katta Fonar", "price": 220, "currency": "dollar", "mode": "charge", "charge_key": "flash_light",
                 "desc": "Kechasi qorong'ilikdagi yashirin harakatlarni yoritib beradi."},
}

SHOP_DIAMOND = {
    "qilich":    {"name": "⚔️ Olmos Qilich", "price": 5, "currency": "diamond", "mode": "charge", "charge_key": "duel_adv",
                  "desc": "Keyingi duelda g'alaba imkoniyatini 65% ga oshiradi."},
    "tumor":     {"name": "🔮 Sehrli tumor", "price": 10, "currency": "diamond", "mode": "multiplier",
                  "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    "quti":      {"name": "📦 Nodir quti", "price": 15, "currency": "diamond", "mode": "instant_dollar", "range": (100, 500),
                  "desc": "Ichidan qimmatbaho dollar mukofoti chiqadi."},
    "oq":        {"name": "🟡 Oltin o'q", "price": 20, "currency": "diamond", "mode": "charge", "charge_key": "golden_bullet",
                  "desc": "Mafiyaning o'ldirish urinishi himoya/davolashni chetlab o'tadi (1 marta)."},
    "qalqon":    {"name": "🛡 Imunitet qalqoni", "price": 25, "currency": "diamond", "mode": "shield",
                  "desc": "O'yin paytida o'lishdan 1 marta himoya qiladi."},
    "radar":     {"name": "📡 Maxfiy radar", "price": 30, "currency": "diamond", "mode": "charge", "charge_key": "radar",
                  "desc": "/qayta_tanlash orqali o'z rolingizni tasodifiy boshqasiga almashtirasiz."},
    "jonlanish": {"name": "⚡️ Tezkor jonlanish", "price": 40, "currency": "diamond", "mode": "charge", "charge_key": "revive",
                  "desc": "O'lish arafasida qo'shimcha jon beradi (shielddan keyin ishlaydi)."},
    "imperator": {"name": "👑 Imperator 1 kunlik unvoni", "price": 50, "currency": "diamond", "mode": "expiry",
                  "charge_key": "imperator_until", "duration_seconds": 86400, "desc": "24 soat 'Imperator' maqomi (profilda ko'rinadi)."},
    "ramka":     {"name": "🖼 Mifik ramka", "price": 75, "currency": "diamond", "mode": "permanent_flag", "charge_key": "ramka",
                  "desc": "Profilingizga doimiy eksklyuziv ramka belgisi qo'shadi."},
    "tulki":     {"name": "🦊 Cheksiz omad tulki tumori", "price": 100, "currency": "diamond", "mode": "multiplier",
                  "charge_key": "luck_mult", "mult_value": 3, "desc": "Barcha pul yutuqlaringizni (bonus, duel, o'yin mukofoti) 3x qiladi."},
    # --- YANGI MAHSULOTLAR (qoshimchakod8.py g'oyasi asosida qo'shildi) ---
    "kristal":   {"name": "💠 Sehrli Kristal", "price": 8, "currency": "diamond", "mode": "instant_diamond", "range": (3, 3),
                  "desc": "Hisobingizga darhol +3 ta Olmos qo'shadi."},
    "kolt":      {"name": "🧥 Yashirin Kolt (Plash)", "price": 18, "currency": "diamond", "mode": "charge", "charge_key": "cloak",
                  "desc": "O'yin davomida dushmanlar nishoniga tushishdan himoya qiladi."},
    "eliksir":   {"name": "🧪 Hayot Eliksiri", "price": 35, "currency": "diamond", "mode": "instant_dollar", "range": (3000, 3000),
                  "desc": "Barcha jarohatlarni bitirib, +3000$ bonus beradi."},
}

SHOP_COIN = {
    "toj":         {"name": "👑 Hukmdor toj", "price": 15, "currency": "coin", "mode": "permanent_flag", "charge_key": "toj",
                    "desc": "Doimiy hukmdor maqomi belgisi (profilda ko'rinadi)."},
    "rol_tanlash": {"name": "🎭 Barcha rollarni tanlash huquqi", "price": 20, "currency": "coin", "mode": "charge", "charge_key": "role_choice",
                    "desc": "/rolni_tanla <rol> orqali keyingi o'yinda xohlagan rolni tanlaysiz."},
    "klan":        {"name": "🏛 Klan uchun litsenziya", "price": 25, "currency": "coin", "mode": "permanent_flag", "charge_key": "klan_license",
                    "desc": "/klan <nomi> orqali o'z klaningizni ochish huquqini beradi."},
    "shadow":      {"name": "👤 Maxfiy 'Shadow' statusi", "price": 30, "currency": "coin", "mode": "permanent_flag", "charge_key": "shadow",
                    "desc": "/top reytingida ismingiz endi ko'rinmaydi."},
    "nishon":      {"name": "🗡 Afsonaviy qotil nishoni", "price": 40, "currency": "coin", "mode": "permanent_flag", "charge_key": "legend_killer",
                    "desc": "Barcha duel janglarida doim g'olib chiqasiz."},
    "koz":         {"name": "👁 Barcha o'yinchilarni kuzatish ko'zi", "price": 55, "currency": "coin", "mode": "charge", "charge_key": "watch_eyes",
                    "desc": "Kunduzi kim kimga ovoz berganini to'liq DM orqali ko'rasiz."},
    "duel_qalqon": {"name": "🛡 Cheksiz duel qalqoni", "price": 70, "currency": "coin", "mode": "permanent_flag", "charge_key": "duel_shield",
                    "desc": "Duelda hech qachon yutqazmaysiz."},
    "bank":        {"name": "🏦 Bank foizini 2 barobar oshirish", "price": 90, "currency": "coin", "mode": "multiplier",
                    "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    "admin":       {"name": "⚡️ Admin privilegiyasi (1kun)", "price": 120, "currency": "coin", "mode": "expiry",
                    "charge_key": "temp_admin_until", "duration_seconds": 86400, "desc": "24 soat davomida /NewGame, /StartGame va h.k. buyruqlarni bera olasiz."},
    "qirol":       {"name": "🐉 Hunter Mafia Qiroli unvoni", "price": 200, "currency": "coin", "mode": "permanent_flag", "charge_key": "qirol",
                    "desc": "Doimiy eng oliy maqom — /top reytingida hamisha eng tepada chiqasiz."},
}

SHOP_OSH = {
    "toy":       {"name": "💍 To'y Oshi", "price": 5000, "currency": "dollar", "mode": "instant_dollar", "range": (1000, 1000)},
    "choyxona":  {"name": "🍵 Choyxona Oshi", "price": 4500, "currency": "dollar", "mode": "instant_dollar", "range": (800, 800)},
    "tandir":    {"name": "🔥 Tandir Oshi", "price": 4000, "currency": "dollar", "mode": "instant_dollar", "range": (700, 700)},
    "samarqand": {"name": "🇺🇿 Samarqand Oshi", "price": 3800, "currency": "dollar", "mode": "instant_dollar", "range": (600, 600)},
    "buxoro":    {"name": "🏛 Buxorocha Sofi Oshi", "price": 3600, "currency": "dollar", "mode": "instant_dollar", "range": (500, 500)},
    "fargona":   {"name": "🏔 Farg'ona Devzira Oshi", "price": 3500, "currency": "dollar", "mode": "instant_dollar", "range": (400, 400)},
    "qora":      {"name": "🥷 Qora Mafia Oshi", "price": 3000, "currency": "dollar", "mode": "instant_dollar", "range": (300, 300)},
}

SHOP_CATEGORIES = {
    "dollar": ("💵 Dollar Do'koni", SHOP_DOLLAR),
    "diamond": ("💎 Olmos Do'koni", SHOP_DIAMOND),
    "coin": ("🪙 Hunter Coin Do'koni", SHOP_COIN),
    "osh": ("🥘 Milliy Osh Menyusi", SHOP_OSH),
}


# ================================================================================
#  HAR GURUH UCHUN ALOHIDA O'YIN HOLATI
# ================================================================================

GAMES = {}
GAME_LOCK = threading.RLock()
PENDING_PROPOSALS = {}


def new_game(chat_id, chat_title):
    return {
        "chat_id": chat_id,
        "chat_title": chat_title,
        "phase": "waiting",
        "players": {},
        "join_msg_id": None,
        "group_link": None,
        "day_number": 0,
        "mafia_votes": {},
        "doctor_target": None,
        "komissar_action": None,
        "komissar_target": None,
        "votes": {},
        "voting_open": False,
        "secret_missions": {},
        "last_words_wait": set(),
        "forced_roles": {},
        "poison_marks": set(),
        "timers": [],
    }


def alive_players(game):
    return {uid: p for uid, p in game["players"].items() if p["alive"]}


def player_line_list(game):
    if not game["players"]:
        return "Hozircha hech kim yo'q."
    return "\n".join(f"• {p['name']}" for p in game["players"].values())


def get_group_link(chat_id):
    game = GAMES.get(chat_id)
    if game and game.get("group_link"):
        return game["group_link"]
    try:
        link = bot.export_chat_invite_link(chat_id)
        if game:
            game["group_link"] = link
        return link
    except Exception:
        return None


def safe_delete(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass


def safe_send(uid, text, reply_markup=None):
    try:
        bot.send_message(uid, text, reply_markup=reply_markup)
        return True
    except Exception:
        return False


def mention(uid, name):
    """Guruh xabarlarida o'yinchi ismini bosilganda uning profiliga o'tadigan qilib ko'rsatish uchun."""
    safe_name = (name or "O'yinchi").replace("<", "").replace(">", "")
    return f'<a href="tg://user?id={uid}">{safe_name}</a>'


def roster_breakdown_text(game):
    """qoshimchakod-larda ko'rilgan boshqa botlar uslubida — tirik o'yinchilar ro'yxati
    va ular orasidagi rol tarkibi (kim qaysi rolda ekani oshkor qilinmaydi, faqat statistika)."""
    alive = alive_players(game)
    if not alive:
        return "Tirik o'yinchi qolmadi."

    lines = ["👥 <b>Tirik o'yinchilar:</b>"]
    for i, (uid, p) in enumerate(alive.items(), start=1):
        lines.append(f"{i}. {mention(uid, p['name'])}")

    mafia_roles, indep_roles, town_roles = [], [], []
    for p in alive.values():
        team = team_of(p["role"])
        if team == "mafia":
            mafia_roles.append(p["role"])
        elif team == "independent":
            indep_roles.append(p["role"])
        else:
            town_roles.append(p["role"])

    def group_counts(roles):
        counts = {}
        for r in roles:
            counts[r] = counts.get(r, 0) + 1
        parts = []
        for r, c in counts.items():
            parts.append(r if c == 1 else f"{r} - {c}")
        return ", ".join(parts) if parts else "—"

    lines.append("")
    lines.append(f"🏠 <b>Tinch aholilar - {len(town_roles)}:</b>\n{group_counts(town_roles)}")
    lines.append(f"👤 <b>Yakka rollar - {len(indep_roles)}:</b>\n{group_counts(indep_roles)}")
    lines.append(f"🕶 <b>Mafiyalar - {len(mafia_roles)}:</b>\n{group_counts(mafia_roles)}")
    lines.append("")
    lines.append(f"<b>Jami:</b> {len(alive)} ta")
    return "\n".join(lines)


# ================================================================================
#  ASOSIY MENYU — hech qanday tugma "o'lik" bo'lib qolmasin
# ================================================================================

def get_main_menu(chat_id=None, user_id=None):
    kb = types.InlineKeyboardMarkup()
    group_url = None
    if chat_id and chat_id in GAMES and GAMES[chat_id].get("group_link"):
        group_url = GAMES[chat_id]["group_link"]
    if group_url:
        kb.add(types.InlineKeyboardButton("🚀 Guruhga qaytish", url=group_url))
    kb.add(
        types.InlineKeyboardButton("🎭 28 ta Rollar", callback_data="menu|roles"),
        types.InlineKeyboardButton("👤 Kabinet", callback_data="menu|cabinet"),
    )
    kb.add(
        types.InlineKeyboardButton("🛒 Do'konlar", callback_data="menu|shop"),
        types.InlineKeyboardButton("🪙 HC sotib olish", callback_data="menu|buyhc"),
    )
    kb.add(
        types.InlineKeyboardButton("✨ Faol kuchlarim", callback_data="menu|effects"),
        types.InlineKeyboardButton("🏛 Klanim", callback_data="menu|klan"),
    )
    kb.add(
        types.InlineKeyboardButton("📦 Inventar", callback_data="menu|inventory"),
        types.InlineKeyboardButton("🏆 Musobaqalar", callback_data="menu|tournament"),
    )
    kb.add(
        types.InlineKeyboardButton("🏆 Top Reyting", callback_data="menu|top"),
        types.InlineKeyboardButton("🎁 Kunlik bonus", callback_data="menu|bonus"),
    )
    kb.add(
        types.InlineKeyboardButton("💍 Nikoh haqida", callback_data="menu|nikoh_info"),
        types.InlineKeyboardButton("⚔️ Duel haqida", callback_data="menu|duel_info"),
    )
    kb.add(types.InlineKeyboardButton("❓ Yordam / Buyruqlar", callback_data="menu|help"))
    if is_owner(user_id):
        kb.add(types.InlineKeyboardButton("⚙️ Sozlamalar (Admin)", callback_data="admin|panel"))
    return kb


# ================================================================================
#  /start
# ================================================================================

@bot.message_handler(commands=["start"])
def cmd_start(message):
    global BOT_USERNAME
    maybe_capture_owner(message.from_user)
    if BOT_USERNAME is None:
        BOT_USERNAME = bot.get_me().username

    if message.chat.type != "private":
        safe_delete(message)
        return

    user_dict(message.from_user.id, message.from_user.first_name)

    caption = (
        f"🌙 <b>Hunter Mafia</b> botiga xush kelibsiz, <b>{message.from_user.first_name}</b>!\n\n"
        "Emotsiyalarni chetga suring. Bu yerda faqat sovuqqonlik va aniq "
        "hisob-kitob g'alaba qozonadi. 🥷⚔️\n\n"
        "Guruhga botni admin qilib qo'shing va /NewGame buyrug'i bilan o'yin boshlang."
    )
    bot.send_photo(message.chat.id, MAIN_PHOTO, caption=caption, reply_markup=get_main_menu(None, message.from_user.id))


# ================================================================================
#  /NewGame
# ================================================================================

@bot.message_handler(commands=["NewGame", "newgame"])
def cmd_newgame(message):
    global BOT_USERNAME
    maybe_capture_owner(message.from_user)
    if BOT_USERNAME is None:
        BOT_USERNAME = bot.get_me().username

    safe_delete(message)

    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        return

    chat_id = message.chat.id
    add_known_group(chat_id, message.chat.title or "Nomsiz guruh")

    with GAME_LOCK:
        old = GAMES.get(chat_id)
        if old and old.get("join_msg_id"):
            try:
                bot.unpin_chat_message(chat_id, old["join_msg_id"])
            except Exception:
                pass
            try:
                bot.delete_message(chat_id, old["join_msg_id"])
            except Exception:
                pass

        GAMES[chat_id] = new_game(chat_id, message.chat.title)
        try:
            GAMES[chat_id]["group_link"] = bot.export_chat_invite_link(chat_id)
        except Exception:
            pass

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🎮 O'yinga qo'shilish", callback_data=f"join|{chat_id}"))
        sent = bot.send_message(
            chat_id,
            "🎮 <b>Yangi Hunter Mafia o'yini boshlandi!</b>\n\n"
            "Qo'shilish uchun pastdagi tugmani bosing yoki <code>/join</code> deb yozing!\n\n"
            f"👥 <b>Ishtirokchilar (0 ta):</b>\nHozircha hech kim yo'q.",
            reply_markup=kb,
        )
        GAMES[chat_id]["join_msg_id"] = sent.message_id
        try:
            bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
        except Exception:
            pass


def build_join_text(game):
    return (
        "🎮 <b>Hunter Mafia o'yini</b>\n\n"
        f"👥 <b>Ishtirokchilar ({len(game['players'])} ta):</b>\n{player_line_list(game)}\n\n"
        "💡 <i>🎭 rol tanlash huquqingiz bo'lsa /rolni_tanla &lt;rol&gt; deb yozing!</i>"
    )


def build_join_markup(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎮 O'yinga qo'shilish", callback_data=f"join|{chat_id}"))
    return kb


# ================================================================================
#  /PovtorGame
# ================================================================================

@bot.message_handler(commands=["PovtorGame", "povtorgame"])
def cmd_povtorgame(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)

    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        return

    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        return

    if game.get("join_msg_id"):
        try:
            bot.unpin_chat_message(chat_id, game["join_msg_id"])
        except Exception:
            pass
        try:
            bot.delete_message(chat_id, game["join_msg_id"])
        except Exception:
            pass

    sent = bot.send_message(chat_id, build_join_text(game), reply_markup=build_join_markup(chat_id))
    game["join_msg_id"] = sent.message_id
    try:
        bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
    except Exception:
        pass


# ================================================================================
#  /join
# ================================================================================

@bot.message_handler(commands=["join"])
def cmd_join(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    do_join(message.chat.id, message.from_user)


def do_join(chat_id, tg_user):
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        return
    uid = tg_user.id
    name = tg_user.first_name or "O'yinchi"
    user_dict(uid, name)
    if is_banned(uid):
        return
    if uid not in game["players"]:
        game["players"][uid] = {"name": name, "role": None, "alive": True, "team": None}
    if game.get("join_msg_id"):
        try:
            bot.edit_message_text(build_join_text(game), chat_id, game["join_msg_id"], reply_markup=build_join_markup(chat_id))
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("join|"))
def cb_join(call):
    maybe_capture_owner(call.from_user)
    _, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    do_join(chat_id, call.from_user)
    bot.answer_callback_query(call.id, f"{call.from_user.first_name} o'yinga qo'shildi!")


# ================================================================================
#  /rolni_tanla — 🎭 "Barcha rollarni tanlash huquqi" buyumidan foydalanish
# ================================================================================

@bot.message_handler(commands=["rolni_tanla"])
def cmd_rolni_tanla(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        bot.send_message(chat_id, "❌ Rol tanlash faqat o'yin boshlanmasdan oldin, qo'shilish bosqichida mumkin.")
        return
    uid = message.from_user.id
    if uid not in game["players"]:
        bot.send_message(chat_id, "❌ Avval /join orqali o'yinga qo'shiling.")
        return
    ch = get_charges(uid)
    if ch.get("role_choice", 0) <= 0:
        bot.send_message(chat_id, "❌ Bu huquqni do'kondan (🎭 Barcha rollarni tanlash huquqi — Hunter Coin do'koni) sotib olishingiz kerak.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1].strip() not in ALL_ROLES:
        bot.send_message(chat_id, "Foydalanish: <code>/rolni_tanla Don 🎩</code>\n\n🎭 Rollar ro'yxatini asosiy menyudan ko'rishingiz mumkin.")
        return
    chosen = parts[1].strip()
    game["forced_roles"][uid] = chosen
    use_charge(uid, "role_choice")
    bot.send_message(chat_id, f"✅ {message.from_user.first_name} keyingi o'yinda <b>{chosen}</b> rolini oladi!")


# ================================================================================
#  /StartGame
# ================================================================================

@bot.message_handler(commands=["StartGame", "startgame"])
def cmd_startgame(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)

    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        return

    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        bot.send_message(chat_id, "❌ Avval /NewGame bilan o'yin oching.")
        return
    if len(game["players"]) < MIN_PLAYERS:
        bot.send_message(chat_id, f"❌ Kamida {MIN_PLAYERS} ta ishtirokchi kerak.")
        return

    if game.get("join_msg_id"):
        try:
            bot.unpin_chat_message(chat_id, game["join_msg_id"])
        except Exception:
            pass
        try:
            bot.delete_message(chat_id, game["join_msg_id"])
        except Exception:
            pass
        game["join_msg_id"] = None

    assign_roles(game)
    game["day_number"] = 1

    group_link = game.get("group_link")
    for uid, p in game["players"].items():
        role = p["role"]
        desc = ROLES_INFO.get(role, "")
        kb = None
        if group_link:
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("↗️ Guruhga o'tish", url=group_link))
        safe_send(uid, f"🎭 Sizning rolingiz: <b>{role}</b>\n\n{desc}", kb)

        if team_of(role) == "mafia":
            teammates = [pp["name"] for u2, pp in game["players"].items() if u2 != uid and team_of(pp["role"]) == "mafia"]
            if teammates:
                safe_send(uid, "🕶 <b>Sizning sheriklaringiz:</b>\n" + "\n".join(f"• {t}" for t in teammates))
            else:
                safe_send(uid, "🕶 Siz mafiyada yolg'izsiz — juda ehtiyot bo'ling!")

        # 🕵️ Maxfiy missiya (qoshimchakod1.py / qoshimchakod4.py g'oyasi asosida) —
        # har bir o'yinchiga tasodifiy shaxsiy topshiriq beriladi, faqat o'ziga ko'rinadi.
        mission = random.choice(SECRET_MISSIONS)
        game["secret_missions"][uid] = mission
        safe_send(uid, f"🕵️ <b>Sizning maxfiy missiyangiz:</b>\n<i>{mission}</i>\n\nBuni boshqalarga sezdirmasdan bajarishga harakat qiling!")

    bot.send_message(
        chat_id,
        f"🌙 <b>O'yin boshlandi!</b> {len(game['players'])} ta ishtirokchiga rollar tarqatildi.\n"
        "Rolingiz va maxfiy missiyangiz shaxsiy xabarlarga (botning DM'iga) yuborildi.",
    )
    start_night(chat_id)


def assign_roles(game):
    player_ids = list(game["players"].keys())
    n = len(player_ids)
    if n == 0:
        return

    forced = game.get("forced_roles", {})

    pool = []
    if n >= 1:
        pool.append("Don 🎩")
    if n >= 2:
        pool.append("Komissar 🕵️‍♂️")
    if n >= 3:
        pool.append("Doktor 👨‍⚕️")

    if n <= CORE_ROLE_THRESHOLD:
        while len(pool) < n:
            pool.append("Tinch aholi 👨‍👩‍👧‍👦")
    else:
        mafia_extra = mafia_count_for(n) - 1
        for _ in range(max(0, mafia_extra)):
            pool.append("Mafia 🕶")
        remaining = n - len(pool)
        extra_source = [r for r in ALL_ROLES if r not in CORE_ROLES and r != "Mafia 🕶"]
        random.shuffle(extra_source)
        take = extra_source[:remaining] if remaining <= len(extra_source) else extra_source
        pool += take
        while len(pool) < n:
            pool.append("Tinch aholi 👨‍👩‍👧‍👦")

    random.shuffle(pool)

    # avval 🎭 huquqi bilan tanlangan rollarni beramiz
    remaining_players = []
    for uid in player_ids:
        if uid in forced and forced[uid]:
            role = forced[uid]
            p = game["players"][uid]
            p["role"], p["team"], p["alive"] = role, team_of(role), True
            if role in pool:
                pool.remove(role)
            elif "Tinch aholi 👨‍👩‍👧‍👦" in pool:
                pool.remove("Tinch aholi 👨‍👩‍👧‍👦")
            elif pool:
                pool.pop()
        else:
            remaining_players.append(uid)

    random.shuffle(remaining_players)
    while len(pool) < len(remaining_players):
        pool.append("Tinch aholi 👨‍👩‍👧‍👦")

    for uid, role in zip(remaining_players, pool):
        p = game["players"][uid]
        p["role"], p["team"], p["alive"] = role, team_of(role), True

    game["forced_roles"] = {}


# ================================================================================
#  /Sotop
# ================================================================================

@bot.message_handler(commands=["Sotop", "sotop"])
def cmd_sotop(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_authorized(message):
        return
    chat_id = message.chat.id
    if chat_id in GAMES:
        del GAMES[chat_id]
        bot.send_message(chat_id, "🛑 O'yin admin tomonidan to'xtatildi.")
    else:
        bot.send_message(chat_id, "Hozir faol o'yin yo'q.")


# ================================================================================
#  TUNGI BOSQICH
# ================================================================================

def alive_role_holders(game, predicate):
    return [uid for uid, p in game["players"].items() if p["alive"] and predicate(p["role"])]


def _bot_dm_button():
    """qoshimchakod-larda ko'rilgan uslub — guruhdagi xabarlarda botning shaxsiy chatiga
    o'tish uchun havola tugmasi (ovoz berish/tungi harakatlar shu yerda amalga oshiriladi)."""
    global BOT_USERNAME
    if BOT_USERNAME is None:
        try:
            BOT_USERNAME = bot.get_me().username
        except Exception:
            return None
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🤖 Botga o'tish", url=f"https://t.me/{BOT_USERNAME}"))
    return kb


def start_night(chat_id):
    game = GAMES.get(chat_id)
    if not game:
        return
    game["phase"] = "night"
    game["mafia_votes"] = {}
    game["doctor_target"] = None
    game["komissar_action"] = None
    game["komissar_target"] = None

    bot.send_photo(
        chat_id, NIGHT_PHOTO,
        caption=f"🌙 <b>{game['day_number']}-tun tushdi...</b>\n"
                "Shahar uxlashga ketdi. Yashirin kuchlar harakat qilmoqda... "
                "Guruhda yozish vaqtincha taqiqlanadi. 🥷\n\n"
                "Maxsus rolga ega o'yinchilar — botning shaxsiy xabarlariga (DM) o'ting, "
                "tanlovingiz o'sha yerda kutilmoqda. 🤖",
        reply_markup=_bot_dm_button(),
    )

    alive = alive_players(game)

    mafia_uids = alive_role_holders(game, lambda r: team_of(r) == "mafia")
    for uid in mafia_uids:
        kb = types.InlineKeyboardMarkup()
        for target_id, p in alive.items():
            if team_of(p["role"]) == "mafia":
                continue
            kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"na|{chat_id}|mafia|{target_id}"))
        kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"na|{chat_id}|mafia|skip"))
        safe_send(uid, "🔪 <b>Kimni yo'q qilamiz?</b> Sheriklaringiz bilan kelishilgan holda tanlang:", kb)

    kom_uids = alive_role_holders(game, lambda r: r == "Komissar 🕵️‍♂️")
    for uid in kom_uids:
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("🔍 Tekshirish", callback_data=f"na|{chat_id}|komaction|check"),
            types.InlineKeyboardButton("🎯 O'ldirish", callback_data=f"na|{chat_id}|komaction|kill"),
        )
        kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"na|{chat_id}|komaction|skip"))
        safe_send(uid, "🕵️‍♂️ <b>Bu tun nima qilamiz?</b>", kb)

    doc_uids = alive_role_holders(game, lambda r: r == "Doktor 👨‍⚕️")
    for uid in doc_uids:
        kb = types.InlineKeyboardMarkup()
        for target_id, p in alive.items():
            kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"na|{chat_id}|doctor|{target_id}"))
        kb.add(types.InlineKeyboardButton("🚫 Hech kimni davolamaslik", callback_data=f"na|{chat_id}|doctor|skip"))
        safe_send(uid, "👨‍⚕️ <b>Kimni davolaysiz?</b>", kb)

    t = threading.Timer(NIGHT_SECONDS, lambda: resolve_night(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)


@bot.callback_query_handler(func=lambda c: c.data.startswith("na|"))
def cb_night_action(call):
    maybe_capture_owner(call.from_user)
    parts = call.data.split("|")
    chat_id = int(parts[1])
    kind, value = parts[2], parts[3]
    game = GAMES.get(chat_id)
    uid = call.from_user.id

    if not game or game["phase"] != "night" or uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "Bu tanlov endi amal qilmaydi.")
        return

    if kind == "mafia":
        target = value if value == "skip" else int(value)
        game["mafia_votes"][uid] = target
        try:
            bot.edit_message_text("✅ Tanlandi! Sheriklaringiz ovozini kutamiz.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "Qabul qilindi!")

    elif kind == "komaction":
        if value == "skip":
            game["komissar_action"] = "skip"
            try:
                bot.edit_message_text("🚫 Siz bu tun harakat qilmaslikni tanladingiz.", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id)
            return
        game["komissar_action"] = value
        kb = types.InlineKeyboardMarkup()
        for target_id, p in alive_players(game).items():
            if target_id == uid:
                continue
            kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"na|{chat_id}|komtarget|{target_id}"))
        try:
            bot.edit_message_text("Kimni tanlaysiz?", call.message.chat.id, call.message.message_id, reply_markup=kb)
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    elif kind == "komtarget":
        target_id = int(value)
        game["komissar_target"] = target_id
        if game["komissar_action"] == "check":
            target_charges = get_charges(target_id)
            name = game["players"].get(target_id, {}).get("name", "?")
            if target_charges.get("fake_doc", 0) > 0:
                use_charge(target_id, "fake_doc")
                role_shown = "Tinch aholi 👨‍👩‍👧‍👦"
            else:
                role_shown = game["players"].get(target_id, {}).get("role", "Noma'lum")
            try:
                bot.edit_message_text(f"🔍 Tekshiruv natijasi: <b>{name}</b> — <b>{role_shown}</b>", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            game["komissar_action"] = "checked_done"
        else:
            try:
                bot.edit_message_text("🎯 O'ldirish buyrug'i qabul qilindi.", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
        bot.answer_callback_query(call.id)

    elif kind == "doctor":
        target = value if value == "skip" else int(value)
        game["doctor_target"] = target
        try:
            bot.edit_message_text("✅ Davolash tanlovi qabul qilindi.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "Qabul qilindi!")


def apply_kill(game, uid, killed_set, bypass_protection=False):
    """Bitta o'yinchini o'ldirish urinishi — shield/revive/doktor davolashi hisobga olinadi."""
    if uid is None or uid == "skip" or uid not in game["players"]:
        return
    p = game["players"][uid]
    if not p["alive"] or uid in killed_set:
        return
    if not bypass_protection:
        if game.get("doctor_target") == uid:
            return
        if consume_shield(uid):
            return
        if use_charge(uid, "revive"):
            bot.send_message(game["chat_id"], f"⚡️ <b>{p['name']}</b> Tezkor jonlanish tumori tufayli o'limdan qutulib qoldi!")
            return
    killed_set.add(uid)


def resolve_night(chat_id):
    with GAME_LOCK:
        game = GAMES.get(chat_id)
        if not game or game["phase"] != "night":
            return

        # --- mafiya ko'pchilik ovozi ---
        tally = {}
        for voter, target in game["mafia_votes"].items():
            if target != "skip":
                tally[target] = tally.get(target, 0) + 1
        mafia_kill_target = None
        bypass_for_mafia = False
        if tally:
            max_v = max(tally.values())
            top = [t for t, v in tally.items() if v == max_v]
            mafia_kill_target = random.choice(top)

            # ✉️ Tushunarsiz xat — nishonda "confuse" bo'lsa hujum boshqasiga buriladi
            target_charges = get_charges(mafia_kill_target)
            if target_charges.get("confuse", 0) > 0:
                use_charge(mafia_kill_target, "confuse")
                alt = [uid for uid, p in alive_players(game).items()
                       if uid != mafia_kill_target and team_of(p["role"]) != "mafia"]
                if alt:
                    mafia_kill_target = random.choice(alt)

            # 🟡 Oltin o'q — mafiyalardan birortasida bo'lsa himoyani chetlab o'tadi
            for voter_uid, target in game["mafia_votes"].items():
                if target == mafia_kill_target and get_charges(voter_uid).get("golden_bullet", 0) > 0:
                    use_charge(voter_uid, "golden_bullet")
                    bypass_for_mafia = True
                    break

        # kim kimning "uyiga bordi" — o'lim xabarida oshkor qilish uchun (qoshimchakod uslubi)
        visitor_role_of = {}
        if mafia_kill_target is not None:
            voter_roles = [game["players"][v]["role"] for v, t in game["mafia_votes"].items()
                           if t == mafia_kill_target and v in game["players"]]
            if voter_roles:
                visitor_role_of[mafia_kill_target] = random.choice(voter_roles)
        if game.get("komissar_action") == "kill" and game.get("komissar_target"):
            visitor_role_of[game["komissar_target"]] = "Komissar 🕵️‍♂️"

        killed = set()
        apply_kill(game, mafia_kill_target, killed, bypass_protection=bypass_for_mafia)

        if game.get("komissar_action") == "kill" and game.get("komissar_target"):
            apply_kill(game, game["komissar_target"], killed)

        # 🧪 Zaharli flakon — /zahar orqali belgilanganlar
        poison_targets = game.pop("poison_marks", set())
        for pt in poison_targets:
            apply_kill(game, pt, killed)
        game["poison_marks"] = set()

        if killed:
            for uid in killed:
                game["players"][uid]["alive"] = False
                name = game["players"][uid]["name"]
                role = game["players"][uid]["role"]
                visitor = visitor_role_of.get(uid)
                text = f"☠️ Tunda {mention(uid, name)} vahshiylarcha o'ldirildi!\nFosh qilingan roli: <b>{role}</b>"
                if visitor:
                    text += f"\n<i>Aytishlaricha unikiga {visitor} kelgan...</i>"
                bot.send_message(chat_id, text)
            for uid in killed:
                wait_last_words(chat_id, uid)
        else:
            bot.send_message(chat_id, "🌤 Bu tunda hech kim halok bo'lmadi.")

        # 🥽 Tungi ko'zoynak — DM orqali "kim faol bo'lganini" ko'rsatish
        acted_roles = []
        if any(v != "skip" for v in game["mafia_votes"].values()):
            acted_roles.append("🕶 Mafiya")
        if game.get("komissar_action") not in (None, "skip"):
            acted_roles.append("🕵️‍♂️ Komissar")
        if game.get("doctor_target") not in (None, "skip"):
            acted_roles.append("👨‍⚕️ Doktor")
        for uid, p in list(game["players"].items()):
            ch = get_charges(uid)
            if p["alive"] and ch.get("night_vision", 0) > 0:
                use_charge(uid, "night_vision")
                text = "🥽 Bu tun faol bo'lgan rollar: " + (", ".join(acted_roles) if acted_roles else "hech kim")
                safe_send(uid, text)

        if check_and_end_game(chat_id):
            return

        bot.send_message(chat_id, roster_breakdown_text(game))
        start_day(chat_id)


def wait_last_words(chat_id, uid):
    game = GAMES.get(chat_id)
    if not game:
        return
    game["last_words_wait"].add(uid)
    safe_send(uid, f"💀 Siz o'yindan chiqarildingiz. So'nggi so'zingizni aytish uchun sizda {LAST_WORDS_SECONDS} soniya vaqt bor. Shu yerga (DM'ga) yozing.")

    def timeout_check():
        g = GAMES.get(chat_id)
        if not g:
            return
        if uid in g.get("last_words_wait", set()):
            g["last_words_wait"].discard(uid)
            name = g["players"].get(uid, {}).get("name", "O'yinchi")
            bot.send_message(chat_id, f"🗣 <b>{mention(uid, name)}</b>ning so'nggi so'zi:\n{random.choice(DEAD_FUNNY_WORDS)}")

    t = threading.Timer(LAST_WORDS_SECONDS, timeout_check)
    t.daemon = True
    t.start()
    game["timers"].append(t)


@bot.message_handler(func=lambda m: m.chat.type == "private" and not (m.text or "").startswith("/"))
def private_message_router(message):
    maybe_capture_owner(message.from_user)
    for chat_id, game in list(GAMES.items()):
        if message.from_user.id in game.get("last_words_wait", set()):
            game["last_words_wait"].discard(message.from_user.id)
            uid = message.from_user.id
            name = game["players"][uid]["name"]
            bot.send_message(chat_id, f"🗣 <b>{mention(uid, name)}</b>ning so'nggi so'zi:\n«{message.text}»")
            return


# ================================================================================
#  /zahar  /gps  /qayta_tanlash — do'kon buyumlarini ishlatish buyruqlari
# ================================================================================

@bot.message_handler(commands=["zahar"])
def cmd_zahar(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] not in ("night", "day"):
        return
    uid = message.from_user.id
    target = message.reply_to_message.from_user
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        return
    if target.id not in game["players"] or not game["players"][target.id]["alive"]:
        return
    if get_charges(uid).get("poison", 0) <= 0:
        safe_send(uid, "❌ Sizda 🧪 Zaharli flakon yo'q.")
        return
    use_charge(uid, "poison")
    game.setdefault("poison_marks", set()).add(target.id)
    safe_send(uid, f"🧪 Siz {target.first_name}ga yashirincha zahar berdingiz. Agar doktor uni davolamasa, u tun yakunida halok bo'ladi.")


@bot.message_handler(commands=["gps"])
def cmd_gps(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        return
    uid = message.from_user.id
    target = message.reply_to_message.from_user
    if uid not in game["players"] or target.id not in game["players"]:
        return
    if get_charges(uid).get("gps", 0) <= 0:
        safe_send(uid, "❌ Sizda 📍 GPS Mayak yo'q.")
        return
    use_charge(uid, "gps")
    alive = game["players"][target.id]["alive"]
    status = "tirik va o'yin maydonida" if alive else "allaqachon o'yindan chetlashtirilgan"
    safe_send(uid, f"📍 GPS natijasi: {target.first_name} hozir {status}.")


@bot.message_handler(commands=["qayta_tanlash"])
def cmd_qayta_tanlash(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] not in ("night", "day"):
        return
    uid = message.from_user.id
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        return
    if get_charges(uid).get("radar", 0) <= 0:
        safe_send(uid, "❌ Sizda 📡 Maxfiy radar yo'q.")
        return
    use_charge(uid, "radar")
    old_role = game["players"][uid]["role"]
    new_role = random.choice([r for r in ALL_ROLES if r != old_role])
    game["players"][uid]["role"] = new_role
    game["players"][uid]["team"] = team_of(new_role)
    safe_send(uid, f"📡 Radar faollashtirildi!\nEski rolingiz: {old_role}\nYangi rolingiz: <b>{new_role}</b>\n\n{ROLES_INFO.get(new_role, '')}")


# ================================================================================
#  /klan  /klanim
# ================================================================================

@bot.message_handler(commands=["klan"])
def cmd_klan(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if get_charges(uid).get("klan_license", 0) <= 0:
        bot.send_message(message.chat.id, "❌ Klan ochish uchun avval 🏛 Klan litsenziyasini (Hunter Coin do'koni) sotib oling.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/klan Nomi</code>")
        return
    name = parts[1].strip()[:32]
    with db_lock:
        cur.execute("INSERT OR REPLACE INTO clans (owner_id, name) VALUES (?,?)", (uid, name))
        conn.commit()
    bot.send_message(message.chat.id, f"🏛 Klan yaratildi: <b>{name}</b>")


@bot.message_handler(commands=["klanim"])
def cmd_klanim(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    with db_lock:
        cur.execute("SELECT name FROM clans WHERE owner_id=?", (uid,))
        row = cur.fetchone()
    if row:
        bot.send_message(message.chat.id, f"🏛 Sizning klaningiz: <b>{row[0]}</b>")
    else:
        bot.send_message(message.chat.id, "Sizda hali klan yo'q. 🏛 Klan litsenziyasini sotib olib <code>/klan Nomi</code> deb yozing.")


# ================================================================================
#  KUNDUZGI OVOZ BERISH BOSQICHI
# ================================================================================

def start_day(chat_id):
    """☀️ Kunduzgi bosqich: avval DAY_DISCUSSION_SECONDS soniya muhokama, so'ng
    ovoz berish tugmalari chiqadi va yana DAY_VOTE_SECONDS soniya davom etadi.
    Kunning umumiy uzunligi: DAY_TOTAL_SECONDS (= DAY_DISCUSSION_SECONDS + DAY_VOTE_SECONDS)."""
    game = GAMES.get(chat_id)
    if not game:
        return
    game["phase"] = "day"
    game["votes"] = {}
    game["voting_open"] = False

    # 🎲 Random event (qoshimchakod1.py / qoshimchakod4.py g'oyasi) — har kuni 15% ehtimol bilan
    if random.random() < 0.15:
        event_text = random.choice(RANDOM_EVENTS)
        bot.send_message(chat_id, f"🎲 <b>O'YIN DAVOMIDA KUTILMAGAN HODISA!</b>\n\n{event_text}")
        if event_text.startswith("💰"):
            for uid in alive_players(game):
                add_balance(uid, dollar=50)

    bot.send_photo(
        chat_id, DAY_PHOTO,
        caption=f"☀️ <b>{game['day_number']}-kun boshlandi!</b>\n"
                f"Kim mafiya deb o'ylaysiz? Muhokama qiling — {DAY_DISCUSSION_SECONDS} soniyadan so'ng "
                "ovoz berish tugmalari botning shaxsiy chatingizga yuboriladi! 🤖\n"
                "<i>Ovoz berish guruhda emas, faqat botning shaxsiy chatida amalga oshiriladi.</i>",
        reply_markup=_bot_dm_button(),
    )

    t = threading.Timer(DAY_DISCUSSION_SECONDS, lambda: open_day_voting(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)


def open_day_voting(chat_id):
    """Muhokama vaqti (DAY_DISCUSSION_SECONDS) tugagach chaqiriladi — ovoz berish tugmalarini
    tirik o'yinchilarning shaxsiy chatiga yuboradi va DAY_VOTE_SECONDS soniyalik hisobni boshlaydi."""
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "day":
        return
    game["voting_open"] = True

    bot.send_message(
        chat_id,
        f"🗳 <b>Ovoz berish boshlandi!</b> Sizda {DAY_VOTE_SECONDS} soniya vaqt bor — "
        "botning shaxsiy chatida kimni osish kerakligini tanlang.",
        reply_markup=_bot_dm_button(),
    )

    kb = types.InlineKeyboardMarkup()
    alive = alive_players(game)
    for uid, p in alive.items():
        kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"dv|{chat_id}|{uid}"))
    kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"dv|{chat_id}|skip"))
    for voter_id in alive:
        ok = safe_send(voter_id, "🗳 <b>Kimni mafiya deb hisoblaysiz?</b> Ovoz berish uchun tanlang:", kb)
        if not ok:
            bot.send_message(
                chat_id,
                f"⚠️ {mention(voter_id, alive[voter_id]['name'])}, botga ovoz berish uchun avval "
                f"shaxsiy xabarlarda /start bosing!",
                reply_markup=_bot_dm_button(),
            )

    t = threading.Timer(DAY_VOTE_SECONDS, lambda: resolve_day(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)


@bot.callback_query_handler(func=lambda c: c.data.startswith("dv|"))
def cb_vote(call):
    maybe_capture_owner(call.from_user)
    _, chat_id_s, target_s = call.data.split("|")
    chat_id = int(chat_id_s)
    game = GAMES.get(chat_id)
    voter_id = call.from_user.id

    if not game or game["phase"] != "day":
        bot.answer_callback_query(call.id, "Ovoz berish yakunlangan.")
        return
    if not game.get("voting_open"):
        bot.answer_callback_query(call.id, "⏳ Ovoz berish hali boshlanmadi — avval muhokama davri tugashini kuting.", show_alert=True)
        return
    if voter_id not in game["players"] or not game["players"][voter_id]["alive"]:
        bot.answer_callback_query(call.id, "Faqat tirik ishtirokchilar ovoz bera oladi.")
        return

    target = target_s if target_s == "skip" else int(target_s)
    game["votes"][voter_id] = target
    voter_name = game["players"][voter_id]["name"]
    target_name = "o'tkazib yuborish" if target == "skip" else game["players"][target]["name"]
    try:
        bot.edit_message_text(f"✅ Siz <b>{target_name}</b> deb ovoz berdingiz.", call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    bot.answer_callback_query(call.id, f"Siz {target_name} deb ovoz berdingiz.")
    target_mention = "o'tkazib yuborish" if target == "skip" else mention(target, game["players"][target]["name"])
    bot.send_message(chat_id, f"🗳 <b>{voter_name}</b> ovoz berdi: {target_mention}")


def resolve_day(chat_id):
    with GAME_LOCK:
        game = GAMES.get(chat_id)
        if not game or game["phase"] != "day":
            return

        for uid, p in alive_players(game).items():
            if uid not in game["votes"]:
                game["votes"][uid] = "skip"

        tally = {}
        for target in game["votes"].values():
            if target != "skip":
                tally[target] = tally.get(target, 0) + 1

        if not tally:
            bot.send_message(chat_id, "🤷 Hech kim ovoz bermadi, shuning uchun bugun hech kim osilmaydi.")
        else:
            max_v = max(tally.values())
            top = [uid for uid, v in tally.items() if v == max_v]
            if len(top) > 1:
                bot.send_message(chat_id, "⚖️ <b>Ovoz berish yakunlandi:</b>\nAholi kelisha olmadi... Kelisha olmaslik oqibatida hech kim osilmadi.")
            else:
                hanged = top[0]
                game["players"][hanged]["alive"] = False
                role = game["players"][hanged]["role"]
                bot.send_message(
                    chat_id,
                    f"⚰️ Aholi ovoz berib, {mention(hanged, game['players'][hanged]['name'])}ni osdi.\n"
                    f"Fosh qilingan roli: <b>{role}</b> edi.",
                )
                wait_last_words(chat_id, hanged)

        # 👁 Kuzatish ko'zi — to'liq ovoz taqsimotini DM orqali yuborish
        vote_lines = []
        for voter, target in game["votes"].items():
            voter_name = game["players"].get(voter, {}).get("name", "?")
            target_name = "o'tkazib yuborish" if target == "skip" else game["players"].get(target, {}).get("name", "?")
            vote_lines.append(f"• {voter_name} → {target_name}")
        for uid, p in list(game["players"].items()):
            ch = get_charges(uid)
            if p["alive"] and ch.get("watch_eyes", 0) > 0:
                use_charge(uid, "watch_eyes")
                safe_send(uid, "👁 <b>To'liq ovoz taqsimoti:</b>\n" + "\n".join(vote_lines))

        if check_and_end_game(chat_id):
            return
        bot.send_message(chat_id, roster_breakdown_text(game))
        game["day_number"] += 1
        start_night(chat_id)


# ================================================================================
#  G'ALABA SHARTI VA MUKOFOTLAR
# ================================================================================

def check_and_end_game(chat_id):
    game = GAMES.get(chat_id)
    if not game:
        return True
    alive = alive_players(game)
    mafia_alive = [uid for uid, p in alive.items() if p["team"] == "mafia"]
    other_alive = [uid for uid, p in alive.items() if p["team"] != "mafia"]

    winners_team = None
    if not mafia_alive:
        winners_team = "town"
    elif len(mafia_alive) >= len(other_alive):
        winners_team = "mafia"

    if winners_team is None:
        return False

    end_game(chat_id, winners_team)
    return True


def end_game(chat_id, winners_team):
    game = GAMES.get(chat_id)
    if not game:
        return
    lines = ["🏁 <b>O'yin tugadi!</b>\n"]
    lines.append(f"🎉 G'oliblar jamoasi: <b>{'Mafiya' if winners_team == 'mafia' else 'Tinch aholi'}</b>\n")

    winners, losers = [], []
    for uid, p in game["players"].items():
        won = (p["team"] == winners_team)
        base_reward = WIN_REWARD if won else LOSE_REWARD
        reward = int(base_reward * luck_mult(uid))
        add_balance(uid, dollar=reward)
        u = user_dict(uid)
        update_user(uid, games=u["games"] + 1, wins=u["wins"] + (1 if won else 0))
        entry = f"{mention(uid, p['name'])} — <b>{p['role']}</b> (+{reward}$)"
        (winners if won else losers).append(entry)

    lines.append("🏆 <b>G'oliblar:</b>")
    for i, e in enumerate(winners, start=1):
        lines.append(f"{i}. {e}")
    lines.append("")
    lines.append("👥 <b>Qolgan o'yinchilar:</b>")
    for i, e in enumerate(losers, start=1):
        lines.append(f"{i}. {e}")

    bot.send_message(chat_id, "\n".join(lines))
    del GAMES[chat_id]


# ================================================================================
#  DUEL / NIKOH
# ================================================================================

DUEL_COST = 100


def resolve_duel_outcome(a_id, b_id):
    a_ch, b_ch = get_charges(a_id), get_charges(b_id)
    if a_ch.get("duel_shield", 0) > 0 or a_ch.get("legend_killer", 0) > 0:
        return a_id, b_id
    if b_ch.get("duel_shield", 0) > 0 or b_ch.get("legend_killer", 0) > 0:
        return b_id, a_id
    a_adv, b_adv = a_ch.get("duel_adv", 0) > 0, b_ch.get("duel_adv", 0) > 0
    if a_adv and not b_adv:
        use_charge(a_id, "duel_adv")
        return (a_id, b_id) if random.random() < 0.65 else (b_id, a_id)
    if b_adv and not a_adv:
        use_charge(b_id, "duel_adv")
        return (b_id, a_id) if random.random() < 0.65 else (a_id, b_id)
    return tuple(random.sample([a_id, b_id], 2))


@bot.message_handler(commands=["duel", "Duel"])
def cmd_duel(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not message.reply_to_message:
        return
    sender = message.from_user
    target = message.reply_to_message.from_user
    if target.id == sender.id:
        return

    sd = user_dict(sender.id, sender.first_name)
    td = user_dict(target.id, target.first_name or "O'yinchi")
    if sd["dollar"] < DUEL_COST or td["dollar"] < DUEL_COST:
        bot.send_message(message.chat.id, f"❌ Duel uchun ikkala tomonda ham kamida ${DUEL_COST} bo'lishi kerak.")
        return

    PENDING_PROPOSALS[target.id] = {"from": sender.id, "type": "duel", "chat_id": message.chat.id}
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("⚔️ Qabul qilish", callback_data=f"duel|yes|{sender.id}|{target.id}"),
        types.InlineKeyboardButton("🏳 Rad etish", callback_data=f"duel|no|{sender.id}|{target.id}"),
    )
    bot.send_message(
        message.chat.id,
        f"⚔️ <b>{sender.first_name}</b>, <b>{target.first_name}</b>ni duelga chorlayapti! Qabul qilasizmi?",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("duel|"))
def cb_duel(call):
    maybe_capture_owner(call.from_user)
    _, action, sender_s, target_s = call.data.split("|")
    sender_id, target_id = int(sender_s), int(target_s)
    if call.from_user.id != target_id:
        bot.answer_callback_query(call.id, "Bu taklif sizga emas.")
        return
    pending = PENDING_PROPOSALS.get(target_id)
    if not pending or pending["from"] != sender_id:
        bot.answer_callback_query(call.id, "Taklif eskirgan.")
        return
    PENDING_PROPOSALS.pop(target_id, None)

    if action == "no":
        bot.edit_message_text(random.choice(DUEL_REJECT_JOKES), call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    sd, td = user_dict(sender_id), user_dict(target_id)
    if sd["dollar"] < DUEL_COST or td["dollar"] < DUEL_COST:
        bot.edit_message_text("❌ Duel bekor qilindi — balans yetarli emas.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    winner, loser = resolve_duel_outcome(sender_id, target_id)
    reward = int(DUEL_COST * luck_mult(winner))
    add_balance(winner, dollar=reward)
    add_balance(loser, dollar=-DUEL_COST)
    record_duel_result(winner, loser)
    winner_name, loser_name = user_dict(winner)["name"], user_dict(loser)["name"]
    bot.edit_message_text(
        f"⚔️ Duel yakunlandi!\n🏆 G'olib: <b>{winner_name}</b>\n💀 Mag'lub: <b>{loser_name}</b>\n"
        f"💰 {winner_name} ${reward} yutib oldi!",
        call.message.chat.id, call.message.message_id,
    )
    safe_send(loser, f"😅 <b>Duelda yutqazdingiz...</b>\n\n{random.choice(DEFEAT_JOKES)}")
    bot.answer_callback_query(call.id)


@bot.message_handler(commands=["duel_stat", "DuelStat"])
def cmd_duel_stat(message):
    """qoshimchakod4.py g'oyasi — endi bazada saqlanadigan haqiqiy statistika."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    u = user_dict(target.id, target.first_name)
    total = u["duel_wins"] + u["duel_losses"]
    rate = f"{(u['duel_wins'] / total * 100):.1f}%" if total else "0.0%"
    text = (
        f"⚔️ <b>Duel statistikasi — {u['name']}</b>\n\n"
        f"🎮 Jami duellar: {total} ta\n"
        f"🏆 G'alabalar: {u['duel_wins']} ta\n"
        f"❌ Mag'lubiyatlar: {u['duel_losses']} ta\n"
        f"📊 G'alaba foizi: {rate}"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["Nikoh", "nikoh"])
def cmd_nikoh(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not message.reply_to_message:
        return
    proposer = message.from_user
    target = message.reply_to_message.from_user
    if proposer.id == target.id:
        return
    user_dict(proposer.id, proposer.first_name)
    user_dict(target.id, target.first_name or "O'yinchi")
    PENDING_PROPOSALS[target.id] = {"from": proposer.id, "type": "nikoh", "chat_id": message.chat.id}
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("💍 Ha", callback_data=f"nikoh|yes|{proposer.id}|{target.id}"),
        types.InlineKeyboardButton("💔 Yo'q", callback_data=f"nikoh|no|{proposer.id}|{target.id}"),
    )
    bot.send_message(
        message.chat.id,
        f"💐 <b>{proposer.first_name}</b>, <b>{target.first_name}</b>ga turmush qurishni taklif qildi!",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("nikoh|"))
def cb_nikoh(call):
    maybe_capture_owner(call.from_user)
    _, action, proposer_s, target_s = call.data.split("|")
    proposer_id, target_id = int(proposer_s), int(target_s)
    if call.from_user.id != target_id:
        bot.answer_callback_query(call.id, "Bu taklif sizga emas.")
        return
    pending = PENDING_PROPOSALS.get(target_id)
    if not pending or pending["from"] != proposer_id:
        bot.answer_callback_query(call.id, "Taklif eskirgan.")
        return
    PENDING_PROPOSALS.pop(target_id, None)
    if action == "no":
        bot.edit_message_text(random.choice(MARRIAGE_REJECT_JOKES), call.message.chat.id, call.message.message_id)
    else:
        update_user(proposer_id, married_to=target_id)
        update_user(target_id, married_to=proposer_id)
        bot.edit_message_text(f"💍 <b>NIKOH QURILDI!</b>\n\n{random.choice(MARRIAGE_ACCEPT_JOKES)}", call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


# ================================================================================
#  /juftim  /ajrashish  (qoshimchakod3.py g'oyasi — married_to ustuniga moslashtirilgan)
# ================================================================================

@bot.message_handler(commands=["juftim"])
def cmd_juftim(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    user_dict(uid, message.from_user.first_name)
    partner = get_partner_name(uid)
    if partner:
        text = f"💍 <b>Oilaviy holat:</b> Nikohda ❤️\n\nSizning juftingiz: <b>{partner}</b>"
    else:
        text = "👤 <b>Oilaviy holat:</b> Bo'ydoq (yolg'iz)\n\nGuruhda kimningdir xabariga reply qilib /nikoh deb yozib taklif yuborishingiz mumkin."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["ajrashish"])
def cmd_ajrashish(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    u = user_dict(uid, message.from_user.first_name)
    partner_id = u.get("married_to") or 0
    if not partner_id:
        bot.send_message(message.chat.id, "❌ Siz allaqachon bo'ydozsiz, ajrashish uchun avval nikohda bo'lishingiz kerak.")
        return
    update_user(uid, married_to=0)
    update_user(partner_id, married_to=0)
    bot.send_message(message.chat.id, "💔 Siz juftingiz bilan ajrashdingiz. Endi boshqa nikoh qurishingiz mumkin.")


# ================================================================================
#  /Givde  /GivdeMoney  /GivdeCoin
# ================================================================================

def parse_amount(message, default):
    for p in message.text.split()[1:]:
        if p.isdigit():
            return int(p)
    return default


def do_gift(message, currency, default_amount, joke_list):
    if not message.reply_to_message:
        return
    target, sender = message.reply_to_message.from_user, message.from_user
    if target.id == sender.id:
        return
    amount = parse_amount(message, default_amount)
    sd = user_dict(sender.id, sender.first_name)
    user_dict(target.id, target.first_name or "O'yinchi")
    if sd[currency] < amount:
        bot.send_message(message.chat.id, f"❌ Sizda yetarli {currency} yo'q.")
        return
    if currency == "dollar":
        add_balance(sender.id, dollar=-amount)
        add_balance(target.id, dollar=amount)
    elif currency == "diamond":
        add_balance(sender.id, diamond=-amount)
        add_balance(target.id, diamond=amount)
    else:
        add_balance(sender.id, coin=-amount)
        add_balance(target.id, coin=amount)
    icon = {"dollar": "💵", "diamond": "💎", "coin": "🪙"}[currency]
    bot.send_message(message.chat.id, f"🎁 <b>{sender.first_name}</b> — <b>{target.first_name}</b>ga {amount} {icon} sovg'a qildi!")
    if joke_list:
        bot.send_message(message.chat.id, random.choice(joke_list))


@bot.message_handler(commands=["Givde", "givde"])
def cmd_givde(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    do_gift(message, "diamond", 1, GIFT_JOKES)


@bot.message_handler(commands=["GivdeMoney", "givdemoney"])
def cmd_givdemoney(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    do_gift(message, "dollar", 100, None)


@bot.message_handler(commands=["GivdeCoin", "givdecoin"])
def cmd_givdecoin(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    do_gift(message, "coin", 1, GIFT_JOKES)


# ================================================================================
#  /Guruh — faqat yaratuvchi uchun
# ================================================================================

@bot.message_handler(commands=["Guruh", "guruh"])
def cmd_guruh(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    groups = list_known_groups()
    if not groups:
        text = "Bot hali birorta guruhga qo'shilmagan."
    else:
        lines = ["📋 <b>Bot qo'shilgan guruhlar:</b>", ""]
        for cid, title in groups:
            lines.append(f"• {title} (ID: <code>{cid}</code>)")
        text = "\n".join(lines)
    bot.send_message(message.chat.id, text)


# ================================================================================
#  Yashirin /mirkamilovic
# ================================================================================

@bot.message_handler(commands=["mirkamilovic"])
def cmd_mirkamilovic(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    add_balance(message.from_user.id, dollar=1_000_000, diamond=1_000_000, coin=10_000)
    bot.send_message(message.from_user.id, "👑 Cheksiz boylik faollashtirildi!\n+1,000,000 $\n+1,000,000 💎\n+10,000 🪙")


# ================================================================================
#  BOT GURUHGA QO'SHILGANDA — YARATUVCHIGA SO'ROV
# ================================================================================

@bot.my_chat_member_handler()
def handle_my_chat_member(update: types.ChatMemberUpdated):
    me = bot.get_me()
    if update.new_chat_member.user.id != me.id:
        return
    chat = update.chat
    old_status, new_status = update.old_chat_member.status, update.new_chat_member.status
    adder = update.from_user

    if new_status in ("member", "administrator") and old_status in ("left", "kicked"):
        add_known_group(chat.id, chat.title or "Nomsiz guruh")
        if OWNER_ID:
            adder_info = adder.first_name + (f" (@{adder.username})" if adder.username else "")
            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton("✅ Qabul qilish", callback_data=f"grp|accept|{chat.id}"),
                types.InlineKeyboardButton("❌ Rad etish", callback_data=f"grp|reject|{chat.id}"),
            )
            try:
                bot.send_message(
                    OWNER_ID,
                    f"🆕 <b>Bot yangi guruhga qo'shildi!</b>\n\n"
                    f"📛 Nomi: {chat.title}\n🆔 ID: <code>{chat.id}</code>\n👤 Qo'shgan: {adder_info}",
                    reply_markup=kb,
                )
            except Exception:
                pass
    elif new_status in ("left", "kicked"):
        remove_known_group(chat.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("grp|"))
def cb_group_decision(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.")
        return
    _, action, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    if action == "accept":
        bot.answer_callback_query(call.id, "✅ Qabul qilindi.")
        try:
            bot.edit_message_text(f"✅ Guruh qabul qilindi (ID: {chat_id}).", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        try:
            bot.send_message(chat_id, "🎉 Salom! Men Hunter Mafia botiman. /NewGame buyrug'i bilan o'yin boshlashingiz mumkin.")
        except Exception:
            pass
    else:
        bot.answer_callback_query(call.id, "❌ Rad etildi.")
        try:
            bot.edit_message_text(f"❌ Guruh rad etildi (ID: {chat_id}). Bot chiqib ketmoqda.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        try:
            bot.leave_chat(chat_id)
        except Exception:
            pass
        remove_known_group(chat_id)


# ================================================================================
#  KABINET / PROFIL
# ================================================================================

@bot.message_handler(commands=["profile", "kabinet"])
def cmd_profile(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    show_profile(message.chat.id, message.from_user.id, message.from_user.first_name)


def format_active_effects(uid):
    ch = get_charges(uid)
    lines = []

    def add(cond, text):
        if cond:
            lines.append(text)

    add(ch.get("fake_doc", 0) > 0, f"📜 Soxta hujjat: {ch.get('fake_doc', 0)} ta")
    add(ch.get("night_vision", 0) > 0, f"🥽 Tungi ko'zoynak: {ch.get('night_vision', 0)} ta")
    add(ch.get("confuse", 0) > 0, f"✉️ Tushunarsiz xat: {ch.get('confuse', 0)} ta")
    add(ch.get("poison", 0) > 0, f"🧪 Zaharli flakon: {ch.get('poison', 0)} ta")
    add(ch.get("gps", 0) > 0, f"📍 GPS Mayak: {ch.get('gps', 0)} ta")
    add(ch.get("duel_adv", 0) > 0, f"⚔️ Olmos Qilich (duel ustunligi): {ch.get('duel_adv', 0)} ta")
    add(ch.get("golden_bullet", 0) > 0, f"🟡 Oltin o'q: {ch.get('golden_bullet', 0)} ta")
    add(ch.get("radar", 0) > 0, f"📡 Maxfiy radar: {ch.get('radar', 0)} ta")
    add(ch.get("revive", 0) > 0, f"⚡️ Tezkor jonlanish: {ch.get('revive', 0)} ta")
    add(ch.get("role_choice", 0) > 0, f"🎭 Rol tanlash huquqi: {ch.get('role_choice', 0)} marta")
    add(ch.get("watch_eyes", 0) > 0, f"👁 Kuzatish ko'zi: {ch.get('watch_eyes', 0)} ta")

    imp_until = ch.get("imperator_until", 0)
    if imp_until and imp_until > time.time():
        rem = int(imp_until - time.time())
        add(True, f"👑 Imperator maqomi: {rem // 3600} soat {(rem % 3600) // 60} daqiqa qoldi")

    admin_until = ch.get("temp_admin_until", 0)
    if admin_until and admin_until > time.time():
        rem = int(admin_until - time.time())
        add(True, f"⚡️ Vaqtinchalik admin huquqi: {rem // 3600} soat qoldi")

    add(ch.get("ramka", 0) > 0, "🖼 Mifik ramka faol")
    add(ch.get("toj", 0) > 0, "👑 Hukmdor toj faol")
    add(ch.get("qirol", 0) > 0, "🐉 Hunter Mafia Qiroli unvoni faol")
    add(ch.get("legend_killer", 0) > 0, "🗡 Afsonaviy qotil nishoni (duelda doim g'olib)")
    add(ch.get("duel_shield", 0) > 0, "🛡 Cheksiz duel qalqoni (duelda doim g'olib)")
    add(ch.get("shadow", 0) > 0, "👤 Shadow status (reytingda yashirin)")
    add(ch.get("klan_license", 0) > 0, "🏛 Klan litsenziyasi faol")

    bm = ch.get("bonus_mult", 1)
    if bm > 1:
        add(True, f"🎁 Kunlik bonus ko'paytiruvchi: x{bm}")
    lm = ch.get("luck_mult", 1)
    if lm > 1:
        add(True, f"🦊 Umumiy yutuq ko'paytiruvchi: x{lm}")

    if not lines:
        return "Hozircha faol kuchlaringiz yo'q. Do'kondan xarid qiling!"
    return "✨ <b>FAOL KUCHLARINGIZ</b>\n\n" + "\n".join(lines)


def show_profile(chat_id, uid, name):
    u = user_dict(uid, name)
    partner = get_partner_name(uid)
    marriage_line = f"💍 Oilaviy holat: Nikohda ({partner})" if partner else "💍 Oilaviy holat: Bo'ydoq"
    duel_total = u["duel_wins"] + u["duel_losses"]
    duel_rate = f"{(u['duel_wins'] / duel_total * 100):.1f}%" if duel_total else "0.0%"
    text = (
        "👤 <b>SHAXSIY KABINET</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🏷 Ism: {u['name']}\n"
        f"🎮 O'yinlar: {u['games']} ta | 🏆 G'alaba: {u['wins']} ta\n"
        f"💵 Dollar ($): ${u['dollar']}\n"
        f"💎 Olmoslar: {u['diamond']} ta\n"
        f"🪙 Hunter Coin: {u['coin']} ta\n"
        f"🛡 Himoya (shield): {u['shield']} ta\n"
        f"⚔️ Duellar: {duel_total} ta ({u['duel_wins']} g'alaba / {u['duel_losses']} mag'lubiyat, {duel_rate})\n"
        f"{marriage_line}\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(chat_id, text)


# ================================================================================
#  📦 INVENTAR (qoshimchakod10.py g'oyasi — endi haqiqiy DB "inventory" ustunidan)
# ================================================================================

def show_inventory(chat_id, uid):
    u = user_dict(uid)
    try:
        items = json.loads(u["inventory"] or "[]")
    except Exception:
        items = []
    if not items:
        text = "📦 Sizning inventaringiz hozircha bo'sh.\n🛒 Do'kondan buyum sotib oling!"
    else:
        counts = {}
        for it in items:
            counts[it] = counts.get(it, 0) + 1
        lines = ["📦 <b>SIZNING INVENTARINGIZ</b>\n"]
        for name, n in counts.items():
            lines.append(f"• {name} — {n} ta" if n > 1 else f"• {name}")
        text = "\n".join(lines)
    bot.send_message(chat_id, text)


@bot.message_handler(commands=["inventar", "Inventar"])
def cmd_inventar(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    show_inventory(message.chat.id, message.from_user.id)


# ================================================================================
#  MENYU CALLBACK
# ================================================================================

@bot.callback_query_handler(func=lambda c: c.data.startswith("menu|"))
def cb_menu(call):
    maybe_capture_owner(call.from_user)
    _, action = call.data.split("|")
    uid = call.from_user.id

    if action == "roles":
        lines = ["🎭 <b>Hunter Mafia — 28 ta rol</b>\n"]
        for role, desc in ROLES_INFO.items():
            lines.append(f"<b>{role}</b> — {desc}")
        text = "\n".join(lines)
        for i in range(0, len(text), 3500):
            bot.send_message(call.message.chat.id, text[i:i + 3500])
        bot.answer_callback_query(call.id)

    elif action == "cabinet":
        show_profile(call.message.chat.id, uid, call.from_user.first_name)
        bot.answer_callback_query(call.id)

    elif action == "shop":
        open_shop_main(call.message.chat.id)
        bot.answer_callback_query(call.id)

    elif action == "buyhc":
        open_hc_stars_menu(call.message.chat.id)
        bot.answer_callback_query(call.id)

    elif action == "effects":
        bot.send_message(call.message.chat.id, format_active_effects(uid))
        bot.answer_callback_query(call.id)

    elif action == "klan":
        with db_lock:
            cur.execute("SELECT name FROM clans WHERE owner_id=?", (uid,))
            row = cur.fetchone()
        if row:
            bot.send_message(call.message.chat.id, f"🏛 Sizning klaningiz: <b>{row[0]}</b>")
        else:
            bot.send_message(call.message.chat.id, "Sizda hali klan yo'q. 🏛 Klan litsenziyasini Hunter Coin do'konidan sotib olib <code>/klan Nomi</code> deb yozing.")
        bot.answer_callback_query(call.id)

    elif action == "top":
        rows = get_top_players()
        if not rows:
            text = "🏆 Hozircha reyting bo'sh."
        else:
            lines = ["🏆 <b>TOP O'YINCHILAR</b>\n"]
            for i, (name, wins, dollar, is_qirol) in enumerate(rows, 1):
                crown = "🐉 " if is_qirol else ""
                lines.append(f"{i}. {crown}{name} — {wins} g'alaba, ${dollar}")
            text = "\n".join(lines)
        bot.send_message(call.message.chat.id, text)
        bot.answer_callback_query(call.id)

    elif action == "inventory":
        show_inventory(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "tournament":
        bot.send_message(
            call.message.chat.id,
            "🏆 <b>MUSOBAQALAR (Turnirlar)</b>\n\n"
            "Bu bo'lim tez orada ishga tushadi — guruhlararo Hunter Mafia turnirlari, "
            "reyting bo'yicha mukofotlar va maxsus yutuqlar shu yerda e'lon qilinadi. 🚀"
        )
        bot.answer_callback_query(call.id)

    elif action == "nikoh_info":
        partner = get_partner_name(uid)
        if partner:
            bot.send_message(call.message.chat.id, f"💍 <b>Oilaviy holat:</b> Nikohda ❤️\nJuftingiz: <b>{partner}</b>\n\nAjrashish uchun /ajrashish deb yozing.")
        else:
            bot.send_message(call.message.chat.id, "👤 <b>Oilaviy holat:</b> Bo'ydoq.\n\nBoshqa o'yinchi bilan nikoh qurish uchun guruhda uning xabariga <b>Reply</b> qilib /nikoh deb yozing!")
        bot.answer_callback_query(call.id)

    elif action == "duel_info":
        bot.send_message(call.message.chat.id, "⚔️ Boshqa o'yinchi bilan duel o'ynash uchun guruhda uning xabariga <b>Reply</b> qilib /duel deb yozing!")
        bot.answer_callback_query(call.id)

    elif action == "help":
        text = (
            "❓ <b>BUYRUQLAR RO'YXATI</b>\n\n"
            "<b>O'yin (guruh admini):</b>\n"
            "/NewGame — yangi o'yin ochish\n"
            "/PovtorGame — qo'shilish xabarini yangilash\n"
            "/StartGame — o'yinni boshlash\n"
            "/Sotop — o'yinni to'xtatish\n\n"
            "<b>O'yinchilar uchun:</b>\n"
            "/join — o'yinga qo'shilish\n"
            "/rolni_tanla &lt;rol&gt; — 🎭 huquqi bo'lsa rol tanlash\n"
            "/zahar (reply) — 🧪 zaharlash\n"
            "/gps (reply) — 📍 holatni bilish\n"
            "/qayta_tanlash — 📡 rolni qayta tanlash\n"
            "/duel (reply) — duelga chaqirish\n"
            "/duel_stat (yoki reply) — duel statistikasi\n"
            "/nikoh (reply) — turmush taklifi\n"
            "/juftim — oilaviy holatingiz\n"
            "/ajrashish — ajrashish\n"
            "/inventar — buyumlaringiz ro'yxati\n"
            "/Givde, /GivdeMoney, /GivdeCoin (reply) — sovg'a berish\n"
            "/klan &lt;nomi&gt;, /klanim — klan\n"
            "/promo &lt;KOD&gt; — promo-kodni ishlatish\n"
            "/profile — shaxsiy kabinet\n\n"
            "<b>Faqat bot yaratuvchisi / adminlar:</b>\n"
            "/Guruh, /mirkamilovic, /sendall, /addmoney, /adddiamond, /addcoin, /ban, /unban\n"
            "/promo_create &lt;KOD&gt; &lt;dollar&gt; &lt;diamond&gt; &lt;coin&gt; &lt;limit&gt; — promo-kod yaratish\n"
            "/tarqatish &lt;dollar|diamond|coin&gt; &lt;miqdor&gt; &lt;kishi&gt; — sovg'a tarqatish"
        )
        bot.send_message(call.message.chat.id, text)
        bot.answer_callback_query(call.id)

    elif action == "bonus":
        u = user_dict(uid, call.from_user.first_name)
        today = time.strftime("%Y-%m-%d")
        if u["last_bonus_date"] == today:
            bot.answer_callback_query(call.id, "⏳ Siz bugungi bonusni allaqachon olgansiz!", show_alert=True)
            return
        update_user(uid, last_bonus_date=today)
        roll = random.random() * 100
        mult = bonus_mult(uid) * luck_mult(uid)
        if roll < 85:
            reward = int(10 * mult)
            add_balance(uid, dollar=reward)
            bot.answer_callback_query(call.id, f"🎁 Bonus: +{reward}$ Dollar yutib oldingiz! 🎉", show_alert=True)
        else:
            reward = max(1, int(1 * mult))
            add_balance(uid, diamond=reward)
            bot.answer_callback_query(call.id, f"💎 Bonus: {reward} ta Olmos yutib oldingiz! 🚀", show_alert=True)


# ================================================================================
#  DO'KON (dollar/olmos/coin/osh)
# ================================================================================

def open_shop_main(chat_id):
    kb = types.InlineKeyboardMarkup()
    for key, (title, _items) in SHOP_CATEGORIES.items():
        kb.add(types.InlineKeyboardButton(title, callback_data=f"shopcat|{key}"))
    bot.send_message(chat_id, "🛒 Do'konga xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("shopcat|"))
def cb_shop_category(call):
    maybe_capture_owner(call.from_user)
    _, cat = call.data.split("|")
    title, items = SHOP_CATEGORIES[cat]
    kb = types.InlineKeyboardMarkup()
    for key, item in items.items():
        symbol = {"dollar": "$", "diamond": "💎", "coin": "🪙"}[item["currency"]]
        kb.add(types.InlineKeyboardButton(f"{item['name']} — {item['price']}{symbol}", callback_data=f"buy|{cat}|{key}"))
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="shopback"))
    try:
        bot.edit_message_text(f"{title}\nKerakli buyumni tanlang (tavsif uchun ustiga bosing):", call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        bot.send_message(call.message.chat.id, f"{title}\nKerakli buyumni tanlang:", reply_markup=kb)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data == "shopback")
def cb_shop_back(call):
    maybe_capture_owner(call.from_user)
    open_shop_main(call.message.chat.id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("buy|"))
def cb_buy(call):
    maybe_capture_owner(call.from_user)
    _, cat, key = call.data.split("|")
    _, items = SHOP_CATEGORIES[cat]
    item = items[key]
    uid = call.from_user.id
    u = user_dict(uid, call.from_user.first_name)
    balance = u[item["currency"]]

    if balance < item["price"]:
        bot.answer_callback_query(call.id, "❌ Balansingiz yetarli emas!", show_alert=True)
        return

    if item["currency"] == "dollar":
        add_balance(uid, dollar=-item["price"])
    elif item["currency"] == "diamond":
        add_balance(uid, diamond=-item["price"])
    else:
        add_balance(uid, coin=-item["price"])

    mode = item["mode"]
    result_note = ""
    if mode == "shield":
        add_shield(uid, 1)
        result_note = "🛡 Himoya (+1 shield) hisobingizga qo'shildi."
    elif mode == "instant_dollar":
        lo, hi = item["range"]
        bonus = int(random.randint(lo, hi) * luck_mult(uid))
        add_balance(uid, dollar=bonus)
        result_note = f"💵 +{bonus}$ hisobingizga qo'shildi."
    elif mode == "instant_diamond":
        lo, hi = item["range"]
        bonus = int(random.randint(lo, hi) * luck_mult(uid))
        add_balance(uid, diamond=bonus)
        result_note = f"💎 +{bonus} Olmos hisobingizga qo'shildi."
    elif mode == "charge":
        add_charge(uid, item["charge_key"], 1)
        result_note = f"✅ Ishlatish uchun tayyor — {item.get('desc', '')}"
    elif mode == "multiplier":
        ch = get_charges(uid)
        cur_v = ch.get(item["charge_key"], 1)
        set_charge_value(uid, item["charge_key"], max(cur_v, item["mult_value"]))
        result_note = f"✅ Multiplikator faollashtirildi: x{item['mult_value']}"
    elif mode == "expiry":
        until = time.time() + item["duration_seconds"]
        set_charge_value(uid, item["charge_key"], until)
        result_note = f"✅ {item['duration_seconds']//3600} soatga faollashtirildi."
    elif mode == "permanent_flag":
        set_charge_value(uid, item["charge_key"], 1)
        result_note = "✅ Doimiy maqom faollashtirildi."

    add_inventory_item(uid, item["name"])
    bot.answer_callback_query(call.id, f"✅ {item['name']} sotib olindi!\n{result_note}", show_alert=True)


# ================================================================================
#  🪙 HUNTER COIN — TELEGRAM STARS ORQALI SOTIB OLISH
# ================================================================================

def open_hc_stars_menu(chat_id):
    kb = types.InlineKeyboardMarkup()
    for qty in (1, 5, 10, 20, 50, 100):
        kb.add(types.InlineKeyboardButton(f"{qty} 🪙 — {qty * HC_STAR_RATE} ⭐️", callback_data=f"buyhc|{qty}"))
    bot.send_message(
        chat_id,
        "🪙 <b>Hunter Coin sotib olish</b>\n\n"
        "To'lov Telegram Stars orqali amalga oshiriladi — <b>5 ⭐️ = 1 🪙</b>.\n"
        "Miqdorni tanlang:",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("buyhc|"))
def cb_buy_hc_stars(call):
    maybe_capture_owner(call.from_user)
    _, qty_s = call.data.split("|")
    qty = int(qty_s)
    stars_price = qty * HC_STAR_RATE
    try:
        bot.send_invoice(
            call.message.chat.id,
            title=f"{qty} Hunter Coin",
            description=f"{qty} dona Hunter Coin sotib olish ({stars_price} ⭐️ Stars)",
            invoice_payload=f"hc_{call.from_user.id}_{qty}",
            provider_token="",     # Telegram Stars uchun bo'sh qoldiriladi
            currency="XTR",         # Telegram Stars valyutasi
            prices=[types.LabeledPrice(label=f"{qty} Hunter Coin", amount=stars_price)],
        )
        bot.answer_callback_query(call.id)
    except Exception:
        bot.answer_callback_query(call.id, "❌ To'lov tizimida xatolik. Keyinroq urinib ko'ring.", show_alert=True)


@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout_handler(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def successful_payment_handler(message):
    payload = message.successful_payment.invoice_payload
    try:
        _, uid_s, qty_s = payload.split("_")
        uid, qty = int(uid_s), int(qty_s)
    except Exception:
        return
    add_balance(uid, coin=qty)
    bot.send_message(message.chat.id, f"✅ To'lov muvaffaqiyatli o'tdi! +{qty} 🪙 Hunter Coin hisobingizga qo'shildi.\nRahmat!")


# ================================================================================
#  ADMIN PANEL (faqat bot yaratuvchisi)
# ================================================================================

@bot.callback_query_handler(func=lambda c: c.data == "admin|panel")
def cb_admin_panel(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📋 Guruhlar ro'yxati", callback_data="admin|groups"))
    kb.add(types.InlineKeyboardButton("📊 Statistika", callback_data="admin|stats"))
    kb.add(types.InlineKeyboardButton("🛑 Barcha faol o'yinlarni to'xtatish", callback_data="admin|stopall"))
    kb.add(types.InlineKeyboardButton("📢 Global xabar (broadcast)", callback_data="admin|broadcast_info"))
    kb.add(types.InlineKeyboardButton("💰 Balans boshqaruvi", callback_data="admin|money_info"))
    kb.add(types.InlineKeyboardButton("🚫 Ban / Unban", callback_data="admin|ban_info"))
    kb.add(types.InlineKeyboardButton("📥 Bazadan zaxira nusxa (backup)", callback_data="admin|backup"))
    bot.send_message(
        call.message.chat.id,
        "⚙️ <b>ADMIN PANEL</b> (faqat yaratuvchi uchun)\n\n"
        "Ba'zi funksiyalar buyruq orqali ishlaydi — tugmani bosganingizda kerakli buyruq ko'rsatiladi.",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|groups")
def cb_admin_groups(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    groups = list_known_groups()
    if not groups:
        text = "Bot hali birorta guruhga qo'shilmagan."
    else:
        lines = ["📋 <b>Guruhlar:</b>", ""]
        for cid, title in groups:
            lines.append(f"• {title} (ID: <code>{cid}</code>)")
        text = "\n".join(lines)
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda c: c.data == "admin|stats")
def cb_admin_stats(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    with db_lock:
        cur.execute("SELECT COUNT(*) FROM users")
        total_users = cur.fetchone()[0]
    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Ro'yxatdan o'tgan foydalanuvchilar: {total_users}\n"
        f"🏘 Bot qo'shilgan guruhlar: {len(list_known_groups())}\n"
        f"🎮 Faol o'yinlar soni: {len(GAMES)}"
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda c: c.data == "admin|stopall")
def cb_admin_stopall(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    n = len(GAMES)
    GAMES.clear()
    bot.answer_callback_query(call.id, f"🛑 {n} ta faol o'yin to'xtatildi.", show_alert=True)


# --- QO'SHIMCHA ADMIN FUNKSIYALARI (qoshimchakod7.py g'oyasi, telebot uslubiga moslashtirildi) ---

@bot.callback_query_handler(func=lambda c: c.data == "admin|broadcast_info")
def cb_admin_broadcast_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "📢 Barcha foydalanuvchilarga xabar yuborish uchun:\n<code>/sendall Sizning xabaringiz</code>")


@bot.callback_query_handler(func=lambda c: c.data == "admin|money_info")
def cb_admin_money_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "💰 <b>Balans boshqaruvi:</b>\n\n"
        "<code>/addmoney &lt;user_id&gt; &lt;summa&gt;</code> — Dollar qo'shish/ayirish\n"
        "<code>/adddiamond &lt;user_id&gt; &lt;miqdor&gt;</code> — Olmos qo'shish/ayirish\n"
        "<code>/addcoin &lt;user_id&gt; &lt;miqdor&gt;</code> — Hunter Coin qo'shish/ayirish\n\n"
        "<i>Manfiy son yozsangiz, balansdan ayiradi.</i>\n\n"
        "🎁 <b>Promo-kod va tarqatish:</b>\n"
        "<code>/promo_create &lt;KOD&gt; &lt;dollar&gt; &lt;diamond&gt; &lt;coin&gt; &lt;limit&gt;</code>\n"
        "<code>/tarqatish &lt;dollar|diamond|coin&gt; &lt;har_biriga&gt; &lt;kishi_soni&gt;</code>"
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|ban_info")
def cb_admin_ban_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🚫 <b>Ban / Unban:</b>\n\n"
        "<code>/ban &lt;user_id&gt;</code> — foydalanuvchini bloklash (o'yinlarga qo'shila olmaydi)\n"
        "<code>/unban &lt;user_id&gt;</code> — blokdan chiqarish",
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|backup")
def cb_admin_backup(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    try:
        with db_lock:
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
        data = [dict(zip(USER_COLS, r)) for r in rows]
        path = "/tmp/hunter_mafia_backup.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(path, "rb") as f:
            bot.send_document(call.message.chat.id, f, caption="📥 Foydalanuvchilar bazasining zaxira nusxasi (JSON).")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Zaxira nusxa olishda xatolik: {e}")


@bot.message_handler(commands=["sendall"])
def cmd_sendall(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/sendall Xabar matni</code>")
        return
    text = parts[1]
    with db_lock:
        cur.execute("SELECT user_id FROM users")
        user_ids = [r[0] for r in cur.fetchall()]
    sent, failed = 0, 0
    for uid in user_ids:
        try:
            bot.send_message(uid, f"📢 <b>E'lon:</b>\n\n{text}")
            sent += 1
        except Exception:
            failed += 1
    bot.send_message(message.chat.id, f"📢 Xabar yuborildi: {sent} ta muvaffaqiyatli, {failed} ta yetib bormadi.")


def _admin_adjust_balance(message, field_name, icon):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].lstrip("-").isdigit() or not parts[2].lstrip("-").isdigit():
        bot.send_message(message.chat.id, f"Foydalanish: <code>/{parts[0].lstrip('/')} &lt;user_id&gt; &lt;miqdor&gt;</code>")
        return
    target_id, amount = int(parts[1]), int(parts[2])
    user_dict(target_id)
    add_balance(target_id, **{field_name: amount})
    bot.send_message(message.chat.id, f"✅ Foydalanuvchi <code>{target_id}</code> balansiga {amount} {icon} qo'shildi/ayrildi.")


@bot.message_handler(commands=["addmoney"])
def cmd_addmoney(message):
    _admin_adjust_balance(message, "dollar", "$")


@bot.message_handler(commands=["adddiamond"])
def cmd_adddiamond(message):
    _admin_adjust_balance(message, "diamond", "💎")


@bot.message_handler(commands=["addcoin"])
def cmd_addcoin(message):
    _admin_adjust_balance(message, "coin", "🪙")


@bot.message_handler(commands=["ban"])
def cmd_ban(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/ban &lt;user_id&gt;</code>")
        return
    target_id = int(parts[1])
    user_dict(target_id)
    ban_user(target_id)
    bot.send_message(message.chat.id, f"🚫 Foydalanuvchi <code>{target_id}</code> bloklandi.")


@bot.message_handler(commands=["unban"])
def cmd_unban(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/unban &lt;user_id&gt;</code>")
        return
    target_id = int(parts[1])
    unban_user(target_id)
    bot.send_message(message.chat.id, f"✅ Foydalanuvchi <code>{target_id}</code> blokdan chiqarildi.")


# ================================================================================
#  PROMO-KODLAR (qoshimchakod8.py "Promo-kod Yaratish" g'oyasi asosida)
# ================================================================================

@bot.message_handler(commands=["promo_create"])
def cmd_promo_create(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 6:
        bot.send_message(
            message.chat.id,
            "Foydalanish: <code>/promo_create &lt;KOD&gt; &lt;dollar&gt; &lt;diamond&gt; &lt;coin&gt; &lt;max_ishlatish&gt;</code>\n"
            "Masalan: <code>/promo_create BAYRAM2026 500 10 5 100</code>",
        )
        return
    _, code, dollar_s, diamond_s, coin_s, max_uses_s = parts
    if not all(p.lstrip("-").isdigit() for p in (dollar_s, diamond_s, coin_s, max_uses_s)):
        bot.send_message(message.chat.id, "❌ Miqdorlar butun son bo'lishi kerak.")
        return
    code = code.upper()
    with db_lock:
        cur.execute(
            "INSERT OR REPLACE INTO promo_codes (code, dollar, diamond, coin, max_uses, used_count) VALUES (?,?,?,?,?,0)",
            (code, int(dollar_s), int(diamond_s), int(coin_s), int(max_uses_s)),
        )
        conn.commit()
    bot.send_message(
        message.chat.id,
        f"✅ Promo-kod yaratildi: <code>{code}</code>\n"
        f"💵 {dollar_s}$ | 💎 {diamond_s} | 🪙 {coin_s} | 👥 Ishlatish limiti: {max_uses_s}",
    )


@bot.message_handler(commands=["promo"])
def cmd_promo_redeem(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if is_banned(uid):
        return
    user_dict(uid, message.from_user.first_name)
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/promo &lt;KOD&gt;</code>")
        return
    code = parts[1].upper()
    with db_lock:
        cur.execute("SELECT dollar, diamond, coin, max_uses, used_count FROM promo_codes WHERE code=?", (code,))
        row = cur.fetchone()
        if not row:
            bot.send_message(message.chat.id, "❌ Bunday promo-kod topilmadi.")
            return
        dollar, diamond, coin, max_uses, used_count = row
        cur.execute("SELECT 1 FROM promo_redemptions WHERE code=? AND user_id=?", (code, uid))
        if cur.fetchone():
            bot.send_message(message.chat.id, "❌ Siz bu promo-kodni allaqachon ishlatgansiz.")
            return
        if used_count >= max_uses:
            bot.send_message(message.chat.id, "❌ Bu promo-kodning ishlatish limiti tugagan.")
            return
        cur.execute("INSERT INTO promo_redemptions (code, user_id) VALUES (?,?)", (code, uid))
        cur.execute("UPDATE promo_codes SET used_count=used_count+1 WHERE code=?", (code,))
        conn.commit()
    add_balance(uid, dollar=dollar, diamond=diamond, coin=coin)
    bot.send_message(
        message.chat.id,
        f"🎁 <b>Promo-kod muvaffaqiyatli ishlatildi!</b>\n💵 +{dollar}$ 💎 +{diamond} 🪙 +{coin}",
    )


# ================================================================================
#  SOVG'A TARQATISH / GIVEAWAY — /tarqatish
#  (qoshimchakod6.py g'oyasi asosida, aiogram'dan telebot'ga moslashtirildi)
# ================================================================================

GIVEAWAYS = {}
GIVEAWAY_CURRENCY_ICON = {"dollar": "💵", "diamond": "💎", "coin": "🪙"}


@bot.message_handler(commands=["tarqatish"])
def cmd_tarqatish(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_authorized(message):
        return
    parts = message.text.split()
    if len(parts) != 4 or parts[1] not in GIVEAWAY_CURRENCY_ICON or not parts[2].isdigit() or not parts[3].isdigit():
        bot.send_message(
            message.chat.id,
            "Foydalanish: <code>/tarqatish &lt;dollar|diamond|coin&gt; &lt;har_biriga&gt; &lt;necha_kishiga&gt;</code>\n"
            "Masalan: <code>/tarqatish diamond 5 10</code> — 10 kishiga 5 tadan olmos.",
        )
        return
    currency, per_person, people_count = parts[1], int(parts[2]), int(parts[3])
    chat_id = message.chat.id
    icon = GIVEAWAY_CURRENCY_ICON[currency]

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f"{icon} {per_person} {currency} olish", callback_data=f"gw|{chat_id}"))
    sent = bot.send_message(
        chat_id,
        f"🎉 <b>SOVG'A TARQATISH BOSHLANDI!</b>\n\n"
        f"Har bir ishtirokchiga: {icon} <b>{per_person} {currency}</b>\n"
        f"Jami: <b>{people_count}</b> kishiga yetadi.\n\n"
        f"👇 Tez bo'ling, tugmani bosing!",
        reply_markup=kb,
    )
    GIVEAWAYS[chat_id] = {
        "currency": currency,
        "per_person": per_person,
        "remaining": people_count,
        "claimed": set(),
        "message_id": sent.message_id,
    }


@bot.callback_query_handler(func=lambda c: c.data.startswith("gw|"))
def cb_giveaway(call):
    maybe_capture_owner(call.from_user)
    _, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    gw = GIVEAWAYS.get(chat_id)
    uid = call.from_user.id

    if not gw:
        bot.answer_callback_query(call.id, "🎉 Tarqatish yakunlangan.")
        return
    if uid in gw["claimed"]:
        bot.answer_callback_query(call.id, "❌ Siz allaqachon oldingiz!", show_alert=True)
        return
    if gw["remaining"] <= 0:
        bot.answer_callback_query(call.id, "😔 Afsuski, hammasi tugadi.", show_alert=True)
        return

    user_dict(uid, call.from_user.first_name)
    add_balance(uid, **{gw["currency"]: gw["per_person"]})
    gw["claimed"].add(uid)
    gw["remaining"] -= 1
    icon = GIVEAWAY_CURRENCY_ICON[gw["currency"]]
    bot.answer_callback_query(call.id, f"🎉 Siz {icon} {gw['per_person']} {gw['currency']} yutib oldingiz!", show_alert=True)

    if gw["remaining"] <= 0:
        try:
            bot.edit_message_text(
                f"🎉 <b>SOVG'A TARQATISH YAKUNLANDI!</b>\n\n"
                f"Barcha {icon} sovg'alar {len(gw['claimed'])} kishiga tarqatildi. Rahmat, ishtirok etganlarga!",
                chat_id, gw["message_id"],
            )
        except Exception:
            pass
        GIVEAWAYS.pop(chat_id, None)
    else:
        try:
            bot.edit_message_text(
                f"🎉 <b>SOVG'A TARQATISH DAVOM ETMOQDA!</b>\n\n"
                f"Har bir ishtirokchiga: {icon} <b>{gw['per_person']} {gw['currency']}</b>\n"
                f"Qolgan o'rinlar: <b>{gw['remaining']}</b>\n\n"
                f"👇 Tez bo'ling, tugmani bosing!",
                chat_id, gw["message_id"],
                reply_markup=call.message.reply_markup,
            )
        except Exception:
            pass


# ================================================================================
#  /heros
# ================================================================================

@bot.message_handler(commands=["heros"])
def cmd_heros(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    bot.send_message(message.chat.id, ", ".join(ALL_ROLES))


# ================================================================================
#  GURUHDAGI ODDIY MATNLARNI BOSHQARISH — TUN/KUN QOIDALARI
# ================================================================================

@bot.message_handler(
    func=lambda m: m.chat.type in ("group", "supergroup") and not (m.text or "").startswith("/"),
    content_types=["text"],
)
def group_text_guard(message):
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        return

    phase = game.get("phase")
    if phase == "night":
        safe_delete(message)
        return
    if phase == "day":
        if message.from_user.id not in game["players"]:
            safe_delete(message)
        return


# ================================================================================
#  ISHGA TUSHIRISH
# ================================================================================

if __name__ == "__main__":
    print("Hunter Mafia bot v4 (telebot, to'liq do'kon + Stars + promo + tarqatish) ishga tushmoqda...")
    BOT_USERNAME = bot.get_me().username
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
