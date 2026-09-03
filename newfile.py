# -*- coding: utf-8 -*-
"""
================================================================================
 HUNTER MAFIA — TO'LIQ VERSIYA v7 (pyTelegramBotAPI / telebot, sinxron)
================================================================================

YANGI (v7) — Admin panelga 3 ta yangi, TO'LIQ ISHLAYDIGAN owner-funksiyasi
qo'shildi (mavjud hech bir funksiya o'chirilmadi/qisqartirilmadi, faqat
qo'shildi):

    1) 🔍 /useri <user_id yoki reply> — istalgan foydalanuvchining TO'LIQ
       profilini (balans, statistika, ELITE holati, oila, geroy, ban holati)
       bitta xabarda ko'rsatadi, tagida tezkor "Ban/Unban" va "30 kun ELITE
       berish" tugmalari bilan.
    2) 🚪 /guruhdan_chiq <chat_id> — botni istalgan guruhdan HAQIQIY Telegram
       API (leave_chat) orqali chiqaradi va known_groups bazasidan o'chiradi.
    3) 👑 /elite_ber <kun> (reply) — istalgan foydalanuvchiga qo'lda, xohlagan
       muddatga HUNTER ELITE (VIP) beradi; mavjud grant_elite_days() ustiga
       qurilgan — sotib olingan ELITE bilan 100% mos (muddatlar qo'shiladi).

    Har uchalasi ham ⚙️ Admin panel tugmalari orqali ham chaqiriladi.

YANGI (v6) — "Almex Black Bot" tahlili asosida qo'shilgan, TO'LIQ ISHLAYDIGAN
HUNTER ELITE tizimi (fayl oxirida, "ISHGA TUSHIRISH" bo'limidan oldin joylashgan):

    - 👑 /elite — tarifli VIP obuna (7 / 15 / 30 kun), narxi Olmosda YOKI
      Telegram Stars'da ko'rsatiladi, ikkalasi ham haqiqiy ishlaydi (Olmos —
      darhol balансdan yechiladi; Stars — send_invoice orqali, to'lov
      muvaffaqiyatli o'tgach avtomatik faollashadi). Mavjud "VIP" (charges
      ustunidagi vip_until) infratuzilmasi ustiga qurilgan — eski /birja
      orqali olingan VIP bilan TO'LIQ mos, muddatlar bir-biriga QO'SHILADI.
    - 🏷 /taxallus <laqab> — faqat ELITE a'zolar uchun shaxsiy laqab. Guruhda
      chaqirilsa, Almex'dagidek 👍/👎 jamoaviy tasdiqlash ovoz berishi ochiladi
      (30 soniya); DM'da chaqirilsa darhol o'rnatiladi. Tasdiqlangan laqab
      keyin BUTUN botda (o'yin e'lonlari, o'lim xabarlari, reyting) 👑 nishoni
      bilan birga ko'rinadi (mention() funksiyasi kengaytirildi).
    - 🌐 /til — 7 tilli (Turkcha/English/Rus/Ukrain/Qozoq/O'zbek/Indonez) til
      tanlash menyusi. Tanlangan til ELITE/laqab/sovg'a xabarlarida ishlaydi —
      botning asosiy o'yin matnlari ataylab o'zbekcha qoladi (soxta "to'liq
      tarjima" va'da qilinmadi, faqat haqiqatan tarjima qilingan qism ishlaydi).
    - 🎁 /sovga — ro'yxatdan o'tgan boshqa foydalanuvchiga Olmos sovg'a qilish
      (reply orqali yoki Telegram ID orqali) — real balans o'tkazmasi.
    - 🚪 /chiqish — ELITE a'zolari uchun o'yin lobbysidan istalgan payt chiqish.

    Bularning barchasi UCHUN yangi DB ustuni QO'SHILMAGAN — hammasi mavjud
    "charges" JSON ustunida saqlanadi, shuning uchun eski foydalanuvchilarning
    balansi, inventari, statistikasi va h.k. 100% saqlanib qoladi.
================================================================================

YANGI (v5) — QO'SHIMCHA FAYLLARDAN QO'SHILGAN BARCHA FUNKSIYALAR:

    kod1.py / kod4.py g'oyasi:
        - 🕵️ Har bir o'yinchiga o'yin boshida shaxsiy MAXFIY MISSIYA beriladi (DM orqali).
        - 🎲 Kunduzi 15% ehtimol bilan kutilmagan RANDOM EVENT chiqadi.
        - 💳 VIP tushunchasi allaqachon do'konda "💳 VIP Litsenziya" sifatida mavjud.

    kod2.py g'oyasi:
        - 🌙 Tun boshlanganda, tirik o'yinchilarning rollariga qarab har xil
          ATMOSFERA (hikoya) matnlari guruhga yuboriladi (23 ta qo'shimcha rol uchun).

    kod3.py g'oyasi:
        - Do'kon menyusi va foydalanuvchi statistikasi (o'ynagan o'yinlar, g'alabalar)
          allaqachon asosiy botning /profile va do'kon tizimida to'liq mavjud edi.

    kod5.py g'oyasi:
        - 🛒 QORA BOZOR — o'yinchilar o'rtasidagi savdo tizimi TO'LIQ qo'shildi:
          /sell (inventarni ko'rish yoki sotuvga qo'yish), /market (faol e'lonlar),
          /buy (xarid), xarid tasdiqlash/bekor qilish tugmalari — barchasi endi
          haqiqiy SQLite bazasida (market_listings jadvali) ishlaydi.

    kod6.py g'oyasi (aiogram'dan telebot'ga moslashtirildi):
        - 🎉 SOVG'A TARQATISH — /tarqatish buyrug'i, "olish" tugmasi bilan.

    kod8.py g'oyasi:
        - ⚡️ Admin panelga qo'shimcha bo'limlar: Promo-kod va Balans boshqaruvi.
        - 🎁 PROMO-KOD tizimi to'liq qo'shildi: /promo_create (admin), /promo (foydalanuvchi).

    kod9.py g'oyasi:
        - 🏛 KLANLAR JANGI — foydalanuvchi yuborgan TXT texnik topshiriq asosida TO'LIQ tizim:
          klan darajalari (1-3, xarajat va cheklovlar bilan), lider/o'rinbosar, a'zo darajalari,
          Ritsar/Sehrgar maqomlari, klan xazinasi (dollar+olmos), jang taklifi (jangga chiqish /
          taslim bo'lish / rad etish), g'alaba-mag'lubiyat iqtisodiyoti, ketma-ket g'alaba uchun
          olmos mukofoti, 3 oylik TOP klan mukofotlari, 30 kunlik faolsizlik jarimasi.
          Buyruqlar: /klan, /klanim, /klanga_qoshil, /klan_tark, /klan_chetlash, /klan_orinbosar,
          /klan_azo_daraja, /klan_lvl, /klan_nomi, /klan_maqom, /klan_hazna, /klan_taqsimla,
          /klanlar, /klanjang, /klan_mukofot.
        - 😅 Duelda va klan jangida yutqazganlarga hazil-mutoyiba xabarlari (DEFEAT_JOKES).

    botMalumotlari.py g'oyasi:
        - get_or_create_user / add_item / add_match_played / update_balance funksiyalari —
          bularning barchasi asosiy botda allaqachon SQLite orqali (user_dict, add_balance,
          add_inventory_item, games ustuni) TO'LIQ va yanada kengroq shaklda mavjud edi.

    BOSHQA SO'RALGAN O'ZGARISHLAR:
        - Boshlang'ich balans endi 0$ / 0💎 (avval 5000$/100💎 edi) — FAQAT yangi
          ro'yxatdan o'tadigan foydalanuvchilar uchun. Mavjud foydalanuvchilarning
          barcha ma'lumotlari (balans, inventar, statistika, klan a'zoligi va h.k.)
          kodni yangilashda TO'LIQ saqlanib qoladi.
        - 🌙 Tun: 45 soniya.
        - ☀️ Kun: jami 90 soniya — 30 soniya muhokama, so'ng ovoz berish tugmalari
          chiqadi va yana 60 soniya ovoz berish davom etadi.
================================================================================

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
import logging
import sqlite3
import random
import threading
import time
import json
import os
import sys
import signal

# ================================================================================
#  ASOSIY SOZLAMALAR
# ================================================================================

TOKEN = os.environ.get("HUNTER_MAFIA_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "HUNTER_MAFIA_TOKEN muhit o'zgaruvchisi topilmadi!\n"
        "Botni ishga tushirishdan oldin tokenni sozlang, masalan:\n"
        "  export HUNTER_MAFIA_TOKEN=\"123456:ABC-...\"  (Linux/Mac)\n"
        "  set HUNTER_MAFIA_TOKEN=123456:ABC-...        (Windows)\n"
        "Tokenni hech qachon kod ichiga ochiq yozmang — u chiqib ketsa, "
        "botingizni istalgan kishi to'liq boshqarib olishi mumkin."
    )
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
_logger = logging.getLogger("hunter_mafia")


class _SafeExceptionHandler(telebot.ExceptionHandler):
    """Har qanday handler ichidagi kutilmagan xato butun botni yiqitmasligi uchun.
    Xato faqat log'ga yoziladi, bot polling'ni davom ettiraveradi."""

    def handle(self, exception):
        _logger.exception("Handlerda kutilmagan xato: %s", exception)
        return True  # True = xato "boshqarildi" deb hisoblanadi, polling to'xtamaydi


bot = telebot.TeleBot(TOKEN, parse_mode="HTML", exception_handler=_SafeExceptionHandler(), threaded=True, num_threads=16)

BOT_USERNAME = None
OWNER_USERNAME = "Mirkamilovic"
# Ishonchli usul: agar aniq user_id muhit o'zgaruvchisida berilgan bo'lsa, shu ustuvor bo'ladi.
# Bu username o'zgarib qolsa ham yoki bir nechta admin bo'lsa ham ishonchli ishlaydi.
# Muhit o'zgaruvchisi berilmagan hollarda bot yaratuvchisining shaxsiy Telegram ID'si
# standart qiymat sifatida ishlatiladi (5588583777).
_owner_env_raw = os.environ.get("HUNTER_MAFIA_OWNER_ID", "").strip()
OWNER_ID_FROM_ENV = int(_owner_env_raw) if _owner_env_raw.lstrip("-").isdigit() else 5588583777

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
# 👍/👎 eng ko'p ovoz olgan ishtirokchini "rostan ham osamizmi?" deb yakuniy
# tasdiqlash ovoz berishi shu qadar soniya davom etadi (yoki barcha tirik
# o'yinchilar ovoz bergach, muddatidan oldin yakunlanadi)
CONFIRM_VOTE_SECONDS = 20

WIN_REWARD = 70
LOSE_REWARD = 20

HC_STAR_RATE = 15    # 15 ⭐️ Stars = 1 🪙 Hunter Coin (avval 5 edi — Hunter Coin qimmatroq bo'lishi uchun oshirildi)

# 🛒 Qora bozor faqat shu guruhda ishlashi kerak: https://t.me/+v9bYoMk-0hAyZTcy
# Telegram taklif havolasi orqali chat_id'ni oldindan bilib bo'lmaydi (bot guruhga
# qo'shilmaguncha), shuning uchun bot egasi guruhga botni qo'shgach, o'sha guruhda
# bir marta /shu_bozor buyrug'ini yozishi kerak — chat_id shu yerda avtomatik saqlanadi.
BLACK_MARKET_CHAT_ID = None  # dastlab bo'sh, keyin /shu_bozor orqali yoki bazadan yuklanadi
CURRENCY_ICON = {"dollar": "💵", "diamond": "💎", "coin": "🪙"}

NIGHT_PHOTO = "https://images.unsplash.com/photo-1518837695005-2083093ee35b?q=80&w=1200&auto=format&fit=crop"
DAY_PHOTO = "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop"
MAIN_PHOTO = "https://images.unsplash.com/photo-1514565131-fce0801e5785?q=80&w=1000&auto=format&fit=crop"
# 🌆 Foydalanuvchi o'zi tanlagan suratlar — skript bilan bir joyda "assets" papkasida
# saqlanadi. Agar shu fayllar mavjud bo'lsa, ular yuqoridagi Unsplash havolalari
# o'rniga ishlatiladi (fayl topilmasa, xavfsiz tarzda eski URL'ga qaytiladi).
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
NIGHT_PHOTO_LOCAL = os.path.join(ASSETS_DIR, "night.jpg")
DAY_PHOTO_LOCAL = os.path.join(ASSETS_DIR, "day.jpg")


# ================================================================================
#  MA'LUMOTLAR BAZASI (SQLite)
# ================================================================================

# MUHIM TUZATISH: baza fayli nisbiy yo'l ("hunter_mafia.db") emas, balki skript
# joylashgan papkaga QATTIQ bog'langan yo'l bilan ochiladi. Aks holda botni har xil
# papkadan yoki har xil ishga tushirish usulida (masalan hosting qayta ishga
# tushganda) ishga tushirilsa, Python HAR SAFAR YANGI, BO'SH baza fayli yaratib
# qo'yardi — go'yo eski foydalanuvchilar ma'lumoti "o'chib ketganday" ko'rinardi,
# aslida esa eski fayl boshqa joyda tinch turardi.
# MUHIM: Railway kabi hostinglarda konteyner fayl tizimi VAQTINCHALIK (ephemeral) —
# har deploy/qayta ishga tushishda hamma fayl o'chib, botning "eski foydalanuvchilar
# yo'qolib qoldi" degan muammosi aynan shundan kelib chiqadi. Buni hal qilish uchun
# Railway'da "Volume" (doimiy disk) ulanib, uning yo'li DB_DIR muhit o'zgaruvchisiga
# beriladi (masalan: DB_DIR=/data). Volume ulanmagan/lokal ishlatilganda esa avvalgidek
# skript papkasining o'zida saqlanadi.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.environ.get("DB_DIR", "").strip() or BASE_DIR
DB_PATH = os.path.join(DB_DIR, "hunter_mafia.db")
# 🔄 Bot tiklash (restore) tizimi uchun — aktiv o'yinlarning "suratini" shu faylga
# saqlaymiz, DB bilan bir xil (doimiy) papkada, shunda qayta ishga tushganda
# (deploy, xatolik, /tiklash buyrug'i) o'yinlar avtomatik davom ettiriladi.
STATE_PATH = os.path.join(DB_DIR, "hunter_mafia_state.json")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
db_lock = threading.RLock()
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'")
_users_table_existed = cur.fetchone()[0] > 0
logging.info(f"📂 Baza fayli: {DB_PATH}")

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

# YANGI: /paralar buyrug'i uchun — nikoh qurilgan sanani saqlaymiz (necha kunligini hisoblash uchun)
try:
    cur.execute("ALTER TABLE users ADD COLUMN married_at TEXT DEFAULT ''")
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
# --- YANGI (qoshimchakod9.py "Klan jangi" g'oyasi asosida) — klan a'zolari va jang statistikasi ---
cur.execute("""
CREATE TABLE IF NOT EXISTS clan_members (
    owner_id INTEGER,
    member_id INTEGER,
    member_name TEXT,
    PRIMARY KEY (owner_id, member_id)
)
""")

# --- KLANLAR JANGI — TO'LIQ TIZIM (foydalanuvchi yuborgan TXT texnik topshiriq asosida) ---
# Mavjud "clans"/"clan_members" jadvallariga yangi ustunlar qo'shamiz (eski bazalar buzilmasin
# deb har biri alohida, xavfsiz try/except bilan). Lider deb "clans.owner_id" ishlatiladi.
_CLAN_COLUMNS = [
    ("clans", "level", "INTEGER DEFAULT 1"),
    ("clans", "deputy_id", "INTEGER"),
    ("clans", "leader_level", "INTEGER DEFAULT 3"),
    ("clans", "treasury_dollar", "INTEGER DEFAULT 0"),
    ("clans", "treasury_diamond", "INTEGER DEFAULT 0"),
    ("clans", "levelup_tokens", "INTEGER DEFAULT 10"),   # "birinchi o'yinda liderga 10 lvl up beriladi"
    ("clans", "wins", "INTEGER DEFAULT 0"),
    ("clans", "losses", "INTEGER DEFAULT 0"),
    ("clans", "win_streak", "INTEGER DEFAULT 0"),
    ("clans", "war_declines_streak", "INTEGER DEFAULT 0"),
    ("clans", "last_war_at", "REAL DEFAULT 0"),
    ("clans", "deputy_levelups_used", "INTEGER DEFAULT 0"),
    ("clans", "last_inactivity_penalty_at", "REAL DEFAULT 0"),
    ("clan_members", "level", "INTEGER DEFAULT 0"),
    ("clan_members", "title", "TEXT"),  # NULL, 'ritsar' yoki 'sehrgar'
]
for _table, _col, _decl in _CLAN_COLUMNS:
    try:
        cur.execute(f"ALTER TABLE {_table} ADD COLUMN {_col} {_decl}")
        conn.commit()
    except sqlite3.OperationalError:
        pass

cur.execute("""
CREATE TABLE IF NOT EXISTS clan_join_requests (
    owner_id INTEGER,
    user_id INTEGER,
    user_name TEXT,
    requested_at REAL,
    PRIMARY KEY (owner_id, user_id)
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS clan_wars (
    war_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clan_a INTEGER,
    clan_b INTEGER,
    winner_owner_id INTEGER,
    started_at REAL,
    ended_at REAL
)
""")
conn.commit()

# --- YANGI: FAOLLIK BALLARI TIZIMI (kunlik/haftalik/oylik/mutlaq reyting uchun) ---
# Har bir voqea (o'yin g'alaba/mag'lubiyat, faollik, AFK jarima) alohida qatorda,
# vaqt belgisi bilan saqlanadi — shu orqali istalgan davr uchun yig'indi hisoblanadi.
cur.execute("""
CREATE TABLE IF NOT EXISTS points_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    points INTEGER,
    reason TEXT,
    ts REAL
)
""")
conn.commit()

# --- YANGI: GEROYLAR TIZIMI (Olmos do'konidagi "Afsonaviy Sandiq") ---
cur.execute("""
CREATE TABLE IF NOT EXISTS heroes (
    user_id INTEGER PRIMARY KEY,
    hero_key TEXT,
    level INTEGER DEFAULT 1,
    acquired_at REAL DEFAULT 0
)
""")
conn.commit()
# eski bazalarda "acquired_at" ustuni bo'lmasligi mumkin — xavfsiz qo'shamiz
try:
    cur.execute("ALTER TABLE heroes ADD COLUMN acquired_at REAL DEFAULT 0")
    conn.commit()
except Exception:
    pass
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
# 🎁 shaxsiylashtirilgan promo-kodlar — eng faol o'yinchilar uchun, kodni ishlatgan
# har bir kishi kod egasiga +10$ olib keladi
try:
    cur.execute("ALTER TABLE promo_codes ADD COLUMN owner_id INTEGER")
    conn.commit()
except sqlite3.OperationalError:
    pass
cur.execute("""
CREATE TABLE IF NOT EXISTS promo_redemptions (
    code TEXT,
    user_id INTEGER,
    PRIMARY KEY (code, user_id)
)
""")
# --- YANGI: ikki guruhli "Qizil vs Ko'k" musobaqa tizimi ---
# Ikkita alohida guruh bir-biriga "juft" qilib bog'lanadi. Har birida o'z mafiya
# o'yini mustaqil o'ynaladi, lekin har bir o'yin natijasi umumiy hisobga (score) qo'shiladi.
cur.execute("""
CREATE TABLE IF NOT EXISTS group_pairs (
    chat_id_a INTEGER PRIMARY KEY,
    chat_id_b INTEGER,
    label_a TEXT DEFAULT 'Qizil 🔴',
    label_b TEXT DEFAULT 'Ko''k 🔵',
    score_a INTEGER DEFAULT 0,
    score_b INTEGER DEFAULT 0
)
""")
conn.commit()
# --- YANGI (qoshimchakod5.py "Qora Bozor" g'oyasi asosida) — o'yinchilar o'rtasidagi savdo ---
cur.execute("""
CREATE TABLE IF NOT EXISTS market_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    seller_id INTEGER,
    seller_name TEXT,
    item TEXT,
    price INTEGER,
    active INTEGER DEFAULT 1
)
""")
conn.commit()
# eski bazalarda "currency" ustuni bo'lmasligi mumkin — xavfsiz qo'shamiz (standart: coin)
try:
    cur.execute("ALTER TABLE market_listings ADD COLUMN currency TEXT DEFAULT 'coin'")
    conn.commit()
except sqlite3.OperationalError:
    pass

USER_COLS = ["user_id", "name", "dollar", "diamond", "coin", "games", "wins",
             "shield", "inventory", "married_to", "last_bonus_date", "charges",
             "duel_wins", "duel_losses", "banned", "married_at"]


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
    if d.get("married_at") is None:
        d["married_at"] = ""
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


def remove_inventory_item_by_index(uid, index):
    """Qora bozorga sotuvga qo'yish uchun — inventardagi index bo'yicha buyumni
    olib tashlaydi va nomini qaytaradi (qoshimchakod5.py g'oyasi asosida)."""
    u = user_dict(uid)
    inv = json.loads(u["inventory"])
    if index < 0 or index >= len(inv):
        return None
    item = inv.pop(index)
    update_user(uid, inventory=json.dumps(inv))
    return item


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


# ================================================================================
#  BUYUMLARNI YOQISH/O'CHIRISH (faqat avtomatik ishlaydigan buyumlar uchun) —
#  o'yinchi xohlagan buyumini "faol" yoki "faol emas" holatga o'tkaza oladi.
#  Standart: agar hech qachon o'zgartirilmagan bo'lsa — FAOL (eski xatti-harakat saqlanadi).
# ================================================================================

TOGGLABLE_ITEMS = {
    "fake_doc": "📜 Soxta Hujjat",
    "night_vision": "🥽 Tungi ko'zoynak",
    "confuse": "✉️ Tushunarsiz xat",
    "golden_bullet": "🟡 Oltin o'q",
    "revive": "⚡️ Tezkor jonlanish",
    "watch_eyes": "👁 Kuzatish ko'zi",
    "duel_adv": "⚔️ Olmos Qilich (duel ustunligi)",
    "antidote": "🩹 Kichik Aptechka",
    "hidden_vote": "💼 Shubhali sumka",
}


def is_item_active(uid, key):
    ch = get_charges(uid)
    active_map = ch.get("active", {})
    return active_map.get(key, True)  # standart: faol


def toggle_item_active(uid, key):
    ch = get_charges(uid)
    active_map = ch.get("active", {})
    new_state = not active_map.get(key, True)
    active_map[key] = new_state
    ch["active"] = active_map
    set_charges(uid, ch)
    return new_state


def build_toggle_menu(uid):
    ch = get_charges(uid)
    kb = types.InlineKeyboardMarkup()
    any_item = False
    for key, label in TOGGLABLE_ITEMS.items():
        if ch.get(key, 0) <= 0:
            continue
        any_item = True
        state = "✅ FAOL" if is_item_active(uid, key) else "⛔ O'CHIQ"
        kb.add(types.InlineKeyboardButton(f"{label} — {state}", callback_data=f"toggleitem|{key}"))
    return kb, any_item


@bot.message_handler(commands=["kuchlarim"])
def cmd_kuchlarim(message):
    """Foydalanuvchi o'ziga tegishli avtomatik ishlaydigan buyumlarni yoqib/o'chirib qo'ya oladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    kb, any_item = build_toggle_menu(uid)
    if not any_item:
        bot.send_message(
            message.chat.id,
            "🎒 Sizda hozircha yoqish/o'chirish mumkin bo'lgan buyum yo'q.\n"
            "Do'kondan xarid qiling, keyin shu yerdan boshqarasiz.",
        )
        return
    bot.send_message(
        message.chat.id,
        "⚙️ <b>Buyumlaringizni boshqarish</b>\n\n"
        "Quyidagi buyumlar o'yin davomida avtomatik ishlaydi. Kerak bo'lmasa, o'chirib qo'yishingiz mumkin — "
        "shunda ular o'zi ishlab ketmaydi, faqat siz xohlagan payt yana yoqasiz.",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("toggleitem|"))
def cb_toggle_item(call):
    maybe_capture_owner(call.from_user)
    key = call.data.split("|", 1)[1]
    uid = call.from_user.id
    if get_charges(uid).get(key, 0) <= 0:
        bot.answer_callback_query(call.id, "❌ Bu buyum sizda mavjud emas.", show_alert=True)
        return
    new_state = toggle_item_active(uid, key)
    label = TOGGLABLE_ITEMS.get(key, key)
    bot.answer_callback_query(call.id, f"{label}: {'✅ Yoqildi' if new_state else '⛔ O\u02bbchirildi'}")
    kb, _ = build_toggle_menu(uid)
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        pass


def luck_mult(uid):
    """🦊 Cheksiz omad tulki tumori — barcha pul yutuqlarini ko'paytiradi.
    🏆 Geroy (Elandriel/Zephyrion "Omad tumori") — qo'shimcha ustama beradi."""
    base = get_charges(uid).get("luck_mult", 1)
    return base + hero_luck_boost(uid)


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


# ---- "Qizil vs Ko'k" ikki-guruhli musobaqa yordamchilari ----

def get_pair(chat_id):
    """Berilgan guruh biror juftlikka bog'langan bo'lsa, o'sha yozuvni qaytaradi
    (chat_id qaysi tomonda bo'lishidan qat'iy nazar), aks holda None."""
    with db_lock:
        cur.execute("SELECT chat_id_a, chat_id_b, label_a, label_b, score_a, score_b FROM group_pairs WHERE chat_id_a=? OR chat_id_b=?", (chat_id, chat_id))
        return cur.fetchone()


def create_pair(chat_id_a, chat_id_b):
    with db_lock:
        cur.execute("DELETE FROM group_pairs WHERE chat_id_a IN (?,?) OR chat_id_b IN (?,?)", (chat_id_a, chat_id_b, chat_id_a, chat_id_b))
        cur.execute("INSERT INTO group_pairs (chat_id_a, chat_id_b) VALUES (?,?)", (chat_id_a, chat_id_b))
        conn.commit()


def remove_pair(chat_id):
    with db_lock:
        cur.execute("DELETE FROM group_pairs WHERE chat_id_a=? OR chat_id_b=?", (chat_id, chat_id))
        conn.commit()


def add_pair_score(chat_id, winning_chat_id):
    """`chat_id` juftlikning bir tomoni. `winning_chat_id` shu turdagi o'yin g'olibi
    bo'lgan guruh (odatda chat_id'ning o'zi). Ballni oshirib, yangilangan yozuvni qaytaradi."""
    pair = get_pair(chat_id)
    if not pair:
        return None
    ca, cb, label_a, label_b, score_a, score_b = pair
    if winning_chat_id == ca:
        score_a += 1
    elif winning_chat_id == cb:
        score_b += 1
    with db_lock:
        cur.execute("UPDATE group_pairs SET score_a=?, score_b=? WHERE chat_id_a=?", (score_a, score_b, ca))
        conn.commit()
    return (ca, cb, label_a, label_b, score_a, score_b)


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
    """👑 Qirol unvoni egalari tepada chiqadi, 👤 Shadow statusidagilar va bot
    egasi reytingdan doim yashiriladi."""
    with db_lock:
        cur.execute("SELECT user_id, name, wins, dollar, charges FROM users ORDER BY wins DESC, dollar DESC LIMIT 200")
        rows = cur.fetchall()
    normal, qirol = [], []
    for user_id, name, wins, dollar, charges_json in rows:
        if is_owner(user_id):
            continue
        try:
            ch = json.loads(charges_json or "{}")
        except Exception:
            ch = {}
        if ch.get("shadow_until", 0) > time.time():
            continue
        entry = (user_id, name, wins, dollar, ch.get("qirol_until", 0) > time.time())
        (qirol if entry[4] else normal).append(entry)
    return (qirol + normal)[:limit]


def build_top_text():
    rows = get_top_players()
    if not rows:
        return "🏆 Hozircha reyting bo'sh."
    lines = ["🏆 <b>TOP O'YINCHILAR (g'alabalar bo'yicha)</b>\n"]
    for i, (user_id, name, wins, dollar, is_qirol) in enumerate(rows, 1):
        crown = "🐉 " if is_qirol else ""
        lines.append(f"{i}. {crown}{mention(user_id, name)} — {wins} g'alaba, ${dollar}")
    return "\n".join(lines)


def get_top_by_field(field, limit=10):
    """field: 'diamond' yoki 'dollar' — 👤 Shadow statusidagilar va bot egasi reytingdan doim yashiriladi."""
    with db_lock:
        cur.execute(f"SELECT user_id, name, {field}, charges FROM users ORDER BY {field} DESC LIMIT 200")
        rows = cur.fetchall()
    result = []
    for user_id, name, value, charges_json in rows:
        if is_owner(user_id):
            continue
        try:
            ch = json.loads(charges_json or "{}")
        except Exception:
            ch = {}
        if ch.get("shadow_until", 0) > time.time():
            continue
        result.append((user_id, name, value))
    return result[:limit]


def build_top_diamond_text():
    rows = get_top_by_field("diamond")
    if not rows:
        return "💎 Hozircha reyting bo'sh."
    lines = ["💎 <b>TOP ENG KO'P OLMOSI BOR O'YINCHILAR</b>\n"]
    for i, (user_id, name, diamond) in enumerate(rows, 1):
        lines.append(f"{i}. {mention(user_id, name)} — 💎 {diamond}")
    return "\n".join(lines)


def build_top_dollar_text():
    rows = get_top_by_field("dollar")
    if not rows:
        return "💵 Hozircha reyting bo'sh."
    lines = ["💵 <b>TOP ENG KO'P DOLLARI BOR O'YINCHILAR</b>\n"]
    for i, (user_id, name, dollar) in enumerate(rows, 1):
        lines.append(f"{i}. {mention(user_id, name)} — 💵 ${dollar}")
    return "\n".join(lines)


# ================================================================================
#  🏅 FAOLLIK BALLARI TIZIMI — har bir o'yin natijasiga qarab ball beriladi/ayiriladi:
#    • G'alaba qozongan (va oxirigacha qolgan) o'yinchi: +5 ball
#    • Mag'lub bo'lgan (lekin oxirigacha qolgan) o'yinchi: -5 ball
#    • O'yin davomidagi ENG FAOL o'yinchi (eng ko'p tun/kun harakati qilgan): +25 ball
#    • O'yinni tashlab ketgan yoki AFK bo'lib chetlashtirilgan o'yinchi: -10 ball
#  /balltop_kun, /balltop_hafta, /balltop_oy, /balltop_mutlaq — davr bo'yicha reyting
# ================================================================================

def add_points(uid, points, reason=""):
    with db_lock:
        cur.execute(
            "INSERT INTO points_log (user_id, points, reason, ts) VALUES (?, ?, ?, ?)",
            (uid, points, reason, time.time()),
        )
        conn.commit()


def get_points_leaderboard(period, limit=10):
    """period: 'kun', 'hafta', 'oy', 'mutlaq'"""
    now = time.time()
    since = {
        "kun": now - 86400,
        "hafta": now - 7 * 86400,
        "oy": now - 30 * 86400,
        "mutlaq": 0,
    }.get(period, 0)
    with db_lock:
        cur.execute(
            "SELECT user_id, SUM(points) FROM points_log WHERE ts >= ? GROUP BY user_id ORDER BY SUM(points) DESC LIMIT ?",
            (since, limit),
        )
        rows = cur.fetchall()
    result = []
    for uid, total in rows:
        if total is None:
            continue
        u = user_dict(uid)
        result.append((uid, u.get("name") or "O'yinchi", total))
    return result


PERIOD_LABELS = {"kun": "📅 Kunlik", "hafta": "🗓 Haftalik", "oy": "📆 Oylik", "mutlaq": "♾ Mutlaq (bot boshidan)"}


def build_points_top_text(period):
    rows = get_points_leaderboard(period)
    label = PERIOD_LABELS.get(period, period)
    if not rows:
        return f"🏅 {label} ball reytingi hozircha bo'sh."
    lines = [f"🏅 <b>{label} FAOLLIK BALLARI REYTINGI</b>\n"]
    for i, (uid, name, total) in enumerate(rows, 1):
        lines.append(f"{i}. {mention(uid, name)} — <b>{total}</b> ball")
    return "\n".join(lines)


@bot.message_handler(commands=["balltop_kun"])
def cmd_balltop_kun(message):
    maybe_capture_owner(message.from_user)
    bot.send_message(message.chat.id, build_points_top_text("kun"))


@bot.message_handler(commands=["balltop_hafta"])
def cmd_balltop_hafta(message):
    maybe_capture_owner(message.from_user)
    bot.send_message(message.chat.id, build_points_top_text("hafta"))


@bot.message_handler(commands=["balltop_oy"])
def cmd_balltop_oy(message):
    maybe_capture_owner(message.from_user)
    bot.send_message(message.chat.id, build_points_top_text("oy"))


@bot.message_handler(commands=["balltop_mutlaq"])
def cmd_balltop_mutlaq(message):
    maybe_capture_owner(message.from_user)
    bot.send_message(message.chat.id, build_points_top_text("mutlaq"))


@bot.callback_query_handler(func=lambda c: c.data.startswith("ptop|"))
def cb_points_top(call):
    maybe_capture_owner(call.from_user)
    _, period = call.data.split("|")
    bot.send_message(call.message.chat.id, build_points_top_text(period))
    bot.answer_callback_query(call.id)


def build_top_groups_text(limit=10):
    groups = list_known_groups()
    if not groups:
        return "🏘 Hozircha ma'lum guruhlar yo'q."
    lines = ["🏘 <b>TOP GURUHLAR</b>\n"]
    for i, (chat_id, title) in enumerate(groups[:limit], 1):
        lines.append(f"{i}. {title or chat_id} (<code>{chat_id}</code>)")
    return "\n".join(lines)


# ================================================================================
#  BOT YARATUVCHISINI ANIQLASH
# ================================================================================

_owner_id_raw = get_setting("owner_id")
OWNER_ID = int(_owner_id_raw) if _owner_id_raw else None

_bm_chat_raw = get_setting("black_market_chat_id")
BLACK_MARKET_CHAT_ID = int(_bm_chat_raw) if _bm_chat_raw else None

_owner_channel_raw = get_setting("owner_channel_id")
OWNER_CHANNEL_ID = int(_owner_channel_raw) if _owner_channel_raw else None


def is_owner_channel(chat):
    """Kanal postlari uchun: message.from_user doim None bo'ladi (Telegram buni
    hech kimga ko'rsatmaydi), shuning uchun faqat oldindan tasdiqlangan kanal
    chat_id'siga ishonamiz — chunki faqat o'sha kanalning administratorlari
    unga post qila oladi."""
    return chat.type == "channel" and OWNER_CHANNEL_ID is not None and chat.id == OWNER_CHANNEL_ID


@bot.message_handler(commands=["shu_kanal"])
def cmd_set_owner_channel(message):
    """Bot egasi shu buyruqni SHAXSIY chatda yozadi (kanalning o'zida emas — chunki u
    yerda foydalanuvchi shaxsi Telegram tomonidan yashiriladi). Masalan:
    /shu_kanal @Mirkamilovic   yoki   /shu_kanal -1001234567890
    Bot avval o'sha kanalga administrator sifatida qo'shilgan bo'lishi shart."""
    global OWNER_CHANNEL_ID
    maybe_capture_owner(message.from_user)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/shu_kanal @kanal_username</code> yoki <code>/shu_kanal -100...</code>")
        return
    identifier = parts[1].strip()
    try:
        chat = bot.get_chat(identifier)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Kanalni topib bo'lmadi: {e}\n"
            "Bot o'sha kanalga administrator sifatida qo'shilganiga ishonch hosil qiling.",
        )
        return
    if chat.type != "channel":
        bot.send_message(message.chat.id, "❌ Bu kanal emas.")
        return
    OWNER_CHANNEL_ID = chat.id
    set_setting("owner_channel_id", OWNER_CHANNEL_ID)
    bot.send_message(message.chat.id, f"✅ Endi <b>{chat.title}</b> kanalidan buyruq berishingiz mumkin (masalan: /top, /topalmaz, /topdollar, /topguruh, /tarqatish).")


def is_owner(user_id):
    # 1) Muhit o'zgaruvchisida aniq berilgan ID — eng ishonchli, doim ustuvor.
    if OWNER_ID_FROM_ENV is not None and user_id == OWNER_ID_FROM_ENV:
        return True
    # 2) Avtomatik aniqlangan/bazada saqlangan owner_id.
    return OWNER_ID is not None and user_id == OWNER_ID


def maybe_capture_owner(tg_user):
    """OWNER_ID_FROM_ENV berilgan bo'lsa, bu funksiya hech narsa qilmaydi —
    chunki ishonchli manba muhit o'zgaruvchisi hisoblanadi. Aks holda,
    eski (zaif) username-asosidagi avtomatik aniqlash ishlashda davom etadi,
    lekin bu endi faqat OWNER_ID_FROM_ENV sozlanmagan hollar uchun zaxira usul."""
    global OWNER_ID
    if OWNER_ID_FROM_ENV is not None:
        return
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


def get_partner_id(uid):
    u = user_dict(uid)
    return u.get("married_to") or 0


def get_partner_name(uid):
    """qoshimchakod3.py / qoshimchakod6.py g'oyasi — married_to ustuni asosida haqiqiy holat."""
    partner_id = get_partner_id(uid)
    if not partner_id:
        return None
    return user_dict(partner_id)["name"]


def get_partner_mention(uid):
    """Juftim (turmush o'rtoq) ismini bosilganda Telegram profiliga o'tadigan link ko'rinishida qaytaradi."""
    partner_id = get_partner_id(uid)
    if not partner_id:
        return None
    return mention(partner_id, user_dict(partner_id)["name"])


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
    {"key": "first_speaker", "text": "Kunduzgi muhokamada birinchi bo'lib guruhga yoz."},
    {"key": "vote_skip", "text": "Ovoz berishda hech kimga ovoz bermay, 'O'tkazib yuborish'ni tanla."},
    {"key": "self_vote", "text": "Ovoz berishda o'zingga ovoz ber."},
    {"key": "say_xayrli_tun", "text": "Tun boshlanishidan oldin guruhda 'Xayrli tun' deb yoz."},
    {"key": "talk_atleast_once", "text": "Kunduzgi muhokamada kamida bitta marta guruhga yoz."},
    {"key": "first_voter", "text": "Ovoz berishda birinchi bo'lib ovoz ber."},
    {"key": "last_voter", "text": "Ovoz berishda oxirgi bo'lib ovoz ber."},
    {"key": "never_say_tinch", "text": "Bugungi o'yinda hech qachon 'Men tinch aholiman' deb yozma."},
    {"key": "vote_against_mafia_kill", "text": "Kunduzgi ovoz berishda, o'tgan tunda mafiya hujum qilgan kishiga qarshi ovoz ber."},
    {"key": "active_5msg", "text": "O'yin davomida kamida 5 marta guruhga xabar yoz (faollik ko'rsat)."},
    {"key": "say_men_ham", "text": "Kimningdir fikriga qo'shilib, 'Men ham shunday o'ylayman' deb yoz."},
    {"key": "silent_until_vote", "text": "Kunduzgi bosqichda ovoz berish ochilgunga qadar mutlaqo jim o'tir, guruhga yozma."},
    {"key": "vote_majority", "text": "Kunduzgi ovoz berishda, oxir-oqibat eng ko'p ovoz olgan kishiga ovoz ber."},
    {"key": "max3_msg", "text": "Kunduzgi muhokamada jami 3 martadan ko'p yozma (kamroq gapir, ko'proq kuzat)."},
    {"key": "survive_night", "text": "Bu tunda tirik qolib, ertalabgacha yetib kel."},
]

RANDOM_EVENTS = [
    {"key": "silence", "text": "⚡️ Chaqmoq chaqdi! Bugun sirli bir kayfiyat hukm surmoqda... (hikoya, o'yin oxirigacha davom etadi)"},
    {"key": "lucky_all", "text": "💰 Omadli daqiqa! Barcha tirik o'yinchilarga +50$ bonus taqdim etildi."},
    {"key": "fog", "text": "🔀 Sirli tuman! Bugun Komissar kimni tekshirsa ham, natija aniqlanmay, xira ko'rinadi."},
    {"key": "no_lynch", "text": "🔍 Taqdir hukmi! Bugungi kunduzgi ovoz berishda hech kim osilmaydi (natijadan qat'i nazar)."},
    {"key": "weak_night", "text": "🌪 Bo'ron boshlandi! Bugungi tunda himoya qobiliyatlari (shield/qorovul) 50% ehtimol bilan ishlamay qoladi."},
    {"key": "lucky_one", "text": "🎁 Sirli sovg'a qutisi topildi! Tasodifiy bitta o'yinchiga +100$ tushdi."},
    {"key": "rumor", "text": "📢 Shov-shuv! Guruh bo'ylab kimdir shubhali gap tarqatdi — hamma bir-biriga qarab qoldi. (Hikoya)"},
    {"key": "short_vote", "text": "🕯 Sokinlik kuni! Bugungi kunduzgi ovoz berish bosqichi 15 soniyaga qisqartirildi."},
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

# ================================================================================
#  QO'SHIMCHA 25 TA ROL — TO'LIQ ISHLAYDIGAN TUNGI HARAKATLAR
#  (Don/Komissar/Doktor — "asosiy rollar" — allaqachon yuqorida ishlab turibdi;
#  Mafia 🕶 ham Don bilan birga umumiy mafiya ovoziga qo'shiladi.)
#  Har bir rol tun davomida harakatni BOSHLASA, guruhga ASOSIY ROLLAR kabi
#  ANONIM (kim ekani aytilmasdan) tarzda e'lon qilinadi.
# ================================================================================

EXTRA_ROLE_SLUGS = {
    "Qotil 🗡": "qotil",
    "Manyak 🔪": "manyak",
    "Serjant 👮‍♂️": "serjant",
    "Advokat ⚖️": "advokat",
    "Fohisha 💋": "fohisha",
    "Mergan 🏹": "mergan",
    "Sadoqatli yordamchi 🤝": "sadoqat",
    "Snayper 🎯": "snayper",
    "O'g'ri 🥷": "ogri",
    "Sehrgar 🧙‍♂️": "sehrgar",
    "Sehrgar yordamchisi 🪄": "sehryor",
    "Arvoh 👻": "arvoh",
    "Sudya 👨‍⚖️": "sudya",
    "Provokator 🗣": "provokator",
    "General 🎖": "general",
    "Josus 🕵️": "josus",
    "Bomj 🧟‍♂️": "bomj",
    "Arxitektor 📐": "arxitektor",
    "Telba 🤪": "telba",
    "Qorovul 🔦": "qorovul",
}
SLUG_TO_ROLE = {v: k for k, v in EXTRA_ROLE_SLUGS.items()}

# slug -> (o'yinchiga yuboriladigan savol, guruhga anonim e'lon qilinadigan atmosfera matni)
EXTRA_ROLE_PROMPTS = {
    "qotil":      ("🗡 Kimni yashirincha pichoqlaymiz?", "🗡 <i>Yolg'iz qotil qorong'ulikda o'ljasini poylamoqda...</i>"),
    "manyak":     ("🔪 Kimga tunda hujum qilamiz?", "🔪 <i>Manyak shahar bo'ylab qurbon izlab yurmoqda...</i>"),
    "serjant":    ("👮‍♂️ Komissar o'rniga kimni tekshiramiz?", "👮‍♂️ <i>Serjant Komissar vazifasini o'z zimmasiga oldi...</i>"),
    "advokat":    ("⚖️ Kimni ertangi kunduzgi osishdan himoya qilamiz?", "⚖️ <i>Advokat tungi hujjatlarni tayyorlab, birovni himoya qilishga tayyorlanmoqda...</i>"),
    "fohisha":    ("💋 Kimning oldiga borib, uni band qilamiz?", "💋 <i>Sirli mehmon birovning uyiga yo'l oldi...</i>"),
    "mergan":     ("🏹 Kimni nishonga olamiz?", "🏹 <i>Mergan uzoqdan kimningdir izidan tushdi...</i>"),
    "sadoqat":    ("🤝 Kimni jonim bilan himoya qilaman?", "🤝 <i>Sadoqatli yordamchi birovni tungi hujumdan himoya qilishga qasamyod qildi...</i>"),
    "snayper":    ("🎯 Kimni otib tashlaymiz? (bu qobiliyat butun o'yinda faqat 1 marta ishlaydi)", "🎯 <i>Uzoqdan Snayper nishonini tekshirmoqda...</i>"),
    "ogri":       ("🥷 Kimning cho'ntagini kavlaymiz?", "🥷 <i>Kimdir soyada birovning cho'ntagiga qo'l soldi...</i>"),
    "sehrgar":    ("🧙‍♂️ Kimga sehrli kuch yo'naltiramiz?", "🧙‍♂️ <i>Sehrgar sirli belgilar chizib, taqdirlarni aralashtirmoqda...</i>"),
    "sehryor":    ("🪄 Kimga qo'shimcha himoya berasiz?", "🪄 <i>Sehrgar yordamchisi kimningdir atrofiga sehrli devor tortdi...</i>"),
    "arvoh":      ("👻 Tirik o'yinchilardan kimga sirli imo-ishora yubormoqchisiz?", "👻 <i>Arvoh olamidan sirli bir imo-ishora yetib keldi...</i>"),
    "sudya":      ("👨‍⚖️ Ertangi kun ovozingizni 2x kuchga ega qilasizmi?", "👨‍⚖️ <i>Sudya ertangi hukm uchun tayyorgarlik ko'rmoqda...</i>"),
    "provokator": ("🗣 Kimni ertaga aholiga qarshi gij-gijlaymiz?", "🗣 <i>Provokator allaqachon mish-mish tarqatishni boshladi...</i>"),
    "general":    ("🎖 Kimga qo'shimcha himoya beramiz?", "🎖 <i>General o'z jamoasiga qo'shimcha himoya taqdim etmoqda...</i>"),
    "josus":      ("🕵️ Kimning qaysi tarafda ekanini bilib olamiz?", "🕵️ <i>Josus soyalarda yashirin ma'lumot yig'moqda...</i>"),
    "bomj":       ("🧟‍♂️ Kimning ortidan yashirincha kuzatamiz?", "🧟‍♂️ <i>Bomj ko'cha burchagida kimnidir kuzatib turibdi...</i>"),
    "arxitektor": ("📐 Kimga himoya devori quramiz?", "📐 <i>Arxitektor tungi to'siq qurish bilan band...</i>"),
    "telba":      ("🤪 Bugun kimga tasodifiy 'baxt' ulashamiz? (natija oldindan noma'lum)", "🤪 <i>Telba hech kim kutmagan bir harakat qildi...</i>"),
    "qorovul":    ("🔦 Kimni tunda qo'riqlaymiz?", "🔦 <i>Qorovul fonarini yoqib, kimningdir uyi oldida qorovullik qilmoqda...</i>"),
}

# darhol (shu zahoti) natija beradigan tekshiruv-turdagi rollar
EXTRA_ROLE_INSTANT_INFO = {"josus", "bomj", "serjant"}
# faqat "ha/yo'q" tanlovi bo'lgan rol
EXTRA_ROLE_YESNO = {"sudya"}
# o'z-o'zini ham nishonga olishi mumkin bo'lgan (o'zini himoyalay oladigan) rollar
EXTRA_ROLE_SELF_TARGET_OK = {"arxitektor", "sehryor"}
# tun yakunida (resolve_night) birgalikda ishlanadigan (kechiktirilgan) rollar
EXTRA_ROLE_DEFERRED = {
    "qotil", "manyak", "mergan", "snayper", "telba", "fohisha", "sehrgar",
    "general", "arxitektor", "qorovul", "sadoqat",
}

# ================================================================================
#  🌙 TUNGI ATMOSFERA XABARLARI — har bir rol uchun (qoshimchakod2.py g'oyasi asosida,
#  telebot uslubiga moslashtirildi). Bu matnlar faqat hikoya/atmosfera uchun —
#  o'yinning asosiy mexanikasi (Don/Mafia/Komissar/Doktor) allaqachon alohida ishlab turibdi.
# ================================================================================

NIGHT_FLAVOR_TEXTS = {
    "Qotil 🗡": "🗡 Shaharning qorong'u burchagida yolg'iz qotilning soyasi ko'rindi...",
    "Manyak 🔪": "🔪 Shaharda manyakning qadam tovushlari eshitildi...",
    "Serjant 👮‍♂️": "👮‍♂️ Serjant tungi patrulni boshladi, hushyor turibdi.",
    "Advokat ⚖️": "⚖️ Advokat kimnidir himoya qilish uchun tungi hujjat tayyorladi.",
    "Fohisha 💋": "💋 Shahar ko'chalarida sirli mehmon kezib yurdi...",
    "Terrorist 💣": "🧨 Tun qorong'usida shubhali portlovchi modda hidi keldi.",
    "Mergan 🏹": "🏹 Mergan o'z pozitsiyasini egallab, nishonga ko'z tikdi.",
    "Varvar 🪓": "🪓 Baquvvat jangchining qadam tovushlari uzoqdan eshitildi.",
    "Sadoqatli yordamchi 🤝": "🤝 Kimdir sodiqlik bilan o'z homiysini tungi soyada kuzatdi.",
    "Snayper 🎯": "🎯 Uzoqdan turib kimdir nishonga ko'z tikkandek tuyuldi...",
    "O'g'ri 🥷": "🖐 Kechasi yashirin qadamlar ovozi eshitildi — kimningdir cho'ntagi titkilandi...",
    "Sehrgar 🧙‍♂️": "🔮 Sehrgar sehrli kuchlarni tun qorong'usida ishga soldi.",
    "Sehrgar yordamchisi 🪄": "🪄 Sehrgar yordamchisi ustoziga yordam berib, kuchlarni oshirdi.",
    "Arvoh 👻": "👻 Narigi dunyodan turib kimdir tunni sirli kuzatib turibdi...",
    "Sudya 👨‍⚖️": "⚖️ Sudya ertangi kun uchun adolat tarozisini tayyorlab qo'ydi.",
    "Provokator 🗣": "🗣 Kimdir soyada turib janjal rejasini tuzmoqda...",
    "General 🎖": "🎖 General o'z taktikasini tungi qorong'ulikda ishlab chiqdi.",
    "Josus 🕵️": "🕵️ Josus boshqalarning sirlarini poylab, izlarni yashirincha kuzatdi.",
    "Bomj 🧟‍♂️": "🧟‍♂️ Ko'chada kezib yurgan bir soyaning nafasi eshitildi...",
    "Arxitektor 📐": "📐 Arxitektor tun bo'yi yashirin to'siqlar rejasini chizdi.",
    "Telba 🤪": "🤪 Shaharda kimdir g'alati, tushunarsiz qiliqlar qilib yuribdi...",
    "Qorovul 🔦": "🔦 Qorovul o'z hududini tinimsiz qo'riqlashni boshladi.",
    "Beshikdagi bola 👶": "👶 Tinch uyqudagi kenja qahramonni hech kim bezovta qilmadi.",
}


def alive_role_flavor_lines(game):
    """Tirik o'yinchilar orasidagi rollarga qarab tungi atmosfera matnlarini yig'adi."""
    lines = []
    seen_roles = set()
    for p in alive_players(game).values():
        role = p["role"]
        if role in NIGHT_FLAVOR_TEXTS and role not in seen_roles:
            seen_roles.add(role)
            lines.append(NIGHT_FLAVOR_TEXTS[role])
    return lines


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

# 😴 2 tun ketma-ket harakatsiz qolgan (AFK) o'yinchi avtomatik chiqarilganda
# guruhga yuboriladigan hazil xabarlar (kim ekani aytilmaydi)
# 🌙 O'lim xabarida "kim tashrif buyurgani" haqida har bir rolga mos individual
# ibora — kim ekani (nikneymi) hech qachon oshkor qilinmaydi, faqat ROL turi.
VISIT_PHRASE = {
    "Don 🎩": "Aytishlaricha, unikiga tunda Don shaxsan tashrif buyurgan...",
    "Mafia 🕶": "Aytishlaricha, unikiga tunda mafiya soyalari kelgan...",
    "Komissar 🕵️‍♂️": "Aytishlaricha, unikiga tunda Komissar tashrif buyurgan...",
    "Doktor 👨‍⚕️": "Aytishlaricha, unikiga tunda Doktor kelgan edi...",
    "Qotil 🗡": "Aytishlaricha, unikiga tunda yolg'iz qotil pichoq bilan kelgan...",
    "Manyak 🔪": "Aytishlaricha, unikiga tunda manyak vahshiylarcha bostirib kirgan...",
    "Mergan 🏹": "Aytishlaricha, uni uzoqdan Mergan nishonga olgan...",
    "Snayper 🎯": "Aytishlaricha, uni Snayper uzoq masofadan otib tushirgan...",
    "Telba 🤪": "Aytishlaricha, unikiga tasodifiy Telba kirib qolgan...",
    "Serjant 👮‍♂️": "Aytishlaricha, unikiga Serjant tashrif buyurgan...",
    "Advokat ⚖️": "Aytishlaricha, unikiga Advokat kelgan edi...",
    "Fohisha 💋": "Aytishlaricha, unikiga sirli mehmon kelgan...",
    "Sadoqatli yordamchi 🤝": "Aytishlaricha, unikiga Sadoqatli yordamchi kelgan...",
    "O'g'ri 🥷": "Aytishlaricha, unikiga tunda kimdir kirib chiqqan...",
    "Sehrgar 🧙‍♂️": "Aytishlaricha, unikiga Sehrgar sehrli tashrif buyurgan...",
    "Sehrgar yordamchisi 🪄": "Aytishlaricha, unikiga Sehrgar yordamchisi kelgan...",
    "Arvoh 👻": "Aytishlaricha, unikiga g'ayritabiiy bir soya kelgan...",
    "Sudya 👨‍⚖️": "Aytishlaricha, Sudya undan xabar olgan...",
    "Provokator 🗣": "Aytishlaricha, unikiga Provokator kelib, mish-mish tarqatgan...",
    "General 🎖": "Aytishlaricha, unikiga General tashrif buyurgan...",
    "Josus 🕵️": "Aytishlaricha, unikiga Josus yashirincha kelgan...",
    "Bomj 🧟‍♂️": "Aytishlaricha, uning oldidan Bomj o'tib ketgan...",
    "Arxitektor 📐": "Aytishlaricha, unikiga Arxitektor tashrif buyurgan...",
    "Qorovul 🔦": "Aytishlaricha, uni Qorovul tunda kuzatib turgan...",
}

AFK_KICK_JOKES = [
    "😴 {who} shu qadar chuqur uxlab qolibdiki, o'yin uni o'zi bilan olib keta olmadi... (Roli: {role})",
    "🛌 {who} ikki tundan beri sukut saqlagani uchun shaharni tark etdi. (Roli: {role})",
    "📴 {who}ning aloqasi 2 tundan beri yo'q — ehtimol pitsa buyurtma qilgandir. U endi o'yinda emas. (Roli: {role})",
    "🚪 Sukunat ikki tunga cho'zilsa, eshik ham ochiladi... {who} jimgina chiqib ketdi. (Roli: {role})",
    "💤 {who} shunchalik og'ir uxlab qoldiki, hatto Telegram ham uni unutdi. U o'yindan chetlatildi. (Roli: {role})",
    "🧊 {who} 2 tun muzlab qoldi va endi butunlay eriб yo'qoldi. (Roli: {role})",
    "🌫 {who} tumanga aylanib, shahardan g'oyib bo'ldi — 2 tun hech kim uni ko'rmadi. (Roli: {role})",
    "📵 {who} telefonini uyda unutgan shekilli — 2 tundan beri sado-savo yo'q. Chetlatildi. (Roli: {role})",
    "🕳 {who} qandaydir sirli teshikka tushib ketdi va 2 tun qaytmadi. Endi o'yinda emas. (Roli: {role})",
    "🐌 {who} shu qadar sekin harakat qildiki, hatto soat milliga ham ulgurmadi. 2 tun sukunat — chetlatildi. (Roli: {role})",
    "🎭 {who} sahnadan 2 tunga g'oyib bo'lgan aktyorday — endi rolini boshqa hech kim o'ynamaydi. (Roli: {role})",
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
    "kunhimoya": {"name": "🛡🌞 Kunduzgi himoya", "price": 200, "currency": "dollar", "mode": "charge", "charge_key": "day_shield",
                 "desc": "Aholi tomonidan kunduzi osilishdan 1 marta himoya qiladi. Bitta o'yinda faqat 1 marta ishlaydi."},
    "hujjat":   {"name": "📜 Soxta Hujjat", "price": 350, "currency": "dollar", "mode": "charge", "charge_key": "fake_doc",
                 "desc": "Komissar sizni tekshirsa, 'Tinch aholi' bo'lib ko'rinasiz."},
    "aptechka": {"name": "🩹 Kichik Aptechka", "price": 150, "currency": "dollar", "mode": "charge", "charge_key": "antidote",
                 "charge_amount": 1,
                 "desc": "Sizni /zahar (zaharlash) ta'siridan 1 marta avtomatik davolaydi — zaharlansangiz, tunda o'zi ishga tushadi."},
    "kozoynak": {"name": "🥽 Tungi ko'zoynak", "price": 500, "currency": "dollar", "mode": "charge", "charge_key": "night_vision",
                 "desc": "Tundan keyin qaysi rollar faol bo'lganini shaxsiy xabarda ko'rasiz."},
    "xat":      {"name": "✉️ Tushunarsiz xat", "price": 100, "currency": "dollar", "mode": "charge", "charge_key": "confuse",
                 "desc": "Mafiya sizni nishonga olsa, hujum tasodifiy boshqa odamga burilib ketadi."},
    "sumka":    {"name": "💼 Shubhali sumka", "price": 450, "currency": "dollar", "mode": "charge", "charge_key": "hidden_vote",
                 "charge_amount": 3,
                 "desc": "Kunduzi kimga ovoz berganingiz 👁 Kuzatish ko'zi orqali ham 'noma'lum' bo'lib ko'rinadi (3 marta)."},
    "niqob":    {"name": "🎭 Temir niqob", "price": 600, "currency": "dollar", "mode": "shield",
                 "desc": "O'yin paytida o'lishdan 1 marta himoya qiladi (qo'shimcha)."},
    "zahar":    {"name": "🧪 Zaharli flakon", "price": 800, "currency": "dollar", "mode": "charge", "charge_key": "poison",
                 "desc": "/zahar buyrug'i orqali (reply) birovni zaharlash imkonini beradi."},
    "gps":      {"name": "📍 GPS Mayak", "price": 900, "currency": "dollar", "mode": "charge", "charge_key": "gps",
                 "desc": "/gps buyrug'i orqali (reply) birovning tirik/o'lganligini bilib olasiz."},
    "kompas":   {"name": "🧭 Sirli kompas", "price": 950, "currency": "dollar", "mode": "charge", "charge_key": "compass",
                 "desc": "/kompas buyrug'i orqali (reply) birovning qaysi tarafda (mafiya/tinch aholi/mustaqil) ekanini bilib olasiz — rolini emas, faqat tarafini."},
    "vip":      {"name": "💳 Oltin Litsenziya", "price": 1000, "currency": "dollar", "mode": "multiplier",
                 "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    # --- YANGI MAHSULOTLAR (qoshimchakod8.py g'oyasi asosida qo'shildi) ---
    "energy":   {"name": "⚡️ Energiya ichimligi", "price": 120, "currency": "dollar", "mode": "charge", "charge_key": "revote",
                 "charge_amount": 2,
                 "desc": "Kunduzi ovoz bergandan keyin fikringizni o'zgartirib, qayta ovoz berish imkonini beradi (2 marta)."},
    "tutun":    {"name": "💣 Tutunli bomba", "price": 280, "currency": "dollar", "mode": "charge", "charge_key": "smoke_bomb",
                 "desc": "Xavfli vaziyatda izingizni yo'qotib, dushmandan yashiringan bo'lasiz."},
    "zar":      {"name": "🎲 Sehrli Zarlar", "price": 320, "currency": "dollar", "mode": "gamble_ability",
                 "desc": "Ochilganda tasodifiy: 🛡 Himoya YOKI 🥽 Tungi ko'zoynak qobiliyatlaridan biri chiqadi (pul emas)."},
    "fonar":    {"name": "🔦 Katta Fonar", "price": 220, "currency": "dollar", "mode": "charge", "charge_key": "flash_light",
                 "desc": "Kechasi qorong'ilikdagi yashirin harakatlarni yoritib beradi."},
}

SHOP_DIAMOND = {
    "qilich":    {"name": "⚔️ Olmos Qilich", "price": 5, "currency": "diamond", "mode": "charge", "charge_key": "duel_adv",
                  "charge_amount": 5,
                  "desc": "Keyingi 5 ta duelda g'alaba imkoniyatini 65% ga oshiradi."},
    "tumor":     {"name": "🔮 Sehrli tumor", "price": 10, "currency": "diamond", "mode": "multiplier",
                  "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    "quti":      {"name": "📦 Nodir quti", "price": 15, "currency": "diamond", "mode": "gamble_ability",
                  "desc": "Ichidan tasodifiy: 📍 GPS, 🧭 Kompas yoki 🛡 Himoya qobiliyatlaridan biri chiqadi (pul emas)."},
    "oq":        {"name": "🟡 Oltin o'q", "price": 20, "currency": "diamond", "mode": "charge", "charge_key": "golden_bullet",
                  "charge_amount": 5,
                  "desc": "Mafiyaning o'ldirish urinishi himoya/davolashni chetlab o'tadi (5 marta)."},
    "qalqon":    {"name": "🛡 Imunitet qalqoni", "price": 25, "currency": "diamond", "mode": "shield",
                  "desc": "O'yin paytida o'lishdan 1 marta himoya qiladi."},
    "radar":     {"name": "📡 Maxfiy radar", "price": 30, "currency": "diamond", "mode": "charge", "charge_key": "radar",
                  "charge_amount": 6,
                  "desc": "/qayta_tanlash orqali o'z rolingizni tasodifiy boshqasiga almashtirasiz (6 marta)."},
    "jonlanish": {"name": "⚡️ Tezkor jonlanish", "price": 40, "currency": "diamond", "mode": "charge", "charge_key": "revive",
                  "charge_amount": 6,
                  "desc": "O'lish arafasida qo'shimcha jon beradi (6 marta, shielddan keyin ishlaydi)."},
    "imperator": {"name": "👑 1 kunlik imperator", "price": 50, "currency": "diamond", "mode": "expiry",
                  "charge_key": "imperator_until", "duration_seconds": 86400, "desc": "24 soat 'Imperator' maqomi (profilda ko'rinadi)."},
    "ramka":     {"name": "🖼 Mifik ramka", "price": 75, "currency": "diamond", "mode": "expiry", "charge_key": "ramka_until",
                  "duration_seconds": 30 * 86400,
                  "desc": "Profilingizga 30 kunga eksklyuziv ramka belgisi qo'shadi."},
    "tulki":     {"name": "🦊 Omad tumori", "price": 100, "currency": "diamond", "mode": "multiplier",
                  "charge_key": "luck_mult", "mult_value": 3, "desc": "Barcha pul yutuqlaringizni (bonus, duel, o'yin mukofoti) 3x qiladi."},
    "vip_olmos": {"name": "🔭 Kuzatuv minorasi", "price": 60, "currency": "diamond", "mode": "charge", "charge_key": "night_vision",
                  "charge_amount": 3,
                  "desc": "3 marta — 🥽 Tungi ko'zoynak bilan bir xil: tunda qaysi rollar faol bo'lganini (kim ekanini emas) DM orqali bildiradi."},
    # --- YANGI MAHSULOTLAR (qoshimchakod8.py g'oyasi asosida qo'shildi) ---
    "kristal":   {"name": "💠 Sehrli Kristal", "price": 8, "currency": "diamond", "mode": "charge", "charge_key": "compass",
                  "charge_amount": 1,
                  "desc": "Kristall kelajakni ko'rsatadi — 1 marta 🧭 Kompas qobiliyati beradi (birovning tarafini bilib olasiz)."},
    "kolt":      {"name": "🧥 Yashirin plash", "price": 18, "currency": "diamond", "mode": "charge", "charge_key": "cloak",
                  "charge_amount": 5,
                  "desc": "O'yin davomida dushmanlar nishoniga tushishdan himoya qiladi (5 marta)."},
    "eliksir":   {"name": "🧪 Hayot Eliksiri", "price": 35, "currency": "diamond", "mode": "charge", "charge_key": "revive",
                  "charge_amount": 1,
                  "desc": "O'lim arafasida hayotingizni saqlab qoladi — 1 marta qo'shimcha jon (⚡️ Tezkor jonlanish bilan bir xil)."},
    "sandiq":    {"name": "🏆 Afsonaviy Sandiq", "price": 110, "currency": "diamond", "mode": "hero_chest",
                  "desc": "Ichidan 5 xil noyob GEROYDAN biri chiqadi! Har biri o'ziga xos kuchli qobiliyatga ega "
                          "(1-15 lvl gacha rivojlantiriladi). /geroyim orqali ko'ring."},
}

# ================================================================================
#  🏆 GEROYLAR TIZIMI — "Afsonaviy Sandiq" ichidan chiqadigan 5 xil geroy.
#  4 tasi bir-biriga teng kuchli, 1 tasi (🦅 Zephyrion) biroz kuchliroq,
#  lekin tushish ehtimoli atigi 0.05% (chit bo'lib qolmasligi uchun cheklangan).
#  Har bir geroy 1-lvldan boshlanadi, 15-lvlgacha rivojlanadi; lvl oshgani sari
#  effekt kuchi asta-sekin, muvozanatli tarzda oshib boradi.
# ================================================================================

HEROES = {
    "sardor": {
        "name": "⚔️ Draven the Warlord", "image": "hero_draven.jpg",
        "abilities": [
            {"key": "survive", "unlock": 1, "name": "🛡 Tungi chidamlilik",
             "desc": "Tunda hujumdan tasodifiy foizda avtomatik omon qolasiz.", "base": 0.05, "cap": 0.18},
            {"key": "revive_once", "unlock": 6, "name": "⚰️ O'lmas ruh",
             "desc": "O'yin davomida BIR MARTA, hech qanday himoya ishlamay qolsa ham, kafolatlangan tirik qolasiz."},
            {"key": "vote_shield_once", "unlock": 11, "name": "🗳 Xalq himoyasi",
             "desc": "O'yin davomida BIR MARTA, kunduzgi ovoz berishda eng ko'p ovoz olsangiz ham osilmaysiz."},
        ],
    },
    "malika": {
        "name": "🔮 Seraphine the Oracle", "image": "hero_seraphine.jpg",
        "abilities": [
            {"key": "compass_free", "unlock": 1, "name": "🧭 Cheksiz kompas",
             "desc": "Har kuni bepul, cheklovsiz /kompas ishlatish imkoniyati (do'kondan sotib olmasdan)."},
            {"key": "night_vision_auto", "unlock": 6, "name": "👁 Tungi nazar",
             "desc": "Har tun avtomatik ravishda nechta o'yinchi faol harakat qilganini (kimligini emas) DM orqali bilib olasiz."},
            {"key": "role_reveal_once", "unlock": 11, "name": "🔍 Chuqur bashorat",
             "desc": "O'yin davomida BIR MARTA, istalgan o'yinchining ANIQ rolini (/geroy_bashorat orqali) bilib olasiz."},
        ],
    },
    "temur": {
        "name": "🛡️ Magnus the Conqueror", "image": "hero_magnus.jpg",
        "abilities": [
            {"key": "duel_bonus", "unlock": 1, "name": "⚔️ Jangchi mahorati",
             "desc": "Duellarda g'alaba qozonish ehtimoli oshadi.", "base": 0.05, "cap": 0.18},
            {"key": "duel_draw_chance", "unlock": 6, "name": "🏹 Qat'iy zarba",
             "desc": "Duelda mag'lub bo'lish o'rniga, tasodifiy foizda durrang (hech kim yutqazmaydi) bo'lish imkoniyati.",
             "base": 0.08, "cap": 0.20},
            {"key": "vote_weight", "unlock": 11, "name": "👑 General nufuzi",
             "desc": "Kunduzgi ovoz berishda ovozingiz qo'shimcha og'irlikka ega bo'ladi."},
        ],
    },
    "layli": {
        "name": "🌙 Elandriel the Enchantress", "image": "hero_elandriel.jpg",
        "abilities": [
            {"key": "bonus_dollar", "unlock": 1, "name": "💰 Sehrli bonus",
             "desc": "Kunlik bonus miqdori oshadi.", "base": 20, "cap": 150},
            {"key": "luck_boost", "unlock": 6, "name": "🍀 Omad tumori",
             "desc": "Do'kondagi tasodifiy pul beruvchi buyumlardan (zar, sumka, quti) ko'proq yutish ehtimoli oshadi.",
             "base": 0.08, "cap": 0.25},
            {"key": "diamond_trickle", "unlock": 11, "name": "💎 Boylik siri",
             "desc": "Har o'yin boshlanganda avtomatik +1 💎 Olmos olasiz."},
        ],
    },
    "burgut": {
        "name": "🦅 Zephyrion, the Ascendant One", "image": "hero_zephyrion.jpg",
        "abilities": [
            {"key": "survive", "unlock": 1, "name": "🛡 Osmoniy chidamlilik",
             "desc": "Tunda hujumdan tasodifiy foizda avtomatik omon qolasiz.", "base": 0.08, "cap": 0.22},
            {"key": "compass_free", "unlock": 4, "name": "🧭 Cheksiz kompas",
             "desc": "Har kuni bepul, cheklovsiz /kompas ishlatish imkoniyati."},
            {"key": "duel_bonus", "unlock": 7, "name": "⚔️ Ascendant zarbasi",
             "desc": "Duellarda g'alaba qozonish ehtimoli oshadi.", "base": 0.08, "cap": 0.22},
            {"key": "bonus_dollar", "unlock": 10, "name": "💰 Oltin qanotlar",
             "desc": "Kunlik bonus miqdori oshadi.", "base": 15, "cap": 110},
            {"key": "revive_once", "unlock": 13, "name": "🔥 O'limni yengish",
             "desc": "ENG NODIR QOBILIYAT — o'yin davomida BIR MARTA, hech qanday himoya ishlamay qolsa ham, kafolatlangan tirik qolasiz."},
        ],
    },
}


def hero_image_path(hero_key):
    """Geroyning o'ziga xos rasmi — skript bilan bir papkada joylashgan bo'lishi kerak
    (masalan hero_draven.jpg). Fayl topilmasa None qaytaradi (chaqiruvchi shunda
    rasmsiz, faqat matn bilan davom etadi)."""
    rel = HEROES.get(hero_key, {}).get("image")
    if not rel:
        return None
    path = os.path.join(ASSETS_DIR, rel)
    return path if os.path.exists(path) else None


HERO_LEVEL_UP_COSTS = [int(40 + (220 - 40) * i / 13) for i in range(14)]  # 1→2 ... 14→15 (14 ta narx)
HERO_MAX_LEVEL = 15


def roll_hero():
    if random.random() < 0.0005:  # 0.05%
        return "burgut"
    others = [k for k in HEROES if k != "burgut"]
    return random.choice(others)


def get_hero(uid):
    with db_lock:
        cur.execute("SELECT hero_key, level, acquired_at FROM heroes WHERE user_id=?", (uid,))
        row = cur.fetchone()
    if not row:
        return None
    key, level, acquired_at = row
    data = HEROES.get(key, {})
    days_active = int((time.time() - (acquired_at or time.time())) // 86400)
    return {"key": key, "level": level, "acquired_at": acquired_at, "days_active": days_active,
            "name": data.get("name"), "image": data.get("image"), "abilities": data.get("abilities", [])}


def hero_level_up_cost(current_level):
    if current_level < 1 or current_level >= HERO_MAX_LEVEL:
        return None
    return HERO_LEVEL_UP_COSTS[current_level - 1]


def _ability_power(level, unlock, base, cap):
    """`unlock` darajada `base`dan boshlanib, 15-lvlda `cap`gacha chiziqli o'sadigan,
    chegaralangan (chit bo'lib qolmaydigan) kuch qiymati. `unlock`dan past level uchun 0."""
    if level < unlock:
        return 0.0
    if unlock >= HERO_MAX_LEVEL:
        return base
    t = (level - unlock) / (HERO_MAX_LEVEL - unlock)
    return base + (cap - base) * t


def hero_unlocked_abilities(uid):
    """Foydalanuvchining geroyi va uning HOZIRGI darajasida ochilgan qobiliyatlari
    ro'yxatini (hisoblangan qiymati bilan) qaytaradi. Har biri: {key,name,desc,value,unlocked}."""
    hero = get_hero(uid)
    if not hero:
        return []
    result = []
    for ab in hero["abilities"]:
        unlocked = hero["level"] >= ab["unlock"]
        value = None
        if unlocked and "base" in ab:
            value = _ability_power(hero["level"], ab["unlock"], ab["base"], ab["cap"])
        result.append({**ab, "unlocked": unlocked, "value": value})
    return result


def hero_ability_value(uid, ability_key):
    """Berilgan turdagi (masalan 'survive', 'duel_bonus') qobiliyat qiymatini qaytaradi
    (0 — agar geroy yo'q, ochilmagan yoki bu turdagi qobiliyat yo'q bo'lsa)."""
    for ab in hero_unlocked_abilities(uid):
        if ab["key"] == ability_key and ab["unlocked"]:
            return ab["value"] or 0.0
    return 0.0


def hero_has_ability(uid, ability_key):
    """Binary (bor/yo'q) qobiliyatlar uchun — masalan 'compass_free', 'revive_once'."""
    for ab in hero_unlocked_abilities(uid):
        if ab["key"] == ability_key and ab["unlocked"]:
            return True
    return False


def hero_survive_chance(uid):
    return hero_ability_value(uid, "survive")


def hero_duel_bonus(uid):
    return hero_ability_value(uid, "duel_bonus")


def hero_bonus_extra_dollar(uid):
    return int(hero_ability_value(uid, "bonus_dollar"))


def hero_has_free_compass(uid):
    return hero_has_ability(uid, "compass_free")


def hero_luck_boost(uid):
    return hero_ability_value(uid, "luck_boost")


def hero_duel_draw_chance(uid):
    return hero_ability_value(uid, "duel_draw_chance")


def hero_vote_weight_bonus(uid):
    return 1 if hero_has_ability(uid, "vote_weight") else 0


SHOP_COIN = {
    "toj":         {"name": "👑 Hukmdor toj", "price": 15, "currency": "coin", "mode": "expiry", "charge_key": "toj_until",
                    "duration_seconds": 15 * 86400,
                    "desc": "15 kunga hukmdor maqomi belgisi (profilda ko'rinadi)."},
    "rol_tanlash": {"name": "🎭 Rol tanlash huquqi", "price": 20, "currency": "coin", "mode": "charge", "charge_key": "role_choice",
                    "charge_amount": 5,
                    "desc": "/rolni_tanla <rol> orqali keyingi 5 ta o'yinda xohlagan rolni tanlaysiz."},
    "klan":        {"name": "🏛 Klan litsenziyasi", "price": 25, "currency": "coin", "mode": "charge", "charge_key": "klan_license",
                    "charge_amount": 1,
                    "desc": "/klan <nomi> orqali o'z klaningizni ochish huquqini beradi (bir martalik — 1 klan ochishga yetadi)."},
    "shadow":      {"name": "👤 Yashirin status", "price": 30, "currency": "coin", "mode": "expiry", "charge_key": "shadow_until",
                    "duration_seconds": 20 * 86400,
                    "desc": "20 kun davomida /top reytingida ismingiz ko'rinmaydi."},
    "nishon":      {"name": "🗡 Qotil nishoni", "price": 60, "currency": "coin", "mode": "charge", "charge_key": "duel_guaranteed_win",
                    "charge_amount": 5,
                    "desc": "Keyingi 5 ta duelingizda 100% g'alaba kafolatlaydi."},
    "koz":         {"name": "👁 Kuzatish ko'zi", "price": 55, "currency": "coin", "mode": "charge", "charge_key": "watch_eyes",
                    "charge_amount": 5,
                    "desc": "Kunduzi kim kimga ovoz berganini to'liq DM orqali ko'rasiz (5 marta)."},
    "duel_qalqon": {"name": "🛡 Duel qalqoni", "price": 150, "currency": "coin", "mode": "charge", "charge_key": "duel_guaranteed_win",
                    "charge_amount": 10,
                    "desc": "Keyingi 10 ta duelingizda 100% g'alaba kafolatlaydi."},
    "bank":        {"name": "🏦 Bank foizi x2", "price": 90, "currency": "coin", "mode": "multiplier",
                    "charge_key": "bonus_mult", "mult_value": 2, "desc": "Kunlik bonusingizni 2 barobar qiladi."},
    "admin":       {"name": "⚡️ 1 kunlik admin", "price": 120, "currency": "coin", "mode": "expiry",
                    "charge_key": "temp_admin_until", "duration_seconds": 86400, "desc": "24 soat davomida /NewGame, /StartGame va h.k. buyruqlarni bera olasiz."},
    "qirol":       {"name": "🐉 Qirol unvoni", "price": 200, "currency": "coin", "mode": "expiry", "charge_key": "qirol_until",
                    "duration_seconds": 10 * 86400,
                    "desc": "10 kun davomida eng oliy maqom — /top reytingida eng tepada chiqasiz."},
    "vip_coin":    {"name": "🎯 Snayper puxta nishonchi", "price": 180, "currency": "coin", "mode": "charge", "charge_key": "golden_bullet",
                    "charge_amount": 2,
                    "desc": "2 marta — mafiya hujumi himoyalarni (shield/doktor/qorovul) chetlab o'tadi."},
}

SHOP_OSH = {
    "toy":       {"name": "💍 To'y Oshi", "price": 5000, "currency": "dollar", "gift_shield": 2, "gift_charge": ("revive", 1)},
    "choyxona":  {"name": "🍵 Choyxona Oshi", "price": 4500, "currency": "dollar", "gift_shield": 2, "gift_charge": ("night_vision", 1)},
    "tandir":    {"name": "🔥 Tandir Oshi", "price": 4000, "currency": "dollar", "gift_shield": 1, "gift_charge": ("gps", 1)},
    "samarqand": {"name": "🇺🇿 Samarqand Oshi", "price": 3800, "currency": "dollar", "gift_shield": 1, "gift_charge": ("compass", 1)},
    "buxoro":    {"name": "🏛 Buxorocha Sofi Oshi", "price": 3600, "currency": "dollar", "gift_shield": 1, "gift_charge": ("confuse", 1)},
    "fargona":   {"name": "🏔 Farg'ona Devzira Oshi", "price": 3500, "currency": "dollar", "gift_shield": 1, "gift_charge": ("fake_doc", 1)},
    "qora":      {"name": "🥷 Qora Mafia Oshi", "price": 3000, "currency": "dollar", "gift_shield": 1, "gift_charge": None},
}

SHOP_CATEGORIES = {
    "dollar": ("💵 Dollar Do'koni", SHOP_DOLLAR),
    "diamond": ("💎 Olmos Do'koni", SHOP_DIAMOND),
    "coin": ("🪙 Hunter Coin Do'koni", SHOP_COIN),
}

# 📦 Inventar tugmalarida ishlatish uchun: buyum nomidan uning do'kon kalitiga
# ("himoya", "kozoynak" va h.k.) qaytadan yo'l topish uchun lug'at.
ITEM_NAME_TO_SHOPKEY = {}
for _cat, (_title, _items) in SHOP_CATEGORIES.items():
    for _key, _item in _items.items():
        ITEM_NAME_TO_SHOPKEY[_item["name"]] = (_cat, _key)


# ================================================================================
#  HAR GURUH UCHUN ALOHIDA O'YIN HOLATI
# ================================================================================

GAMES = {}
GAME_LOCK = threading.RLock()
PENDING_PROPOSALS = {}

# 📋 Guruhga kirish uchun a'zolik so'rovlari (zayavkalar) navbati.
# Faqat guruh havolasi "Admin tasdig'i" (request to join) rejimida bo'lsa ishlaydi.
# {chat_id: [ {"user_id":, "name":, "username":, "ts":}, ... ]}
PENDING_JOIN_REQUESTS = {}
JOIN_REQ_LOCK = threading.RLock()

# ================================================================================
#  🏆 MUSOBAQALAR (TURNIRLAR) — Hunter Mafia o'yinidan MUSTAQIL, alohida rejim.
#  Guruh egasi/admin o'yinchilarni yig'ib, ular orasidan ikkitasini tanlab
#  1v1 "Turnir Jangi" (duel'dan farqli — bracket asosida, elimination) o'tkazadi,
#  oxirida bitta chempion qoladi va katta mukofot oladi.
# ================================================================================

TOURNAMENTS = {}     # chat_id -> {"name","status","participants":{uid:name},"eliminated":[],"matches":[],"host_id"}
TOURNAMENT_PICK = {}  # host_id -> {"chat_id":.., "a": uid_or_None}  (jang uchun 2 kishini ketma-ket tanlash holati)


# ================================================================================
#  🔄 BOT TIKLASH (RESTORE/RESTART) TIZIMI
# ================================================================================
#  Bot har qanday sababdan (xatolik, deploy, host qayta ishga tushirishi yoki
#  /tiklash buyrug'i) to'xtab qolsa ham, aktiv o'yinlar GAMES xotiradan yo'qolib
#  ketmasin deb, muhim bosqich (checkpoint) larda holat diskka (STATE_PATH) JSON
#  ko'rinishida yoziladi. Bot qayta ishga tushganda, shu fayldan o'qib, o'yinlarni
#  qayta tiklaydi va qolgan vaqtni hisoblab tegishli taymerlarni qayta ishga
#  tushiradi — guruh a'zolari uchun o'yin deyarli uzilishsiz davom etadi.

STATE_LOCK = threading.RLock()

# game{} ichidagi qaysi maydonlar `set()` ekanini bilib, JSON'ga list, qaytishda
# yana set() qilib tiklaymiz (JSON o'z-o'zidan set turini bilmaydi).
_STATE_SET_FIELDS = {"last_words_wait", "poison_marks", "night_protected", "snayper_used",
                     "prompted_tonight", "responded_tonight", "touched_tonight",
                     "hero_revive_used", "hero_vote_shield_used", "hero_role_reveal_used",
                     "hero_armed_defense", "hero_armed_vote_shield", "hero_income_claimed"}
# qaysi maydonlar {int_uid: ...} ko'rinishidagi lug'at ekanini bilib, JSON kalitlarini
# (JSON'da har doim string bo'ladi) qaytadan int'ga o'giramiz.
_STATE_INT_KEYED_FIELDS = {"players", "mafia_votes", "votes", "forced_day_votes", "secret_missions",
                           "forced_roles", "afk_streak", "squads"}


def _game_to_jsonable(game):
    """Bitta o'yin holatini (GAMES[chat_id]) JSON'ga yozsa bo'ladigan lug'atga aylantiradi."""
    data = {}
    for key, value in game.items():
        if key == "timers":
            continue  # threading.Timer obyektlari saqlanmaydi — tiklashda yangisi yaratiladi
        if key in _STATE_SET_FIELDS:
            data[key] = list(value)
        elif key == "confirm_vote":
            if value:
                data[key] = {
                    "target": value["target"],
                    "yes": list(value["yes"]),
                    "no": list(value["no"]),
                    "message_id": value.get("message_id"),
                }
            else:
                data[key] = None
        elif key in _STATE_INT_KEYED_FIELDS and isinstance(value, dict):
            data[key] = {str(k): v for k, v in value.items()}
        else:
            data[key] = value
    return data


def _game_from_jsonable(data):
    """_game_to_jsonable() natijasini yana ishlaydigan GAMES[chat_id] lug'atiga qaytaradi."""
    game = dict(data)
    game["timers"] = []
    for key in _STATE_SET_FIELDS:
        if key in game and game[key] is not None:
            game[key] = set(game[key])
    if game.get("confirm_vote"):
        cv = game["confirm_vote"]
        game["confirm_vote"] = {
            "target": cv["target"],
            "yes": set(cv["yes"]),
            "no": set(cv["no"]),
            "message_id": cv.get("message_id"),
        }
    for key in _STATE_INT_KEYED_FIELDS:
        if key in game and isinstance(game[key], dict):
            game[key] = {int(k): v for k, v in game[key].items()}
    return game


def save_games_state():
    """Barcha aktiv o'yinlarning holatini STATE_PATH fayliga yozadi. Muhim bosqich
    o'zgarishlarida (tun/kun boshlanishi, ovoz berish ochilishi, o'yin tugashi va h.k.)
    chaqiriladi. Xatolik yuz bersa ham o'yin davom etaveradi — bu faqat 'sug'urta'."""
    try:
        with GAME_LOCK, STATE_LOCK:
            snapshot = {
                "saved_at": time.time(),
                "games": {str(chat_id): _game_to_jsonable(g) for chat_id, g in GAMES.items()},
            }
            tmp_path = STATE_PATH + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, ensure_ascii=False)
            os.replace(tmp_path, STATE_PATH)
    except Exception:
        logging.exception("⚠️ O'yinlar holatini saqlashda xatolik yuz berdi.")


def _resume_game_timer(chat_id, game):
    """Saqlangan 'phase_deadline'ga asoslanib navbatdagi bosqich uchun yangi
    threading.Timer o'rnatadi (qolgan vaqtni hisoblab). Agar vaqt allaqachon
    tugagan bo'lsa ham, bot to'liq ishga tushib ulgurishi uchun kamida bir necha
    soniya kutib, keyin yakunlaydi."""
    phase = game.get("phase")
    deadline = game.get("phase_deadline")
    sub_phase = game.get("day_sub_phase")

    resolver = None
    if game.get("confirm_vote"):
        resolver = lambda: resolve_hang_confirmation(chat_id)
    elif phase == "night":
        resolver = lambda: resolve_night(chat_id)
    elif phase == "day":
        if sub_phase == "voting":
            resolver = lambda: resolve_day(chat_id)
        elif sub_phase == "discussion":
            resolver = lambda: open_day_voting(chat_id)

    if resolver is None or deadline is None:
        return

    remaining = deadline - time.time()
    delay = max(remaining, 5)  # bot to'liq ishga tushib ulgursin deb kamida 5 soniya
    t = threading.Timer(delay, resolver)
    t.daemon = True
    t.start()
    game["timers"].append(t)


def load_games_state():
    """Bot ishga tushganda (yoki /tiklash orqali qayta ishga tushgandan keyin)
    chaqiriladi. Agar oldingi ishga tushishda saqlangan aktiv o'yinlar bo'lsa,
    ularni GAMES ichiga tiklaydi, faz-taymerlarini qayta o'rnatadi va guruhlarga
    'bot tiklandi' xabarini yuboradi."""
    if not os.path.exists(STATE_PATH):
        return

    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            snapshot = json.load(f)
    except Exception:
        logging.exception("⚠️ Saqlangan o'yin holatini o'qib bo'lmadi, tiklash o'tkazib yuborildi.")
        return

    games_data = snapshot.get("games") or {}
    if not games_data:
        return

    restored = 0
    for chat_id_s, gdata in games_data.items():
        try:
            chat_id = int(chat_id_s)
            game = _game_from_jsonable(gdata)
            GAMES[chat_id] = game
            restored += 1
            if game.get("phase") in ("night", "day"):
                _resume_game_timer(chat_id, game)
                try:
                    bot.send_message(
                        chat_id,
                        "🔄 <b>Bot muvaffaqiyatli qayta ishga tushdi!</b>\n"
                        "Sizning o'yiningiz avtomatik tiklandi — davom etaveramiz. 🎮",
                    )
                except Exception:
                    pass
        except Exception:
            logging.exception(f"⚠️ {chat_id_s} guruhi uchun o'yinni tiklashda xatolik yuz berdi.")

    logging.info(f"🔄 Bot tiklandi: {restored} ta aktiv o'yin holati qayta yuklandi.")

    # tiklab bo'lgach eski faylni tozalaymiz — keyingi checkpointlarda qaytadan yoziladi
    try:
        os.remove(STATE_PATH)
    except Exception:
        pass


def _graceful_shutdown_save(*_args):
    """Host (Railway/systemd/Docker va h.k.) botni SIGTERM/SIGINT bilan to'xtatganda
    ham oxirgi lahzadagi o'yin holati yo'qolib ketmasligi uchun signal handler."""
    save_games_state()
    sys.exit(0)


try:
    signal.signal(signal.SIGTERM, _graceful_shutdown_save)
    signal.signal(signal.SIGINT, _graceful_shutdown_save)
except (ValueError, AttributeError):
    # ba'zi platformalarda (masalan asosiy bo'lmagan thread) signal o'rnatib bo'lmaydi — muammo emas
    pass


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
        # --- qo'shimcha 25 rol uchun holat ---
        "extra_actions": {},
        "night_protected": set(),
        "advocate_protect": None,
        "forced_day_votes": {},
        "judge_double_vote": None,
        "snayper_used": set(),
        # --- kunduzgi tasdiqlash ovoz berishi (👍/👎) ---
        "confirm_vote": None,
        # --- 🏆 geroylarning bir martalik qobiliyatlari uchun (o'yin davomida 1 marta) ---
        "hero_revive_used": set(),
        "hero_vote_shield_used": set(),
        "hero_role_reveal_used": set(),
        # --- 🔄 bot tiklash (restart/restore) tizimi uchun checkpoint maydonlari ---
        "phase_deadline": None,   # joriy bosqich qachon tugashi kerak (Unix vaqt)
        "day_sub_phase": None,    # "discussion" yoki "voting" — faqat phase == "day" uchun
        # --- 😴 AFK (harakatsizlik) nazorati ---
        "prompted_tonight": set(),
        "responded_tonight": set(),
        "afk_streak": {},
        # --- 🕵️ tunda kimga qanday harakat qilinganini kuzatish (natija DM'lari uchun) ---
        "touched_tonight": set(),
        # --- 🐺🦅 Jamoaviy o'yin rejimi (/teamgame) va 💍 Para o'yin rejimi (/parateam) ---
        "squad_mode": False,
        "couple_mode": False,
        "squads": {},  # uid -> "wolf" | "eagle"
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


def notify_target_touched(game, target_uid):
    """🌙 Har qanday rol tunda kimnidir nishonga olsa, o'sha kishiga (kim ekani
    oshkor qilinmasdan) umumiy ogohlantiruvchi xabar yuboriladi — bir kechada
    bir kishiga faqat bitta marta (bir nechta rol bir xil odamni tanlasa ham)."""
    if target_uid in (None, "skip", "yes", "no") or target_uid not in game["players"]:
        return
    touched = game.setdefault("touched_tonight", set())
    if target_uid in touched:
        return
    touched.add(target_uid)
    safe_send(target_uid, "🌙 <i>Kimdir tunda sizga qiziqib, harakatingizni yashirincha kuzatdi...</i>")


def send_scene_photo(chat_id, local_path, url_fallback, caption, reply_markup=None):
    """Mahalliy 'assets' papkasidagi surat bo'lsa o'shani, bo'lmasa zaxira URL'ni yuboradi."""
    try:
        if os.path.isfile(local_path):
            with open(local_path, "rb") as f:
                bot.send_photo(chat_id, f, caption=caption, reply_markup=reply_markup)
                return
    except Exception:
        pass
    try:
        bot.send_photo(chat_id, url_fallback, caption=caption, reply_markup=reply_markup)
    except Exception:
        bot.send_message(chat_id, caption, reply_markup=reply_markup)


def mention(uid, name):
    """Guruh xabarlarida o'yinchi ismini bosilganda uning profiliga o'tadigan qilib ko'rsatish uchun.
    🖼 Agar o'yinchida faol Mifik ramka bo'lsa, uning ismi HAMMA ko'radigan joyda
    (o'yin e'lonlari, reytinglar, o'lim xabarlari va h.k.) maxsus ramka bilan ko'rinadi."""
    safe_name = (name or "O'yinchi").replace("<", "").replace(">", "")
    try:
        ch = get_charges(uid)
        # 👑 HUNTER ELITE a'zosi bo'lsa va shaxsiy laqab (taxallus) o'rnatgan bo'lsa —
        # hamma joyda (o'yin e'lonlari, reytinglar, o'lim xabarlari) o'sha laqab bilan ko'rinadi.
        elite_until = ch.get("vip_until", 0)
        if elite_until and elite_until > time.time():
            nick = (ch.get("nickname") or "").strip()
            if nick:
                safe_name = nick.replace("<", "").replace(">", "")
            safe_name = f"👑 {safe_name}"
        ramka_until = ch.get("ramka_until", 0)
        if ramka_until and ramka_until > time.time():
            safe_name = f"🖼✨ {safe_name} ✨🖼"
    except Exception:
        pass
    return f'<a href="tg://user?id={uid}">{safe_name}</a>'


# ================================================================================
#  🌟 MAXSUS (PREMIUM) EMOJILAR — HTML <tg-emoji emoji-id="..."> yordamida yuborish
#  ================================================================================
#  ⚠️ SHART: bu funksiyalar ishlashi uchun BOTNI YARATGAN shaxsning (ya'ni sizning
#  shaxsiy Telegram akkountingiz — botni @BotFather orqali ro'yxatdan o'tkazgan
#  akkount) da FAOL Telegram Premium obunasi bo'lishi kerak. Bu shart 2026-yil
#  9-fevraldan beri Bot API'ning rasmiy qoidasi (Fragment orqali qimmat username
#  sotib olish ENDI shart emas — Premium kifoya). Agar Premium bo'lmasa, Telegram
#  entity'ni e'tiborsiz qoldiradi va faqat oddiy "fallback" emoji ko'rinadi (xato
#  chiqmaydi, shunchaki maxsus emoji ko'rinmaydi).
#
#  📌 O'ZINGIZNING EMOJI ID'LARINGIZNI TOPISH:
#  1) Botni ishga tushiring.
#  2) Botning shaxsiy chatida (DM), o'zingiz yaratgan to'plamdagi (HunterMafiaPack)
#     istalgan maxsus emojini yuboring (oddiy xabar sifatida, klaviaturadan tanlab).
#  3) Bot avtomatik o'sha emojining "custom_emoji_id" raqamini sizga javob qilib
#     yuboradi (pastdagi `collect_custom_emoji_ids` funksiyasi orqali).
#  4) Shu ID'larni PREMIUM_EMOJI lug'atiga joylashtiring va istalgan xabarda
#     `premium_emoji(key)` yoki `render_premium_text(...)` orqali ishlating.
# ================================================================================

# 🗂 ID'larni shu yerga joylashtiring — masalan: "fire": "5379748062124056162"
# (Har bir qiymat — collect_custom_emoji_ids orqali botga yuborilgandan keyin olingan ID)
PREMIUM_EMOJI = {
    "ring": "5228727030492738251",          # 💍
    "sword": "5229187373677451945",         # ⚔️
    "question": "5228799898907876726",      # ❓
    "money": "5229014153351443614",         # 💰
    "diamond": "5228894821980087473",       # 💎
    "moon": "5228923817304306302",          # 🌙
    "sun": "5228719290961670553",           # ☀️
    "shield": "5228922863821564668",        # 🛡️
    "plus": "5231359149660478554",          # ➕
    "scroll": "5228891871337554041",        # 📜
    "bandage": "5228903618073114276",       # 🩹
    "love_letter": "5228856768569844597",   # 💌
    "briefcase": "5228848397678586256",     # 💼
    "mask": "5231303735992425075",          # 🎭
    "potion": "5228960741138141726",        # ⚗️
    "radar": "5228772393937317770",         # 📡
    "compass": "5229157918791739430",       # 🧭
    "vip_card": "5231146733462919805",      # 💳
    "fox": "5228800723541597880",           # 🦊
    "box": "5231026641882356456",           # 📦
    "dice": "5229098343300378907",          # 🎲
    "crystal_ball": "5228845996791868859",  # 🔮
    "archive": "5228956141228172000",       # 🗃️
    "ring_2": "5229144226435997413",        # 💍
    "signal": "5229167771446719759",        # 📶
    "crown": "5230938646592395061",         # 👑
    "frame": "5229048143722618619",         # 🖼️
    "vase": "5231481483213971535",          # 🏺
    "vase_2": "5231272129328093395",        # 🏺
    "fox_2": "5229173436508582890",         # 🦊
    "top_hat": "5231412377190177912",       # 🎩
    "medal": "5228773948715473417",         # 🎖️
    "mother_daughter": "5231291551170207761",  # 👩‍👧
    "gun": "5229058065097075989",           # 🔫
    "dagger": "5229063068733976438",        # 🗡️
    "axe": "5230968002693866223",           # 🪓
    "police": "5228998876152771465",        # 👮
    "scale": "5231254489897409072",         # ⚖️
    "rose": "5231093682026879373",          # 🌹
    "bomb": "5228795333357646088",          # 💣
    "bow": "5228683836006640638",           # 🏹
    "helmet": "5231163183187664108",        # 🪖
    "salute": "5228984067105533985",        # 🫡
    "gun_2": "5229239488810626417",         # 🔫
    "ninja": "5228777788416238250",         # 🥷
    "wizard": "5228948625035403012",        # 🧙
    "book": "5231404238227153516",          # 📖
    "ghost": "5231343726432918883",         # 👻
    "scale_2": "5228804760810861333",       # ⚖️
    "angry": "5231491868444889568",         # 😡
    "medal_2": "5231334208785389927",       # 🎖️
    "detective": "5228742543914609211",     # 🕵️
    "wizard_man": "5229099369797559818",    # 🧙‍♂️
    "ruler": "5228749763754637223",         # 📐
    "crazy": "5231447076230963307",         # 🤪
    "shield_2": "5228881885538593285",      # 🛡️
    "crazy_2": "5231153455086738225",       # 🤪
    "rocket": "5229061780243787527",        # 🚀
    "mask_2": "5228833515616904819",        # 🎭
    "person": "5229067325046567300",        # 👤
    "shop": "5229138862021849198",          # 🏪
    "coin": "5229115566119235957",          # 🪙
    "chart": "5228728198723838647",         # 📈
    "pillar": "5229232204546095451",        # 🏛️
    "toolbox": "5228918689113350715",       # 🧰
    "trophy": "5231216024170306098",        # 🏆
    "gift": "5229169845915922937",          # 🎁
}


def premium_emoji(key, fallback="⭐️"):
    """PREMIUM_EMOJI lug'atidan shu kalit uchun tayyor HTML <tg-emoji> tegini qaytaradi.
    ID hali kiritilmagan bo'lsa, shunchaki oddiy fallback emojini qaytaradi (xato bermaydi)."""
    emoji_id = PREMIUM_EMOJI.get(key)
    if not emoji_id:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


def render_premium_text(template, **emoji_keys):
    """Shablon matn ichidagi {key} joylarini mos PREMIUM_EMOJI bilan almashtiradi.
    Masalan: render_premium_text("G'alaba {fire}!", fire=("fire", "🔥"))
    bu yerda qiymat (kalit, fallback) juftligi."""
    values = {name: premium_emoji(key, fallback) for name, (key, fallback) in emoji_keys.items()}
    return template.format(**values)


def send_premium_message(chat_id, text_with_tags, reply_markup=None):
    """<tg-emoji> teglari bo'lgan HTML matnni yuboradi. Agar biror sababdan xato
    chiqsa (masalan juda eski bot kutubxonasi versiyasi), oddiy xabar sifatida
    (teglarsiz, faqat fallback emojilar bilan) qayta yuborishga urinadi."""
    try:
        return bot.send_message(chat_id, text_with_tags, reply_markup=reply_markup)
    except Exception as e:
        _logger.warning("Premium emoji xabari yuborilmadi, oddiy matn bilan urinilmoqda: %s", e)
        import re as _re
        plain = _re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', text_with_tags)
        return bot.send_message(chat_id, plain, reply_markup=reply_markup)


def _extract_custom_emoji_entities(message):
    """Xabardagi barcha custom_emoji turidagi entity'larni (ID + fallback emoji matni
    bilan birga) ro'yxat qilib qaytaradi."""
    result = []
    entities = (message.entities or []) + (message.caption_entities or [])
    text = message.text or message.caption or ""
    # Telegram offset/length UTF-16 birliklarida hisoblanadi — Python uchun to'g'ri kesish
    utf16 = text.encode("utf-16-le")
    for ent in entities:
        if ent.type == "custom_emoji":
            try:
                piece = utf16[ent.offset * 2: (ent.offset + ent.length) * 2].decode("utf-16-le")
            except Exception:
                piece = ""
            result.append((ent.custom_emoji_id, piece))
    return result


@bot.message_handler(
    func=lambda m: m.chat.type == "private" and _extract_custom_emoji_entities(m),
    content_types=["text"],
)
def collect_custom_emoji_ids(message):
    """🆔 YORDAMCHI: bot egasi shaxsiy chatda o'zi yaratgan maxsus emojilarni yuborsa,
    bot ularning HAR BIRINING custom_emoji_id raqamini konsolga (log) VA chatga
    darhol qaytarib beradi. Bu orqali PREMIUM_EMOJI lug'atini to'ldirish oson bo'ladi."""
    if not is_owner(message.from_user.id):
        return
    found = _extract_custom_emoji_entities(message)
    if not found:
        return
    lines = ["🆔 <b>Topilgan maxsus emoji ID'lari:</b>\n"]
    for emoji_id, fallback in found:
        line = f"{fallback}  →  <code>{emoji_id}</code>"
        lines.append(line)
        _logger.info("Custom emoji topildi: fallback=%s id=%s", fallback, emoji_id)
        print(f"[PREMIUM EMOJI] fallback={fallback!r}  custom_emoji_id={emoji_id}")
    lines.append("\n📋 Shu ID'larni <code>PREMIUM_EMOJI</code> lug'atiga qo'shing, masalan:\n"
                  f'<code>"nomi": "{found[0][0]}"</code>')
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["emoji_test"])
def cmd_emoji_test(message):
    """🧪 Sinov buyrug'i — PREMIUM_EMOJI lug'atidagi barcha emojilarni bitta xabarda
    ko'rsatadi (faqat bot egasi uchun), shu orqali ID to'g'ri kiritilganini tekshirish mumkin."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    if not PREMIUM_EMOJI:
        bot.send_message(
            message.chat.id,
            "⚠️ PREMIUM_EMOJI lug'ati hali bo'sh.\n\n"
            "1) Shaxsiy chatda (bot bilan DM) o'zingiz yaratgan maxsus emojini yuboring.\n"
            "2) Bot sizga uning ID raqamini qaytaradi.\n"
            "3) Shu ID'ni kod ichidagi PREMIUM_EMOJI lug'atiga qo'shing va botni qayta ishga tushiring.",
        )
        return
    parts = [f"{key}: {premium_emoji(key)}" for key in PREMIUM_EMOJI]
    send_premium_message(message.chat.id, "🌟 <b>Premium emoji sinovi:</b>\n\n" + "\n".join(parts))


ITEM_ANNOUNCE_FLAVORS = {
    "🧪 Zaharli flakon": "🧪 <i>Tunning zulmatida kimdir zaharli flakonni ishlatdi... kimningdir tanasida zahar yura boshladi!</i>",
    "📍 GPS Mayak": "📍 <i>Kimdir yashirin GPS mayagini faollashtirdi va kimningdir joylashuvini kuzatmoqda...</i>",
    "🧭 Sirli kompas": "🧭 <i>Kimdir sirli kompasni ishlatib, kimningdir haqiqiy tarafini bilib oldi...</i>",
    "💣 Tutunli bomba": "💣 <i>Guruh ichida kutilmaganda tutun bombasi portladi — kimdir bugun linchdan qochib qutulmoqchi!</i>",
    "🔦 Katta Fonar": "🔦 <i>Kimdir Katta Fonarni yoqib, birovning haqiqiy qiyofasini yorug'likka chiqardi...</i>",
    "📡 Maxfiy radar": "📡 <i>Kimdir maxfiy radar yordamida o'z rolini boshqasiga almashtirdi...</i>",
}


def announce_item_use(chat_id, user_id, item_label, target_id=None, effect_text=""):
    """🎒 Do'kondan olingan buyum o'yin ichida ishlatilganda guruhga — KIM ekani oshkor
    qilinmasdan (anonim), lekin QAYSI buyum ishlaganini aniq bildiruvchi tarzda e'lon
    qilinadi. Ishlatgan kishiga natija haqidagi DM chaqiruvchi joyda alohida yuboriladi,
    shu funksiya faqat guruh e'loni va (ixtiyoriy) qo'shimcha DM uchun."""
    flavor = ITEM_ANNOUNCE_FLAVORS.get(item_label, f"🎒 <i>Kimdir do'kondan olingan buyumini ishlatdi:</i> <b>{item_label}</b>")
    try:
        bot.send_message(chat_id, flavor)
    except Exception:
        pass
    if target_id is not None:
        # ba'zi chaqiruvchilar uchun qo'shimcha DM kerak bo'lishi mumkin — ixtiyoriy
        target_name = user_dict(target_id).get("name", "O'yinchi")
        extra = f"\n🎯 Qo'llanildi: {mention(target_id, target_name)}"
        if effect_text:
            extra += f"\n{effect_text}"
        safe_send(user_id, extra)


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
    kb.add(types.InlineKeyboardButton("💎 Almaz sotib olish", callback_data="menu|birja"))
    kb.add(
        types.InlineKeyboardButton("👑 HUNTER ELITE", callback_data="menu|elite"),
        types.InlineKeyboardButton("🌐 Til / Language", callback_data="menu|lang"),
    )
    kb.add(
        types.InlineKeyboardButton("💵 Dollar do'koni", callback_data="menu|dollarshop"),
        types.InlineKeyboardButton("💎➜🪙 Olmos ayirboshlash", callback_data="menu|d2c"),
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
        types.InlineKeyboardButton("🏆 Geroyim", callback_data="menu|hero"),
        types.InlineKeyboardButton("🏅 Ball reytingi", callback_data="menu|points_top"),
    )
    kb.add(
        types.InlineKeyboardButton("🛒 Qora Bozor", callback_data="menu|market_info"),
        types.InlineKeyboardButton("🏆 Top Reyting", callback_data="menu|top"),
    )
    kb.add(types.InlineKeyboardButton("🎁 Kunlik bonus", callback_data="menu|bonus"))
    kb.add(
        types.InlineKeyboardButton("💍 Nikoh haqida", callback_data="menu|nikoh_info"),
        types.InlineKeyboardButton("⚔️ Duel haqida", callback_data="menu|duel_info"),
    )
    kb.add(types.InlineKeyboardButton("❓ Yordam / Buyruqlar", callback_data="menu|help"))
    kb.add(types.InlineKeyboardButton("🧭 Qanday o'ynash kerak? (Boshlang'ich)", callback_data="menu|guide"))
    if is_owner(user_id):
        kb.add(types.InlineKeyboardButton("⚙️ Sozlamalar (Admin)", callback_data="admin|panel"))
    return kb


@bot.callback_query_handler(func=lambda c: c.data == "menu|guide")
def cb_menu_guide(call):
    """🧭 Chalkash tuyulgan yangi foydalanuvchilar uchun — bot qanday
    ishlashini 5 ta oddiy qadamda tushuntiruvchi qisqa yo'l-yo'riq.
    Botning to'liq imkoniyatlari (klan, jamoaviy o'yin, ELITE va h.k.)
    o'zgarishsiz qoladi — bu faqat yangi boshlovchiga mo'ljallangan qisqacha
    xarita, murakkab qismlarni O'CHIRMAYDI."""
    try:
        maybe_capture_owner(call.from_user)
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "🧭 <b>Botdan foydalanish — 5 ta oddiy qadam</b>\n\n"
            "1️⃣ Botni guruhingizga <b>admin</b> qilib qo'shing.\n"
            "2️⃣ Guruhda <code>/newgame</code> deb yozing — o'yin ro'yxati ochiladi.\n"
            "3️⃣ \"🎮 O'yinga qo'shilish\" tugmasini bosing.\n"
            "4️⃣ Yetarli o'yinchi yig'ilgach, o'yin o'zi boshlanadi — sizga shaxsiy "
            "chatda <b>rolingiz</b> keladi.\n"
            "5️⃣ Tun/kunduz navbat bilan davom etadi — bot har safar nima qilish "
            "kerakligini o'zi aytib turadi.\n\n"
            "💡 <i>Boshqa hamma narsa (klan, ELITE, jamoaviy o'yin, do'kon) — "
            "ixtiyoriy qo'shimchalar. Ularsiz ham oddiy o'yinni bemalol o'ynay olasiz!</i>\n\n"
            "❓ Savol bo'lsa — <code>/help</code> orqali to'liq buyruqlar ro'yxatini ko'ring.",
        )
    except Exception as e:
        _logger.warning("cb_menu_guide xatolik: %s", e)


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

    # 🎮 guruhdagi "O'yinga qo'shilish" tugmasi orqali kelingan bo'lsa (deep-link:
    # https://t.me/BOT?start=join_<chat_id>) — shu yerda avtomatik o'yinga qo'shamiz
    parts = message.text.split(maxsplit=1)
    payload = parts[1].strip() if len(parts) > 1 else ""
    if payload.startswith("join_"):
        try:
            join_chat_id = int(payload[len("join_"):])
        except ValueError:
            join_chat_id = None

        if join_chat_id is not None:
            status = do_join(join_chat_id, message.from_user)
            game = GAMES.get(join_chat_id)
            group_title = (game.get("chat_title") if game else None) or "guruh"
            group_link = game.get("group_link") if game else None
            kb = None
            if group_link:
                kb = types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton(f"🔙 {group_title} guruhiga qaytish", url=group_link))

            if status == "ok":
                bot.send_message(
                    message.chat.id,
                    f"✅ <b>Siz o'yinga muvaffaqiyatli qo'shildingiz!</b>\n\n🎮 Guruh: <b>{group_title}</b>",
                    reply_markup=kb,
                )
            elif status == "already":
                bot.send_message(message.chat.id, "ℹ️ Siz allaqachon bu o'yinga qo'shilgansiz.", reply_markup=kb)
            elif status == "banned":
                bot.send_message(message.chat.id, "⛔ Siz botdan foydalanishdan bloklangansiz.")
            else:  # no_game
                bot.send_message(
                    message.chat.id,
                    "❌ Bu o'yin allaqachon boshlangan yoki topilmadi. Guruhda yangi o'yin ochilishini kuting.",
                    reply_markup=kb,
                )
            return

    caption = (
        f"🌙 <b>Hunter Mafia</b> botiga xush kelibsiz, <b>{message.from_user.first_name}</b>!\n\n"
        "Emotsiyalarni chetga suring. Bu yerda faqat sovuqqonlik va aniq "
        "hisob-kitob g'alaba qozonadi. 🥷⚔️\n\n"
        "Guruhga botni admin qilib qo'shing va /NewGame buyrug'i bilan o'yin boshlang."
    )
    bot.send_photo(message.chat.id, MAIN_PHOTO, caption=caption, reply_markup=get_main_menu(None, message.from_user.id))


# ================================================================================
#  🐺🦅 TEAM GAME — mustaqil, sodda "ikki jamoaga bo'linish" o'yini
#  (Asosiy Hunter Mafia o'yinidan BUTUNLAY MUSTAQIL — o'z holatiga, o'z
#  buyruqlariga va o'z callback'lariga ega alohida tizim.)
#
#  Talablar (to'liq bajarilgan):
#   1) Faqat 2 ta tugma: "🐺 Bo'rilar" va "🦅 Burgutlar" — ortiqcha tugma yo'q.
#   2) /start_team va /stop_team — FAQAT admin/owner uchun (is_authorized).
#      Oddiy foydalanuvchi buyruq bersa — "⛔ Siz admin emassiz" javobi.
#   3) Tugma bosilganda darhol shu jamoaga yoziladi; ikkala jamoada bir vaqtda
#      bo'la olmaydi — boshqa jamoaga o'tsa, avvalgisidan avtomatik chiqariladi;
#      xabar matnida ikkala jamoaning soni REAL VAQTDA yangilanadi.
#   4) /stop_team bosilganda — ko'proq a'zoli jamoa g'olib (teng bo'lsa random),
#      tabriknoma yuboriladi.
#   5) To'liq try/except — o'yin yo'qligida yoki takroriy bosishlarda bot
#      hech qachon "qotib qolmaydi" va xato bermaydi.
# ================================================================================

TEAM_GAMES = {}          # chat_id -> {"phase": "waiting"/"ended", "teams": {"wolf": {uid: name}, "eagle": {uid: name}}, "msg_id": int}
TEAM_GAMES_LOCK = threading.RLock()


def _team_game_text(tg):
    wolf = tg["teams"]["wolf"]
    eagle = tg["teams"]["eagle"]
    lines = [
        "🐺🦅 <b>Jamoaviy o'yin — ro'yxatga olish</b>\n",
        f"🐺 <b>Bo'rilar:</b> {len(wolf)} ta",
    ]
    if wolf:
        lines.append(", ".join(wolf.values()))
    lines.append(f"\n🦅 <b>Burgutlar:</b> {len(eagle)} ta")
    if eagle:
        lines.append(", ".join(eagle.values()))
    lines.append("\n\n👇 O'z jamoangizni tanlang (istalgan payt almashtirishingiz mumkin):")
    return "\n".join(lines)


def _team_game_markup(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🐺 Bo'rilar", callback_data=f"teampick|{chat_id}|wolf"),
        types.InlineKeyboardButton("🦅 Burgutlar", callback_data=f"teampick|{chat_id}|eagle"),
    )
    return kb


@bot.message_handler(commands=["start_team"])
def cmd_start_team(message):
    """🐺🦅 FAQAT admin/owner — jamoaviy o'yinga ro'yxatga olishni e'lon qiladi."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if message.chat.type not in ("group", "supergroup"):
            bot.send_message(message.chat.id, "🐺🦅 Bu buyruq faqat guruhda ishlaydi.")
            return
        if not is_authorized(message):
            bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
            return

        chat_id = message.chat.id
        with TEAM_GAMES_LOCK:
            old = TEAM_GAMES.get(chat_id)
            if old and old.get("phase") == "waiting":
                bot.send_message(message.chat.id, "⚠️ Bu guruhda allaqachon faol Jamoaviy o'yin ro'yxati bor. Avval /stop_team qiling.")
                return
            tg = {"phase": "waiting", "teams": {"wolf": {}, "eagle": {}}, "msg_id": None}
            TEAM_GAMES[chat_id] = tg
            sent = bot.send_message(message.chat.id, _team_game_text(tg), reply_markup=_team_game_markup(chat_id))
            tg["msg_id"] = sent.message_id
    except Exception as e:
        _logger.warning("cmd_start_team xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ Jamoaviy o'yinni boshlashda xatolik yuz berdi. Qaytadan urinib ko'ring.")
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("teampick|"))
def cb_team_pick(call):
    """🐺🦅 Har qanday foydalanuvchi bosishi mumkin — jamoasiga yoziladi yoki
    boshqa jamoaga o'tadi. To'liq xavfsizlik tekshiruvlari bilan."""
    try:
        maybe_capture_owner(call.from_user)
        parts = call.data.split("|")
        if len(parts) != 3:
            bot.answer_callback_query(call.id, "⚠️ Noto'g'ri so'rov.", show_alert=True)
            return
        _, chat_id_s, team = parts
        chat_id = int(chat_id_s)
        if team not in ("wolf", "eagle"):
            bot.answer_callback_query(call.id, "⚠️ Noto'g'ri jamoa.", show_alert=True)
            return

        with TEAM_GAMES_LOCK:
            tg = TEAM_GAMES.get(chat_id)
            if not tg or tg.get("phase") != "waiting":
                bot.answer_callback_query(call.id, "❌ Hozir faol Jamoaviy o'yin ro'yxati yo'q.", show_alert=True)
                return

            uid = call.from_user.id
            name = call.from_user.first_name or "O'yinchi"
            other = "eagle" if team == "wolf" else "wolf"

            if uid in tg["teams"][team]:
                bot.answer_callback_query(call.id, "✅ Siz allaqachon shu jamoadasiz!")
                return

            # ⚔️ Bir vaqtning o'zida ikkala jamoada bo'lolmaydi — avvalgisidan avtomatik chiqariladi
            switched = uid in tg["teams"][other]
            tg["teams"][other].pop(uid, None)
            tg["teams"][team][uid] = name

            try:
                bot.edit_message_text(_team_game_text(tg), chat_id, tg["msg_id"], reply_markup=_team_game_markup(chat_id))
            except Exception:
                pass  # xabar matni o'zgarmagan yoki tahrirlab bo'lmagan bo'lsa ham bot qotib qolmaydi

            label = "🐺 Bo'rilar" if team == "wolf" else "🦅 Burgutlar"
            bot.answer_callback_query(call.id, f"🔁 Siz {label} jamoasiga o'tdingiz!" if switched else f"✅ {label} jamoasiga qo'shildingiz!")
    except Exception as e:
        _logger.warning("cb_team_pick xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi, qaytadan urinib ko'ring.", show_alert=True)
        except Exception:
            pass


@bot.message_handler(commands=["stop_team"])
def cmd_stop_team(message):
    """🐺🦅 FAQAT admin/owner — ro'yxatni yopadi, ko'proq a'zoli jamoani g'olib
    e'lon qiladi (teng bo'lsa — tasodifiy), tabriknoma yuboradi."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if message.chat.type not in ("group", "supergroup"):
            bot.send_message(message.chat.id, "🐺🦅 Bu buyruq faqat guruhda ishlaydi.")
            return
        if not is_authorized(message):
            bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
            return

        chat_id = message.chat.id
        with TEAM_GAMES_LOCK:
            tg = TEAM_GAMES.get(chat_id)
            if not tg or tg.get("phase") != "waiting":
                bot.send_message(message.chat.id, "❌ Hozir faol Jamoaviy o'yin ro'yxati yo'q.")
                return

            wolf = tg["teams"]["wolf"]
            eagle = tg["teams"]["eagle"]
            tg["phase"] = "ended"

            if not wolf and not eagle:
                bot.send_message(message.chat.id, "🐺🦅 Hech kim ro'yxatga yozilmagan edi — o'yin bekor qilindi.")
                TEAM_GAMES.pop(chat_id, None)
                return

            if len(wolf) > len(eagle):
                winner, wname = wolf, "🐺 Bo'rilar"
            elif len(eagle) > len(wolf):
                winner, wname = eagle, "🦅 Burgutlar"
            else:
                winner, wname = random.choice([(wolf, "🐺 Bo'rilar"), (eagle, "🦅 Burgutlar")])

            names = ", ".join(winner.values()) if winner else "—"
            bot.send_message(
                message.chat.id,
                f"🏁 <b>Jamoaviy o'yin yakunlandi!</b>\n\n"
                f"🐺 Bo'rilar: {len(wolf)} ta | 🦅 Burgutlar: {len(eagle)} ta\n\n"
                f"🏆 <b>G'olib jamoa: {wname}!</b>\n🎉 Tabriklaymiz: {names}",
            )
            TEAM_GAMES.pop(chat_id, None)
    except Exception as e:
        _logger.warning("cmd_stop_team xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ O'yinni yakunlashda xatolik yuz berdi.")
        except Exception:
            pass


# ================================================================================
#  💍 PARA GAME — "Nikohdagi juftliklar" mafiyasi (BUTUNLAY MUSTAQIL tizim)
#
#  Talablar (to'liq bajarilgan):
#   1) Ro'yxatga olishda FAQAT bitta tugma: "💍 O'yinga qo'shilish". Nikohsiz
#      bosgan foydalanuvchiga popup: "Siz nikohda bo'lishingiz kerak!..."
#      Nikohdagi bo'lsa — IKKALASI birga (bitta juftlik sifatida) yoziladi.
#   2) Adminlar o'z juftlari bilan oddiy o'yinchidek to'g'ridan-to'g'ri qo'shiladi
#      (button umumiy — cheklov yo'q). Boshqaruv buyruqlari FAQAT admin/owner:
#      /parastart, /paraforce, /parastop.
#   3) Juftlikning umumiy (bog'langan) joni: bittasi halok bo'lsa — ikkalasi
#      ham DARHOL o'yindan chiqariladi va guruhga xabar boradi.
#   4) Rollar JUFTLIKKA (ikkalasiga birdan) beriladi: Juftlik Mafiya,
#      Juftlik Tinch aholi, Juftlik Doktor. Tun/Kunduz sikllari ishlaydi.
#   5) G'alaba shartlari: mafiya juftliklar 0 bo'lsa -> Tinch g'olib;
#      mafiya soni tinch juftliklar soniga tenglashsa -> Mafiya g'olib.
#   6) To'liq try/except — hech qanday holatda bot qotib qolmaydi.
# ================================================================================

PARA_GAMES = {}
PARA_GAMES_LOCK = threading.RLock()
PARA_NIGHT_SECONDS = 40
PARA_DAY_VOTE_SECONDS = 40


def new_para_game():
    return {
        "phase": "waiting",  # waiting -> night -> day -> ended
        "couples": {},            # couple_id -> {"members":[uid1,uid2], "names":[n1,n2], "alive":True, "hp":100, "role":None}
        "member_to_couple": {},   # uid -> couple_id
        "next_couple_id": 1,
        "msg_id": None,
        "mafia_votes": {},        # voter_couple_id -> target_couple_id
        "protect_target": None,   # couple_id
        "day_votes": {},          # voter_uid -> target_couple_id
        "timers": [],
        "day_number": 0,
    }


def _para_cancel_timers(pg):
    for t in pg.get("timers", []):
        try:
            t.cancel()
        except Exception:
            pass
    pg["timers"] = []


def _para_couple_label(couple):
    return f"{couple['names'][0]} 💍 {couple['names'][1]}"


def _para_alive_couples(pg):
    return {cid: c for cid, c in pg["couples"].items() if c["alive"]}


def _para_game_text(pg):
    lines = ["💍 <b>Para o'yin (Nikohdagi juftliklar) — ro'yxatga olish</b>\n"]
    lines.append(f"👫 <b>Ro'yxatdagi juftliklar ({len(pg['couples'])} ta):</b>")
    if pg["couples"]:
        for c in pg["couples"].values():
            lines.append(f"• {_para_couple_label(c)}")
    else:
        lines.append("Hozircha hech kim yo'q.")
    lines.append("\n👇 Qo'shilish uchun tugmani bosing (faqat nikohdagilar uchun):")
    return "\n".join(lines)


@bot.message_handler(commands=["parastart"])
def cmd_parastart(message):
    """💍 FAQAT admin/owner — Para o'yinga ro'yxatga olishni e'lon qiladi."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if message.chat.type not in ("group", "supergroup"):
            bot.send_message(message.chat.id, "💍 Bu buyruq faqat guruhda ishlaydi.")
            return
        if not is_authorized(message):
            bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
            return
        chat_id = message.chat.id
        with PARA_GAMES_LOCK:
            old = PARA_GAMES.get(chat_id)
            if old and old.get("phase") != "ended":
                bot.send_message(message.chat.id, "⚠️ Bu guruhda allaqachon faol Para o'yin bor. Avval /parastop qiling.")
                return
            pg = new_para_game()
            PARA_GAMES[chat_id] = pg
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("💍 O'yinga qo'shilish", callback_data=f"parajoin|{chat_id}"))
            sent = bot.send_message(message.chat.id, _para_game_text(pg), reply_markup=kb)
            pg["msg_id"] = sent.message_id
    except Exception as e:
        _logger.warning("cmd_parastart xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ Para o'yinni boshlashda xatolik yuz berdi.")
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("parajoin|"))
def cb_para_join(call):
    """💍 Nikohdagi foydalanuvchi bosganda — IKKALASI (u va turmush o'rtog'i)
    birga bitta juftlik sifatida ro'yxatga yoziladi. Adminlar ham xuddi shu
    tugma orqali, hech qanday farqsiz qo'shiladi."""
    try:
        maybe_capture_owner(call.from_user)
        _, chat_id_s = call.data.split("|")
        chat_id = int(chat_id_s)
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "waiting":
                bot.answer_callback_query(call.id, "❌ Hozir faol Para o'yin ro'yxati yo'q.", show_alert=True)
                return

            uid = call.from_user.id
            if uid in pg["member_to_couple"]:
                bot.answer_callback_query(call.id, "✅ Siz allaqachon ro'yxatdasiz!")
                return

            u = user_dict(uid, call.from_user.first_name)
            spouse_id = u.get("married_to")
            if not spouse_id:
                bot.answer_callback_query(
                    call.id,
                    "💍 Siz nikohda bo'lishingiz kerak! Bu o'yin faqat nikohdagi juftliklar uchundir.",
                    show_alert=True,
                )
                return
            if spouse_id in pg["member_to_couple"]:
                bot.answer_callback_query(call.id, "✅ Siz allaqachon ro'yxatdasiz (sherigingiz orqali qo'shilgan)!")
                return

            su = user_dict(spouse_id)
            couple_id = pg["next_couple_id"]
            pg["next_couple_id"] += 1
            pg["couples"][couple_id] = {
                "members": [uid, spouse_id],
                "names": [u.get("name") or "O'yinchi", su.get("name") or "Sherik"],
                "alive": True,
                "hp": 100,
                "role": None,
            }
            pg["member_to_couple"][uid] = couple_id
            pg["member_to_couple"][spouse_id] = couple_id

            try:
                bot.edit_message_text(_para_game_text(pg), chat_id, pg["msg_id"],
                                       reply_markup=types.InlineKeyboardMarkup().add(
                                           types.InlineKeyboardButton("💍 O'yinga qo'shilish", callback_data=f"parajoin|{chat_id}")))
            except Exception:
                pass

            safe_send(spouse_id, "💍 Turmush o'rtog'ingiz sizni Para o'yinga (Hunter Mafia) birga qo'shdi!")
            bot.answer_callback_query(call.id, "✅ Siz va turmush o'rtog'ingiz birga qo'shildingiz!")
    except Exception as e:
        _logger.warning("cb_para_join xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi, qaytadan urinib ko'ring.", show_alert=True)
        except Exception:
            pass


@bot.message_handler(commands=["parastop"])
def cmd_parastop(message):
    """💍 FAQAT admin/owner — Para o'yinni (qaysi bosqichda bo'lishidan qat'i
    nazar) darhol to'xtatadi va barcha jarayonlarni bekor qiladi."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if message.chat.type not in ("group", "supergroup"):
            bot.send_message(message.chat.id, "💍 Bu buyruq faqat guruhda ishlaydi.")
            return
        if not is_authorized(message):
            bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
            return
        chat_id = message.chat.id
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg:
                bot.send_message(message.chat.id, "❌ Hozir faol Para o'yin yo'q.")
                return
            _para_cancel_timers(pg)
            PARA_GAMES.pop(chat_id, None)
        bot.send_message(message.chat.id, "🛑 Para o'yin to'xtatildi va barcha jarayonlar bekor qilindi.")
    except Exception as e:
        _logger.warning("cmd_parastop xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ To'xtatishda xatolik yuz berdi.")
        except Exception:
            pass


def _para_assign_roles(pg):
    couple_ids = list(pg["couples"].keys())
    random.shuffle(couple_ids)
    n = len(couple_ids)
    mafia_count = max(1, n // 3)
    doctor_count = 1 if n >= 2 else 0
    for i, cid in enumerate(couple_ids):
        if i < mafia_count:
            pg["couples"][cid]["role"] = "Juftlik Mafiya 🕶💍"
        elif i < mafia_count + doctor_count:
            pg["couples"][cid]["role"] = "Juftlik Doktor 👨‍⚕️💍"
        else:
            pg["couples"][cid]["role"] = "Juftlik Tinch aholi 🏠💍"


@bot.message_handler(commands=["paraforce"])
def cmd_paraforce(message):
    """💍 FAQAT admin/owner — kutish vaqtini tugatib, o'yinni MAJBURIY
    boshlaydi: rollarni juftliklarga taqsimlaydi va birinchi Tun bosqichini
    ochadi. Kamida 2 ta juftlik ro'yxatdan o'tgan bo'lishi shart."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if message.chat.type not in ("group", "supergroup"):
            bot.send_message(message.chat.id, "💍 Bu buyruq faqat guruhda ishlaydi.")
            return
        if not is_authorized(message):
            bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")
            return
        chat_id = message.chat.id
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "waiting":
                bot.send_message(message.chat.id, "❌ Hozir ro'yxatga olish bosqichida Para o'yin yo'q.")
                return
            if len(pg["couples"]) < 2:
                bot.send_message(message.chat.id, "⚠️ O'yin boshlanishi uchun kamida 2 ta juftlik ro'yxatdan o'tishi kerak.")
                return

            _para_assign_roles(pg)
            for c in pg["couples"].values():
                for m_uid in c["members"]:
                    partner_name = c["names"][1] if c["members"][0] == m_uid else c["names"][0]
                    safe_send(
                        m_uid,
                        f"💍 <b>Para o'yin boshlandi!</b>\n\n"
                        f"🎭 Juftligingizning roli: <b>{c['role']}</b>\n"
                        f"👫 Turmush o'rtog'ingiz (sherigingiz): <b>{partner_name}</b>\n\n"
                        f"⚠️ Eslatma: agar sizlardan biri halok bo'lsa, ikkalangiz ham birga o'yindan chiqasiz!",
                    )
            bot.send_message(
                chat_id,
                f"🎬 <b>Para o'yin majburiy boshlandi!</b>\n"
                f"👫 Jami {len(pg['couples'])} ta juftlik ishtirok etmoqda.\n"
                f"🌙 Birinchi tun boshlandi...",
            )
        _para_start_night(chat_id)
    except Exception as e:
        _logger.warning("cmd_paraforce xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ O'yinni boshlashda xatolik yuz berdi.")
        except Exception:
            pass


def _para_start_night(chat_id):
    try:
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg:
                return
            pg["phase"] = "night"
            pg["day_number"] += 1
            pg["mafia_votes"] = {}
            pg["protect_target"] = None
            alive = _para_alive_couples(pg)

            mafia_couples = {cid: c for cid, c in alive.items() if c["role"] == "Juftlik Mafiya 🕶💍"}
            doctor_couples = {cid: c for cid, c in alive.items() if c["role"] == "Juftlik Doktor 👨‍⚕️💍"}

            targets = [(cid, c) for cid, c in alive.items() if c["role"] != "Juftlik Mafiya 🕶💍"]
            for cid, c in mafia_couples.items():
                kb = types.InlineKeyboardMarkup()
                for t_cid, t_c in targets:
                    kb.add(types.InlineKeyboardButton(_para_couple_label(t_c), callback_data=f"paranight|{chat_id}|{t_cid}"))
                for m_uid in c["members"]:
                    safe_send(m_uid, f"🌙 <b>{pg['day_number']}-tun</b> — qaysi juftlikni yo'q qilamiz?", reply_markup=kb)

            for cid, c in doctor_couples.items():
                kb = types.InlineKeyboardMarkup()
                for t_cid, t_c in alive.items():
                    kb.add(types.InlineKeyboardButton(_para_couple_label(t_c), callback_data=f"paraprotect|{chat_id}|{t_cid}"))
                for m_uid in c["members"]:
                    safe_send(m_uid, f"🌙 <b>{pg['day_number']}-tun</b> — qaysi juftlikni himoya qilamiz?", reply_markup=kb)

            bot.send_message(chat_id, f"🌙 <b>{pg['day_number']}-tun tushdi...</b> Juftliklar yashirin harakat qilmoqda.")

            t = threading.Timer(PARA_NIGHT_SECONDS, lambda: _para_resolve_night(chat_id))
            t.daemon = True
            t.start()
            pg["timers"].append(t)
    except Exception as e:
        _logger.warning("_para_start_night xatolik: %s", e)


@bot.callback_query_handler(func=lambda c: c.data.startswith("paranight|"))
def cb_para_night_vote(call):
    try:
        maybe_capture_owner(call.from_user)
        _, chat_id_s, target_cid_s = call.data.split("|")
        chat_id, target_cid = int(chat_id_s), int(target_cid_s)
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "night":
                bot.answer_callback_query(call.id, "❌ Hozir tun bosqichi emas.", show_alert=True)
                return
            uid = call.from_user.id
            voter_cid = pg["member_to_couple"].get(uid)
            if voter_cid is None or not pg["couples"][voter_cid]["alive"]:
                bot.answer_callback_query(call.id, "❌ Siz bu o'yinda emassiz yoki halok bo'lgansiz.", show_alert=True)
                return
            pg["mafia_votes"][voter_cid] = target_cid
        bot.answer_callback_query(call.id, "✅ Ovozingiz qabul qilindi!")
    except Exception as e:
        _logger.warning("cb_para_night_vote xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi.", show_alert=True)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("paraprotect|"))
def cb_para_protect(call):
    try:
        maybe_capture_owner(call.from_user)
        _, chat_id_s, target_cid_s = call.data.split("|")
        chat_id, target_cid = int(chat_id_s), int(target_cid_s)
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "night":
                bot.answer_callback_query(call.id, "❌ Hozir tun bosqichi emas.", show_alert=True)
                return
            pg["protect_target"] = target_cid
        bot.answer_callback_query(call.id, "✅ Himoya tanlovingiz qabul qilindi!")
    except Exception as e:
        _logger.warning("cb_para_protect xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi.", show_alert=True)
        except Exception:
            pass


def _para_eliminate_couple(chat_id, pg, cid, reason):
    """💔 Bir juftlikni butunlay o'yindan chiqaradi — ikkala a'zosi BIRGA,
    'bog'langan taqdir' mexanikasiga ko'ra."""
    c = pg["couples"][cid]
    c["alive"] = False
    c["hp"] = 0
    name1, name2 = c["names"]
    bot.send_message(
        chat_id,
        f"💔 {reason}\n"
        f"☠️ <b>{name1}</b> halok bo'ldi, uning turmush o'rtog'i <b>{name2}</b> ham "
        f"taqdir taqozosi bilan o'yindan chiqdi!\n"
        f"🎭 Ularning roli: <b>{c['role']}</b> edi.",
    )


def _para_check_win(chat_id):
    """G'alaba shartini tekshiradi; agar o'yin tugagan bo'lsa True qaytaradi."""
    pg = PARA_GAMES.get(chat_id)
    if not pg:
        return True
    alive = _para_alive_couples(pg)
    mafia_alive = [c for c in alive.values() if c["role"] == "Juftlik Mafiya 🕶💍"]
    peace_alive = [c for c in alive.values() if c["role"] != "Juftlik Mafiya 🕶💍"]

    if not mafia_alive:
        _para_end_game(chat_id, "peace")
        return True
    if len(mafia_alive) >= len(peace_alive):
        _para_end_game(chat_id, "mafia")
        return True
    return False


def _para_end_game(chat_id, winner_side):
    try:
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg:
                return
            _para_cancel_timers(pg)
            if winner_side == "peace":
                winners = [c for c in pg["couples"].values() if c["role"] != "Juftlik Mafiya 🕶💍"]
                label = "🏠💍 Juftlik Tinch aholi"
            else:
                winners = [c for c in pg["couples"].values() if c["role"] == "Juftlik Mafiya 🕶💍"]
                label = "🕶💍 Juftlik Mafiya"
            names = ", ".join(_para_couple_label(c) for c in winners) if winners else "—"
            bot.send_message(
                chat_id,
                f"🏁 <b>Para o'yin tugadi!</b>\n\n"
                f"🏆 <b>G'olib taraf: {label}!</b>\n"
                f"🎉 Tabriklaymiz: {names}",
            )
            PARA_GAMES.pop(chat_id, None)
    except Exception as e:
        _logger.warning("_para_end_game xatolik: %s", e)


def _para_resolve_night(chat_id):
    try:
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "night":
                return

            votes = list(pg["mafia_votes"].values())
            target_cid = None
            if votes:
                tally = {}
                for v in votes:
                    tally[v] = tally.get(v, 0) + 1
                mx = max(tally.values())
                top = [cid for cid, cnt in tally.items() if cnt == mx]
                target_cid = random.choice(top)

            if target_cid is not None and target_cid != pg.get("protect_target") and pg["couples"].get(target_cid, {}).get("alive"):
                _para_eliminate_couple(chat_id, pg, target_cid, "🌙 Tunda mafiya juftlik hujum qildi!")
            elif target_cid is not None:
                bot.send_message(chat_id, "🛡 Doktor juftlik bu kechada nishonni saqlab qoldi!")
            else:
                bot.send_message(chat_id, "😴 Bu kecha hech kim hujum qilmadi — tinch tun bo'ldi.")

        if _para_check_win(chat_id):
            return
        _para_start_day(chat_id)
    except Exception as e:
        _logger.warning("_para_resolve_night xatolik: %s", e)


def _para_start_day(chat_id):
    try:
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg:
                return
            pg["phase"] = "day"
            pg["day_votes"] = {}
            alive = _para_alive_couples(pg)

            kb = types.InlineKeyboardMarkup()
            for cid, c in alive.items():
                kb.add(types.InlineKeyboardButton(_para_couple_label(c), callback_data=f"paradayvote|{chat_id}|{cid}"))

            text = (
                f"☀️ <b>{pg['day_number']}-kun</b> — muhokama va ovoz berish vaqti!\n\n"
                f"👫 <b>Tirik juftliklar ({len(alive)} ta):</b>\n" +
                "\n".join(f"• {_para_couple_label(c)}" for c in alive.values()) +
                "\n\nKimni o'yindan chiqarasiz? Pastdagi tugmalar orqali ovoz bering:"
            )
            bot.send_message(chat_id, text, reply_markup=kb)

            t = threading.Timer(PARA_DAY_VOTE_SECONDS, lambda: _para_resolve_day(chat_id))
            t.daemon = True
            t.start()
            pg["timers"].append(t)
    except Exception as e:
        _logger.warning("_para_start_day xatolik: %s", e)


@bot.callback_query_handler(func=lambda c: c.data.startswith("paradayvote|"))
def cb_para_day_vote(call):
    try:
        maybe_capture_owner(call.from_user)
        _, chat_id_s, target_cid_s = call.data.split("|")
        chat_id, target_cid = int(chat_id_s), int(target_cid_s)
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "day":
                bot.answer_callback_query(call.id, "❌ Hozir ovoz berish bosqichi emas.", show_alert=True)
                return
            uid = call.from_user.id
            voter_cid = pg["member_to_couple"].get(uid)
            if voter_cid is None or not pg["couples"][voter_cid]["alive"]:
                bot.answer_callback_query(call.id, "❌ Siz bu o'yinda emassiz yoki halok bo'lgansiz.", show_alert=True)
                return
            pg["day_votes"][uid] = target_cid
        bot.answer_callback_query(call.id, "✅ Ovozingiz qabul qilindi!")
    except Exception as e:
        _logger.warning("cb_para_day_vote xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi.", show_alert=True)
        except Exception:
            pass


def _para_resolve_day(chat_id):
    try:
        with PARA_GAMES_LOCK:
            pg = PARA_GAMES.get(chat_id)
            if not pg or pg.get("phase") != "day":
                return
            votes = list(pg["day_votes"].values())
            if votes:
                tally = {}
                for v in votes:
                    tally[v] = tally.get(v, 0) + 1
                mx = max(tally.values())
                top = [cid for cid, cnt in tally.items() if cnt == mx]
                target_cid = random.choice(top)
                if pg["couples"].get(target_cid, {}).get("alive"):
                    _para_eliminate_couple(chat_id, pg, target_cid, "⚖️ Ovoz berish natijasida aholi qaror qildi:")
            else:
                bot.send_message(chat_id, "🤷 Hech kim ovoz bermadi — bu kun hech kim chiqarilmadi.")

        if _para_check_win(chat_id):
            return
        _para_start_night(chat_id)
    except Exception as e:
        _logger.warning("_para_resolve_day xatolik: %s", e)


# ================================================================================
#  /NewGame
# ================================================================================

# ================================================================================
#  🔮 TAQDIR G'ILDIRAGI — /taqdir (barcha uchun, kuniga 1 marta)
#  💎 ELITE SIRLI SANDIQ — /elite_sandiq (faqat HUNTER ELITE uchun, kuniga 1 marta)
#
#  Bu ikkalasi ham Almex Black Bot'da UMUMAN YO'Q, original Hunter Mafia
#  funksiyalari — botni "hashamatliroq" va o'ziga xos ko'rsatish uchun.
#  🔧 TUZATILDI: "VIP" so'zi butunlay olib tashlandi — botda faqat 👑 HUNTER
#  ELITE bor, boshqa hech qanday "VIP" nomli narsa yo'q.
# ================================================================================

TAQDIR_PRIZES = [
    # (og'irlik, turi, miqdor, matn)
    (30, "dollar", 15, "💵 Kichik omad"),
    (22, "dollar", 40, "💵 Yaxshi omad"),
    (15, "coin", 5, "🪙 Hunter Coin topilmasi"),
    (12, "diamond", 1, "💎 Kichik olmos siyi"),
    (10, "dollar", 100, "🍀 Katta omad!"),
    (6, "diamond", 3, "💎💎 Katta olmos siyi!"),
    (4, "coin", 15, "🪙🪙 Coin yomg'iri!"),
    (1, "jackpot", 0, "👑 JACKPOT!"),
]


@bot.message_handler(commands=["taqdir", "fortune", "gildirak"])
def cmd_taqdir(message):
    """🔮 TAQDIR G'ILDIRAGI — kuniga 1 marta aylantiriladigan, animatsiyali
    omad g'ildiragi. Kunlik oddiy bonusdan farqli o'laroq, bu yerda 8 xil
    natija bor (jumladan kam ehtimolli 👑 JACKPOT — 3 valyutaning barchasi
    birdan!). Bepul va barcha foydalanuvchilar uchun ochiq."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    user_dict(uid, message.from_user.first_name)
    today = time.strftime("%Y-%m-%d")
    key = f"taqdir_date_{uid}"
    if get_setting(key) == today:
        bot.send_message(message.chat.id, "⏳ Siz bugungi Taqdir G'ildiragini allaqachon aylantirgansiz. Ertaga qayting!")
        return
    set_setting(key, today)

    # 🎡 Animatsiyali "aylanish" effekti — bir necha marta xabarni tahrirlab, taassurot yaratamiz
    spin_frames = ["🔮 ⚪️🔴🟡🟢 ⚪️", "🔮 🔴🟡🟢⚪️ 🟡", "🔮 🟡🟢⚪️🔴 🟢", "🔮 🟢⚪️🔴🟡 ⚪️"]
    sent = bot.send_message(message.chat.id, f"🔮 <b>Taqdir G'ildiragi aylanmoqda...</b>\n{spin_frames[0]}")
    for frame in spin_frames[1:]:
        time.sleep(0.35)
        try:
            bot.edit_message_text(f"🔮 <b>Taqdir G'ildiragi aylanmoqda...</b>\n{frame}", message.chat.id, sent.message_id)
        except Exception:
            pass
    time.sleep(0.35)

    weights = [w for w, *_ in TAQDIR_PRIZES]
    _, ptype, amount, label = random.choices(TAQDIR_PRIZES, weights=weights, k=1)[0]
    mult = luck_mult(uid)

    if ptype == "jackpot":
        j_dollar, j_diamond, j_coin = int(200 * mult), 5, 25
        add_balance(uid, dollar=j_dollar, diamond=j_diamond, coin=j_coin)
        result_text = (
            f"👑 <b>JACKPOT!!!</b> 👑\n"
            f"Naqadar omad! Siz olib qoldingiz:\n"
            f"💵 +{j_dollar}$  💎 +{j_diamond}  🪙 +{j_coin}"
        )
    else:
        amount = int(amount * mult) if ptype == "dollar" else amount
        add_balance(uid, **{ptype: amount})
        unit = {"dollar": "$", "diamond": "💎", "coin": "🪙"}[ptype]
        result_text = f"{label}\n\nSiz yutdingiz: <b>+{amount}{unit}</b>"

    try:
        bot.edit_message_text(f"🔮 <b>Taqdir G'ildiragi to'xtadi!</b>\n\n{result_text}\n\n⏳ Ertaga yana urinib ko'ring!", message.chat.id, sent.message_id)
    except Exception:
        bot.send_message(message.chat.id, f"🔮 {result_text}")


ELITE_BOX_PRIZES = [
    # 🔧 TUZATILDI: 🪙 Hunter Coin sovg'asi butunlay olib tashlandi (endi bu
    # sandiqdan Coin chiqmaydi); 💎 Olmos chiqish ehtimoli sezilarli pasaytirildi
    # (28 -> 8), o'rniga 💵 pul sovg'alari og'irligi oshirildi.
    (55, "dollar", 80, "💵 Kumush sovg'a"),
    (8, "diamond", 2, "💎 Olmos sovg'a"),
    (32, "dollar", 250, "🏆 Oltin sovg'a"),
    (5, "jackpot", 0, "👑✨ AFSONAVIY SOVG'A"),
]


@bot.message_handler(commands=["elite_sandiq", "vip_sandiq", "vipbox"])
def cmd_elite_sandiq(message):
    """💎 ELITE SIRLI SANDIQ — FAQAT HUNTER ELITE obunachilari uchun, kuniga 1
    marta ochiladigan premium sovg'a sandig'i. Oddiy /taqdir'dan farqli
    o'laroq, bu yerdagi barcha mukofotlar SEZILARLI KATTAROQ — ELITE
    obunaning haqiqiy qiymatini his qildirish uchun mo'ljallangan.
    (Eski /vip_sandiq nomi ham ishlaydi — orqaga moslik uchun.)"""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    user_dict(uid, message.from_user.first_name)
    if not is_elite(uid):
        bot.send_message(
            message.chat.id,
            "🔒 ELITE Sirli Sandiq faqat <b>HUNTER ELITE</b> obunachilari uchun ochiq.\n"
            "👑 ELITE olish uchun: <code>/elite</code>",
        )
        return
    today = time.strftime("%Y-%m-%d")
    key = f"vipbox_date_{uid}"
    if get_setting(key) == today:
        bot.send_message(message.chat.id, "⏳ Siz bugungi ELITE sandiqni allaqachon ochgansiz. Ertaga qayting!")
        return
    set_setting(key, today)

    sent = bot.send_message(message.chat.id, "💎 <b>ELITE Sirli Sandiq ochilmoqda...</b> 🔒➜🔓")
    time.sleep(0.6)

    weights = [w for w, *_ in ELITE_BOX_PRIZES]
    _, ptype, amount, label = random.choices(ELITE_BOX_PRIZES, weights=weights, k=1)[0]
    mult = luck_mult(uid)

    if ptype == "jackpot":
        # 🔧 TUZATILDI: Hunter Coin sovg'asi olib tashlandi, o'rniga pul biroz oshirildi
        j_dollar, j_diamond = int(650 * mult), 10
        add_balance(uid, dollar=j_dollar, diamond=j_diamond)
        result_text = (
            f"👑✨ <b>AFSONAVIY ELITE SANDIQ!!!</b> ✨👑\n"
            f"💵 +{j_dollar}$  💎 +{j_diamond}\n\n"
            f"<i>ELITE bo'lganingiz bejiz emas!</i>"
        )
    else:
        amount = int(amount * mult) if ptype == "dollar" else amount
        add_balance(uid, **{ptype: amount})
        unit = {"dollar": "$", "diamond": "💎", "coin": "🪙"}[ptype]
        result_text = f"{label}\n\nSiz yutdingiz: <b>+{amount}{unit}</b>"

    try:
        bot.edit_message_text(f"💎 <b>Sandiq ochildi!</b>\n\n{result_text}\n\n⏳ Ertaga yana urinib ko'ring!", message.chat.id, sent.message_id)
    except Exception:
        bot.send_message(message.chat.id, f"💎 {result_text}")


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
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
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
        # 🐺🦅💍 Owner /teamgame yoki /parateam orqali shu guruh uchun oldindan
        # yoqib qo'ygan bo'lsa — yangi o'yin AVTOMATIK shu rejimda boshlanadi.
        GAMES[chat_id]["squad_mode"] = get_setting(f"squad_mode_{chat_id}") == "1"
        GAMES[chat_id]["couple_mode"] = get_setting(f"couple_mode_{chat_id}") == "1"
        try:
            GAMES[chat_id]["group_link"] = bot.export_chat_invite_link(chat_id)
        except Exception:
            pass

        kb = build_join_markup(chat_id, GAMES[chat_id])
        mode_lines = []
        if GAMES[chat_id]["squad_mode"]:
            mode_lines.append("🐺🦅 <b>Jamoaviy rejim yoqilgan</b> — qo'shilganda o'z jamoangizni tanlang!")
        if GAMES[chat_id]["couple_mode"]:
            mode_lines.append("💍 <b>Para rejim yoqilgan</b> — turmush qurganlar birga bitta tugma bilan qo'shiladi!")
        mode_block = ("\n" + "\n".join(mode_lines) + "\n") if mode_lines else ""
        sent = bot.send_message(
            chat_id,
            "🎮 <b>Yangi Hunter Mafia o'yini boshlandi!</b>\n"
            f"{mode_block}\n"
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
    lines = [
        "🎮 <b>Hunter Mafia o'yini</b>\n",
        f"👥 <b>Ishtirokchilar ({len(game['players'])} ta):</b>\n{player_line_list(game)}\n",
    ]
    if game.get("squad_mode"):
        wolf = [p["name"] for uid, p in game["players"].items() if game["squads"].get(uid) == "wolf"]
        eagle = [p["name"] for uid, p in game["players"].items() if game["squads"].get(uid) == "eagle"]
        lines.append(f"🐺 <b>Bo'ri jamoasi ({len(wolf)}):</b> {', '.join(wolf) if wolf else '—'}")
        lines.append(f"🦅 <b>Burgut jamoasi ({len(eagle)}):</b> {', '.join(eagle) if eagle else '—'}\n")
    lines.append("💡 <i>🎭 rol tanlash huquqingiz bo'lsa /rolni_tanla &lt;rol&gt; deb yozing!</i>")
    return "\n".join(lines)


def build_join_markup(chat_id, game=None):
    kb = types.InlineKeyboardMarkup()
    if BOT_USERNAME:
        # 🤖 endi guruhdagi tugma bosilganda foydalanuvchi avtomatik botning shaxsiy
        # chatiga o'tkaziladi va o'sha yerda o'yinga qo'shiladi (do'stona, tushunarli UX)
        kb.add(types.InlineKeyboardButton("🎮 O'yinga qo'shilish", url=f"https://t.me/{BOT_USERNAME}?start=join_{chat_id}"))
    else:
        kb.add(types.InlineKeyboardButton("🎮 O'yinga qo'shilish", callback_data=f"join|{chat_id}"))
    if game and game.get("squad_mode"):
        kb.add(
            types.InlineKeyboardButton("🐺 Bo'ri jamoasi", callback_data=f"squadjoin|{chat_id}|wolf"),
            types.InlineKeyboardButton("🦅 Burgut jamoasi", callback_data=f"squadjoin|{chat_id}|eagle"),
        )
    if game and game.get("couple_mode"):
        kb.add(types.InlineKeyboardButton("💍 Men va turmush o'rtog'imni qo'shish", callback_data=f"couplejoin|{chat_id}"))
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
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
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

    sent = bot.send_message(chat_id, build_join_text(game), reply_markup=build_join_markup(chat_id, game))
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


@bot.message_handler(commands=["teamgame"])
def cmd_teamgame(message):
    """🐺🦅 FAQAT BOT EGASI — ushbu guruh uchun 'Jamoaviy o'yin' rejimini
    yoqadi/o'chiradi. Yoqilgan bo'lsa, KEYINGI /newgame'da ishtirokchilar
    qo'shilish payti 🐺 Bo'ri yoki 🦅 Burgut jamosini tanlashlari mumkin bo'ladi
    (bu — faqat qo'shimcha "qaysi jamoa g'olib chiqdi" statistikasi uchun;
    asosiy Mafiya/Tinch aholi rollari va g'alaba shartlari o'zgarmaydi)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        bot.send_message(message.chat.id, "🐺🦅 Bu buyruq faqat guruhda ishlaydi.")
        return
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu sozlamani FAQAT bot egasi o'zgartira oladi.")
        return
    chat_id = message.chat.id
    current = get_setting(f"squad_mode_{chat_id}") == "1"
    new_val = not current
    set_setting(f"squad_mode_{chat_id}", "1" if new_val else "0")
    bot.send_message(
        message.chat.id,
        f"🐺🦅 Jamoaviy o'yin rejimi: {'✅ YOQILDI' if new_val else '❌ O\'CHIRILDI'}\n"
        "Bu sozlama keyingi <code>/newgame</code>'dan boshlab kuchga kiradi.",
    )


@bot.message_handler(commands=["parateam"])
def cmd_parateam(message):
    """💍 FAQAT BOT EGASI — ushbu guruh uchun 'Para (juftlik) o'yin' rejimini
    yoqadi/o'chiradi. Yoqilgan bo'lsa, turmush qurgan (/nikoh) foydalanuvchilar
    KEYINGI /newgame'da bitta tugma bilan ikkalasi birga qo'shila oladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        bot.send_message(message.chat.id, "💍 Bu buyruq faqat guruhda ishlaydi.")
        return
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu sozlamani FAQAT bot egasi o'zgartira oladi.")
        return
    chat_id = message.chat.id
    current = get_setting(f"couple_mode_{chat_id}") == "1"
    new_val = not current
    set_setting(f"couple_mode_{chat_id}", "1" if new_val else "0")
    bot.send_message(
        message.chat.id,
        f"💍 Para o'yin rejimi: {'✅ YOQILDI' if new_val else '❌ O\'CHIRILDI'}\n"
        "Bu sozlama keyingi <code>/newgame</code>'dan boshlab kuchga kiradi.",
    )


@bot.message_handler(commands=["setting", "mode"])
def cmd_setting_mode(message):
    """⚙️ FAQAT BOT EGASI — joriy guruh uchun barcha maxsus o'yin rejimlarini
    (Jamoaviy 🐺🦅, Para 💍) bitta panelda ko'radi va tugma orqali yoqib/o'chira oladi.
    Bu buyruq (/setting va /mode) shaxsiy chatda ham, guruhda ham ishlaydi,
    lekin FAQAT bot egasiga ko'rinadi — boshqa hech kim ishlata olmaydi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return  # ⛔ boshqa hech kimga bu buyruq mavjudligi haqida hatto izoh ham berilmaydi

    if message.chat.type in ("group", "supergroup"):
        chat_id = message.chat.id
        title = message.chat.title or "bu guruh"
    else:
        bot.send_message(
            message.chat.id,
            "⚙️ <code>/setting</code> ni istalgan guruhda yozing — o'sha guruh uchun sozlamalar paneli ochiladi.",
        )
        return

    squad_on = get_setting(f"squad_mode_{chat_id}") == "1"
    couple_on = get_setting(f"couple_mode_{chat_id}") == "1"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        f"🐺🦅 Jamoaviy o'yin: {'✅ Yoqilgan' if squad_on else '❌ O\'chirilgan'}",
        callback_data=f"ownersetting|squad|{chat_id}",
    ))
    kb.add(types.InlineKeyboardButton(
        f"💍 Para o'yin: {'✅ Yoqilgan' if couple_on else '❌ O\'chirilgan'}",
        callback_data=f"ownersetting|couple|{chat_id}",
    ))
    bot.send_message(
        message.chat.id,
        f"⚙️ <b>{title} uchun o'yin sozlamalari</b>\n\n"
        "Rejimlarni yoqish/o'chirish uchun pastdagi tugmalarni bosing. "
        "O'zgarish KEYINGI <code>/newgame</code>'dan boshlab kuchga kiradi.",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("ownersetting|"))
def cb_owner_setting_toggle(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Faqat bot egasi uchun.", show_alert=True)
        return
    _, which, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    key = f"squad_mode_{chat_id}" if which == "squad" else f"couple_mode_{chat_id}"
    new_val = not (get_setting(key) == "1")
    set_setting(key, "1" if new_val else "0")

    squad_on = get_setting(f"squad_mode_{chat_id}") == "1"
    couple_on = get_setting(f"couple_mode_{chat_id}") == "1"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        f"🐺🦅 Jamoaviy o'yin: {'✅ Yoqilgan' if squad_on else '❌ O\'chirilgan'}",
        callback_data=f"ownersetting|squad|{chat_id}",
    ))
    kb.add(types.InlineKeyboardButton(
        f"💍 Para o'yin: {'✅ Yoqilgan' if couple_on else '❌ O\'chirilgan'}",
        callback_data=f"ownersetting|couple|{chat_id}",
    ))
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        pass
    bot.answer_callback_query(call.id, "✅ Yangilandi!")


def do_join(chat_id, tg_user, squad=None):
    """O'yinga qo'shilishga urinadi va holatni qaytaradi:
    'ok' — muvaffaqiyatli qo'shildi, 'already' — allaqachon qo'shilgan,
    'banned' — bloklangan, 'no_game' — hozir qo'shilsa bo'ladigan o'yin yo'q.
    squad — agar berilsa ('wolf' yoki 'eagle'), 🐺🦅 jamoaviy rejimda o'yinchi
    shu jamoaga yoziladi (faqat game['squad_mode'] yoqilgan bo'lsa)."""
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        return "no_game"
    uid = tg_user.id
    name = tg_user.first_name or "O'yinchi"
    user_dict(uid, name)
    if is_banned(uid):
        return "banned"
    already = uid in game["players"]
    if not already:
        game["players"][uid] = {"name": name, "role": None, "alive": True, "team": None}
    if squad in ("wolf", "eagle") and game.get("squad_mode"):
        game["squads"][uid] = squad
    if game.get("join_msg_id"):
        try:
            bot.edit_message_text(build_join_text(game), chat_id, game["join_msg_id"], reply_markup=build_join_markup(chat_id, game))
        except Exception:
            pass
    return "already" if already else "ok"


@bot.callback_query_handler(func=lambda c: c.data.startswith("join|"))
def cb_join(call):
    maybe_capture_owner(call.from_user)
    _, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    do_join(chat_id, call.from_user)
    bot.answer_callback_query(call.id, f"{call.from_user.first_name} o'yinga qo'shildi!")


@bot.callback_query_handler(func=lambda c: c.data.startswith("squadjoin|"))
def cb_squad_join(call):
    """🐺🦅 Jamoaviy o'yin rejimida — o'yinchi bir tugma bosishi bilan HAM o'yinga
    qo'shiladi, HAM o'zi xohlagan jamoaga (Bo'ri yoki Burgut) yoziladi."""
    maybe_capture_owner(call.from_user)
    _, chat_id_s, squad = call.data.split("|")
    chat_id = int(chat_id_s)
    status = do_join(chat_id, call.from_user, squad=squad)
    squad_label = "🐺 Bo'ri jamoasi" if squad == "wolf" else "🦅 Burgut jamoasi"
    if status == "banned":
        bot.answer_callback_query(call.id, "⛔ Siz bloklangansiz.", show_alert=True)
    elif status == "no_game":
        bot.answer_callback_query(call.id, "❌ Hozir qo'shilsa bo'ladigan o'yin yo'q.", show_alert=True)
    else:
        bot.answer_callback_query(call.id, f"✅ {squad_label}ga qo'shildingiz!")


@bot.callback_query_handler(func=lambda c: c.data.startswith("couplejoin|"))
def cb_couple_join(call):
    """💍 Para o'yin rejimida — turmush qurgan foydalanuvchi BITTA tugma bosib,
    o'zini VA turmush o'rtog'ini birgalikda o'yinga qo'shadi (agar o'rtog'i
    hali qo'shilmagan bo'lsa). Turmush qurmagan yoki juftisi topilmagan
    foydalanuvchilar uchun oddiy qo'shilish sifatida ishlaydi."""
    maybe_capture_owner(call.from_user)
    _, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "waiting":
        bot.answer_callback_query(call.id, "❌ Hozir qo'shilsa bo'ladigan o'yin yo'q.", show_alert=True)
        return

    uid = call.from_user.id
    status = do_join(chat_id, call.from_user)
    if status == "banned":
        bot.answer_callback_query(call.id, "⛔ Siz bloklangansiz.", show_alert=True)
        return

    u = user_dict(uid, call.from_user.first_name)
    spouse_id = u.get("married_to")
    if not spouse_id:
        bot.answer_callback_query(call.id, "✅ Qo'shildingiz! (Turmush o'rtog'ingiz yo'q — /nikoh orqali oila qurishingiz mumkin.)")
        return
    if spouse_id in game["players"]:
        bot.answer_callback_query(call.id, "✅ Siz qo'shildingiz — turmush o'rtog'ingiz allaqachon o'yinda ekan!")
        return

    # 💍 Turmush o'rtog'ini ham shaxsiy chatida bot bilan gaplashgan bo'lsa avtomatik qo'shamiz
    su = user_dict(spouse_id)
    spouse_name = su.get("name") or "Sherigingiz"

    class _FakeUser:
        pass

    fake = _FakeUser()
    fake.id = spouse_id
    fake.first_name = spouse_name
    join_status = do_join(chat_id, fake)
    if join_status in ("ok", "already"):
        bot.answer_callback_query(call.id, f"💍 Siz va {spouse_name} birgalikda o'yinga qo'shildingiz!")
        safe_send(spouse_id, f"💍 Turmush o'rtog'ingiz sizni <b>{game['chat_title']}</b> guruhidagi Hunter Mafia o'yiniga birga qo'shdi!")
    else:
        bot.answer_callback_query(call.id, "✅ Siz qo'shildingiz. (Turmush o'rtog'ingizni avtomatik qo'shib bo'lmadi.)")


# ================================================================================
#  📋 GURUHGA A'ZOLIK SO'ROVLARI (ZAYAVKALAR) — avtomatik qabul qilish
#  Eslatma: bu faqat guruh havolasi "Administrator tasdig'i talab qilinsin"
#  (request to join) rejimida yaratilgan bo'lsa ishlaydi — aks holda odamlar
#  havola orqali to'g'ridan-to'g'ri kirib ketaveradi va navbat hosil bo'lmaydi.
# ================================================================================

@bot.chat_join_request_handler()
def handle_chat_join_request(update):
    """Guruhga kirish uchun yangi so'rov kelganda navbatga qo'shib boradi."""
    chat_id = update.chat.id
    user = update.from_user
    with JOIN_REQ_LOCK:
        lst = PENDING_JOIN_REQUESTS.setdefault(chat_id, [])
        if not any(r["user_id"] == user.id for r in lst):
            lst.append({
                "user_id": user.id,
                "name": user.first_name or "Foydalanuvchi",
                "username": user.username,
                "ts": time.time(),
            })
    try:
        add_known_group(chat_id, update.chat.title or "Nomsiz guruh")
    except Exception:
        pass


@bot.message_handler(commands=["zayafka_soni"])
def cmd_zayafka_soni(message):
    """Guruhda hozir nechta a'zolik so'rovi kutib turganini ko'rsatadi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return
    chat_id = message.chat.id
    with JOIN_REQ_LOCK:
        count = len(PENDING_JOIN_REQUESTS.get(chat_id, []))
    if count == 0:
        bot.send_message(
            chat_id,
            "📭 Hozircha kutilayotgan a'zolik so'rovi yo'q.\n\n"
            "💡 <i>Eslatma: bu faqat guruh havolasi \"Administrator tasdig'i talab qilinsin\" "
            "rejimida bo'lsa ishlaydi.</i>"
        )
        return
    bot.send_message(
        chat_id,
        f"📋 Hozirda kutilayotgan a'zolik so'rovlari: <b>{count} ta</b>\n\n"
        f"✅ Qabul qilish: <code>/zayafka_qabul {min(count, 150)}</code>\n"
        f"✅ Barchasini qabul qilish: <code>/zayafka_hammasi</code>"
    )


@bot.message_handler(commands=["zayafka_qabul"])
def cmd_zayafka_qabul(message):
    """/zayafka_qabul <soni> — navbatdagi eng birinchi so'rovlardan shuncha
    donasini avtomatik qabul qiladi, qolganini navbatda saqlab qoladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return

    chat_id = message.chat.id
    parts = (message.text or "").split()
    if len(parts) < 2 or not parts[1].isdigit() or int(parts[1]) <= 0:
        bot.send_message(chat_id, "❗ To'g'ri format: <code>/zayafka_qabul 150</code>\n(qabul qilinadigan odamlar soni)")
        return
    soni = int(parts[1])

    with JOIN_REQ_LOCK:
        queue = PENDING_JOIN_REQUESTS.get(chat_id, [])
        if not queue:
            bot.send_message(
                chat_id,
                "📭 Hozircha kutilayotgan a'zolik so'rovi yo'q.\n\n"
                "💡 <i>Eslatma: bu faqat guruh havolasi \"Administrator tasdig'i talab qilinsin\" "
                "rejimida bo'lsa ishlaydi.</i>"
            )
            return
        to_accept = queue[:soni]
        remaining = queue[soni:]
        PENDING_JOIN_REQUESTS[chat_id] = remaining

    status_msg = bot.send_message(
        chat_id,
        f"⏳ {len(to_accept)} ta a'zolik so'rovi qabul qilinmoqda, biroz kuting...\n"
        f"📋 Navbatda yana: {len(remaining)} ta"
    )

    def _worker():
        accepted = 0
        failed = 0
        for req in to_accept:
            try:
                bot.approve_chat_join_request(chat_id, req["user_id"])
                accepted += 1
            except Exception:
                failed += 1
            time.sleep(0.05)  # Telegram limitiga tushib qolmaslik uchun kichik pauza
        try:
            result_text = (
                f"✅ Qabul qilish yakunlandi!\n\n"
                f"👥 Qabul qilindi: <b>{accepted} ta</b>\n"
            )
            if failed:
                result_text += f"⚠️ Xatolik yuz berdi: {failed} ta\n"
            result_text += f"📋 Navbatda qoldi: <b>{len(remaining)} ta</b>"
            bot.edit_message_text(result_text, chat_id, status_msg.message_id)
        except Exception:
            pass

    threading.Thread(target=_worker, daemon=True).start()


@bot.message_handler(commands=["zayafka_hammasi"])
def cmd_zayafka_hammasi(message):
    """Navbatdagi BARCHA a'zolik so'rovlarini qabul qiladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return

    chat_id = message.chat.id
    with JOIN_REQ_LOCK:
        queue = PENDING_JOIN_REQUESTS.get(chat_id, [])
        PENDING_JOIN_REQUESTS[chat_id] = []

    if not queue:
        bot.send_message(chat_id, "📭 Hozircha kutilayotgan a'zolik so'rovi yo'q.")
        return

    status_msg = bot.send_message(chat_id, f"⏳ Barcha {len(queue)} ta so'rov qabul qilinmoqda, biroz kuting...")

    def _worker():
        accepted = 0
        failed = 0
        for req in queue:
            try:
                bot.approve_chat_join_request(chat_id, req["user_id"])
                accepted += 1
            except Exception:
                failed += 1
            time.sleep(0.05)
        try:
            result_text = f"✅ Barcha so'rovlar yakunlandi!\n\n👥 Qabul qilindi: <b>{accepted} ta</b>"
            if failed:
                result_text += f"\n⚠️ Xatolik yuz berdi: {failed} ta"
            bot.edit_message_text(result_text, chat_id, status_msg.message_id)
        except Exception:
            pass

    threading.Thread(target=_worker, daemon=True).start()


@bot.message_handler(commands=["zayafka_rad"])
def cmd_zayafka_rad(message):
    """/zayafka_rad <soni> — navbatdagi eng birinchi so'rovlardan shuncha
    donasini rad etadi (masalan, shubhali/bot akkountlarni tozalash uchun)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return

    chat_id = message.chat.id
    parts = (message.text or "").split()
    if len(parts) < 2 or not parts[1].isdigit() or int(parts[1]) <= 0:
        bot.send_message(chat_id, "❗ To'g'ri format: <code>/zayafka_rad 50</code>\n(rad etiladigan odamlar soni)")
        return
    soni = int(parts[1])

    with JOIN_REQ_LOCK:
        queue = PENDING_JOIN_REQUESTS.get(chat_id, [])
        if not queue:
            bot.send_message(chat_id, "📭 Hozircha kutilayotgan a'zolik so'rovi yo'q.")
            return
        to_decline = queue[:soni]
        remaining = queue[soni:]
        PENDING_JOIN_REQUESTS[chat_id] = remaining

    declined = 0
    for req in to_decline:
        try:
            bot.decline_chat_join_request(chat_id, req["user_id"])
            declined += 1
        except Exception:
            pass
        time.sleep(0.05)

    bot.send_message(
        chat_id,
        f"🚫 Rad etildi: <b>{declined} ta</b>\n📋 Navbatda qoldi: <b>{len(remaining)} ta</b>"
    )


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
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
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
        safe_send(uid, f"🎭 Rolingiz: <b>{role}</b>\n{desc}", kb)

        if team_of(role) == "mafia":
            teammates = [pp["name"] for u2, pp in game["players"].items() if u2 != uid and team_of(pp["role"]) == "mafia"]
            if teammates:
                safe_send(uid, "🕶 Sheriklaringiz: " + ", ".join(teammates) + "\n💬 Ular bilan yashirin gaplashish uchun: <code>/jamoa xabar matni</code>")
            else:
                safe_send(uid, "🕶 Mafiyada yolg'izsiz — ehtiyot bo'ling!")

        # 🕵️‍♂️👮‍♂️ Komissar va Serjant — "Qonun jamoasi": bir-birini bilishadi va
        # o'yin davomida bot orqali yashirin gaplasha oladi (Serjant, Komissar
        # halok bo'lgach uning vazifasini davom ettiradi).
        if role in ("Komissar 🕵️‍♂️", "Serjant 👮‍♂️"):
            law_mates = [pp["name"] for u2, pp in game["players"].items()
                         if u2 != uid and pp["role"] in ("Komissar 🕵️‍♂️", "Serjant 👮‍♂️")]
            if law_mates:
                safe_send(uid, "🕵️‍♂️👮‍♂️ Qonun jamoasidagi sherigingiz: " + ", ".join(law_mates)
                           + "\n💬 U bilan yashirin gaplashish uchun: <code>/adolat xabar matni</code>")

        # 🕵️ Maxfiy missiya — har bir o'yinchiga tasodifiy shaxsiy topshiriq beriladi,
        # faqat o'ziga ko'rinadi. O'yin oxirida bajarilgan-bajarilmagani tekshiriladi.
        mission = random.choice(SECRET_MISSIONS)
        game["secret_missions"][uid] = mission["key"]
        safe_send(uid, f"🕵️ Maxfiy missiya: <i>{mission['text']}</i>\n(O'yin oxirida bajarilgan-bajarilmaganingiz tekshiriladi — bajarsangiz +25$.)")

    bot.send_message(chat_id, f"🌙 <b>O'yin boshlandi!</b> {len(game['players'])} kishiga rol berildi. Roldan DM'da qarang.")
    start_night(chat_id)


def _assign_no_repeat(uids, pool):
    """`uids` ro'yxatidagi har bir o'yinchiga `pool` dagi rollarni, iloji boricha
    o'sha o'yinchining OXIRGI o'ynagan roli bilan bir xil bo'lmaydigan qilib
    taqsimlaydi (bir xil rol ketma-ket 2 marta bir kishiga tushmasin degan talab).
    Agar imkoni bo'lmasa (masalan, kichik o'yin, muqobil yo'q) — eng kam
    to'qnashuvli variant qaytariladi."""
    best = None
    for _ in range(40):
        shuffled = pool[:]
        random.shuffle(shuffled)
        conflicts = sum(
            1 for uid, role in zip(uids, shuffled)
            if get_charges(uid).get("last_role") == role
        )
        if conflicts == 0:
            return list(zip(uids, shuffled))
        if best is None or conflicts < best[0]:
            best = (conflicts, list(zip(uids, shuffled)))
    return best[1] if best else list(zip(uids, pool))


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

    # 🎲 rol — o'yinchining oldingi o'yindagi roliga imkon qadar mos kelmaydigan qilib taqsimlanadi
    for uid, role in _assign_no_repeat(remaining_players, pool):
        p = game["players"][uid]
        p["role"], p["team"], p["alive"] = role, team_of(role), True

    # keyingi o'yinda solishtirish uchun har bir o'yinchining ENDIGI rolini "last_role" sifatida saqlaymiz
    for uid in player_ids:
        ch = get_charges(uid)
        ch["last_role"] = game["players"][uid]["role"]
        set_charges(uid, ch)

    # 🏆 Geroy (Elandriel/Zephyrion "Boylik siri") — har o'yin boshlanganda avtomatik +1 💎
    for uid in player_ids:
        if hero_has_ability(uid, "diamond_trickle"):
            add_balance(uid, diamond=1)
            safe_send(uid, "💎 Geroyingiz sizga bu o'yin uchun +1 Olmos in'om qildi!")

    game["forced_roles"] = {}


# ================================================================================
#  /Sotop
# ================================================================================

@bot.message_handler(commands=["Sotop", "sotop"])
def cmd_sotop(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return
    chat_id = message.chat.id
    if chat_id in GAMES:
        del GAMES[chat_id]
        save_games_state()
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

    # 🏆 Geroy — har tun yangidan qo'lda faollashtiriladigan himoya holatini tozalaymiz
    game["hero_armed_defense"] = set()

    # ============================================================================
    #  🚨 AFK NAZORATI — o'tgan tunda taklif olib, javob bermagan o'yinchilarni
    #  belgilaymiz. 2 tun ketma-ket harakat qilmasa, shu tunda avtomatik chiqariladi.
    # ============================================================================
    prev_prompted = game.get("prompted_tonight", set())
    prev_responded = game.get("responded_tonight", set())
    afk_streak = game.setdefault("afk_streak", {})
    kicked_afk = []
    for uid in prev_prompted:
        p = game["players"].get(uid)
        if not p or not p["alive"]:
            continue
        if uid in prev_responded:
            afk_streak[uid] = 0
        else:
            afk_streak[uid] = afk_streak.get(uid, 0) + 1
            if afk_streak[uid] >= 2:
                p["alive"] = False
                kicked_afk.append(uid)
                afk_streak[uid] = 0
    for uid in kicked_afk:
        p = game["players"][uid]
        p["left_game"] = True  # 🚪 o'yin oxirida avtomatik mag'lub sifatida hisoblanadi
        joke = random.choice(AFK_KICK_JOKES).format(who=mention(uid, p["name"]), role=f"<b>{p['role']}</b>")
        bot.send_message(chat_id, joke)
        safe_send(uid, "😴 Siz 2 tun ketma-ket harakatsiz qolganingiz uchun o'yindan avtomatik chiqarildingiz.")
        add_points(uid, -10, "afk_kick")
    if kicked_afk and check_and_end_game(chat_id):
        return

    game["phase"] = "night"
    game["mafia_votes"] = {}
    game["doctor_target"] = None
    game["komissar_action"] = None
    game["komissar_target"] = None
    game["night_announced"] = set()
    game["prompted_tonight"] = set()
    game["responded_tonight"] = set()
    # o'tgan kunning bir martalik grantlari (Advokat himoyasi, Provokator, Sudya)
    # yangi tunda qayta tanlanadi, shuning uchun bu yerda tozalanadi
    game["advocate_protect"] = None
    game["forced_day_votes"] = {}
    game["judge_double_vote"] = None

    send_scene_photo(
        chat_id, NIGHT_PHOTO_LOCAL, NIGHT_PHOTO,
        caption=f"🌙 <b>{game['day_number']}-tun.</b> Shahar uxlamoqda... Guruhda yozish taqiqlangan.\n"
                "Rolga ega o'yinchilar — botning shaxsiy chatida sizni tanlov kutmoqda. 🤖",
        reply_markup=_bot_dm_button(),
    )

    # 🌙 Tungi atmosfera matnlari — faol (tirik) o'yinchilarning rollariga qarab (qoshimchakod2.py g'oyasi)
    flavor_lines = alive_role_flavor_lines(game)
    if flavor_lines:
        bot.send_message(chat_id, "🌙 <b>Tun voqealari:</b>\n\n" + "\n".join(flavor_lines))

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
        game["prompted_tonight"].add(uid)

    kom_uids = alive_role_holders(game, lambda r: r == "Komissar 🕵️‍♂️")
    for uid in kom_uids:
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("🔍 Tekshirish", callback_data=f"na|{chat_id}|komaction|check"),
            types.InlineKeyboardButton("🎯 O'ldirish", callback_data=f"na|{chat_id}|komaction|kill"),
        )
        kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"na|{chat_id}|komaction|skip"))
        safe_send(uid, "🕵️‍♂️ <b>Bu tun nima qilamiz?</b>", kb)
        game["prompted_tonight"].add(uid)

    doc_uids = alive_role_holders(game, lambda r: r == "Doktor 👨‍⚕️")
    for uid in doc_uids:
        kb = types.InlineKeyboardMarkup()
        for target_id, p in alive.items():
            kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"na|{chat_id}|doctor|{target_id}"))
        kb.add(types.InlineKeyboardButton("🚫 Hech kimni davolamaslik", callback_data=f"na|{chat_id}|doctor|skip"))
        safe_send(uid, "👨‍⚕️ <b>Kimni davolaysiz?</b>", kb)
        game["prompted_tonight"].add(uid)

    # ============================================================================
    #  QO'SHIMCHA 25 ROL — hech biri chetda qolmasin, barchasi tunda o'z
    #  qobiliyatini ishlata oladi (asosiy rollar kabi shaxsiy DM orqali).
    # ============================================================================
    game["extra_actions"] = {}
    komissar_alive = bool(alive_role_holders(game, lambda r: r == "Komissar 🕵️‍♂️"))
    for uid, p in alive.items():
        role = p["role"]
        slug = EXTRA_ROLE_SLUGS.get(role)
        if not slug or slug == "arvoh":
            continue
        if slug == "serjant" and komissar_alive:
            continue  # Serjant faqat Komissar halok bo'lganda faollashadi
        if slug == "snayper" and uid in game.get("snayper_used", set()):
            continue  # Snayper qobiliyati butun o'yin davomida faqat 1 marta ishlaydi
        prompt_text, _flavor = EXTRA_ROLE_PROMPTS[slug]
        kb = types.InlineKeyboardMarkup()
        if slug in EXTRA_ROLE_YESNO:
            kb.add(
                types.InlineKeyboardButton("✅ Ha", callback_data=f"na|{chat_id}|ex|{slug}:yes"),
                types.InlineKeyboardButton("🚫 Yo'q", callback_data=f"na|{chat_id}|ex|{slug}:no"),
            )
        else:
            for target_id, tp in alive.items():
                if target_id == uid and slug not in EXTRA_ROLE_SELF_TARGET_OK:
                    continue
                kb.add(types.InlineKeyboardButton(tp["name"], callback_data=f"na|{chat_id}|ex|{slug}:{target_id}"))
            kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"na|{chat_id}|ex|{slug}:skip"))
        safe_send(uid, f"{ROLES_INFO.get(role, '')}\n\n{prompt_text}", kb)
        game["prompted_tonight"].add(uid)

    # 👻 Arvoh — faqat o'lgandan keyin faollashadi, tirik o'yinchiga sirli imo-ishora beradi
    if alive:
        for uid, p in game["players"].items():
            if p["alive"] or p["role"] != "Arvoh 👻":
                continue
            kb = types.InlineKeyboardMarkup()
            for target_id, tp in alive.items():
                kb.add(types.InlineKeyboardButton(tp["name"], callback_data=f"na|{chat_id}|ex|arvoh:{target_id}"))
            kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"na|{chat_id}|ex|arvoh:skip"))
            safe_send(uid, EXTRA_ROLE_PROMPTS["arvoh"][0], kb)

    # 🏆 Geroy — himoyaga ega (Draven/Zephyrion) o'yinchilarga har tun eslatma + tugma
    for uid, p in alive.items():
        if hero_has_ability(uid, "survive") or hero_has_ability(uid, "revive_once"):
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("🛡 Geroy himoyasini faollashtirish", callback_data=f"heroarm|defense|{chat_id}"))
            safe_send(uid, "🏆 Geroyingiz bu tun himoya qobiliyatini taklif qilmoqda. Xohlasangiz faollashtiring "
                           "(faollashtirmasangiz, bu tun geroyingiz sizni himoya QILMAYDI):", kb)

    t = threading.Timer(NIGHT_SECONDS, lambda: resolve_night(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)

    # 🔄 checkpoint — bot qayta ishga tushsa, shu tundan qolgan vaqtni hisoblab davom etadi
    game["day_sub_phase"] = None
    game["phase_deadline"] = time.time() + NIGHT_SECONDS
    save_games_state()


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

    # 🚨 AFK nazorati — foydalanuvchi shu tunda javob berdi, streak nolga tushadi
    game.setdefault("responded_tonight", set()).add(uid)
    # 🏅 Faollik balli — har bir tungi harakat uchun +1 (o'yin oxirida eng faol o'yinchi aniqlanadi)
    game.setdefault("activity_score", {})
    game["activity_score"][uid] = game["activity_score"].get(uid, 0) + 1

    if kind == "mafia":
        target = value if value == "skip" else int(value)
        game["mafia_votes"][uid] = target
        if "mafia" not in game["night_announced"]:
            game["night_announced"].add("mafia")
            bot.send_message(chat_id, "🕶 <i>Mafiya soyada birlashib, o'ljasini muhokama qilmoqda...</i>")
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
        if "komissar" not in game["night_announced"]:
            game["night_announced"].add("komissar")
            if value == "check":
                bot.send_message(chat_id, "🕵️ <i>Komissar biror kishining hujjatlarini tekshirishga tayyorlanmoqda...</i>")
            else:
                bot.send_message(chat_id, "🎯 <i>Komissar hukm chiqarishga qaror qildi — kimdir bu tundan tirik chiqmasligi mumkin...</i>")
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
        notify_target_touched(game, target_id)
        if game["komissar_action"] == "check":
            target_charges = get_charges(target_id)
            name = game["players"].get(target_id, {}).get("name", "?")
            if target_charges.get("fake_doc", 0) > 0 and is_item_active(target_id, "fake_doc"):
                use_charge(target_id, "fake_doc")
                role_shown = "Tinch aholi 👨‍👩‍👧‍👦"
                # 🔧 TUZATILDI: avval bu yerda hech qanday DM yuborilmas edi
                safe_send(target_id, "📁 Sizning <b>Soxta hujjat</b> buyumingiz ishladi — Komissar sizni tekshirganda haqiqiy rolingiz yashirin qoldi!")
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
        if target != "skip":
            notify_target_touched(game, target)
        if target != "skip" and "doctor" not in game["night_announced"]:
            game["night_announced"].add("doctor")
            bot.send_message(chat_id, "🩺 <i>Doktor navbatchilikka chiqdi, kimnidir davolashga shay turibdi...</i>")
        try:
            bot.edit_message_text("✅ Davolash tanlovi qabul qilindi.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "Qabul qilindi!")

    elif kind == "ex":
        # qo'shimcha 25 rolning tungi harakatlari — value = "{slug}:{target_yoki_skip/yes/no}"
        if ":" not in value:
            bot.answer_callback_query(call.id, "Xatolik yuz berdi.")
            return
        slug, target_s = value.split(":", 1)
        role_name = SLUG_TO_ROLE.get(slug)
        if not role_name or game["players"].get(uid, {}).get("role") != role_name:
            bot.answer_callback_query(call.id, "Bu tanlov endi amal qilmaydi.")
            return

        def _announce_once():
            if slug not in game["night_announced"]:
                game["night_announced"].add(slug)
                bot.send_message(chat_id, EXTRA_ROLE_PROMPTS[slug][1])

        # --- darhol natija beradigan (tekshiruv) rollar: Josus, Bomj, Serjant ---
        if slug in EXTRA_ROLE_INSTANT_INFO:
            if target_s == "skip":
                result = "🚫 Siz bu tun harakat qilmaslikni tanladingiz."
            else:
                target_id = int(target_s)
                tname = game["players"].get(target_id, {}).get("name", "?")
                trole = game["players"].get(target_id, {}).get("role", "Noma'lum")
                notify_target_touched(game, target_id)
                if slug == "josus":
                    result = f"🕵️ Tekshiruv natijasi: <b>{tname}</b> — taraf: <b>{team_of(trole)}</b>"
                elif slug == "serjant":
                    result = f"👮‍♂️ Tekshiruv natijasi: <b>{tname}</b> — <b>{trole}</b>"
                else:  # bomj — tasodifiy ehtimol bilan aniqlaydi
                    if random.random() < 0.5:
                        result = f"🧟‍♂️ Siz tasodifan bilib oldingiz: <b>{tname}</b> — <b>{trole}</b>"
                    else:
                        result = "🧟‍♂️ Afsuski, bu tun hech narsani aniq bila olmadingiz."
                _announce_once()
            try:
                bot.edit_message_text(result, call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- Advokat: ertangi kunduzgi osishdan himoya belgilanadi ---
        if slug == "advokat":
            if target_s != "skip":
                game["advocate_protect"] = int(target_s)
                notify_target_touched(game, int(target_s))
                _announce_once()
            try:
                bot.edit_message_text("✅ Himoya tanlovingiz qabul qilindi.", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- Provokator: tanlangan o'yinchining ertangi ovozi majburan boshqaga burib yuboriladi ---
        if slug == "provokator":
            if target_s != "skip":
                target_id = int(target_s)
                notify_target_touched(game, target_id)
                alive_others = [pid for pid in alive_players(game) if pid not in (uid, target_id)]
                if alive_others:
                    game.setdefault("forced_day_votes", {})[target_id] = random.choice(alive_others)
                    _announce_once()
                    fb = "✅ Tanlovingiz qabul qilindi — ertaga uning ovozi majburan burib yuboriladi."
                else:
                    # 🔧 TUZATILDI: juda kam tirik o'yinchi qolganda jim-jit "hech narsa bo'lmadi"
                    # taassurotini beruvchi eski xatolik — endi sabab ANIQ tushuntiriladi.
                    fb = "⚠️ Hozir yetarli boshqa tirik o'yinchi yo'q — bu safar ovozni burib bo'lmadi."
            else:
                fb = "🚫 Siz bu tun harakat qilmaslikni tanladingiz."
            try:
                bot.edit_message_text(fb, call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- Sudya: ertangi kun ovozini 2x kuchga ega qiladi ---
        if slug == "sudya":
            if target_s == "yes":
                game["judge_double_vote"] = uid
                _announce_once()
            try:
                bot.edit_message_text("✅ Tanlovingiz qabul qilindi.", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- O'g'ri: tanlangan o'yinchidan darhol pul o'g'irlaydi ---
        if slug == "ogri":
            if target_s != "skip":
                target_id = int(target_s)
                notify_target_touched(game, target_id)
                tu = user_dict(target_id)
                steal = min(tu.get("dollar", 0), random.randint(20, 100))
                if steal > 0:
                    update_user(target_id, dollar=tu["dollar"] - steal)
                    add_balance(uid, dollar=steal)
                    feedback = f"🥷 Siz {game['players'][target_id]['name']}dan ${steal} o'g'irladingiz!"
                else:
                    feedback = "🥷 Uning cho'ntagi bo'sh ekan, hech narsa topa olmadingiz."
                _announce_once()
            else:
                feedback = "🚫 Siz bu tun harakat qilmaslikni tanladingiz."
            try:
                bot.edit_message_text(feedback, call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- Arvoh (o'lgandan keyin): tirik o'yinchiga sirli imo-ishora yuboradi ---
        if slug == "arvoh":
            if target_s != "skip":
                target_id = int(target_s)
                game["players"][uid]["ghost_hint_given"] = True
                safe_send(target_id, "👻 <i>G'ayrioddiy sovuq shabada his qildingiz... kimdir sizga nimadir "
                                      "aytmoqchidek bo'ldi, lekin so'zlar tushunarsiz bo'lib qoldi.</i>")
                _announce_once()
            try:
                bot.edit_message_text("✅ Qabul qilindi.", call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            bot.answer_callback_query(call.id, "Qabul qilindi!")
            return

        # --- Qolganlari (Qotil/Manyak/Mergan/Snayper/Telba/Fohisha/Sehrgar/
        #     General/Arxitektor/Qorovul/Sadoqatli yordamchi) — tun yakunida
        #     resolve_night() ichida birgalikda hisoblanadi ---
        target = target_s if target_s == "skip" else int(target_s)
        game.setdefault("extra_actions", {})[slug] = {"actor": uid, "target": target}
        if target != "skip":
            _announce_once()
        try:
            bot.edit_message_text("✅ Tanlovingiz qabul qilindi.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.answer_callback_query(call.id, "Qabul qilindi!")


def apply_kill(game, uid, killed_set, bypass_protection=False, attacker_uids=None):
    """Bitta o'yinchini o'ldirish urinishi — shield/revive/doktor davolashi hisobga olinadi.
    attacker_uids — (ixtiyoriy) shu hujumni amalga oshirgan o'yinchi(lar) ID'lari; agar
    geroy qobiliyati himoya qilib qolsa, ularga ANONIM tarzda DM yuboriladi."""
    if uid is None or uid == "skip" or uid not in game["players"]:
        return
    p = game["players"][uid]
    if not p["alive"] or uid in killed_set:
        return
    if not bypass_protection:
        if game.get("doctor_target") == uid:
            return
        if uid in game.get("night_protected", set()):
            return
        # 👶 Beshikdagi bola — o'yinning birinchi tunida hech kim unga tega olmaydi
        if p["role"] == "Beshikdagi bola 👶" and game.get("day_number", 0) <= 1:
            return
        # 🪓 Varvar — baquvvat jangchi, ayrim hujumlarga qarshilik ko'rsatadi (30% ehtimol)
        if p["role"] == "Varvar 🪓" and random.random() < 0.3:
            return
        # 🏆 Geroy (Draven / Zephyrion) — FAQAT o'zi /geroy_qalqon bilan shu tunga QO'LDA
        # faollashtirgan bo'lsa ishlaydi (avtomatik EMAS). Avval kafolatlangan "revive_once"
        # (agar hali sarflanmagan bo'lsa), aks holda oddiy % ehtimolli "survive" tekshiriladi.
        if uid in game.get("hero_armed_defense", set()):
            if hero_has_ability(uid, "revive_once") and uid not in game.setdefault("hero_revive_used", set()):
                game["hero_revive_used"].add(uid)
                bot.send_message(game["chat_id"], "🔥 <i>Kimningdir geroyi o'limni yengib, uni oxirgi marta hayotga qaytardi!</i>")
                safe_send(uid, "🔥 Geroyingizning bir martalik qobiliyati ishga tushdi — bu safar o'limdan qutuldingiz! (Endi sarflandi.)")
                for a_uid in (attacker_uids or []):
                    safe_send(a_uid, "🏆 <i>Nishoningiz kimningdir geroy qobiliyati tufayli o'limdan qutulib qoldi...</i>")
                return
            h_chance = hero_survive_chance(uid)
            if h_chance > 0 and random.random() < h_chance:
                bot.send_message(game["chat_id"], "🏆 <i>Kimningdir geroyi uni tunda hujumdan qutqarib qoldi!</i>")
                safe_send(uid, "🏆 Geroyingiz faollashtirilgan edi — bu kecha sizga hujum qilishdi, lekin geroyingiz sizni qutqardi!")
                for a_uid in (attacker_uids or []):
                    safe_send(a_uid, "🏆 <i>Nishoningiz kimningdir geroy qobiliyati tufayli hujumdan omon qoldi...</i>")
                return
        if consume_shield(uid):
            bot.send_message(game["chat_id"], "🛡 <i>Kimningdir maxsus buyumi uni tunda hujumdan asrab qoldi!</i>")
            safe_send(uid, "🛡 Bu kecha sizga hujum qilishdi, lekin buyumingiz sizni himoya qildi!")
            return
        if is_item_active(uid, "revive") and use_charge(uid, "revive"):
            bot.send_message(game["chat_id"], "⚡️ <i>Kimningdir tezkor jonlanish tumori uni o'limdan qutqarib qoldi!</i>")
            safe_send(uid, "⚡️ Bu kecha sizga hujum qilishdi, lekin Tezkor jonlanish tumoringiz sizni qutqardi!")
            return
    killed_set.add(uid)


def resolve_night(chat_id):
    with GAME_LOCK:
        game = GAMES.get(chat_id)
        if not game or game["phase"] != "night":
            return

        # ========================================================================
        #  QO'SHIMCHA ROLLAR — 1-bosqich: bloklash va himoya (kimlar bloklandi/
        #  himoyalandi, boshqa harakatlardan OLDIN aniqlanishi kerak)
        # ========================================================================
        extra = game.get("extra_actions", {})
        roleblocked = set()
        night_protected = set()

        fohisha_act = extra.get("fohisha")
        if fohisha_act and fohisha_act["target"] != "skip":
            roleblocked.add(fohisha_act["target"])

        # 🧙‍♂️ Sehrgar — bashorat qilib bo'lmaydigan sehr: yo himoya, yoki bloklash
        sehrgar_act = extra.get("sehrgar")
        if sehrgar_act and sehrgar_act["target"] != "skip":
            t = sehrgar_act["target"]
            if random.random() < 0.5:
                night_protected.add(t)
            else:
                roleblocked.add(t)

        for slug in ("general", "arxitektor", "qorovul", "sadoqat", "sehryor"):
            act = extra.get(slug)
            if act and act["target"] != "skip":
                night_protected.add(act["target"])
                notify_target_touched(game, act["target"])
        game["night_protected"] = night_protected

        if fohisha_act and fohisha_act["target"] != "skip":
            notify_target_touched(game, fohisha_act["target"])
        if sehrgar_act and sehrgar_act["target"] != "skip":
            notify_target_touched(game, sehrgar_act["target"])

        if roleblocked:
            doctor_uid = next(iter(alive_role_holders(game, lambda r: r == "Doktor 👨‍⚕️")), None)
            komissar_uid = next(iter(alive_role_holders(game, lambda r: r == "Komissar 🕵️‍♂️")), None)
            for voter in list(game["mafia_votes"].keys()):
                if voter in roleblocked:
                    game["mafia_votes"][voter] = "skip"
            if doctor_uid in roleblocked:
                game["doctor_target"] = "skip"
            if komissar_uid in roleblocked:
                game["komissar_action"] = "skip"
            for act in extra.values():
                if act["actor"] in roleblocked:
                    act["target"] = "skip"

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
            if target_charges.get("confuse", 0) > 0 and is_item_active(mafia_kill_target, "confuse"):
                use_charge(mafia_kill_target, "confuse")
                # 🔧 TUZATILDI: avval bu yerda hech qanday DM yuborilmas edi — endi
                # o'zining "Tushunarsiz xat" buyumi ishlaganini albatta biladi.
                safe_send(mafia_kill_target, "✉️ Sizning <b>Tushunarsiz xat</b> buyumingiz ishladi — mafiyaning hujumi sizdan chalg'itib yuborildi!")
                alt = [uid for uid, p in alive_players(game).items()
                       if uid != mafia_kill_target and team_of(p["role"]) != "mafia"]
                if alt:
                    mafia_kill_target = random.choice(alt)

            # 🟡 Oltin o'q — mafiyalardan birortasida bo'lsa himoyani chetlab o'tadi
            for voter_uid, target in game["mafia_votes"].items():
                if target == mafia_kill_target and get_charges(voter_uid).get("golden_bullet", 0) > 0 and is_item_active(voter_uid, "golden_bullet"):
                    use_charge(voter_uid, "golden_bullet")
                    bypass_for_mafia = True
                    safe_send(voter_uid, "🟡 Bu kecha 🟡 Oltin o'qingiz ishlatildi — bu safar hujumingiz barcha himoyalarni chetlab o'tadi!")
                    break

        # 🕵️ Missiya kuzatuvi — ertangi kunduzgi ovoz berish uchun "bugungi tunda
        # mafiya kimni nishonga oldi" ma'lumotini saqlaymiz
        game["last_night_mafia_target"] = mafia_kill_target

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
        attempted_targets = set()
        if mafia_kill_target is not None:
            attempted_targets.add(mafia_kill_target)
            notify_target_touched(game, mafia_kill_target)
        apply_kill(game, mafia_kill_target, killed, bypass_protection=bypass_for_mafia,
                   attacker_uids=[v for v, t in game["mafia_votes"].items() if t == mafia_kill_target])

        if game.get("komissar_action") == "kill" and game.get("komissar_target"):
            attempted_targets.add(game["komissar_target"])
            _kom_uid = next(iter(alive_role_holders(game, lambda r: r == "Komissar 🕵️‍♂️")), None)
            apply_kill(game, game["komissar_target"], killed, attacker_uids=[_kom_uid] if _kom_uid else None)

        # 🧪 Zaharli flakon — /zahar orqali belgilanganlar
        poison_targets = game.pop("poison_marks", set())
        for pt in poison_targets:
            attempted_targets.add(pt)
            # 🩹 Kichik Aptechka — zaharga qarshi 1 martalik avtomatik davo
            if get_charges(pt).get("antidote", 0) > 0 and is_item_active(pt, "antidote"):
                use_charge(pt, "antidote")
                safe_send(pt, "🩹 Sizni kimdir zaharlamoqchi bo'ldi, lekin Aptechkangiz avtomatik davoladi!")
                continue
            apply_kill(game, pt, killed)
        game["poison_marks"] = set()

        # ========================================================================
        #  QO'SHIMCHA ROLLAR — 2-bosqich: mustaqil qotillar (Qotil/Manyak/Mergan/Snayper)
        #  va Telba ning tasodifiy harakati
        # ========================================================================
        for slug in ("qotil", "manyak", "mergan"):
            act = extra.get(slug)
            if act and act["target"] != "skip":
                notify_target_touched(game, act["target"])
                attempted_targets.add(act["target"])
                actor_role = game["players"].get(act["actor"], {}).get("role")
                if actor_role and act["target"] not in visitor_role_of:
                    visitor_role_of[act["target"]] = actor_role
                apply_kill(game, act["target"], killed, attacker_uids=[act["actor"]])

        snayper_act = extra.get("snayper")
        if snayper_act and snayper_act["target"] != "skip":
            notify_target_touched(game, snayper_act["target"])
            attempted_targets.add(snayper_act["target"])
            actor_role = game["players"].get(snayper_act["actor"], {}).get("role")
            if actor_role and snayper_act["target"] not in visitor_role_of:
                visitor_role_of[snayper_act["target"]] = actor_role
            apply_kill(game, snayper_act["target"], killed, attacker_uids=[snayper_act["actor"]])
            game.setdefault("snayper_used", set()).add(snayper_act["actor"])

        telba_triggered = False
        telba_act = extra.get("telba")
        if telba_act and telba_act["target"] != "skip":
            notify_target_touched(game, telba_act["target"])
            if random.random() < 0.5:
                telba_triggered = True
                attempted_targets.add(telba_act["target"])
                if telba_act["target"] not in visitor_role_of:
                    visitor_role_of[telba_act["target"]] = "Telba 🤪"
                apply_kill(game, telba_act["target"], killed, attacker_uids=[telba_act["actor"]])

        # ========================================================================
        #  QO'SHIMCHA ROLLAR — 3-bosqich: har bir rolga o'z harakati natijasi
        #  haqida shaxsiy (DM) hisobot — foydali/foydasiz bo'lganini bildiradi
        # ========================================================================
        doctor_uid = next(iter(alive_role_holders(game, lambda r: r == "Doktor 👨‍⚕️")), None)
        if doctor_uid and game.get("doctor_target") not in (None, "skip"):
            d_target = game["doctor_target"]
            t_name = game["players"].get(d_target, {}).get("name", "?")
            if d_target in attempted_targets:
                safe_send(doctor_uid, f"🩺 Bu kecha {mention(d_target, t_name)}ga yordam berdingiz — hujumdan qutqardingiz!")
            else:
                safe_send(doctor_uid, f"🩺 Hech kim {mention(d_target, t_name)}ga hujum qilishga urinmadi — bu safar yordamingiz kerak bo'lmadi.")

        for slug in ("general", "arxitektor", "qorovul", "sadoqat", "sehryor"):
            act = extra.get(slug)
            if act and act["target"] != "skip":
                t_name = game["players"].get(act["target"], {}).get("name", "?")
                if act["target"] in attempted_targets:
                    safe_send(act["actor"], f"🛡 Himoyangiz ishladi! {mention(act['target'], t_name)} tunni omon o'tkazdi.")
                else:
                    safe_send(act["actor"], "😌 Hech kim hujum qilmagani uchun bu kecha himoyangiz kerak bo'lmadi.")

        for slug in ("qotil", "manyak", "mergan"):
            act = extra.get(slug)
            if act and act["target"] != "skip":
                t_name = game["players"].get(act["target"], {}).get("name", "?")
                if act["target"] in killed:
                    safe_send(act["actor"], f"🗡 Nishoningiz {mention(act['target'], t_name)} halok bo'ldi.")
                else:
                    safe_send(act["actor"], f"🛡 {mention(act['target'], t_name)}ni maqsad qilgan edingiz, lekin kimningdir himoyasi tufayli u omon qoldi.")

        # 🔧 TUZATILDI: Telba roliga avval HECH QANDAY natija xabari yuborilmas
        # edi (boshqa barcha rollarga yuboriladi) — endi u ham o'z tasodifiy
        # harakati natijasi haqida ANIQ shaxsiy xabar oladi.
        if telba_act and telba_act["target"] != "skip":
            t_name = game["players"].get(telba_act["target"], {}).get("name", "?")
            if telba_triggered and telba_act["target"] in killed:
                safe_send(
                    telba_act["actor"],
                    f"🤪 Tasodifiy taqdir kulib boqdi... {mention(telba_act['target'], t_name)} sizning "
                    f"g'ayrioddiy harakatingiz qurboni bo'ldi!",
                )
            elif telba_triggered:
                safe_send(
                    telba_act["actor"],
                    f"🤪 Siz {mention(telba_act['target'], t_name)}ga hujum qilishga urindingiz, lekin "
                    f"kimningdir himoyasi tufayli u omon qoldi.",
                )
            else:
                safe_send(
                    telba_act["actor"],
                    f"🤪 Bu safar taqdir boshqacha hal qildi — {mention(telba_act['target'], t_name)}ga "
                    f"hech narsa bo'lmadi. Telbaning harakati har doim ham natija bermaydi!",
                )

        if snayper_act and snayper_act["target"] != "skip":
            t_name = game["players"].get(snayper_act["target"], {}).get("name", "?")
            if snayper_act["target"] in killed:
                safe_send(snayper_act["actor"], f"🎯 Otganingiz aniq tegdi — {mention(snayper_act['target'], t_name)} halok bo'ldi.")
            else:
                safe_send(snayper_act["actor"], f"🛡 {mention(snayper_act['target'], t_name)}ni nishonga oldingiz, lekin himoyasi uni qutqardi.")

        if fohisha_act and fohisha_act["target"] != "skip":
            t_name = game["players"].get(fohisha_act["target"], {}).get("name", "?")
            safe_send(fohisha_act["actor"], f"💋 {mention(fohisha_act['target'], t_name)}ni band qildingiz — u bu kecha qobiliyatini ishlata olmadi.")

        if sehrgar_act and sehrgar_act["target"] != "skip":
            t_name = game["players"].get(sehrgar_act["target"], {}).get("name", "?")
            if sehrgar_act["target"] in night_protected:
                safe_send(sehrgar_act["actor"], f"🧙‍♂️ Sehringiz {mention(sehrgar_act['target'], t_name)}ni himoyaladi!")
            else:
                safe_send(sehrgar_act["actor"], f"🧙‍♂️ Sehringiz {mention(sehrgar_act['target'], t_name)}ning qobiliyatini bloklab qo'ydi!")

        if killed:
            for uid in killed:
                game["players"][uid]["alive"] = False
                name = game["players"][uid]["name"]
                role = game["players"][uid]["role"]
                visitor = visitor_role_of.get(uid)
                text = f"☠️ Tunda {mention(uid, name)} vahshiylarcha o'ldirildi!\nFosh qilingan roli: <b>{role}</b>"
                if visitor:
                    text += f"\n<i>{VISIT_PHRASE.get(visitor, f'Aytishlaricha unikiga {visitor} kelgan...')}</i>"
                bot.send_message(chat_id, text)
                handle_death_side_effects(game, chat_id, uid)  # 👑 Don vorisligi / 👻 Arvoh faollashuvi
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
            if p["alive"] and ch.get("night_vision", 0) > 0 and is_item_active(uid, "night_vision"):
                use_charge(uid, "night_vision")
                text = "🥽 Bu tun faol bo'lgan rollar: " + (", ".join(acted_roles) if acted_roles else "hech kim")
                safe_send(uid, text)

        # 🏆 Geroy (Seraphine/Zephyrion "Tungi nazar") — har tun avtomatik, bepul,
        # nechta o'yinchi faol harakat qilganini (kimligini emas) DM orqali bildiradi
        active_count = len(game.get("responded_tonight", set()))
        for uid, p in list(game["players"].items()):
            if p["alive"] and hero_has_ability(uid, "night_vision_auto"):
                safe_send(uid, f"👁 Geroyingiz sizga pichirlaydi: bu tun <b>{active_count}</b> ta o'yinchi faol harakat qildi.")

        if check_and_end_game(chat_id):
            return

        bot.send_message(chat_id, roster_breakdown_text(game))
        start_day(chat_id)


def handle_death_side_effects(game, chat_id, uid):
    """💀 Bir o'yinchi (istalgan sabab bilan — tunda o'ldirilgan, kunduzi osilgan
    yoki o'zi tark etgan) halok bo'lgach chaqiriladi. Ikkita muhim narsani bajaradi:

      1) 👑 DON VORISLIGI — agar halok bo'lgan DON bo'lsa, tirik qolgan
         Mafia 🕶 a'zolaridan biri tasodifiy tarzda yangi DON etib
         ko'tariladi (Almex Black Bot uslubi: "Siz endi DON bo'ldingiz!").
      2) 👻 ARVOH FAOLLASHUVI — agar halok bo'lgan Arvoh bo'lsa, unga o'zining
         yangi (o'limdan keyingi) qobiliyati haqida aniq tushuntirish yuboriladi
         (aks holda o'yinchi "hech narsa bo'lmadi" deb o'ylashi mumkin edi)."""
    p = game["players"].get(uid)
    if not p:
        return
    role = p.get("role")

    if role == "Don 🎩":
        candidates = [c_uid for c_uid, cp in alive_players(game).items() if cp["role"] == "Mafia 🕶"]
        if candidates:
            new_don = random.choice(candidates)
            game["players"][new_don]["role"] = "Don 🎩"
            safe_send(
                new_don,
                "👑 <b>Siz endi DON bo'ldingiz!</b>\n"
                "Mafiya guruhining yangi rahbari — endigi tunlardan boshlab sheriklaringiz "
                "bilan birga qurbon tanlash huquqi (mafiya ovozi) sizga o'tdi.",
            )
            bot.send_message(chat_id, "👑 <i>Mafiya safida yangi kuch markazi shakllandi... kimdir soyada DON martabasiga ko'tarildi.</i>")

    if role == "Arvoh 👻":
        safe_send(
            uid,
            "👻 <b>Siz Arvohga aylandingiz!</b>\n"
            "Tanangiz halok bo'ldi, ammo ruhingiz o'yinda qoladi. Endi har tun tirik "
            "o'yinchilardan biriga botning shaxsiy chatida sirli imo-ishora yubora olasiz "
            "— bunday xabar sizga tunning boshida avtomatik keladi.",
        )


def get_faction_teammates(game, uid):
    """Foydalanuvchining joriy o'yindagi yashirin 'jamoasi' a'zolarini qaytaradi:
      • ("mafia", [...]) — Don 🎩 + Mafia 🕶 (tirik bo'lganlari)
      • ("qonun", [...]) — Komissar 🕵️‍♂️ + Serjant 👮‍♂️ (tirik bo'lganlari)
      • (None, []) — jamoasi yo'q (yakka rol yoki Tinch aholi)"""
    p = game["players"].get(uid)
    if not p or not p["alive"]:
        return None, []
    role = p["role"]
    if team_of(role) == "mafia":
        mates = [u2 for u2, pp in game["players"].items()
                 if u2 != uid and pp["alive"] and team_of(pp["role"]) == "mafia"]
        return "mafia", mates
    if role in ("Komissar 🕵️‍♂️", "Serjant 👮‍♂️"):
        mates = [u2 for u2, pp in game["players"].items()
                 if u2 != uid and pp["alive"] and pp["role"] in ("Komissar 🕵️‍♂️", "Serjant 👮‍♂️")]
        return "qonun", mates
    return None, []


@bot.message_handler(commands=["jamoa", "adolat"])
def cmd_faction_chat(message):
    """💬 FAQAT shaxsiy chatda va faol o'yin ichida ishlaydi. Guruh buni
    KO'RMAYDI — o'z jamoadoshlaringizga (Mafiya: Don+Mafia — /jamoa, yoki
    Qonun: Komissar+Serjant — /adolat) bot orqali yashirin xabar yuboradi.
    Foydalanish: /jamoa xabar matni  yoki  /adolat xabar matni"""
    maybe_capture_owner(message.from_user)
    if message.chat.type != "private":
        return
    uid = message.from_user.id
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        bot.send_message(
            message.chat.id,
            "Foydalanish:\n<code>/jamoa xabar matni</code> — Mafiya jamoasiga\n"
            "<code>/adolat xabar matni</code> — Qonun (Komissar+Serjant) jamoasiga",
        )
        return
    text = parts[1].strip()

    game = None
    for g in GAMES.values():
        if uid in g["players"] and g["players"][uid]["alive"]:
            game = g
            break
    if not game:
        bot.send_message(message.chat.id, "❌ Siz hozir hech qanday faol o'yinda emassiz.")
        return

    kind, mates = get_faction_teammates(game, uid)
    if kind is None or not mates:
        bot.send_message(message.chat.id, "❌ Sizda hozir bu jamoaviy chatdan foydalanish imkoni yo'q (jamoadoshingiz yo'q yoki rolingiz mos kelmaydi).")
        return

    label = "🕶 Mafiya jamoasi" if kind == "mafia" else "🕵️‍♂️👮‍♂️ Qonun jamoasi"
    sender_name = game["players"][uid]["name"]
    sent = sum(1 for mate_uid in mates if safe_send(mate_uid, f"{label} 💬 <b>{sender_name}:</b> {text}"))
    bot.send_message(
        message.chat.id,
        f"✅ Xabaringiz {sent} ta jamoadoshingizga yetkazildi." if sent else "❌ Hech kimga yetkazib bo'lmadi.",
    )


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

# ================================================================================
#  /zahar  /gps  /qayta_tanlash — do'kon buyumlarini ishlatish buyruqlari
#  (endi har biri alohida `do_*` funksiyaga ajratilgan — shu funksiyalarni
#  ham reply-buyruq, ham 📦 Inventardagi "ishlatish" tugmasi chaqiradi)
# ================================================================================

def find_active_game_for(uid):
    """Foydalanuvchi hozir tirik holda ishtirok etayotgan o'yin (agar bo'lsa) —
    Inventardan to'g'ridan-to'g'ri buyum ishlatish uchun kerak."""
    for chat_id, game in GAMES.items():
        p = game["players"].get(uid)
        if p and p["alive"] and game["phase"] in ("night", "day"):
            return chat_id, game
    return None, None


def do_zahar(chat_id, game, uid, target_id, target_name):
    if get_charges(uid).get("poison", 0) <= 0:
        return False, "❌ Sizda 🧪 Zaharli flakon yo'q."
    if target_id not in game["players"] or not game["players"][target_id]["alive"]:
        return False, "❌ Bu o'yinchi topilmadi yoki allaqachon o'yindan chetlashtirilgan."
    use_charge(uid, "poison")
    game.setdefault("poison_marks", set()).add(target_id)
    return True, f"🧪 Siz {target_name}ga yashirincha zahar berdingiz. Doktor davolamasa, u tun yakunida halok bo'ladi."


def do_gps(chat_id, game, uid, target_id, target_name):
    if get_charges(uid).get("gps", 0) <= 0:
        return False, "❌ Sizda 📍 GPS Mayak yo'q."
    if target_id not in game["players"]:
        return False, "❌ Bu o'yinchi topilmadi."
    use_charge(uid, "gps")
    if get_charges(target_id).get("cloak", 0) > 0:
        use_charge(target_id, "cloak")
        return True, "📍 GPS signali yo'qoldi... Nishon 🧥 Yashirin Kolt yordamida o'zini yashirgan ko'rinadi."
    alive = game["players"][target_id]["alive"]
    status = "tirik va o'yin maydonida" if alive else "allaqachon o'yindan chetlashtirilgan"
    return True, f"📍 GPS natijasi: {target_name} hozir {status}."


def do_kompas(chat_id, game, uid, target_id, target_name):
    has_hero_compass = hero_has_free_compass(uid)  # 🏆 Geroy (Seraphine / Zephyrion)
    if not has_hero_compass and get_charges(uid).get("compass", 0) <= 0:
        return False, "❌ Sizda 🧭 Sirli kompas yo'q."
    if target_id not in game["players"] or not game["players"][target_id]["alive"]:
        return False, "❌ Bu o'yinchi topilmadi yoki allaqachon o'yindan chetlashtirilgan."
    if not has_hero_compass:
        use_charge(uid, "compass")
    target_role = game["players"][target_id]["role"]
    return True, f"🧭 Kompas natijasi: <b>{target_name}</b> — taraf: <b>{team_of(target_role)}</b>"


def do_fonar(chat_id, game, uid, target_id, target_name):
    if get_charges(uid).get("flash_light", 0) <= 0:
        return False, "❌ Sizda 🔦 Katta Fonar yo'q."
    if target_id not in game["players"]:
        return False, "❌ Bu o'yinchi topilmadi."
    use_charge(uid, "flash_light")
    role = game["players"][target_id]["role"]
    return True, f"🔦 Fonar yorug'ligida ko'rindi: {target_name} — <b>{role}</b>"


def do_tutun(chat_id, game, uid):
    if game["phase"] != "day":
        return False, "❌ 💣 Tutunli bombani faqat kunduzi ishlatish mumkin."
    if get_charges(uid).get("smoke_bomb", 0) <= 0:
        return False, "❌ Sizda 💣 Tutunli bomba yo'q."
    if game["players"][uid].get("smoke_active"):
        return False, "💨 Tutun allaqachon faol — bugun uchun himoyalangansiz."
    use_charge(uid, "smoke_bomb")
    game["players"][uid]["smoke_active"] = True
    return True, "💨 Tutunli bomba ishlatildi! Bugun eng ko'p ovoz olsangiz ham, linch qilinmaysiz."


def do_qayta_tanlash(chat_id, game, uid):
    if get_charges(uid).get("radar", 0) <= 0:
        return False, "❌ Sizda 📡 Maxfiy radar yo'q."
    use_charge(uid, "radar")
    old_role = game["players"][uid]["role"]
    new_role = random.choice([r for r in ALL_ROLES if r != old_role])
    game["players"][uid]["role"] = new_role
    game["players"][uid]["team"] = team_of(new_role)
    return True, f"📡 Radar faollashtirildi!\nEski rolingiz: {old_role}\nYangi rolingiz: <b>{new_role}</b>\n\n{ROLES_INFO.get(new_role, '')}"


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
    if is_banned(uid) or is_banned(target.id):
        return
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        return
    ok, msg = do_zahar(chat_id, game, uid, target.id, mention(target.id, target.first_name))
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "🧪 Zaharli flakon")


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
    if uid not in game["players"]:
        return
    ok, msg = do_gps(chat_id, game, uid, target.id, mention(target.id, target.first_name))
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "📍 GPS Mayak")


@bot.message_handler(commands=["kompas"])
def cmd_kompas(message):
    """🧭 Sirli kompas — birovning ANIQ rolini emas, faqat qaysi tarafda
    (mafiya/tinch aholi/mustaqil) ekanini ko'rsatadi. Komissar tekshiruvidan
    ancha kuchsizroq (rol emas, faqat taraf), shuning uchun muvozanatga xavf solmaydi."""
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
    ok, msg = do_kompas(chat_id, game, uid, target.id, mention(target.id, target.first_name))
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "🧭 Sirli kompas")


@bot.message_handler(commands=["tutun"])
def cmd_tutun(message):
    """💣 Tutunli bomba — kunduzi ishlatilsa, sizni shu kunlik ovoz berishda
    linch qilinishdan (eng ko'p ovoz olgan bo'lsangiz ham) bir marta asraydi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        return
    uid = message.from_user.id
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        return
    ok, msg = do_tutun(chat_id, game, uid)
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "💣 Tutunli bomba")


@bot.message_handler(commands=["fonar"])
def cmd_fonar(message):
    """🔦 Katta Fonar — javob berilgan (reply) o'yinchining haqiqiy rolini bir martalik ochib beradi (DM orqali)."""
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
    if uid not in game["players"]:
        return
    ok, msg = do_fonar(chat_id, game, uid, target.id, mention(target.id, target.first_name))
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "🔦 Katta Fonar")


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
    ok, msg = do_qayta_tanlash(chat_id, game, uid)
    safe_send(uid, msg)
    if ok:
        announce_item_use(chat_id, uid, "📡 Maxfiy radar")


# ================================================================================
#  🏛 KLANLAR VA KLANLAR JANGI — TO'LIQ TIZIM
#  (foydalanuvchi yuborgan texnik topshiriq — TXT fayl — asosida qurilgan)
#  Lider = clans.owner_id. O'rinbosar = clans.deputy_id. Oddiy a'zolar clan_members'da.
# ================================================================================

CLAN_LEVEL_CAPS = {1: {"members": 15, "titles": 2}, 2: {"members": 25, "titles": 5}, 3: {"members": 50, "titles": 10}}
CLAN_LEVEL_UP_COST = {2: {"diamond": 75, "coin": 1}, 3: {"diamond": 120, "coin": 3}}
CLAN_MAX_LEVEL = 3

CLAN_WAR_MIN_LEADER_DOLLAR = 1000
CLAN_WAR_WIN_TREASURY = 1000
CLAN_WAR_LOSE_TREASURY = 500
CLAN_WAR_SURRENDER_TREASURY = 300
CLAN_WAR_STREAK_FOR_DIAMOND = 5
CLAN_WAR_STREAK_DIAMOND_REWARD = 3
CLAN_WAR_COOLDOWN_SECONDS = 120
CLAN_WAR_DECLINE_LIMIT = 3
CLAN_WAR_DECLINE_FINE = 500

CLAN_TITLE_RITSAR = "ritsar"
CLAN_TITLE_SEHRGAR = "sehrgar"
CLAN_TITLE_MIN_LEVEL = {CLAN_TITLE_RITSAR: 10, CLAN_TITLE_SEHRGAR: 15}
CLAN_TITLE_COST_DOLLAR = 5000
CLAN_TITLE_MIN_GAMES = {CLAN_TITLE_RITSAR: 5, CLAN_TITLE_SEHRGAR: 10}
CLAN_TITLE_POWER_BONUS = {CLAN_TITLE_RITSAR: 2, CLAN_TITLE_SEHRGAR: 4}
CLAN_TITLE_NAMES = {CLAN_TITLE_RITSAR: "🛡 Ritsar", CLAN_TITLE_SEHRGAR: "🧙‍♂️ Sehrgar"}

CLAN_NAME_CHANGE_COST = 5000
CLAN_DEPUTY_MIN_CLAN_LEVEL = 2
CLAN_DEPUTY_COST_COIN = 1
CLAN_DEPUTY_MAX_LEVELUPS = 2
CLAN_INACTIVITY_DAYS = 30
CLAN_INACTIVITY_PENALTY = 3


def _check_clan_inactivity():
    """🏛 Klan lideri 30 kun davomida jang qilmasa, klan darajasi va barcha
    a'zolar darajasi -3 lvl bo'ladi (spetsifikatsiya talabi). Har 24 soatda
    bir marta tekshiriladi (o'z-o'zini qayta rejalashtiradigan fon vazifasi)."""
    try:
        threshold = time.time() - CLAN_INACTIVITY_DAYS * 86400
        with db_lock:
            cur.execute(
                "SELECT owner_id FROM clans WHERE last_war_at < ? AND last_inactivity_penalty_at < ?",
                (threshold, threshold),
            )
            inactive_owners = [r[0] for r in cur.fetchall()]
            for owner_id in inactive_owners:
                cur.execute(
                    "UPDATE clans SET leader_level = MAX(0, leader_level - ?), last_inactivity_penalty_at = ? WHERE owner_id=?",
                    (CLAN_INACTIVITY_PENALTY, time.time(), owner_id),
                )
                cur.execute(
                    "UPDATE clan_members SET level = MAX(0, level - ?) WHERE owner_id=?",
                    (CLAN_INACTIVITY_PENALTY, owner_id),
                )
            conn.commit()
        for owner_id in inactive_owners:
            clan = get_clan(owner_id)
            note = f"⚠️ <b>{clan['name']}</b> klani 30 kundan beri jang qilmadi — barcha a'zolar -{CLAN_INACTIVITY_PENALTY} lvl oldi." if clan else ""
            if note:
                safe_send(owner_id, note)
    except Exception:
        logging.exception("⚠️ Klan faolsizlik tekshiruvida xatolik.")
    finally:
        t = threading.Timer(86400, _check_clan_inactivity)
        t.daemon = True
        t.start()


def get_clan(owner_id):
    with db_lock:
        cur.execute(
            "SELECT owner_id, name, level, deputy_id, leader_level, treasury_dollar, treasury_diamond, "
            "levelup_tokens, wins, losses, win_streak, war_declines_streak, last_war_at, deputy_levelups_used "
            "FROM clans WHERE owner_id=?",
            (owner_id,),
        )
        row = cur.fetchone()
    if not row:
        return None
    cols = ["owner_id", "name", "level", "deputy_id", "leader_level", "treasury_dollar", "treasury_diamond",
            "levelup_tokens", "wins", "losses", "win_streak", "war_declines_streak", "last_war_at", "deputy_levelups_used"]
    return dict(zip(cols, row))


def find_member_clan(uid):
    """Foydalanuvchi biror klanga a'zomi (lider yoki oddiy a'zo) — shu klan owner_id'sini qaytaradi."""
    clan = get_clan(uid)
    if clan:
        return uid  # o'zi lider
    with db_lock:
        cur.execute("SELECT owner_id FROM clan_members WHERE member_id=?", (uid,))
        row = cur.fetchone()
    return row[0] if row else None


def is_clan_leader(uid, owner_id):
    return uid == owner_id


def is_clan_deputy(uid, owner_id):
    clan = get_clan(owner_id)
    return bool(clan and clan["deputy_id"] == uid)


def clan_can_manage(uid, owner_id):
    return is_clan_leader(uid, owner_id) or is_clan_deputy(uid, owner_id)


def clan_member_count(owner_id):
    with db_lock:
        cur.execute("SELECT COUNT(*) FROM clan_members WHERE owner_id=?", (owner_id,))
        return cur.fetchone()[0] + 1  # + lider


def clan_title_count(owner_id):
    with db_lock:
        cur.execute("SELECT COUNT(*) FROM clan_members WHERE owner_id=? AND title IS NOT NULL", (owner_id,))
        return cur.fetchone()[0]


def get_clan_member_row(owner_id, uid):
    with db_lock:
        cur.execute("SELECT member_id, member_name, level, title FROM clan_members WHERE owner_id=? AND member_id=?", (owner_id, uid))
        row = cur.fetchone()
    if not row:
        return None
    return {"member_id": row[0], "member_name": row[1], "level": row[2] or 0, "title": row[3]}


def clan_power(owner_id):
    """Klanning umumiy 'jang kuchi': lider darajasi + barcha a'zolar darajasi + maqom bonuslari."""
    clan = get_clan(owner_id)
    if not clan:
        return 0
    total = clan["leader_level"] or 3
    with db_lock:
        cur.execute("SELECT level, title FROM clan_members WHERE owner_id=?", (owner_id,))
        rows = cur.fetchall()
    for level, title in rows:
        total += (level or 0)
        if title in CLAN_TITLE_POWER_BONUS:
            total += CLAN_TITLE_POWER_BONUS[title]
    return max(total, 1)


# ================================================================================
#  /klan — klan yaratish
# ================================================================================

@bot.message_handler(commands=["klan"])
def cmd_klan(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if get_charges(uid).get("klan_license", 0) <= 0:
        bot.send_message(message.chat.id, "❌ Klan ochish uchun avval 🏛 Klan litsenziyasini (Hunter Coin do'koni) sotib oling.")
        return
    if get_clan(uid):
        bot.send_message(message.chat.id, "❌ Sizda allaqachon klan bor.")
        return
    if find_member_clan(uid):
        bot.send_message(message.chat.id, "❌ Siz boshqa klanning a'zosisiz — avval /klan_tark deb chiqing.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/klan Nomi</code>")
        return
    name = parts[1].strip()[:32]
    use_charge(uid, "klan_license")
    with db_lock:
        cur.execute(
            "INSERT OR REPLACE INTO clans (owner_id, name, level, deputy_id, leader_level, treasury_dollar, "
            "treasury_diamond, levelup_tokens, wins, losses, win_streak, war_declines_streak, last_war_at, deputy_levelups_used) "
            "VALUES (?,?,1,NULL,3,0,0,10,0,0,0,0,?,0)",
            (uid, name, time.time()),
        )
        conn.commit()
    bot.send_message(
        message.chat.id,
        f"🏛 Klan yaratildi: <b>{name}</b>!\n\n"
        f"👑 Siz lider — boshlang'ich darajangiz: <b>3 lvl</b>\n"
        f"🎁 Sizga darhol <b>10 ta lvl-up</b> berildi — buni a'zolaringizga /klan_azo_daraja orqali taqsimlang "
        f"(yoki xohlasangiz hammasini o'zingizga sarflang).",
    )


# ================================================================================
#  /klanim — klan holati
# ================================================================================

@bot.message_handler(commands=["klanim"])
def cmd_klanim(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    owner_id = find_member_clan(uid)
    if not owner_id:
        bot.send_message(message.chat.id, "Sizda hali klan yo'q. 🏛 Klan litsenziyasini sotib olib <code>/klan Nomi</code> deb yozing.")
        return
    clan = get_clan(owner_id)
    caps = CLAN_LEVEL_CAPS[clan["level"]]
    with db_lock:
        cur.execute("SELECT member_id, member_name, level, title FROM clan_members WHERE owner_id=? ORDER BY level DESC", (owner_id,))
        members = cur.fetchall()

    leader_name = user_dict(owner_id)["name"]
    lines = [
        f"🏛 <b>{clan['name']}</b> — {clan['level']} lvl klan\n",
        f"👑 Lider: {mention(owner_id, leader_name)} ({clan['leader_level']} lvl)",
    ]
    if clan["deputy_id"]:
        dep_name = user_dict(clan["deputy_id"])["name"]
        lines.append(f"🎖 O'rinbosar: {mention(clan['deputy_id'], dep_name)}")
    lines.append(f"👥 A'zolar: {clan_member_count(owner_id)}/{caps['members']} | 🎖 Maqomlar: {clan_title_count(owner_id)}/{caps['titles']}")
    lines.append(f"💰 Xazina: ${clan['treasury_dollar']} | 💎 {clan['treasury_diamond']}")
    lines.append(f"⚔️ {clan['wins']} g'alaba / {clan['losses']} mag'lubiyat (ketma-ket: {clan['win_streak']})")
    if is_clan_leader(uid, owner_id) or is_clan_deputy(uid, owner_id):
        lines.append(f"🎯 Taqsimlanmagan lvl-up tokenlar: {clan['levelup_tokens']}")
    if members:
        lines.append("\n👥 <b>A'zolar:</b>")
        for m_id, m_name, m_level, m_title in members:
            title_tag = f" {CLAN_TITLE_NAMES[m_title]}" if m_title in CLAN_TITLE_NAMES else ""
            lines.append(f"• {mention(m_id, m_name)} — {m_level or 0} lvl{title_tag}")
    bot.send_message(message.chat.id, "\n".join(lines))


# ================================================================================
#  /klanga_qoshil — endi so'rov yuboradi, lider tasdiqlashi kerak
# ================================================================================

@bot.message_handler(commands=["klanga_qoshil"])
def cmd_klanga_qoshil(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if is_banned(uid):
        return
    if find_member_clan(uid):
        bot.send_message(message.chat.id, "❌ Siz allaqachon bir klanning a'zosisiz.")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/klanga_qoshil &lt;klan_egasining_user_id&gt;</code>")
        return
    owner_id = int(parts[1])
    clan = get_clan(owner_id)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bunday klan topilmadi.")
        return
    caps = CLAN_LEVEL_CAPS[clan["level"]]
    if clan_member_count(owner_id) >= caps["members"]:
        bot.send_message(message.chat.id, f"❌ Bu klan to'lgan (maksimal {caps['members']} a'zo).")
        return

    user_dict(uid, message.from_user.first_name)
    with db_lock:
        cur.execute(
            "INSERT OR REPLACE INTO clan_join_requests (owner_id, user_id, user_name, requested_at) VALUES (?,?,?,?)",
            (owner_id, uid, message.from_user.first_name, time.time()),
        )
        conn.commit()

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Qabul qilish", callback_data=f"cjreq|yes|{owner_id}|{uid}"),
        types.InlineKeyboardButton("🚫 Rad etish", callback_data=f"cjreq|no|{owner_id}|{uid}"),
    )
    safe_send(
        owner_id,
        f"📨 <b>{message.from_user.first_name}</b> sizning <b>{clan['name']}</b> klaningizga qo'shilishni so'ramoqda.",
        kb,
    )
    bot.send_message(message.chat.id, f"📨 So'rovingiz <b>{clan['name']}</b> klani liderga yuborildi — javobini kuting.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("cjreq|"))
def cb_clan_join_request(call):
    maybe_capture_owner(call.from_user)
    _, action, owner_s, user_s = call.data.split("|")
    owner_id, user_id = int(owner_s), int(user_s)

    if call.from_user.id != owner_id:
        bot.answer_callback_query(call.id, "Bu so'rovga faqat klan lideri javob bera oladi.")
        return

    with db_lock:
        cur.execute("DELETE FROM clan_join_requests WHERE owner_id=? AND user_id=?", (owner_id, user_id))
        conn.commit()

    clan = get_clan(owner_id)
    if not clan:
        bot.answer_callback_query(call.id, "Klan topilmadi.")
        return

    if action == "no":
        bot.edit_message_text("🚫 So'rov rad etildi.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        safe_send(user_id, f"🚫 <b>{clan['name']}</b> klaniga qo'shilish so'rovingiz rad etildi.")
        return

    caps = CLAN_LEVEL_CAPS[clan["level"]]
    if clan_member_count(owner_id) >= caps["members"]:
        bot.edit_message_text("❌ Klan to'lib qoldi, qabul qilib bo'lmadi.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return
    if find_member_clan(user_id):
        bot.edit_message_text("❌ Bu foydalanuvchi allaqachon boshqa klanga a'zo bo'lgan.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    user_name = user_dict(user_id)["name"]
    with db_lock:
        cur.execute(
            "INSERT OR REPLACE INTO clan_members (owner_id, member_id, member_name, level, title) VALUES (?,?,?,0,NULL)",
            (owner_id, user_id, user_name),
        )
        conn.commit()
    bot.edit_message_text(f"✅ {user_name} klaningizga qabul qilindi!", call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)
    safe_send(user_id, f"✅ Siz <b>{clan['name']}</b> klaniga muvaffaqiyatli qo'shildingiz! Boshlang'ich darajangiz: 0 lvl.")


# ================================================================================
#  /klan_tark, /klan_chetlash — klandan chiqish / chiqarish
# ================================================================================

@bot.message_handler(commands=["klan_tark"])
def cmd_klan_tark(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    owner_id = find_member_clan(uid)
    if not owner_id or owner_id == uid:
        bot.send_message(message.chat.id, "❌ Siz biror klanning oddiy a'zosi emassiz (lider klanni tark eta olmaydi — uni tarqating).")
        return
    clan = get_clan(owner_id)
    with db_lock:
        cur.execute("DELETE FROM clan_members WHERE owner_id=? AND member_id=?", (owner_id, uid))
        if clan and clan["deputy_id"] == uid:
            cur.execute("UPDATE clans SET deputy_id=NULL WHERE owner_id=?", (owner_id,))
        conn.commit()
    bot.send_message(
        message.chat.id,
        f"👋 Siz <b>{clan['name'] if clan else 'klan'}</b>dan chiqdingiz. Darajangiz 0 lvlga tushdi, "
        f"klanga aloqador barcha narsalaringiz yo'qoldi.",
    )


@bot.message_handler(commands=["klan_chetlash"])
def cmd_klan_chetlash(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ Chetlatmoqchi bo'lgan a'zoning xabariga reply qilib yozing.")
        return
    uid = message.from_user.id
    owner_id = find_member_clan(uid)
    if not owner_id or not is_clan_leader(uid, owner_id):
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    target = message.reply_to_message.from_user
    with db_lock:
        cur.execute("DELETE FROM clan_members WHERE owner_id=? AND member_id=?", (owner_id, target.id))
        clan = get_clan(owner_id)
        if clan and clan["deputy_id"] == target.id:
            cur.execute("UPDATE clans SET deputy_id=NULL WHERE owner_id=?", (owner_id,))
        conn.commit()
    bot.send_message(message.chat.id, f"👢 {target.first_name} klandan chetlashtirildi.")
    safe_send(target.id, f"👢 Siz <b>{clan['name'] if clan else 'klan'}</b>dan chetlashtirildingiz. Darajangiz 0 lvlga tushdi.")


# ================================================================================
#  /klan_orinbosar — o'rinbosar tayinlash
# ================================================================================

@bot.message_handler(commands=["klan_orinbosar"])
def cmd_klan_orinbosar(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ O'rinbosar qilmoqchi bo'lgan a'zoning xabariga reply qilib yozing.")
        return
    uid = message.from_user.id
    clan = get_clan(uid)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    if clan["level"] < CLAN_DEPUTY_MIN_CLAN_LEVEL:
        bot.send_message(message.chat.id, f"❌ O'rinbosar tayinlash uchun klan kamida {CLAN_DEPUTY_MIN_CLAN_LEVEL}-lvl bo'lishi kerak.")
        return
    target = message.reply_to_message.from_user
    if get_clan_member_row(uid, target.id) is None:
        bot.send_message(message.chat.id, "❌ Bu odam sizning klaningiz a'zosi emas.")
        return
    u = user_dict(uid)
    if u["coin"] < CLAN_DEPUTY_COST_COIN:
        bot.send_message(message.chat.id, f"❌ Yetarli Hunter Coin yo'q ({CLAN_DEPUTY_COST_COIN} kerak).")
        return
    update_user(uid, coin=u["coin"] - CLAN_DEPUTY_COST_COIN)
    with db_lock:
        cur.execute("UPDATE clans SET deputy_id=?, deputy_levelups_used=0 WHERE owner_id=?", (target.id, uid))
        conn.commit()
    bot.send_message(message.chat.id, f"🎖 {target.first_name} endi klaningiz o'rinbosari!")
    safe_send(target.id, f"🎖 Siz <b>{clan['name']}</b> klanining o'rinbosari etib tayinlandingiz — jangga ruxsat berish va cheklangan lvl taqsimlash huquqiga egasiz.")


# ================================================================================
#  /klan_azo_daraja — a'zoning darajasini oshirish/pasaytirish (faqat lider/o'rinbosar)
# ================================================================================

@bot.message_handler(commands=["klan_azo_daraja"])
def cmd_klan_azo_daraja(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ Daraja bermoqchi bo'lgan a'zoning xabariga reply qilib, miqdorni yozing.")
        return
    uid = message.from_user.id
    owner_id = find_member_clan(uid)
    if not owner_id or not clan_can_manage(uid, owner_id):
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri yoki o'rinbosari uchun.")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].lstrip("-").isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/klan_azo_daraja &lt;son, masalan 3 yoki -2&gt;</code> (a'zoning xabariga reply qiling)")
        return
    amount = int(parts[1])
    target = message.reply_to_message.from_user
    row = get_clan_member_row(owner_id, target.id)
    if row is None and target.id != owner_id:
        bot.send_message(message.chat.id, "❌ Bu odam sizning klaningiz a'zosi emas.")
        return

    clan = get_clan(owner_id)
    is_deputy = is_clan_deputy(uid, owner_id)
    if is_deputy and not is_clan_leader(uid, owner_id):
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ O'rinbosar faqat lvl KO'TARISHI mumkin (pasaytira olmaydi).")
            return
        remaining_deputy_quota = CLAN_DEPUTY_MAX_LEVELUPS - clan["deputy_levelups_used"]
        if remaining_deputy_quota <= 0:
            bot.send_message(message.chat.id, "❌ O'rinbosar sifatida lvl-up limitingiz tugagan.")
            return
        amount = min(amount, remaining_deputy_quota, clan["levelup_tokens"])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Taqsimlash uchun lvl-up tokeningiz yo'q.")
            return
        with db_lock:
            cur.execute("UPDATE clans SET deputy_levelups_used = deputy_levelups_used + ?, levelup_tokens = levelup_tokens - ? WHERE owner_id=?",
                        (amount, amount, owner_id))
            conn.commit()
    else:
        if amount > 0:
            if clan["levelup_tokens"] < amount:
                bot.send_message(message.chat.id, f"❌ Yetarli lvl-up tokeningiz yo'q (bor: {clan['levelup_tokens']}).")
                return
            with db_lock:
                cur.execute("UPDATE clans SET levelup_tokens = levelup_tokens - ? WHERE owner_id=?", (amount, owner_id))
                conn.commit()

    if target.id == owner_id:
        new_level = max(0, clan["leader_level"] + amount)
        with db_lock:
            cur.execute("UPDATE clans SET leader_level=? WHERE owner_id=?", (new_level, owner_id))
            conn.commit()
    else:
        new_level = max(0, (row["level"] if row else 0) + amount)
        with db_lock:
            cur.execute("UPDATE clan_members SET level=? WHERE owner_id=? AND member_id=?", (new_level, owner_id, target.id))
            conn.commit()

    bot.send_message(message.chat.id, f"✅ {target.first_name} darajasi: <b>{new_level} lvl</b>")


# ================================================================================
#  /klan_lvl — klanni yangi darajaga ko'tarish (faqat lider)
# ================================================================================

@bot.message_handler(commands=["klan_lvl"])
def cmd_klan_lvl(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    clan = get_clan(uid)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    if clan["level"] >= CLAN_MAX_LEVEL:
        bot.send_message(message.chat.id, f"✅ Klaningiz allaqachon eng yuqori darajada ({CLAN_MAX_LEVEL} lvl).")
        return
    next_level = clan["level"] + 1
    cost = CLAN_LEVEL_UP_COST[next_level]
    u = user_dict(uid)
    if u["diamond"] >= cost["diamond"]:
        update_user(uid, diamond=u["diamond"] - cost["diamond"])
    elif u["coin"] >= cost["coin"]:
        update_user(uid, coin=u["coin"] - cost["coin"])
    else:
        bot.send_message(
            message.chat.id,
            f"❌ Klanni {next_level}-lvlga ko'tarish uchun 💎{cost['diamond']} yoki 🪙{cost['coin']} kerak.",
        )
        return
    with db_lock:
        cur.execute("UPDATE clans SET level=? WHERE owner_id=?", (next_level, uid))
        conn.commit()
    caps = CLAN_LEVEL_CAPS[next_level]
    bot.send_message(
        message.chat.id,
        f"🏛 Klaningiz <b>{next_level}-lvl</b>ga ko'tarildi!\n"
        f"👥 Endi maksimum {caps['members']} a'zo, {caps['titles']} ta maqom egasi bo'lishi mumkin.",
    )


# ================================================================================
#  /klan_nomi — klan nomini o'zgartirish (5000$)
# ================================================================================

@bot.message_handler(commands=["klan_nomi"])
def cmd_klan_nomi(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    clan = get_clan(uid)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, f"Foydalanish: <code>/klan_nomi Yangi nomi</code> (narxi: ${CLAN_NAME_CHANGE_COST})")
        return
    u = user_dict(uid)
    if u["dollar"] < CLAN_NAME_CHANGE_COST:
        bot.send_message(message.chat.id, f"❌ Yetarli mablag' yo'q (${CLAN_NAME_CHANGE_COST} kerak).")
        return
    new_name = parts[1].strip()[:32]
    update_user(uid, dollar=u["dollar"] - CLAN_NAME_CHANGE_COST)
    with db_lock:
        cur.execute("UPDATE clans SET name=? WHERE owner_id=?", (new_name, uid))
        conn.commit()
    bot.send_message(message.chat.id, f"✅ Klan nomi o'zgartirildi: <b>{new_name}</b>")


# ================================================================================
#  /klan_maqom — a'zoga Ritsar/Sehrgar maqomini berish
# ================================================================================

@bot.message_handler(commands=["klan_maqom"])
def cmd_klan_maqom(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ Maqom bermoqchi bo'lgan a'zoning xabariga reply qilib, <code>ritsar</code> yoki <code>sehrgar</code> deb yozing.")
        return
    uid = message.from_user.id
    clan = get_clan(uid)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    parts = message.text.split()
    if len(parts) != 2 or parts[1].lower() not in CLAN_TITLE_MIN_LEVEL:
        bot.send_message(message.chat.id, "Foydalanish: <code>/klan_maqom ritsar</code> yoki <code>/klan_maqom sehrgar</code> (a'zoning xabariga reply qiling)")
        return
    title = parts[1].lower()
    target = message.reply_to_message.from_user
    row = get_clan_member_row(uid, target.id)
    if row is None:
        bot.send_message(message.chat.id, "❌ Bu odam sizning klaningiz a'zosi emas.")
        return
    if row["title"]:
        bot.send_message(message.chat.id, f"❌ {target.first_name} allaqachon {CLAN_TITLE_NAMES[row['title']]} maqomiga ega.")
        return
    if clan_title_count(uid) >= CLAN_LEVEL_CAPS[clan["level"]]["titles"]:
        bot.send_message(message.chat.id, "❌ Klaningizdagi maqom o'rinlari to'lgan (klan darajasini oshiring).")
        return
    if row["level"] < CLAN_TITLE_MIN_LEVEL[title]:
        bot.send_message(message.chat.id, f"❌ {target.first_name} kamida {CLAN_TITLE_MIN_LEVEL[title]} lvl bo'lishi kerak (hozir: {row['level']}).")
        return
    t_user = user_dict(target.id)
    if t_user["games"] < CLAN_TITLE_MIN_GAMES[title]:
        bot.send_message(message.chat.id, f"❌ {target.first_name} kamida {CLAN_TITLE_MIN_GAMES[title]} ta o'yin o'ynagan bo'lishi kerak.")
        return
    if t_user["dollar"] < CLAN_TITLE_COST_DOLLAR:
        bot.send_message(message.chat.id, f"❌ {target.first_name}da yetarli mablag' yo'q (${CLAN_TITLE_COST_DOLLAR} kerak, a'zoning o'zida bo'lishi kerak).")
        return
    update_user(target.id, dollar=t_user["dollar"] - CLAN_TITLE_COST_DOLLAR)
    with db_lock:
        cur.execute("UPDATE clan_members SET title=? WHERE owner_id=? AND member_id=?", (title, uid, target.id))
        conn.commit()
    bot.send_message(message.chat.id, f"🎉 {target.first_name} endi {CLAN_TITLE_NAMES[title]}!")
    safe_send(target.id, f"🎉 Tabriklaymiz! Siz <b>{clan['name']}</b> klanida {CLAN_TITLE_NAMES[title]} maqomiga ega bo'ldingiz!")


# ================================================================================
#  /klan_hazna — klan xazinasi (faqat lider/o'rinbosar to'liq ko'radi)
# ================================================================================

@bot.message_handler(commands=["klan_hazna"])
def cmd_klan_hazna(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    owner_id = find_member_clan(uid)
    if not owner_id:
        bot.send_message(message.chat.id, "❌ Sizda klan yo'q.")
        return
    clan = get_clan(owner_id)
    if not clan_can_manage(uid, owner_id):
        bot.send_message(message.chat.id, "❌ Xazinani faqat lider va o'rinbosar ko'ra oladi.")
        return
    bot.send_message(
        message.chat.id,
        f"🏦 <b>{clan['name']} — Klan xazinasi</b>\n\n💰 ${clan['treasury_dollar']}\n💎 {clan['treasury_diamond']}\n\n"
        "<i>Xazinadan faqat lider foydalana oladi (a'zolarga taqsimlash yoki boshqa maqsadlarga sarflash).</i>",
    )


@bot.message_handler(commands=["klan_taqsimla"])
def cmd_klan_taqsimla(message):
    """Lider klan xazinasidagi dollarni a'zolarga (yoki o'ziga) taqsimlaydi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ Pul bermoqchi bo'lgan a'zoning xabariga reply qilib, miqdorni yozing.")
        return
    uid = message.from_user.id
    clan = get_clan(uid)
    if not clan:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat klan lideri uchun.")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/klan_taqsimla &lt;dollar&gt;</code> (a'zoning xabariga reply qiling)")
        return
    amount = int(parts[1])
    if clan["treasury_dollar"] < amount:
        bot.send_message(message.chat.id, f"❌ Xazinada yetarli mablag' yo'q (bor: ${clan['treasury_dollar']}).")
        return
    target = message.reply_to_message.from_user
    with db_lock:
        cur.execute("UPDATE clans SET treasury_dollar = treasury_dollar - ? WHERE owner_id=?", (amount, uid))
        conn.commit()
    add_balance(target.id, dollar=amount)
    bot.send_message(message.chat.id, f"💰 {target.first_name}ga klan xazinasidan ${amount} berildi.")


# ================================================================================
#  /klanlar — top klanlar ro'yxati
# ================================================================================

@bot.message_handler(commands=["klanlar"])
def cmd_klanlar(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    with db_lock:
        cur.execute("SELECT owner_id, name, level, wins, losses FROM clans ORDER BY wins DESC LIMIT 15")
        rows = cur.fetchall()
    if not rows:
        bot.send_message(message.chat.id, "🏛 Hozircha klanlar yo'q.")
        return
    lines = ["🏛 <b>TOP KLANLAR</b>\n"]
    for i, (owner_id, name, level, wins, losses) in enumerate(rows, 1):
        lines.append(f"{i}. <b>{name}</b> ({level} lvl) — 🏆{wins} / 💀{losses} — lider ID: <code>{owner_id}</code>")
    bot.send_message(message.chat.id, "\n".join(lines))


# ================================================================================
#  /klanjang — klanlar jangi (mutual rozilik, so'ng kuch balansiga qarab hal qilinadi)
# ================================================================================

CLAN_WAR_PENDING = {}  # (challenger_id, rival_owner_id) -> timestamp, spam/qayta-taklifning oldini olish uchun


@bot.message_handler(commands=["klanjang"])
def cmd_klanjang(message):
    """Ikki klan o'rtasida jang taklifi — klan 'kuchi' (darajalar+maqomlar yig'indisi)ga
    tortilgan ehtimollik bilan g'olib aniqlanadi, so'ng iqtisodiy oqibatlar qo'llaniladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if is_banned(uid):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/klanjang &lt;raqib_klan_egasining_user_id&gt;</code>")
        return
    rival_owner_id = int(parts[1])
    if rival_owner_id == uid:
        bot.send_message(message.chat.id, "❌ O'z klaningiz bilan jang qila olmaysiz!")
        return

    my_clan = get_clan(uid)
    rival_clan = get_clan(rival_owner_id)
    if not my_clan:
        bot.send_message(message.chat.id, "❌ Sizda klan yo'q (faqat lider jang e'lon qila oladi).")
        return
    if not rival_clan:
        bot.send_message(message.chat.id, "❌ Raqibda klan topilmadi.")
        return

    # klan urushi uchun liderda kamida $1000 bo'lishi kerak (mumkin bo'lgan zararni qoplash uchun)
    u = user_dict(uid)
    if u["dollar"] < CLAN_WAR_MIN_LEADER_DOLLAR:
        bot.send_message(message.chat.id, f"❌ Klan urushi e'lon qilish uchun sizda kamida ${CLAN_WAR_MIN_LEADER_DOLLAR} bo'lishi kerak.")
        return

    # daraja farqi qoidasi: 2 lvldan past klanlarga so'rov yuborish erkin, past klan yuqori
    # darajalilarga faqat kamida 15 a'zo bilan taklif yubora oladi
    if rival_clan["level"] > my_clan["level"] and clan_member_count(uid) < 15:
        bot.send_message(message.chat.id, "❌ O'zingizdan yuqori darajali klanga taklif yuborish uchun kamida 15 a'zoingiz bo'lishi kerak.")
        return

    pending_key = (uid, rival_owner_id)
    last_ts = CLAN_WAR_PENDING.get(pending_key)
    if last_ts and (time.time() - last_ts) < CLAN_WAR_COOLDOWN_SECONDS:
        wait_left = int(CLAN_WAR_COOLDOWN_SECONDS - (time.time() - last_ts))
        bot.send_message(message.chat.id, f"⏳ Bu klanga yaqinda jang taklifi yuborgansiz. Yana {wait_left} soniyadan keyin urinib ko'ring.")
        return

    CLAN_WAR_PENDING[pending_key] = time.time()
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⚔️ Jangga chiqish", callback_data=f"cwar|fight|{uid}|{rival_owner_id}"))
    kb.add(types.InlineKeyboardButton("🏳 Taslim bo'lish (-$300)", callback_data=f"cwar|surrender|{uid}|{rival_owner_id}"))
    kb.add(types.InlineKeyboardButton("🚫 Rad etish", callback_data=f"cwar|decline|{uid}|{rival_owner_id}"))
    bot.send_message(
        message.chat.id,
        f"⚔️ <b>KLANLAR JANGI TAKLIFI!</b>\n\n"
        f"🏛 <b>{my_clan['name']}</b> ({clan_power(uid)} kuch) klani 🏛 <b>{rival_clan['name']}</b> "
        f"({clan_power(rival_owner_id)} kuch) klaniga jang e'lon qildi!",
        reply_markup=kb,
    )
    safe_send(
        rival_owner_id,
        f"⚔️ <b>{my_clan['name']}</b> klani sizga jang e'lon qildi! Guruhdagi xabar ostidan javob bering.",
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("cwar|"))
def cb_klanjang(call):
    maybe_capture_owner(call.from_user)
    _, action, challenger_s, rival_owner_s = call.data.split("|")
    challenger_id, rival_owner_id = int(challenger_s), int(rival_owner_s)

    if call.from_user.id != rival_owner_id:
        bot.answer_callback_query(call.id, "Bu taklif sizga emas — faqat raqib klan egasi javob bera oladi.")
        return

    my_clan = get_clan(challenger_id)
    rival_clan = get_clan(rival_owner_id)
    if not my_clan or not rival_clan:
        bot.answer_callback_query(call.id, "❌ Klanlardan biri topilmadi.")
        return

    if action == "decline":
        with db_lock:
            cur.execute("UPDATE clans SET war_declines_streak = war_declines_streak + 1 WHERE owner_id=?", (rival_owner_id,))
            conn.commit()
        new_streak = rival_clan["war_declines_streak"] + 1
        note = ""
        if new_streak >= CLAN_WAR_DECLINE_LIMIT:
            u = user_dict(rival_owner_id)
            update_user(rival_owner_id, dollar=max(0, u["dollar"] - CLAN_WAR_DECLINE_FINE))
            with db_lock:
                cur.execute("UPDATE clans SET war_declines_streak = 0 WHERE owner_id=?", (rival_owner_id,))
                conn.commit()
            note = f"\n\n⚠️ Ketma-ket {CLAN_WAR_DECLINE_LIMIT} marta jangdan bosh tortgani uchun klaningiz -${CLAN_WAR_DECLINE_FINE} jarima oldi."
        bot.edit_message_text(random.choice(DEFEAT_JOKES) + note, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    with db_lock:
        cur.execute("UPDATE clans SET war_declines_streak = 0 WHERE owner_id=?", (rival_owner_id,))
        conn.commit()

    if action == "surrender":
        winner_owner_id, loser_owner_id = challenger_id, rival_owner_id
        winner_clan, loser_clan = my_clan, rival_clan
        surrendered = True
    else:  # fight
        my_power = clan_power(challenger_id)
        rival_power = clan_power(rival_owner_id)
        total = my_power + rival_power
        challenger_win_chance = my_power / total if total else 0.5
        challenger_won = random.random() < challenger_win_chance
        winner_owner_id = challenger_id if challenger_won else rival_owner_id
        loser_owner_id = rival_owner_id if challenger_won else challenger_id
        winner_clan = my_clan if challenger_won else rival_clan
        loser_clan = rival_clan if challenger_won else my_clan
        surrendered = False

    loss_amount = CLAN_WAR_SURRENDER_TREASURY if surrendered else CLAN_WAR_LOSE_TREASURY
    new_streak = winner_clan["win_streak"] + 1
    diamond_bonus = 0
    if new_streak >= CLAN_WAR_STREAK_FOR_DIAMOND:
        diamond_bonus = CLAN_WAR_STREAK_DIAMOND_REWARD
        new_streak = 0

    with db_lock:
        cur.execute(
            "UPDATE clans SET treasury_dollar = treasury_dollar + ?, treasury_diamond = treasury_diamond + ?, "
            "wins = wins + 1, win_streak = ?, levelup_tokens = levelup_tokens + 3, last_war_at = ? WHERE owner_id=?",
            (CLAN_WAR_WIN_TREASURY, diamond_bonus, new_streak, time.time(), winner_owner_id),
        )
        cur.execute(
            "UPDATE clans SET treasury_dollar = MAX(0, treasury_dollar - ?), losses = losses + 1, win_streak = 0, "
            "last_war_at = ? WHERE owner_id=?",
            (loss_amount, time.time(), loser_owner_id),
        )
        cur.execute(
            "INSERT INTO clan_wars (clan_a, clan_b, winner_owner_id, started_at, ended_at) VALUES (?,?,?,?,?)",
            (challenger_id, rival_owner_id, winner_owner_id, time.time(), time.time()),
        )
        conn.commit()

    result_text = (
        f"⚔️ <b>KLANLAR JANGI YAKUNLANDI!</b>\n\n"
        f"🏆 G'olib: <b>{winner_clan['name']}</b> — xazinaga +${CLAN_WAR_WIN_TREASURY}, +3 lvl-up token"
        + (f", +{diamond_bonus}💎 (5 ketma-ket g'alaba!)" if diamond_bonus else "")
        + f"\n💀 Mag'lub: <b>{loser_clan['name']}</b> — xazinadan -${loss_amount}"
        + (" (taslim bo'lgani uchun yumshoqroq jarima)" if surrendered else "")
    )
    bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)
    safe_send(loser_owner_id, f"😅 <b>{loser_clan['name']}</b> klaningiz jangda yutqazdi...\n\n{random.choice(DEFEAT_JOKES)}")
    safe_send(winner_owner_id, f"🏆 <b>{winner_clan['name']}</b> klaningiz g'alaba qozondi! Xazinaga +${CLAN_WAR_WIN_TREASURY} tushdi.")


# ================================================================================
#  /klan_mukofot — 3 oyda bir marta TOP klanlarga mukofot (faqat bot egasi ishga tushiradi)
# ================================================================================

@bot.message_handler(commands=["klan_mukofot"])
def cmd_klan_mukofot(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun (3 oyda 1 marta ishga tushiriladi).")
        return
    with db_lock:
        cur.execute("SELECT owner_id, name, wins FROM clans ORDER BY wins DESC LIMIT 3")
        top3 = cur.fetchall()
    if not top3:
        bot.send_message(message.chat.id, "🏛 Hozircha klanlar yo'q.")
        return
    rewards = [(20000, 20), (15000, 15), (10000, 10)]
    lines = ["🏆 <b>3 OYLIK TOP KLANLAR MUKOFOTI</b>\n"]
    for i, ((owner_id, name, wins), (dollar, diamond)) in enumerate(zip(top3, rewards), 1):
        with db_lock:
            cur.execute("UPDATE clans SET treasury_dollar = treasury_dollar + ?, treasury_diamond = treasury_diamond + ? WHERE owner_id=?",
                        (dollar, diamond, owner_id))
            conn.commit()
        lines.append(f"{i}-o'rin: <b>{name}</b> ({wins} g'alaba) — +${dollar}, +{diamond}💎 (klan xazinasiga)")
        safe_send(owner_id, f"🏆 Klaningiz 3 oylik reytingda {i}-o'rinni egalladi! Xazinaga +${dollar}, +{diamond}💎 tushdi.")
    with db_lock:
        cur.execute("UPDATE clans SET wins=0, losses=0")
        conn.commit()
    bot.send_message(message.chat.id, "\n".join(lines) + "\n\n♻️ Barcha klanlarning g'alaba/mag'lubiyat hisobi yangi mavsum uchun nolga tushirildi.")

# ================================================================================
#  🛒 QORA BOZOR — O'YINCHILAR O'RTASIDAGI SAVDO
#  (qoshimchakod5.py g'oyasi asosida, real SQLite bazasida to'liq ishlaydigan holda)
#  Endi FAQAT bot egasi belgilagan bitta guruhda ishlaydi, va sotuvchi narxni
#  dollar/olmos/coin — o'zi tanlagan valyutada, o'zi xohlagan miqdorda belgilay oladi.
# ================================================================================

@bot.message_handler(commands=["shu_bozor"])
def cmd_set_black_market_group(message):
    """Bot egasi qora bozor ishlaydigan guruhni shu buyruq bilan belgilaydi.
    Guruhga botni qo'shib, shu buyruqni o'sha guruhda yozing (bir marta yetarli)."""
    global BLACK_MARKET_CHAT_ID
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    if message.chat.type not in ("group", "supergroup"):
        bot.send_message(message.chat.id, "⚠️ Bu buyruqni qora bozor ishlashi kerak bo'lgan guruhning ichida yozing.")
        return
    BLACK_MARKET_CHAT_ID = message.chat.id
    set_setting("black_market_chat_id", BLACK_MARKET_CHAT_ID)
    bot.send_message(message.chat.id, f"✅ Qora bozor endi shu guruhda (<code>{message.chat.id}</code>) ishlaydi.")


def _in_black_market_group(chat_id):
    return BLACK_MARKET_CHAT_ID is not None and chat_id == BLACK_MARKET_CHAT_ID


@bot.message_handler(commands=["bozor_holati"])
def cmd_bozor_holati(message):
    """Nosozliklarni tuzatish uchun: joriy guruh ID'si va bot xotirasidagi
    qora bozor ID'sini solishtirib ko'rsatadi (faqat bot egasi uchun)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    bot.send_message(
        message.chat.id,
        f"🆔 Joriy guruh ID: <code>{message.chat.id}</code>\n"
        f"🛒 Saqlangan qora bozor ID: <code>{BLACK_MARKET_CHAT_ID}</code>\n"
        f"{'✅ Bu guruh — qora bozor.' if _in_black_market_group(message.chat.id) else '❌ Bu guruh qora bozor emas. Tuzatish uchun shu yerda /shu_bozor deb yozing.'}",
    )


# ================================================================================
#  QIZIL 🔴 vs KO'K 🔵 — ikki guruhli musobaqa
# ================================================================================

@bot.message_handler(commands=["guruh_id"])
def cmd_guruh_id(message):
    """/jufti buyrug'i uchun kerakli guruh ID'sini ko'rish (faqat bot egasi)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    bot.send_message(message.chat.id, f"🆔 Bu guruhning ID'si: <code>{message.chat.id}</code>")


@bot.message_handler(commands=["jufti"])
def cmd_jufti(message):
    """Joriy guruhni boshqa bir guruh bilan 'Qizil vs Ko'k' musobaqasiga bog'laydi.
    Foydalanish: har ikkala guruhda /guruh_id bilan ID olinadi, so'ng birida
    /jufti <ikkinchi_guruh_ID> deb yoziladi. Faqat bot egasi uchun."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].lstrip("-").isdigit():
        bot.send_message(message.chat.id, "Foydalanish: /jufti &lt;ikkinchi_guruh_ID&gt;\nID'ni ikkinchi guruhda /guruh_id orqali oling.")
        return
    other_id = int(parts[1])
    this_id = message.chat.id
    if other_id == this_id:
        bot.send_message(message.chat.id, "⛔ Guruhni o'zi bilan juftlashtirib bo'lmaydi.")
        return
    create_pair(this_id, other_id)
    bot.send_message(this_id, f"🔴🔵 Bu guruh boshqa guruh (<code>{other_id}</code>) bilan muvaffaqiyatli juftlashtirildi!\nEndi har ikkala guruhdagi o'yinlar umumiy hisobga qo'shiladi. /hisob orqali ko'ring.")
    try:
        bot.send_message(other_id, f"🔴🔵 Bu guruh boshqa guruh (<code>{this_id}</code>) bilan muvaffaqiyatli juftlashtirildi!\nEndi har ikkala guruhdagi o'yinlar umumiy hisobga qo'shiladi. /hisob orqali ko'ring.")
    except Exception:
        bot.send_message(this_id, "⚠️ Ogohlantirish: bot ikkinchi guruhga hozircha xabar yubora olmadi (bot o'sha guruhga qo'shilganini tekshiring).")


@bot.message_handler(commands=["jufti_bekor"])
def cmd_jufti_bekor(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    pair = get_pair(message.chat.id)
    if not pair:
        bot.send_message(message.chat.id, "Bu guruh hech qanday juftlikka bog'lanmagan.")
        return
    ca, cb, *_ = pair
    other_id = cb if ca == message.chat.id else ca
    remove_pair(message.chat.id)
    bot.send_message(message.chat.id, "🔓 Juftlik bekor qilindi.")
    try:
        bot.send_message(other_id, "🔓 Ushbu guruh bilan juftlik bekor qilindi.")
    except Exception:
        pass


@bot.message_handler(commands=["hisob"])
def cmd_hisob(message):
    """Qizil vs Ko'k umumiy hisobini ko'rsatadi."""
    pair = get_pair(message.chat.id)
    if not pair:
        bot.send_message(message.chat.id, "Bu guruh hozircha boshqa guruh bilan juftlashtirilmagan.\n(Bot egasi /jufti buyrug'i orqali bog'lashi mumkin.)")
        return
    ca, cb, label_a, label_b, score_a, score_b = pair
    bot.send_message(
        message.chat.id,
        f"📊 <b>Umumiy hisob</b>\n\n"
        f"{label_a}: <b>{score_a}</b> g'alaba\n"
        f"{label_b}: <b>{score_b}</b> g'alaba",
    )


@bot.message_handler(commands=["paralar"])
def cmd_paralar(message):
    """Admin uchun: barcha nikohdagi juftliklar ro'yxati, necha kundan beri
    nikohda ekanlari bilan. Ism ustiga bosilsa — o'sha kishining Telegram
    profiliga o'tiladi (mention() orqali tg://user?id= havolasi)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_authorized(message):
        bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat guruh admini yoki bot egasi ishlatishi mumkin.")
        return

    with db_lock:
        cur.execute("SELECT user_id, name, married_to, married_at FROM users WHERE married_to != 0")
        rows = cur.fetchall()

    if not rows:
        bot.send_message(message.chat.id, "💔 Hozircha hech kim nikohda emas.")
        return

    seen = set()
    pairs = []
    for uid, name, partner_id, married_at in rows:
        if uid in seen or partner_id in seen:
            continue
        seen.add(uid)
        seen.add(partner_id)
        partner = user_dict(partner_id)
        pairs.append((uid, name, partner_id, partner.get("name"), married_at))

    def days_married(married_at):
        if not married_at:
            return "?"
        try:
            married_ts = time.mktime(time.strptime(married_at, "%Y-%m-%d %H:%M:%S"))
            days = int((time.time() - married_ts) // 86400)
            return max(0, days)
        except Exception:
            return "?"

    lines = [f"💍 <b>Nikohdagi juftliklar</b> — jami {len(pairs)} ta\n"]
    for i, (uid, name, partner_id, partner_name, married_at) in enumerate(pairs, start=1):
        d = days_married(married_at)
        kun_text = f"{d} kun" if isinstance(d, int) else "noma'lum kun"
        lines.append(f"{i}. {mention(uid, name)} ❤️ {mention(partner_id, partner_name)} — {kun_text}")

    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(content_types=["migrate_to_chat_id"])
def handle_group_migration(message):
    """Telegram guruhni supergroup'ga aylantirganda chat_id butunlay o'zgaradi —
    shu sababli eski ID'ga bog'langan qora bozor/guruh ma'lumotlari yangi ID'ga
    avtomatik ko'chiriladi, aks holda qora bozor "guruhga qo'shiling" deb xato
    xabar bera boshlaydi, garchi foydalanuvchi allaqachon o'sha guruhda bo'lsa ham."""
    global BLACK_MARKET_CHAT_ID
    old_id = message.chat.id
    new_id = message.migrate_to_chat_id
    if BLACK_MARKET_CHAT_ID == old_id:
        BLACK_MARKET_CHAT_ID = new_id
        set_setting("black_market_chat_id", BLACK_MARKET_CHAT_ID)
    with db_lock:
        cur.execute("SELECT title FROM known_groups WHERE chat_id=?", (old_id,))
        row = cur.fetchone()
    remove_known_group(old_id)
    add_known_group(new_id, row[0] if row else None)
    with db_lock:
        cur.execute("UPDATE group_pairs SET chat_id_a=? WHERE chat_id_a=?", (new_id, old_id))
        cur.execute("UPDATE group_pairs SET chat_id_b=? WHERE chat_id_b=?", (new_id, old_id))
        conn.commit()
    if old_id in GAMES:
        game = GAMES.pop(old_id)
        game["chat_id"] = new_id
        GAMES[new_id] = game
        save_games_state()
    _logger.info("Guruh supergroup'ga ko'chirildi: %s -> %s", old_id, new_id)


@bot.message_handler(commands=["sell"])
def cmd_sell(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not _in_black_market_group(message.chat.id):
        bot.send_message(
            message.chat.id,
            "⛔ Qora bozor faqat maxsus savdo guruhida ishlaydi. Guruhga qo'shiling: "
            "https://t.me/+v9bYoMk-0hAyZTcy",
        )
        return
    uid = message.from_user.id
    if is_banned(uid):
        return
    user_dict(uid, message.from_user.first_name)

    u = user_dict(uid)
    try:
        inv = json.loads(u["inventory"] or "[]")
    except Exception:
        inv = []

    parts = message.text.split()
    if len(parts) < 4:
        # Format yetarli emas — inventarni va to'g'ri formatni ko'rsatamiz
        if not inv:
            bot.send_message(message.chat.id, "🎒 Sizning inventaringiz bo'sh — sotadigan narsangiz yo'q.")
            return
        lines = ["🎒 <b>Sizning inventaringizdagi buyumlar:</b>\n"]
        for idx, item in enumerate(inv, 1):
            lines.append(f"{idx}. {item}")
        lines.append(
            "\n<i>Sotish uchun: </i><code>/sell &lt;raqam&gt; &lt;dollar|diamond|coin&gt; &lt;narx&gt;</code>"
            "\n<i>Masalan: </i><code>/sell 1 diamond 25</code>"
        )
        bot.send_message(message.chat.id, "\n".join(lines))
        return

    currency = parts[2].lower()
    if currency not in CURRENCY_ICON:
        bot.send_message(message.chat.id, "⚠️ Valyuta faqat <code>dollar</code>, <code>diamond</code> yoki <code>coin</code> bo'lishi kerak!")
        return

    try:
        item_index = int(parts[1]) - 1
        price = int(parts[3])
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Raqam va narx faqat butun sonlardan iborat bo'lishi kerak!")
        return

    if price <= 0:
        bot.send_message(message.chat.id, "⚠️ Narx musbat son bo'lishi kerak!")
        return
    if item_index < 0 or item_index >= len(inv):
        bot.send_message(message.chat.id, "⚠️ Bunday raqamli buyum inventaringizda yo'q!")
        return

    item_to_sell = remove_inventory_item_by_index(uid, item_index)
    if item_to_sell is None:
        bot.send_message(message.chat.id, "⚠️ Bunday raqamli buyum inventaringizda yo'q!")
        return

    icon = CURRENCY_ICON[currency]
    seller_name = message.from_user.first_name
    with db_lock:
        cur.execute(
            "INSERT INTO market_listings (chat_id, seller_id, seller_name, item, price, active, currency) VALUES (?,?,?,?,?,1,?)",
            (message.chat.id, uid, seller_name, item_to_sell, price, currency),
        )
        conn.commit()
        listing_id = cur.lastrowid

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f"🛒 Sotib olish ({price} {icon})", callback_data=f"mbuy|{listing_id}"))
    bot.send_message(
        message.chat.id,
        f"📢 <b>Qora bozorda yangi e'lon!</b>\n\n"
        f"📦 Narsa: <b>{item_to_sell}</b>\n"
        f"💰 Narx: <b>{price}</b> {icon}\n"
        f"👤 Sotuvchi: {seller_name}\n"
        f"🆔 E'lon ID: <code>{listing_id}</code>",
        reply_markup=kb,
    )


@bot.message_handler(commands=["osh"])
def cmd_osh(message):
    """🥘 Milliy osh — o'zingizga emas, GURUHDAGI boshqa bir o'yinchiga ziyofat
    berish uchun: unga bir martalik himoya (shield) va (turiga qarab) qo'shimcha
    qobiliyat sovg'a qiladi — pul emas. Foydalanish: reply qilib /osh <turi>."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not message.reply_to_message:
        lines = ["🥘 <b>Milliy Osh Menyusi</b> — do'stingizga ziyofat bering (pul emas, qobiliyat sovg'a qilasiz)!\n"]
        for key, item in SHOP_OSH.items():
            extra = f" + 1x {TOGGLABLE_ITEMS.get(item['gift_charge'][0], item['gift_charge'][0])}" if item.get("gift_charge") else ""
            lines.append(f"<code>{key}</code> — {item['name']} (${item['price']}) → {item['gift_shield']}🛡{extra}")
        lines.append("\n<i>Foydalanish: kimningdir xabariga reply qilib </i><code>/osh &lt;turi&gt;</code>")
        bot.send_message(message.chat.id, "\n".join(lines))
        return
    parts = message.text.split()
    if len(parts) != 2 or parts[1].lower() not in SHOP_OSH:
        bot.send_message(message.chat.id, "Foydalanish: <code>/osh &lt;turi&gt;</code> (masalan: <code>/osh toy</code>) — turlar uchun reply'siz /osh deb yozing.")
        return
    key = parts[1].lower()
    item = SHOP_OSH[key]
    sender = message.from_user
    target = message.reply_to_message.from_user
    if target.id == sender.id:
        bot.send_message(message.chat.id, "❌ O'zingizga ziyofat berolmaysiz — bu boshqa o'yinchiga sovg'a.")
        return
    u = user_dict(sender.id, sender.first_name)
    user_dict(target.id, target.first_name or "O'yinchi")
    if u["dollar"] < item["price"]:
        bot.send_message(message.chat.id, f"❌ Yetarli mablag' yo'q (${item['price']} kerak).")
        return
    update_user(sender.id, dollar=u["dollar"] - item["price"])
    add_shield(target.id, item["gift_shield"])
    extra_text = ""
    if item.get("gift_charge"):
        ck, amount = item["gift_charge"]
        add_charge(target.id, ck, amount)
        extra_text = f" + {amount}x {TOGGLABLE_ITEMS.get(ck, ck)}"
    bot.send_message(
        message.chat.id,
        f"{item['name']}! {mention(sender.id, sender.first_name)} — {mention(target.id, target.first_name)}ga ziyofat berdi!\n"
        f"🎁 {target.first_name} +{item['gift_shield']}🛡{extra_text} sovg'a oldi.",
    )


@bot.message_handler(commands=["market"])
def cmd_market(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not _in_black_market_group(message.chat.id):
        bot.send_message(
            message.chat.id,
            "⛔ Qora bozor faqat maxsus savdo guruhida ishlaydi. Guruhga qo'shiling: "
            "https://t.me/+v9bYoMk-0hAyZTcy",
        )
        return
    with db_lock:
        cur.execute(
            "SELECT id, item, price, seller_name, currency FROM market_listings WHERE chat_id=? AND active=1 ORDER BY id DESC LIMIT 30",
            (message.chat.id,),
        )
        rows = cur.fetchall()
    if not rows:
        bot.send_message(
            message.chat.id,
            "🛒 Hozirda qora bozorda sotuvdagi buyumlar yo'q.\n"
            "O'z narsangizni sotish uchun <code>/sell &lt;raqam&gt; &lt;dollar|diamond|coin&gt; &lt;narx&gt;</code> buyrug'idan foydalaning.",
        )
        return
    lines = ["🛒 <b>Qora bozordagi faol e'lonlar:</b>\n"]
    for listing_id, item, price, seller_name, currency in rows:
        icon = CURRENCY_ICON.get(currency or "coin", "🪙")
        lines.append(f"🆔 <code>{listing_id}</code> | 📦 <b>{item}</b> — 💰 {price} {icon} | 👤 {seller_name}")
    lines.append("\n<i>Sotib olish uchun e'londagi tugmani bosing yoki: </i><code>/buy &lt;ID&gt;</code>")
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["buy"])
def cmd_buy(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not _in_black_market_group(message.chat.id):
        bot.send_message(
            message.chat.id,
            "⛔ Qora bozor faqat maxsus savdo guruhida ishlaydi. Guruhga qo'shiling: "
            "https://t.me/+v9bYoMk-0hAyZTcy",
        )
        return
    if is_banned(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/buy &lt;E'lon_ID&gt;</code>")
        return
    _show_market_buy_confirm(message.chat.id, None, int(parts[1]), message.from_user.id)


def _show_market_buy_confirm(chat_id, message_id, listing_id, buyer_id):
    with db_lock:
        cur.execute("SELECT item, price, seller_id, seller_name, currency FROM market_listings WHERE id=? AND active=1", (listing_id,))
        row = cur.fetchone()
    if not row:
        bot.send_message(chat_id, "❌ Bu buyum allaqachon sotilgan yoki e'lon topilmadi!")
        return
    item, price, seller_id, seller_name, currency = row
    icon = CURRENCY_ICON.get(currency or "coin", "🪙")
    if seller_id == buyer_id:
        bot.send_message(chat_id, "❌ O'z narsangizni o'zingiz sotib ololmaysiz!")
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Ha, sotib olaman", callback_data=f"mconfirm|{listing_id}"),
        types.InlineKeyboardButton("❌ Bekor qilish", callback_data="mcancel"),
    )
    bot.send_message(chat_id, f"❓ <b>{item}</b>ni {price} {icon} evaziga haqiqatan ham sotib olmoqchimisiz?", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("mbuy|"))
def cb_market_buy(call):
    maybe_capture_owner(call.from_user)
    if not _in_black_market_group(call.message.chat.id):
        bot.answer_callback_query(call.id, "⛔ Qora bozor faqat maxsus savdo guruhida ishlaydi.", show_alert=True)
        return
    listing_id = int(call.data.split("|")[1])
    with db_lock:
        cur.execute("SELECT item, price, seller_id, seller_name, currency FROM market_listings WHERE id=? AND active=1", (listing_id,))
        row = cur.fetchone()
    if not row:
        bot.answer_callback_query(call.id, "❌ Bu buyum allaqachon sotilgan!", show_alert=True)
        return
    item, price, seller_id, seller_name, currency = row
    icon = CURRENCY_ICON.get(currency or "coin", "🪙")
    if seller_id == call.from_user.id:
        bot.answer_callback_query(call.id, "❌ O'z narsangizni o'zingiz sotib ololmaysiz!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Ha, sotib olaman", callback_data=f"mconfirm|{listing_id}"),
        types.InlineKeyboardButton("❌ Bekor qilish", callback_data="mcancel"),
    )
    try:
        bot.edit_message_text(
            f"❓ <b>{item}</b>ni {price} {icon} evaziga haqiqatan ham sotib olmoqchimisiz?",
            call.message.chat.id, call.message.message_id, reply_markup=kb,
        )
    except Exception:
        bot.send_message(call.message.chat.id, f"❓ <b>{item}</b>ni {price} {icon} evaziga haqiqatan ham sotib olmoqchimisiz?", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("mconfirm|") or c.data == "mcancel")
def cb_market_confirm(call):
    maybe_capture_owner(call.from_user)
    if call.data == "mcancel":
        bot.answer_callback_query(call.id, "🚫 Savdo bekor qilindi.", show_alert=True)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        return

    if not _in_black_market_group(call.message.chat.id):
        bot.answer_callback_query(call.id, "⛔ Qora bozor faqat maxsus savdo guruhida ishlaydi.", show_alert=True)
        return

    listing_id = int(call.data.split("|")[1])
    buyer_id = call.from_user.id

    with db_lock:
        cur.execute("SELECT item, price, seller_id, seller_name, active, currency FROM market_listings WHERE id=?", (listing_id,))
        row = cur.fetchone()
        if not row or row[4] != 1:
            bot.answer_callback_query(call.id, "❌ Xatolik: e'lon topilmadi yoki allaqachon sotilgan!", show_alert=True)
            return
        item, price, seller_id, seller_name, _, currency = row
        currency = currency or "coin"
        icon = CURRENCY_ICON.get(currency, "🪙")
        if seller_id == buyer_id:
            bot.answer_callback_query(call.id, "❌ O'z narsangizni o'zingiz sotib ololmaysiz!", show_alert=True)
            return
        buyer = user_dict(buyer_id, call.from_user.first_name)
        if buyer[currency] < price:
            bot.answer_callback_query(
                call.id,
                f"❌ {icon} yetarli emas! Sizda {buyer[currency]} {icon} bor, kerak: {price} {icon}.",
                show_alert=True,
            )
            return
        cur.execute("UPDATE market_listings SET active=0 WHERE id=?", (listing_id,))
        conn.commit()

    add_balance(buyer_id, **{currency: -price})
    add_balance(seller_id, **{currency: price})
    add_inventory_item(buyer_id, item)

    bot.answer_callback_query(call.id, f"🎉 Tabriklaymiz! {item} muvaffaqiyatli sotib olindi!", show_alert=True)
    seller_mention = mention(seller_id, seller_name)
    buyer_mention = mention(buyer_id, call.from_user.first_name)
    try:
        bot.edit_message_text(
            f"✅ <b>Savdo muvaffaqiyatli yakunlandi!</b>\n\n"
            f"📦 Narsa: {item}\n👤 Sotuvchi: {seller_mention}\n🛒 Xaridor: {buyer_mention}\n"
            f"💰 Narx: {price} {icon}",
            call.message.chat.id, call.message.message_id,
        )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            f"✅ <b>Savdo muvaffaqiyatli yakunlandi!</b>\n\n"
            f"📦 Narsa: {item}\n👤 Sotuvchi: {seller_mention}\n🛒 Xaridor: {buyer_mention}\n"
            f"💰 Narx: {price} {icon}",
        )


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
    game["spoke_before_vote_today"] = set()
    game["vote_order"] = []
    game["no_lynch_today"] = False
    game["fog_today"] = False
    game["hero_armed_vote_shield"] = set()
    vote_seconds = DAY_VOTE_SECONDS

    # 🏆 Geroy (Draven/Zephyrion "Xalq himoyasi") — hali sarflanmagan bo'lsa, kunduzi eslatma
    for uid, p in alive_players(game).items():
        if hero_has_ability(uid, "vote_shield_once") and uid not in game.get("hero_vote_shield_used", set()):
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton("🗳 Xalq himoyasini faollashtirish", callback_data=f"heroarm|voteshield|{chat_id}"))
            safe_send(uid, "🏆 Geroyingizning bir martalik 🗳 Xalq himoyasi qobiliyati bor. Xohlasangiz, "
                           "bugungi kun uchun faollashtiring (aks holda ishlamaydi):", kb)

    # 🎲 Random event — har kuni 15% ehtimol bilan, ENDI HAR BIRI HAQIQIY TA'SIR QILADI
    if random.random() < 0.15:
        event = random.choice(RANDOM_EVENTS)
        bot.send_message(chat_id, f"🎲 <b>O'YIN DAVOMIDA KUTILMAGAN HODISA!</b>\n\n{event['text']}")
        key = event["key"]
        if key == "lucky_all":
            for uid in alive_players(game):
                add_balance(uid, dollar=50)
        elif key == "lucky_one":
            alive_uids = list(alive_players(game).keys())
            if alive_uids:
                lucky_uid = random.choice(alive_uids)
                add_balance(lucky_uid, dollar=100)
                safe_send(lucky_uid, "🎁 Tabriklaymiz! Bugungi tasodifiy hodisadan sizga +100$ tushdi!")
        elif key == "no_lynch":
            game["no_lynch_today"] = True
        elif key == "weak_night":
            game["weak_night_today"] = True
        elif key == "fog":
            game["fog_today"] = True
        elif key == "short_vote":
            vote_seconds = 15
    game["vote_seconds_today"] = vote_seconds

    send_scene_photo(
        chat_id, DAY_PHOTO_LOCAL, DAY_PHOTO,
        caption=f"☀️ <b>{game['day_number']}-kun.</b> Muhokama qiling — {DAY_DISCUSSION_SECONDS} soniyadan so'ng "
                "ovoz berish tugmalari shaxsiy chatingizga tushadi. 🤖",
        reply_markup=_bot_dm_button(),
    )

    t = threading.Timer(DAY_DISCUSSION_SECONDS, lambda: open_day_voting(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)

    # 🔄 checkpoint
    game["day_sub_phase"] = "discussion"
    game["phase_deadline"] = time.time() + DAY_DISCUSSION_SECONDS
    save_games_state()


def open_day_voting(chat_id):
    """Muhokama vaqti (DAY_DISCUSSION_SECONDS) tugagach chaqiriladi — ovoz berish tugmalarini
    tirik o'yinchilarning shaxsiy chatiga yuboradi va DAY_VOTE_SECONDS soniyalik hisobni boshlaydi."""
    game = GAMES.get(chat_id)
    if not game or game["phase"] != "day":
        return
    game["voting_open"] = True
    vote_seconds = game.get("vote_seconds_today", DAY_VOTE_SECONDS)

    # 🕵️ Missiya kuzatuvi — ovoz ochilgunga qadar bir marta ham yozmagan tirik
    # o'yinchilar "jim o'tirish" missiyasini shu kunda bajargan hisoblanadi
    spoke = game.get("spoke_before_vote_today", set())
    for uid in alive_players(game):
        if uid not in spoke:
            game.setdefault("silent_before_vote_ever", set()).add(uid)

    bot.send_message(
        chat_id,
        f"🗳 <b>Ovoz berish boshlandi!</b> Sizda {vote_seconds} soniya vaqt bor — "
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

    t = threading.Timer(vote_seconds, lambda: resolve_day(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)

    # 🔄 checkpoint
    game["day_sub_phase"] = "voting"
    game["phase_deadline"] = time.time() + vote_seconds
    save_games_state()


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
    game.setdefault("activity_score", {})
    game["activity_score"][voter_id] = game["activity_score"].get(voter_id, 0) + 1
    game.setdefault("vote_order", [])
    if voter_id in game["vote_order"]:
        game["vote_order"].remove(voter_id)  # qayta ovoz bersa, oxirgi o'ringa ko'chadi
    game["vote_order"].append(voter_id)
    voter_name = game["players"][voter_id]["name"]
    target_name = "o'tkazib yuborish" if target == "skip" else game["players"][target]["name"]

    revote_left = get_charges(voter_id).get("revote", 0)
    kb = None
    if revote_left > 0:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(f"🔄 Ovozni o'zgartirish ({revote_left} ta qoldi)", callback_data=f"revote|{chat_id}"))
    try:
        bot.edit_message_text(f"✅ Siz <b>{target_name}</b> deb ovoz berdingiz.", call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        pass
    bot.answer_callback_query(call.id, f"Siz {target_name} deb ovoz berdingiz.")
    target_mention = "o'tkazib yuborish" if target == "skip" else mention(target, game["players"][target]["name"])
    # 🔧 TUZATILDI: avval faqat NISHON ismi bosiladigan edi — endi OVOZ BERUVCHINING
    # ismi ham bosilganda uning profiliga o'tadi (barcha nik-neymlar izchil bosiladigan).
    bot.send_message(chat_id, f"🗳 {mention(voter_id, voter_name)} ovoz berdi: {target_mention}")


@bot.callback_query_handler(func=lambda c: c.data.startswith("revote|"))
def cb_revote(call):
    """⚡️ Energiya ichimligi — kunduzi ovoz bergandan keyin fikrni o'zgartirib,
    qayta ovoz berish imkonini beradi (charge tugaguncha)."""
    maybe_capture_owner(call.from_user)
    _, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    game = GAMES.get(chat_id)
    voter_id = call.from_user.id
    if not game or game["phase"] != "day" or not game.get("voting_open"):
        bot.answer_callback_query(call.id, "Ovoz berish yakunlangan.")
        return
    if voter_id not in game["players"] or not game["players"][voter_id]["alive"]:
        bot.answer_callback_query(call.id, "Faqat tirik ishtirokchilar ovoz bera oladi.")
        return
    if not use_charge(voter_id, "revote"):
        bot.answer_callback_query(call.id, "❌ Qayta ovoz berish huquqingiz qolmagan.", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup()
    for target_id, p in alive_players(game).items():
        kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"dv|{chat_id}|{target_id}"))
    kb.add(types.InlineKeyboardButton("🚫 O'tkazib yuborish", callback_data=f"dv|{chat_id}|skip"))
    try:
        bot.edit_message_text("🔄 <b>Ovozingizni qayta tanlang:</b>", call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        bot.send_message(chat_id if False else voter_id, "🔄 <b>Ovozingizni qayta tanlang:</b>", reply_markup=kb)
    bot.answer_callback_query(call.id, "✅ Qayta ovoz berishingiz mumkin!")


def resolve_day(chat_id):
    with GAME_LOCK:
        game = GAMES.get(chat_id)
        if not game or game["phase"] != "day":
            return

        for uid, p in alive_players(game).items():
            if uid not in game["votes"]:
                game["votes"][uid] = "skip"

        # 🗣 Provokator — belgilangan o'yinchining ovozi majburan boshqaga buriladi
        for forced_uid, forced_target in game.get("forced_day_votes", {}).items():
            if forced_uid in game["votes"] and game["players"].get(forced_uid, {}).get("alive"):
                game["votes"][forced_uid] = forced_target

        # 🕵️ Missiya kuzatuvi — ovoz berish statistikasi (birinchi/oxirgi ovoz beruvchi,
        # o'ziga/skip ovoz berganlar, mafiya nishoniga qarshi ovoz berganlar)
        vote_order = game.get("vote_order", [])
        if vote_order:
            game.setdefault("first_voter_ever", set()).add(vote_order[0])
            game.setdefault("last_voter_ever", set()).add(vote_order[-1])
        mafia_target = game.get("last_night_mafia_target")
        for voter, target in game["votes"].items():
            if target == voter:
                game.setdefault("self_vote_ever", set()).add(voter)
            if target == "skip":
                game.setdefault("skip_vote_ever", set()).add(voter)
            if mafia_target is not None and target == mafia_target:
                game.setdefault("anti_mafia_vote_ever", set()).add(voter)

        # 👨‍⚖️ Sudya — agar shu tunda faollashtirgan bo'lsa, uning ovozi 2x kuchga ega
        # 👑 Geroy (Magnus/Zephyrion "General nufuzi") — qo'shimcha +1 ovoz og'irligi
        tally = {}
        for voter, target in game["votes"].items():
            if target == "skip":
                continue
            weight = 2 if game.get("judge_double_vote") == voter else 1
            weight += hero_vote_weight_bonus(voter)
            tally[target] = tally.get(target, 0) + weight

        if not tally:
            bot.send_message(chat_id, "🤷 Hech kim ovoz bermadi, shuning uchun bugun hech kim osilmaydi.")
            finish_day_phase(chat_id)
            return

        max_v = max(tally.values())
        top = [uid for uid, v in tally.items() if v == max_v]
        if len(top) > 1:
            bot.send_message(chat_id, "⚖️ <b>Ovoz berish yakunlandi:</b>\nAholi kelisha olmadi... Kelisha olmaslik oqibatida hech kim osilmadi.")
            finish_day_phase(chat_id)
            return

        hanged = top[0]
        # 🕵️ Missiya kuzatuvi — ko'pchilik tanlagan (hozirgi eng ko'p ovoz olgan) kishiga
        # ovoz bergan har bir o'yinchi uchun "vote_majority" missiyasi bajarilgan hisoblanadi
        for voter, target in game["votes"].items():
            if target == hanged:
                game.setdefault("majority_vote_ever", set()).add(voter)

        if game.get("no_lynch_today"):
            bot.send_message(
                chat_id,
                f"🔍 <b>Taqdir hukmi kuchda!</b> {mention(hanged, game['players'][hanged]['name'])} eng ko'p ovoz oldi, "
                "ammo bugungi tasodifiy hodisa tufayli hech kim osilmaydi.",
            )
            finish_day_phase(chat_id)
            return

        # 🏆 Geroy (Draven "Xalq himoyasi") — FAQAT o'zi /geroy_himoya bilan shu kunga
        # QO'LDA faollashtirgan bo'lsa ishlaydi (avtomatik EMAS), va faqat 1 marta o'yin davomida
        if (hanged in game.get("hero_armed_vote_shield", set())
                and hero_has_ability(hanged, "vote_shield_once")
                and hanged not in game.setdefault("hero_vote_shield_used", set())):
            game["hero_vote_shield_used"].add(hanged)
            bot.send_message(
                chat_id,
                f"🗳🏆 <b>Geroy qobiliyati ishga tushdi!</b> {mention(hanged, game['players'][hanged]['name'])} "
                "eng ko'p ovoz oldi, ammo geroyining himoyasi tufayli bu safar osilmaydi! (Qobiliyat sarflandi.)",
            )
            for voter_uid in game["votes"]:
                if game["votes"][voter_uid] == hanged:
                    safe_send(voter_uid, "🗳🏆 <i>Ovoz bergan nishoningiz kimningdir geroy qobiliyati tufayli linchdan qutulib qoldi...</i>")
            finish_day_phase(chat_id)
            return
        if game["players"][hanged].get("smoke_active"):
            game["players"][hanged]["smoke_active"] = False
            bot.send_message(
                chat_id,
                f"💨 Aholi {mention(hanged, game['players'][hanged]['name'])}ni osmoqchi bo'ldi, "
                f"lekin 💣 Tutunli bomba tutuni ostida u qochib qutuldi! Bugun hech kim osilmadi.",
            )
            finish_day_phase(chat_id)
            return

        # 🗳 Eng ko'p ovoz olgan ishtirokchi aniqlandi — endi guruhga uning bosilsa
        # Telegram profiliga o'tadigan nikneymi bilan yakuniy tasdiqlash ovoz berishi ochiladi.
        start_hang_confirmation(chat_id, hanged)


def _confirm_kb(chat_id, yes_n, no_n):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(f"👍 Ha, osish ({yes_n})", callback_data=f"dvc|{chat_id}|yes"),
        types.InlineKeyboardButton(f"👎 Yo'q, osmaslik ({no_n})", callback_data=f"dvc|{chat_id}|no"),
    )
    return kb


def start_hang_confirmation(chat_id, target_uid):
    """Eng ko'p ovoz olgan ishtirokchini haqiqatan ham osish-osmaslik haqida
    guruhda 👍/👎 tasdiqlash ovoz berishini boshlaydi. Har bir tirik o'yinchi
    faqat bitta ovozga ega bo'ladi."""
    game = GAMES.get(chat_id)
    if not game:
        return
    name = game["players"][target_uid]["name"]
    game["confirm_vote"] = {"target": target_uid, "yes": set(), "no": set(), "message_id": None}
    text = (
        f"🗳 <b>Eng ko'p ovoz olgan ishtirokchi:</b> {mention(target_uid, name)}\n\n"
        f"❓ Siz rostan ham bu ishtirokchini osmoqchimisiz?"
    )
    sent = bot.send_message(chat_id, text, reply_markup=_confirm_kb(chat_id, 0, 0))
    game["confirm_vote"]["message_id"] = sent.message_id

    t = threading.Timer(CONFIRM_VOTE_SECONDS, lambda: resolve_hang_confirmation(chat_id))
    t.daemon = True
    t.start()
    game["timers"].append(t)

    # 🔄 checkpoint
    game["phase_deadline"] = time.time() + CONFIRM_VOTE_SECONDS
    save_games_state()


@bot.callback_query_handler(func=lambda c: c.data.startswith("dvc|"))
def cb_confirm_vote(call):
    maybe_capture_owner(call.from_user)
    _, chat_id_s, choice = call.data.split("|")
    chat_id = int(chat_id_s)
    game = GAMES.get(chat_id)
    uid = call.from_user.id
    cv = game.get("confirm_vote") if game else None

    if not game or not cv:
        bot.answer_callback_query(call.id, "Bu ovoz berish yakunlangan.")
        return
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "Faqat tirik ishtirokchilar ovoz bera oladi.")
        return

    # bitta o'yinchi — har bir tasdiqlash ovoz berishida bitta ovozga ega
    cv["yes"].discard(uid)
    cv["no"].discard(uid)
    if choice == "yes":
        cv["yes"].add(uid)
    else:
        cv["no"].add(uid)

    try:
        bot.edit_message_reply_markup(chat_id, cv["message_id"], reply_markup=_confirm_kb(chat_id, len(cv["yes"]), len(cv["no"])))
    except Exception:
        pass
    bot.answer_callback_query(call.id, "Ovozingiz qabul qilindi!")

    if len(cv["yes"]) + len(cv["no"]) >= len(alive_players(game)):
        resolve_hang_confirmation(chat_id)


def resolve_hang_confirmation(chat_id):
    with GAME_LOCK:
        game = GAMES.get(chat_id)
        cv = game.get("confirm_vote") if game else None
        if not game or not cv:
            return
        game["confirm_vote"] = None
        target_uid = cv["target"]
        yes_n, no_n = len(cv["yes"]), len(cv["no"])

        if target_uid not in game["players"] or not game["players"][target_uid]["alive"]:
            finish_day_phase(chat_id)
            return
        name = game["players"][target_uid]["name"]

        if yes_n <= no_n:
            bot.send_message(
                chat_id,
                f"🙅 Ovoz berish natijasi: 👍 {yes_n} — 👎 {no_n}.\nAholi rahm qildi, bugun hech kim osilmadi.",
            )
            finish_day_phase(chat_id)
            return

        # ⚖️ Advokat himoyasi yoki 🛡🌞 Kunduzgi himoya buyumi — bittasi bo'lsa yetarli
        protected_by_advokat = game.get("advocate_protect") == target_uid
        has_day_shield = get_charges(target_uid).get("day_shield", 0) > 0 and is_item_active(target_uid, "day_shield")
        if protected_by_advokat or has_day_shield:
            if has_day_shield:
                use_charge(target_uid, "day_shield")
                reason = "🛡🌞 Kunduzgi himoya tumori"
            else:
                reason = "⚖️ Advokat himoyasi"
            bot.send_message(
                chat_id,
                f"{reason} tufayli {mention(target_uid, name)} osilishdan qutulib qoldi! (👍 {yes_n} — 👎 {no_n})",
            )
            finish_day_phase(chat_id)
            return

        game["players"][target_uid]["alive"] = False
        role = game["players"][target_uid]["role"]
        bot.send_message(
            chat_id,
            f"⚰️ Ovoz berish natijasi: 👍 {yes_n} — 👎 {no_n}.\n"
            f"Aholi {mention(target_uid, name)}ni osdi.\n"
            f"Fosh qilingan roli: <b>{role}</b> edi.",
        )
        wait_last_words(chat_id, target_uid)
        handle_death_side_effects(game, chat_id, target_uid)  # 👑 Don vorisligi / 👻 Arvoh faollashuvi

        # 💣 Terrorist — uni kunduzi osib o'ldirishsa, o'zi bilan birga tasodifiy odamni ham portlatib ketadi
        if role == "Terrorist 💣":
            others = [pid for pid in alive_players(game) if pid != target_uid]
            if others:
                boom_target = random.choice(others)
                game["players"][boom_target]["alive"] = False
                bot.send_message(
                    chat_id,
                    f"💣 {mention(target_uid, name)} portlab, o'zi bilan birga "
                    f"{mention(boom_target, game['players'][boom_target]['name'])}ni ham olib ketdi!",
                )
                wait_last_words(chat_id, boom_target)
                handle_death_side_effects(game, chat_id, boom_target)  # 👑 Don vorisligi / 👻 Arvoh faollashuvi

        finish_day_phase(chat_id)


def finish_day_phase(chat_id):
    game = GAMES.get(chat_id)
    if not game:
        return

    # 👁 Kuzatish ko'zi — to'liq ovoz taqsimotini DM orqali yuborish
    # 💼 Shubhali sumka — "hidden_vote" charge'i faol bo'lgan o'yinchining ovozi
    # bu hisobotda "noma'lum" bo'lib ko'rinadi (1 marta ishlatiladi)
    vote_lines = []
    for voter, target in game["votes"].items():
        voter_name = game["players"].get(voter, {}).get("name", "?")
        if get_charges(voter).get("hidden_vote", 0) > 0 and is_item_active(voter, "hidden_vote"):
            use_charge(voter, "hidden_vote")
            vote_lines.append(f"• {voter_name} → 🕵️ noma'lum (buyum bilan yashiringan)")
            # 🔧 TUZATILDI: avval bu yerda hech qanday DM yuborilmas edi
            safe_send(voter, "💼 Sizning <b>Shubhali sumka</b> buyumingiz ishladi — bu safar ovozingiz boshqalardan yashirildi!")
            continue
        target_name = "o'tkazib yuborish" if target == "skip" else game["players"].get(target, {}).get("name", "?")
        vote_lines.append(f"• {voter_name} → {target_name}")
    for uid, p in list(game["players"].items()):
        ch = get_charges(uid)
        if p["alive"] and ch.get("watch_eyes", 0) > 0 and is_item_active(uid, "watch_eyes"):
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


@bot.message_handler(commands=["tark_et"])
def cmd_tark_et(message):
    """🚪 O'yinchi o'zi xohlab o'yinni tark etadi — u avtomatik mag'lub hisoblanadi
    va o'yin oxirida g'olib jamoada bo'lsa ham mukofot olmaydi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    game = None
    chat_id = None
    for cid, g in GAMES.items():
        if uid in g["players"] and g["players"][uid]["alive"]:
            game, chat_id = g, cid
            break
    if not game:
        bot.send_message(message.chat.id, "❌ Siz hozir hech qanday faol o'yinda emassiz.")
        return
    game["players"][uid]["alive"] = False
    game["players"][uid]["left_game"] = True
    add_points(uid, -10, "left_game")
    name = game["players"][uid]["name"]
    bot.send_message(chat_id, f"🚪 {mention(uid, name)} o'yinni o'z xohishi bilan tark etdi. U mag'lub hisoblanadi.")
    safe_send(uid, "🚪 O'yinni tark etdingiz — bu o'yin uchun avtomatik mag'lub hisoblanasiz va yakuniy mukofot olmaysiz.")
    handle_death_side_effects(game, chat_id, uid)  # 👑 Don vorisligi / 👻 Arvoh faollashuvi
    check_and_end_game(chat_id)


def end_game(chat_id, winners_team):
    game = GAMES.get(chat_id)
    if not game:
        return
    lines = ["🏁 <b>O'yin tugadi!</b>\n"]
    lines.append(f"🎉 G'oliblar jamoasi: <b>{'Mafiya' if winners_team == 'mafia' else 'Tinch aholi'}</b>\n")

    # 🏅 Eng faol o'yinchini aniqlaymiz (tun/kun harakatlari soni bo'yicha)
    activity = game.get("activity_score", {})
    most_active_uid = max(activity, key=activity.get) if activity else None

    winners, losers = [], []
    for uid, p in game["players"].items():
        left = p.get("left_game", False)
        won = (p["team"] == winners_team) and not left  # 🚪 tark etganlar hech qachon g'olib hisoblanmaydi
        base_reward = WIN_REWARD if won else LOSE_REWARD
        reward = 0 if left else int(base_reward * luck_mult(uid))
        if reward:
            add_balance(uid, dollar=reward)
        u = user_dict(uid)
        update_user(uid, games=u["games"] + 1, wins=u["wins"] + (1 if won else 0))
        entry = f"{mention(uid, p['name'])} — <b>{p['role']}</b>" + (" (🚪 tark etgan)" if left else "")
        (winners if won else losers).append((uid, entry))  # 🔧 (uid, matn) — pastda aktivlikka qarab tartiblanadi
        # 🔧 TUZATILDI: guruhga yuboriladigan xabarda endi PUL VA BALL miqdorlari
        # KO'RSATILMAYDI (faqat ism+rol) — bularning barchasi FAQAT shaxsiy DM'da
        # ko'rsatiladi (pastdagi safe_send(uid, ...) qismida, o'zgarishsiz qoladi).

        # 🏅 Faollik ballari: g'alaba +5, mag'lubiyat -5, eng faol o'yinchi qo'shimcha +25,
        # tark etgan/AFK bo'lganlar allaqachon -10 olgan (start_night/cmd_tark_et'da)
        points_note = ""
        if not left:
            pts = 5 if won else -5
            add_points(uid, pts, "game_result")
            points_note = f" ({'+'if pts >= 0 else ''}{pts} ball)"
        if uid == most_active_uid and not left:
            add_points(uid, 25, "most_active")
            points_note += " (+25 ball — eng faol o'yinchi)"

        # 🕵️ Maxfiy missiya natijasi — shaxsiy DM
        mission_key = game.get("secret_missions", {}).get(uid)
        mission_note = ""
        if mission_key:
            done = check_mission_completed(game, uid, mission_key)
            if done:
                add_balance(uid, dollar=25)
                mission_note = "\n\n🕵️ Maxfiy missiyangizni <b>bajardingiz</b>! +25$ mukofot berildi."
            else:
                mission_note = "\n\n🕵️ Afsuski, maxfiy missiyangizni bajara olmadingiz."

        # 📬 Har bir o'yinchiga shaxsiy yakuniy xabar — yutilgan pul VA ball shu yerda ko'rsatiladi
        if left:
            outcome_line = "🚪 Siz o'yinni tark etgansiz — shu sabab bu o'yin uchun <b>mag'lub</b> hisoblanasiz va mukofot berilmaydi."
        elif won:
            outcome_line = f"🎉 <b>G'alaba qozondingiz!</b> +{reward}$ mukofot oldingiz{points_note}."
        else:
            outcome_line = f"😔 <b>Mag'lub bo'ldingiz.</b> +{reward}$ (ishtirok uchun) oldingiz{points_note}."
        safe_send(uid, f"🏁 O'yin tugadi!\n{outcome_line}{mission_note}")

    # 🔧 TUZATILDI: g'oliblar/mag'lublar endi o'yindagi FAOLLIKKA qarab (eng faoldan
    # kamroq faolgacha) ketma-ket joylashtiriladi — tasodifiy dict tartibi emas.
    winners.sort(key=lambda t: activity.get(t[0], 0), reverse=True)
    losers.sort(key=lambda t: activity.get(t[0], 0), reverse=True)

    lines.append("🏆 <b>G'oliblar:</b>")
    if winners:
        for i, (_uid, e) in enumerate(winners, start=1):
            lines.append(f"{i}. {e}")
    else:
        lines.append("— Yo'q —")
    lines.append("")
    lines.append("💀 <b>Mag'lublar:</b>")
    if losers:
        for i, (_uid, e) in enumerate(losers, start=1):
            lines.append(f"{i}. {e}")
    else:
        lines.append("— Yo'q —")
    if most_active_uid and most_active_uid in game["players"]:
        lines.append(f"\n🏅 Eng faol o'yinchi: {mention(most_active_uid, game['players'][most_active_uid]['name'])}")

    # 🐺🦅 Jamoaviy o'yin rejimi yoqilgan bo'lsa — qaysi jamoa ko'proq g'alaba
    # qozonganini alohida ko'rsatamiz (asosiy Mafiya/Tinch aholi natijasidan tashqari).
    if game.get("squad_mode") and game.get("squads"):
        wolf_wins = sum(1 for uid, _ in winners if game["squads"].get(uid) == "wolf")
        eagle_wins = sum(1 for uid, _ in winners if game["squads"].get(uid) == "eagle")
        if wolf_wins or eagle_wins:
            squad_winner = "🐺 Bo'ri jamoasi" if wolf_wins > eagle_wins else ("🦅 Burgut jamoasi" if eagle_wins > wolf_wins else "🤝 Durrang")
            lines.append(
                f"\n🐺🦅 <b>Jamoalar hisobi:</b> Bo'ri — {wolf_wins} g'alaba | Burgut — {eagle_wins} g'alaba\n"
                f"🏆 Jamoalar orasida bu safar yutgan: <b>{squad_winner}</b>"
            )

    bot.send_message(chat_id, "\n".join(lines))

    pair = add_pair_score(chat_id, winning_chat_id=chat_id)
    if pair:
        ca, cb, label_a, label_b, score_a, score_b = pair
        scoreboard = (
            f"🔴🔵 <b>Qizil vs Ko'k — umumiy hisob</b>\n\n"
            f"{label_a}: <b>{score_a}</b> g'alaba\n"
            f"{label_b}: <b>{score_b}</b> g'alaba"
        )
        other_id = cb if ca == chat_id else ca
        bot.send_message(chat_id, scoreboard)
        try:
            bot.send_message(other_id, scoreboard)
        except Exception:
            pass

    del GAMES[chat_id]
    save_games_state()

    # 🏛 Klan tizimi: klan lideri bo'lgan o'yinchilar har o'ynagan Hunter Mafia
    # o'yinidan keyin avtomatik +2 lvl oladi (klan spetsifikatsiyasi bo'yicha)
    for uid in game["players"]:
        clan = get_clan(uid)
        if clan:
            with db_lock:
                cur.execute("UPDATE clans SET leader_level = leader_level + 2 WHERE owner_id=?", (uid,))
                conn.commit()


# ================================================================================
#  DUEL / NIKOH
# ================================================================================

DUEL_COST = 100

# ⚔️ Tasodifiy qurollar — har birining nishonchi (chorlovchi) uchun boshlang'ich
# g'alaba ehtimoli turlicha (keyin geroy bonuslari ustiga qo'shiladi)
DUEL_WEAPONS = [
    {"name": "🔫 Pistolet", "verb": "bir-biriga qarab otishdi", "challenger_chance": 0.50},
    {"name": "🔪 Pichoq", "verb": "yaqin jangda to'qnashishdi", "challenger_chance": 0.55},
    {"name": "☠️ Zahar", "verb": "bir-birining ichimligiga zahar qo'shishga urinishdi", "challenger_chance": 0.45},
    {"name": "🎯 Snayper", "verb": "uzoqdan nishonga oldi", "challenger_chance": 0.60},
    {"name": "🥊 Mushtlashuv", "verb": "yelkama-yelka mushtlashdi", "challenger_chance": 0.50},
]

DUEL_ANIMATION_STEPS = [
    "🎯 O'yinchilar nishonga olyapti...",
    "⚔️ Jang boshlandi...",
    "📊 Natijalar hisoblanmoqda...",
]


def resolve_duel_outcome(a_id, b_id, weapon=None):
    """(g'olib, mag'lub) qaytaradi — yoki (None, None) agar durrang bo'lsa
    (🏆 Magnus/Zephyrion "Qat'iy zarba" qobiliyati tufayli). `a_id` — chorlovchi (challenger)."""
    a_ch, b_ch = get_charges(a_id), get_charges(b_id)
    a_guaranteed = a_ch.get("duel_guaranteed_win", 0) > 0
    b_guaranteed = b_ch.get("duel_guaranteed_win", 0) > 0
    winner, loser = None, None
    # Ikkalasida ham kafolatlangan g'alaba bo'lsa — ikkalasi ham sarflanadi,
    # keyin oddiy imkoniyat asosida hal qilinadi (birovi ikkinchisini "yutib" ketmasin).
    if a_guaranteed and b_guaranteed:
        use_charge(a_id, "duel_guaranteed_win")
        use_charge(b_id, "duel_guaranteed_win")
        winner, loser = tuple(random.sample([a_id, b_id], 2))
    elif a_guaranteed:
        use_charge(a_id, "duel_guaranteed_win")
        winner, loser = a_id, b_id
    elif b_guaranteed:
        use_charge(b_id, "duel_guaranteed_win")
        winner, loser = b_id, a_id
    else:
        a_adv = a_ch.get("duel_adv", 0) > 0 and is_item_active(a_id, "duel_adv")
        b_adv = b_ch.get("duel_adv", 0) > 0 and is_item_active(b_id, "duel_adv")
        if a_adv and not b_adv:
            use_charge(a_id, "duel_adv")
            winner, loser = (a_id, b_id) if random.random() < 0.65 else (b_id, a_id)
        elif b_adv and not a_adv:
            use_charge(b_id, "duel_adv")
            winner, loser = (b_id, a_id) if random.random() < 0.65 else (a_id, b_id)
        else:
            # ⚔️ Tasodifiy qurol — chorlovchi (a_id) uchun boshlang'ich ehtimol
            base_chance = (weapon or {}).get("challenger_chance", 0.5)
            # 🏆 Geroy (Magnus / Zephyrion) — duelda g'alaba ehtimolini oshiradi
            a_hero_bonus = hero_duel_bonus(a_id)
            b_hero_bonus = hero_duel_bonus(b_id)
            a_win_chance = max(0.10, min(0.90, base_chance + a_hero_bonus - b_hero_bonus))
            winner, loser = (a_id, b_id) if random.random() < a_win_chance else (b_id, a_id)

    # 🏆 Geroy (Magnus/Zephyrion "Qat'iy zarba") — mag'lub bo'lgan tomonda ushbu
    # qobiliyat bo'lsa, tasodifiy foizda durrang (hech kim yutqazmaydi)
    draw_chance = hero_duel_draw_chance(loser)
    if draw_chance > 0 and random.random() < draw_chance:
        return None, None
    return winner, loser


@bot.message_handler(commands=["duel", "Duel"])
def cmd_duel(message):
    """⚔️ Duel taklifi — ixtiyoriy tikish summasi bilan: /duel 250 (kimningdir xabariga reply qilib).
    Summa ko'rsatilmasa standart $100 ishlatiladi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not message.reply_to_message:
        return
    sender = message.from_user
    target = message.reply_to_message.from_user

    # 🔒 Xavfsizlik: o'z-o'ziga duel tashlab bo'lmaydi
    if target.id == sender.id:
        bot.send_message(message.chat.id, "❌ O'zingizga duel tashlay olmaysiz! 😅")
        return
    if target.is_bot:
        bot.send_message(message.chat.id, "❌ Botga duel tashlab bo'lmaydi.")
        return
    if is_banned(sender.id) or is_banned(target.id):
        return

    # 💰 Tikish summasini o'qish (ixtiyoriy, standart $100)
    parts = message.text.split()
    bet = DUEL_COST
    if len(parts) > 1:
        try:
            bet = int(parts[1])
        except ValueError:
            bot.send_message(message.chat.id, "❌ Tikish summasi butun son bo'lishi kerak. Masalan: <code>/duel 250</code>")
            return
        if bet < 10:
            bot.send_message(message.chat.id, "❌ Eng kam tikish summasi: $10.")
            return

    sd = user_dict(sender.id, sender.first_name)
    td = user_dict(target.id, target.first_name or "O'yinchi")
    if sd["dollar"] < bet:
        bot.send_message(message.chat.id, f"❌ Sizda yetarli mablag' yo'q! Tikish uchun ${bet} kerak, sizda ${sd['dollar']} bor.")
        return
    if td["dollar"] < bet:
        bot.send_message(message.chat.id, f"❌ {td['name']}da yetarli mablag' yo'q (${bet} kerak, unda ${td['dollar']} bor).")
        return

    PENDING_PROPOSALS[target.id] = {"from": sender.id, "type": "duel", "chat_id": message.chat.id, "bet": bet}
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("⚔️ Qabul qilish", callback_data=f"duel|yes|{sender.id}|{target.id}"),
        types.InlineKeyboardButton("🏳 Rad etish", callback_data=f"duel|no|{sender.id}|{target.id}"),
    )
    bot.send_message(
        message.chat.id,
        f"⚔️ {mention(sender.id, sender.first_name)}, {mention(target.id, target.first_name)}ni "
        f"<b>${bet}</b> tikishga duelga chorlayapti! Qabul qilasizmi?",
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
    if not pending or pending["from"] != sender_id or pending.get("type") != "duel":
        bot.answer_callback_query(call.id, "Taklif eskirgan.")
        return
    PENDING_PROPOSALS.pop(target_id, None)
    bet = pending.get("bet", DUEL_COST)

    if action == "no":
        bot.edit_message_text(random.choice(DUEL_REJECT_JOKES), call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    sd, td = user_dict(sender_id), user_dict(target_id)
    if sd["dollar"] < bet or td["dollar"] < bet:
        bot.edit_message_text("❌ Duel bekor qilindi — balans yetarli emas.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return
    bot.answer_callback_query(call.id, "⚔️ Duel boshlandi!")

    # ⚔️ Tasodifiy qurol tanlanadi
    weapon = random.choice(DUEL_WEAPONS)
    sender_name = sd["name"]
    target_name = td["name"]

    # 🎬 Dinamik animatsiya — natija darhol chiqmaydi, bir necha bosqichda yangilanadi
    try:
        bot.edit_message_text(
            f"{weapon['name']} <b>QUROL TANLANDI!</b>\n\n{sender_name} va {target_name} {weapon['verb']}...\n\n"
            f"{DUEL_ANIMATION_STEPS[0]}",
            call.message.chat.id, call.message.message_id,
        )
        for step in DUEL_ANIMATION_STEPS[1:]:
            time.sleep(1.4)
            bot.edit_message_text(
                f"{weapon['name']} <b>{sender_name} 🆚 {target_name}</b>\n\n{step}",
                call.message.chat.id, call.message.message_id,
            )
        time.sleep(1.2)
    except Exception:
        pass

    winner, loser = resolve_duel_outcome(sender_id, target_id, weapon=weapon)
    if winner is None:
        # 🏆 Geroy "Qat'iy zarba" — durrang, hisoblar teng qoladi, hech kim yutqazmaydi
        bot.edit_message_text(
            f"{weapon['name']} 🤝 <b>Duel durrang yakunlandi!</b>\n\nBir tomonning geroy qobiliyati mag'lubiyatni "
            "durrangga aylantirdi — hech kimning puli o'zgarmadi.",
            call.message.chat.id, call.message.message_id,
        )
        safe_send(sender_id, "🤝 Duelingiz durrang tugadi — geroy qobiliyati ishga tushdi!")
        safe_send(target_id, "🤝 Duelingiz durrang tugadi — geroy qobiliyati ishga tushdi!")
        return
    reward = int(bet * luck_mult(winner))
    add_balance(winner, dollar=reward)
    add_balance(loser, dollar=-bet)
    record_duel_result(winner, loser)
    winner_name, loser_name = user_dict(winner)["name"], user_dict(loser)["name"]
    bot.edit_message_text(
        f"{weapon['name']} <b>DUEL YAKUNLANDI!</b>\n\n"
        f"🏆 G'olib: <b>{winner_name}</b>\n💀 Mag'lub: <b>{loser_name}</b>\n"
        f"💰 {winner_name} ${reward} yutib oldi ({loser_name}dan)!",
        call.message.chat.id, call.message.message_id,
    )
    safe_send(loser, f"😅 <b>Duelda yutqazdingiz...</b> (-${bet})\n\n{random.choice(DEFEAT_JOKES)}")
    safe_send(winner, f"🏆 <b>Duelda g'alaba qozondingiz!</b> +${reward}")


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


# ================================================================================
#  🏆 MUSOBAQALAR (TURNIRLAR) — TO'LIQ ISHLAYDIGAN TIZIM
# ================================================================================

def is_group_admin_or_owner(message):
    if is_owner(message.from_user.id):
        return True
    try:
        member = bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


@bot.message_handler(commands=["turnir_boshla"])
def cmd_turnir_boshla(message):
    """🏆 FAQAT BOT EGASI (owner) yangi turnir ochadi — ro'yxatga olish boshlanadi.
    (Musobaqalar rejimi endi faqat owner ruxsati bilan o'tkaziladi — guruh
    admini ENDI mustaqil turnir boshlay olmaydi.)"""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        bot.send_message(message.chat.id, "🏆 Turnirlar faqat guruhda tashkil qilinadi.")
        return
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Musobaqalar (turnir) rejimini FAQAT bot egasi boshlashi mumkin.")
        return
    chat_id = message.chat.id
    if chat_id in TOURNAMENTS and TOURNAMENTS[chat_id]["status"] != "finished":
        bot.send_message(message.chat.id, "⚠️ Bu guruhda allaqachon faol turnir bor. Avval /turnir_tugat bilan yakunlang.")
        return
    parts = message.text.split(maxsplit=1)
    name = parts[1].strip() if len(parts) > 1 else "Hunter Mafia Turniri"
    TOURNAMENTS[chat_id] = {
        "name": name, "status": "registration", "participants": {},
        "eliminated": [], "matches": [], "host_id": message.from_user.id,
    }
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Ishtirok etish", callback_data=f"tjoin|{chat_id}"))
    bot.send_message(
        message.chat.id,
        f"🏆⚔️ <b>YANGI TURNIR OCHILDI: {name}</b>\n\n"
        "Istagan o'yinchi pastdagi tugma orqali ro'yxatdan o'ta oladi!\n"
        "Tashkilotchi tayyor bo'lganda /turnir_yopish buyrug'i bilan ro'yxatni yopadi va jangларни boshlaydi.",
        reply_markup=kb,
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("tjoin|"))
def cb_turnir_join(call):
    maybe_capture_owner(call.from_user)
    chat_id = int(call.data.split("|")[1])
    t = TOURNAMENTS.get(chat_id)
    if not t or t["status"] != "registration":
        bot.answer_callback_query(call.id, "⚠️ Ro'yxatga olish yopilgan yoki turnir topilmadi.", show_alert=True)
        return
    uid = call.from_user.id
    if uid in t["participants"]:
        bot.answer_callback_query(call.id, "✅ Siz allaqachon ro'yxatdasiz!", show_alert=True)
        return
    t["participants"][uid] = call.from_user.first_name
    user_dict(uid, call.from_user.first_name)
    bot.answer_callback_query(call.id, "🎉 Turnirga muvaffaqiyatli qo'shildingiz!", show_alert=True)
    bot.send_message(call.message.chat.id, f"🙋 {mention(uid, call.from_user.first_name)} turnirga qo'shildi! (jami: {len(t['participants'])})")


@bot.message_handler(commands=["turnir_royxat"])
def cmd_turnir_royxat(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    t = TOURNAMENTS.get(message.chat.id)
    if not t:
        bot.send_message(message.chat.id, "📭 Bu guruhda hozircha turnir yo'q.")
        return
    remaining = {uid: name for uid, name in t["participants"].items() if uid not in t["eliminated"]}
    lines = [f"🏆 <b>{t['name']}</b> — holat: {t['status']}\n"]
    lines.append(f"👥 <b>Ishtirokchilar ({len(t['participants'])}):</b>")
    for i, (uid, name) in enumerate(t["participants"].items(), 1):
        tag = " ❌" if uid in t["eliminated"] else " 🟢"
        lines.append(f"{i}. {mention(uid, name)}{tag}")
    if t["status"] == "ongoing":
        lines.append(f"\n⚔️ Hozir kurashda: {len(remaining)} kishi qoldi.")
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["turnir_yopish"])
def cmd_turnir_yopish(message):
    """🏆 Ro'yxatga olishni yopadi va turnirni boshlaydi (kamida 2 kishi kerak)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    chat_id = message.chat.id
    t = TOURNAMENTS.get(chat_id)
    if not t or t["status"] != "registration":
        bot.send_message(chat_id, "⚠️ Hozir yopiladigan ro'yxat yo'q.")
        return
    if not (is_owner(message.from_user.id) or message.from_user.id == t["host_id"]):
        bot.send_message(chat_id, "⛔ Musobaqalar (turnir) rejimini FAQAT bot egasi boshqarishi mumkin.")
        return
    if len(t["participants"]) < 2:
        bot.send_message(chat_id, "⚠️ Turnir boshlanishi uchun kamida 2 ta ishtirokchi kerak.")
        return
    t["status"] = "ongoing"
    names = ", ".join(mention(uid, name) for uid, name in t["participants"].items())
    bot.send_message(
        chat_id,
        f"🔒 <b>Ro'yxatga olish yopildi!</b> Jami {len(t['participants'])} ishtirokchi: {names}\n\n"
        f"⚔️ Tashkilotchi endi /turnir_jang buyrug'i orqali navbatdagi ikki kurashchini tanlaydi.",
    )


@bot.message_handler(commands=["turnir_jang"])
def cmd_turnir_jang(message):
    """⚔️ Tashkilotchi 2 ta qolgan ishtirokchini tanlab, ular orasida Turnir Jangini boshlaydi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    chat_id = message.chat.id
    t = TOURNAMENTS.get(chat_id)
    if not t or t["status"] != "ongoing":
        bot.send_message(chat_id, "⚠️ Hozir faol (ongoing) turnir yo'q.")
        return
    if not (is_owner(message.from_user.id) or message.from_user.id == t["host_id"]):
        bot.send_message(chat_id, "⛔ Musobaqalar (turnir) rejimini FAQAT bot egasi boshqarishi mumkin.")
        return
    remaining = {uid: name for uid, name in t["participants"].items() if uid not in t["eliminated"]}
    if len(remaining) < 2:
        bot.send_message(chat_id, "🏆 Kurashadigan yetarli ishtirokchi qolmadi — turnir allaqachon yakunlangan bo'lishi mumkin.")
        return
    TOURNAMENT_PICK[message.from_user.id] = {"chat_id": chat_id, "a": None}
    kb = types.InlineKeyboardMarkup()
    for uid, name in remaining.items():
        kb.add(types.InlineKeyboardButton(name, callback_data=f"tpick|{message.from_user.id}|{uid}"))
    bot.send_message(chat_id, "⚔️ <b>1-kurashchini tanlang:</b>", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("tpick|"))
def cb_turnir_pick(call):
    maybe_capture_owner(call.from_user)
    _, host_id_s, uid_s = call.data.split("|")
    host_id, picked_uid = int(host_id_s), int(uid_s)
    if call.from_user.id != host_id:
        bot.answer_callback_query(call.id, "❌ Bu tanlov sizga tegishli emas.", show_alert=True)
        return
    state = TOURNAMENT_PICK.get(host_id)
    if not state:
        bot.answer_callback_query(call.id, "❌ Tanlov muddati tugagan, qaytadan /turnir_jang bosing.", show_alert=True)
        return
    t = TOURNAMENTS.get(state["chat_id"])
    if not t or t["status"] != "ongoing":
        bot.answer_callback_query(call.id, "❌ Turnir faol emas.", show_alert=True)
        return
    remaining = {uid: name for uid, name in t["participants"].items() if uid not in t["eliminated"]}

    if state["a"] is None:
        state["a"] = picked_uid
        bot.answer_callback_query(call.id, f"✅ 1-kurashchi: {remaining.get(picked_uid, '?')}")
        kb = types.InlineKeyboardMarkup()
        for uid, name in remaining.items():
            if uid == picked_uid:
                continue
            kb.add(types.InlineKeyboardButton(name, callback_data=f"tpick|{host_id}|{uid}"))
        try:
            bot.edit_message_text(
                f"✅ 1-kurashchi: <b>{remaining.get(picked_uid, '?')}</b>\n\n⚔️ Endi 2-kurashchini tanlang:",
                call.message.chat.id, call.message.message_id, reply_markup=kb,
            )
        except Exception:
            pass
        return

    if picked_uid == state["a"]:
        bot.answer_callback_query(call.id, "❌ Bir xil odamni 2 marta tanlab bo'lmaydi.", show_alert=True)
        return

    a_id, b_id = state["a"], picked_uid
    a_name, b_name = remaining.get(a_id, "?"), remaining.get(b_id, "?")
    del TOURNAMENT_PICK[host_id]
    bot.answer_callback_query(call.id, "⚔️ Jang boshlanmoqda!")
    try:
        bot.edit_message_text(
            f"⚔️ <b>JANG:</b> {a_name} 🆚 {b_name}\n\n🎲 Natija aniqlanmoqda...",
            call.message.chat.id, call.message.message_id,
        )
    except Exception:
        pass
    run_tournament_match(t, state["chat_id"], a_id, b_id)


def run_tournament_match(t, chat_id, a_id, b_id):
    """⚔️ Turnir jangi — duel'dan farqli, faqat 1v1 elimination uchun; hero
    bonuslari (Magnus/Zephyrion) shu yerda ham hisobga olinadi, lekin duel
    statistikasiga (/duel_stat) ta'sir qilmaydi — bu alohida rejim."""
    a_name = t["participants"].get(a_id, "?")
    b_name = t["participants"].get(b_id, "?")
    # 🏆 Geroy "Qat'iy zarba" durrang berishi mumkin, lekin turnirda albatta bitta
    # g'olib chiqishi SHART — shuning uchun durrang chiqsa, qayta hal qilinadi.
    winner, loser = resolve_duel_outcome(a_id, b_id)
    retries = 0
    while winner is None and retries < 5:
        winner, loser = tuple(random.sample([a_id, b_id], 2))
        retries += 1
    winner_name = t["participants"].get(winner, "?")
    loser_name = t["participants"].get(loser, "?")

    t["eliminated"].append(loser)
    t["matches"].append({"a": a_id, "b": b_id, "winner": winner})
    add_points(winner, 3, "tournament_match_win")

    fight_flavor = random.choice([
        "🗡 Ayovsiz jang yakunlandi!",
        "💥 Hayratlanarli kurashdan so'ng g'olib aniqlandi!",
        "🔥 Ikkalasi ham jonbozlik ko'rsatdi, lekin faqat bittasi qoldi!",
        "⚡️ Bir zumda hal bo'lgan ajoyib jang!",
        "🎯 Aniq va shafqatsiz zarba bilan yakunlandi!",
    ])
    bot.send_message(
        chat_id,
        f"{fight_flavor}\n\n"
        f"🏆 <b>G'olib: {mention(winner, winner_name)}</b>\n"
        f"💀 Mag'lub: {mention(loser, loser_name)} — turnirdan chetlashtirildi.",
    )
    safe_send(winner, f"🏆 Turnir jangida g'olib chiqdingiz: {a_name} 🆚 {b_name}! Keyingi bosqichga o'tdingiz.")
    safe_send(loser, f"💀 Turnir jangida mag'lub bo'ldingiz: {a_name} 🆚 {b_name}. Turnir shu yerda tugadi, lekin harakatingiz uchun rahmat!")

    remaining = {uid: name for uid, name in t["participants"].items() if uid not in t["eliminated"]}
    if len(remaining) == 1:
        champion_id = list(remaining.keys())[0]
        champion_name = remaining[champion_id]
        t["status"] = "finished"
        add_balance(champion_id, dollar=500, diamond=20)
        add_points(champion_id, 50, "tournament_champion")
        bot.send_message(
            chat_id,
            f"👑🏆 <b>TURNIR CHEMPIONI: {mention(champion_id, champion_name)}!</b> 🏆👑\n\n"
            f"🎉 <b>{t['name']}</b> g'olibi aniqlandi!\n"
            f"🎁 Mukofot: +500$ 💵, +20 💎, +50 🏅 ball!\n\n"
            "Yangi turnir uchun /turnir_boshla deb yozing!",
        )
        safe_send(champion_id, f"👑 Tabriklaymiz! Siz <b>{t['name']}</b> turnirining CHEMPIONI bo'ldingiz! +500$, +20💎, +50 ball oldingiz!")
    else:
        bot.send_message(chat_id, f"⚔️ Kurash davom etadi — {len(remaining)} kishi qoldi. Tashkilotchi /turnir_jang bilan navbatdagi jangni boshlaydi.")


@bot.message_handler(commands=["turnir_tugat"])
def cmd_turnir_tugat(message):
    """🛑 Turnirni majburan yakunlaydi/bekor qiladi (tashkilotchi/admin/owner)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    chat_id = message.chat.id
    t = TOURNAMENTS.get(chat_id)
    if not t:
        bot.send_message(chat_id, "📭 Bu guruhda hozircha turnir yo'q.")
        return
    if not (is_owner(message.from_user.id) or message.from_user.id == t["host_id"]):
        bot.send_message(chat_id, "⛔ Musobaqalar (turnir) rejimini FAQAT bot egasi bekor qila oladi.")
        return
    del TOURNAMENTS[chat_id]
    bot.send_message(chat_id, "🛑 Turnir bekor qilindi/yakunlandi.")



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
    if is_banned(proposer.id) or is_banned(target.id):
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
        f"💐 {mention(proposer.id, proposer.first_name)}, {mention(target.id, target.first_name)}ga turmush qurishni taklif qildi!",
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
        married_at = time.strftime("%Y-%m-%d %H:%M:%S")
        update_user(proposer_id, married_to=target_id, married_at=married_at)
        update_user(target_id, married_to=proposer_id, married_at=married_at)
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
    partner = get_partner_mention(uid)
    if partner:
        text = f"💍 <b>Oilaviy holat:</b> Nikohda ❤️\n\nSizning juftingiz: {partner}"
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
    update_user(uid, married_to=0, married_at="")
    update_user(partner_id, married_to=0, married_at="")
    bot.send_message(message.chat.id, "💔 Siz juftingiz bilan ajrashdingiz. Endi boshqa nikoh qurishingiz mumkin.")


# ================================================================================
#  💍 OILAVIY QO'SHIMCHA FUNKSIYALAR (5 ta) — /OilaInfo /Quchoqla /OilaTop /Sovgla /Xiyonat
#  Barchasi mavjud "married_to"/"married_at" ustunlariga moslashtirilgan, hech qanday
#  o'yin imtiyozi bermaydi — faqat qiziqarli/hazil funksiyalar.
# ================================================================================

def _married_seconds(married_at_str):
    """married_at ('%Y-%m-%d %H:%M:%S') dan hozirgi vaqtgacha o'tgan soniyalarni hisoblaydi."""
    if not married_at_str:
        return None
    try:
        then = time.mktime(time.strptime(married_at_str, "%Y-%m-%d %H:%M:%S"))
    except Exception:
        return None
    return max(0, time.time() - then)


def _format_duration(seconds):
    """Soniyani 'X kun Y soat Z daqiqa' ko'rinishiga o'giradi."""
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days} kun")
    if hours or days:
        parts.append(f"{hours} soat")
    parts.append(f"{minutes} daqiqa")
    return " ".join(parts)


@bot.message_handler(commands=["OilaInfo", "oilainfo"])
def cmd_oila_info(message):
    """💍 Juftlik qancha vaqtdan beri birga ekanini ko'rsatadi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    u = user_dict(uid, message.from_user.first_name)
    partner_id = u.get("married_to") or 0
    if not partner_id:
        bot.send_message(message.chat.id, "👤 Siz hozircha bo'ydozsiz. Nikoh qurish uchun kimningdir xabariga reply qilib /nikoh deb yozing.")
        return
    partner_name = user_dict(partner_id).get("name", "Noma'lum")
    secs = _married_seconds(u.get("married_at"))
    if secs is None:
        bot.send_message(message.chat.id, "💍 Siz nikohdasiz, ammo nikoh sanasi topilmadi.")
        return
    duration = _format_duration(secs)
    milestone = ""
    days = secs // 86400
    if days >= 365:
        milestone = "\n🎉 Tabriklaymiz, allaqachon 1 yildan ortiq birgasiz! 💞"
    elif days >= 30:
        milestone = "\n🎊 1 oydan ortiq davom etayotgan mustahkam oila!"
    elif days < 1:
        milestone = "\n🌸 Yangi qurilgan oila — hali gullar so'lmagan!"
    bot.send_message(
        message.chat.id,
        f"💍 <b>OILAVIY MA'LUMOT</b>\n\n"
        f"{mention(uid, u['name'])} ❤️ {mention(partner_id, partner_name)}\n\n"
        f"⏳ Birga bo'lganingizga: <b>{duration}</b> bo'ldi.{milestone}",
    )


HUG_JOKES = [
    "{a} {b}ni mahkam quchoqladi — atrofdagilar hatto \"awww\" deb yubordi! 🤗💞",
    "{a} {b}ga shunday quchoq berdiki, hatto guruh admin botlari ham hayajonlandi! 🥹🤗",
    "{a} {b}ni quchoqladi va \"seni sog'indim!\" deb pichirladi... yoki shunga o'xshash narsa dedi. 🤗",
    "{a} {b}ni quchoqlab, ikkalasi ham 5 daqiqa jilmayib turishdi. 😊🤗",
    "{a} {b}ga issiq quchoq berdi — guruh chatida vaqtincha romantika hidi taraldi! 🌸🤗",
]

CUDDLE_JOKES = [
    "{a} {b}ning yonog'idan chiroyli o'pich oldi — {b} qizarib ketdi! 😳💋",
    "{a} {b}ga mehr bilan o'pich yubordi — havoda yurak shakllari uchib ketdi! 💋💕",
    "{a} {b}ni erkalatdi, {b} esa \"yana!\" deb hazillashdi. 💋😄",
    "{a} {b}ga shirin o'pich berdi — atrofdagilar \"voy tuya\" deb ketishdi! 💋🥰",
    "{a} {b}ni erkalab, ikkalasi bir-birlariga jilmayib qarab qolishdi. 💋😊",
]


def _require_partner_reply(message):
    """Reply qilingan kishi haqiqatan ham xabar yuboruvchining turmush o'rtog'imi — tekshiradi.
    (ok, uid, partner_id, partner_name, error_msg) qaytaradi."""
    uid = message.from_user.id
    u = user_dict(uid, message.from_user.first_name)
    partner_id = u.get("married_to") or 0
    if not partner_id:
        return False, uid, None, None, "👤 Siz bo'ydozsiz — bu buyruq faqat nikohdagilar uchun."
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return False, uid, None, None, "❌ Bu buyruqni juftingizning xabariga REPLY qilib yozing."
    target = message.reply_to_message.from_user
    if target.id != partner_id:
        return False, uid, None, None, "❌ Siz faqat o'zingizning turmush o'rtog'ingizga shu amalni bajarishingiz mumkin."
    return True, uid, partner_id, target.first_name, None


@bot.message_handler(commands=["Quchoqla", "quchoqla", "Opich", "opich"])
def cmd_quchoqla(message):
    """🤗💋 Juftiga reply qilib, guruhda chiroyli/hazilomuz erkalash matni chiqadi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    ok, uid, partner_id, partner_name, err = _require_partner_reply(message)
    if not ok:
        bot.send_message(message.chat.id, err)
        return
    is_opich = message.text.split()[0].lower().lstrip("/").startswith("opich")
    jokes = CUDDLE_JOKES if is_opich else HUG_JOKES
    text = random.choice(jokes).format(a=mention(uid, message.from_user.first_name), b=mention(partner_id, partner_name))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["OilaTop", "oilatop"])
def cmd_oila_top(message):
    """🏆 Guruhdagi (yoki bot bo'yicha umuman) eng uzoq vaqt birga bo'lgan juftliklar TOP ro'yxati."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    with db_lock:
        cur.execute("SELECT user_id, name, married_to, married_at FROM users WHERE married_to != 0 AND married_at != ''")
        rows = cur.fetchall()
    seen = set()
    pairs = []
    for uid, name, partner_id, married_at in rows:
        pair_key = tuple(sorted((uid, partner_id)))
        if pair_key in seen:
            continue
        seen.add(pair_key)
        secs = _married_seconds(married_at)
        if secs is None:
            continue
        partner_name = user_dict(partner_id).get("name", "Noma'lum")
        pairs.append((secs, uid, name, partner_id, partner_name))
    if not pairs:
        bot.send_message(message.chat.id, "💍 Hozircha hech qanday nikohlangan juftlik yo'q.")
        return
    pairs.sort(key=lambda x: x[0], reverse=True)
    lines = ["🏆 <b>ENG MUSTAHKAM OILALAR TOP RO'YXATI</b>\n"]
    for i, (secs, uid, name, partner_id, partner_name) in enumerate(pairs[:10], 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        lines.append(f"{medal} {mention(uid, name)} ❤️ {mention(partner_id, partner_name)} — {_format_duration(secs)}")
    bot.send_message(message.chat.id, "\n".join(lines))


GIFT_OPTIONS = {
    "atirgul": ("🌹", "atirgul"),
    "yurak": ("💖", "yurak"),
    "shokolad": ("🍫", "shokolad"),
}

GIFT_JOKES = [
    "{a} {b}ga {emoji} {gift} sovg'a qildi! {b} juda hayajonlandi! 🥰",
    "{a} {b}ga {emoji} {gift} tortiq qildi — atrofdagilar \"voy naqadar romantik\" deyishdi! 😍",
    "{a} sevgisini bildirib, {b}ga {emoji} {gift} yubordi! 💌",
    "{a}dan {b}ga {emoji} {gift} — sevgi tili so'zsiz ham tushunarli! 💞",
]


@bot.message_handler(commands=["Sovgla", "sovgla"])
def cmd_sovgla(message):
    """🎁 Juftiga reply orqali virtual sovg'a (atirgul/yurak/shokolad) yuborish."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    ok, uid, partner_id, partner_name, err = _require_partner_reply(message)
    if not ok:
        bot.send_message(message.chat.id, err)
        return
    parts = message.text.split(maxsplit=1)
    gift_key = parts[1].strip().lower() if len(parts) > 1 else ""
    if gift_key not in GIFT_OPTIONS:
        options = ", ".join(f"<code>{k}</code> {v[0]}" for k, v in GIFT_OPTIONS.items())
        bot.send_message(
            message.chat.id,
            f"🎁 Qaysi sovg'ani yubormoqchisiz? Juftingizning xabariga reply qilib yozing:\n"
            f"<code>/Sovgla &lt;sovg'a nomi&gt;</code>\n\nMavjud sovg'alar: {options}",
        )
        return
    emoji, gift_name = GIFT_OPTIONS[gift_key]
    text = random.choice(GIFT_JOKES).format(
        a=mention(uid, message.from_user.first_name), b=mention(partner_id, partner_name),
        emoji=emoji, gift=gift_name,
    )
    bot.send_message(message.chat.id, text)


BETRAYAL_JOKES = [
    "😱 {a} {b}ga \"xiyonat\" qildi — aslida faqat oxirgi bo'lak pitsani yeb qo'ygan edi! 🍕😂",
    "😨 SHOK! {a} {b}ning nomidan boshqasiga \"salom\" degan... hazil edi, tinchlaning! 😄",
    "💔 {a} {b}ga \"xiyonat\" qildi — telefon batareyasini oxirigacha ishlatib qo'yganini yashirgan edi! 🔋😂",
    "😂 Guruhda shov-shuv: {a} {b}ning sevimli seriyasini undan oldin ko'rib qo'yibdi! Bu haqiqiy \"xiyonat\" ekan! 📺",
    "🎭 {a} {b}ga hazilomuz \"xiyonat\" qildi... lekin tez orada \"kechir, hazil edi!\" deb ketidan yugurdi! 🏃💨",
]


@bot.message_handler(commands=["Xiyonat", "xiyonat"])
def cmd_xiyonat(message):
    """😄 Juftiga hazil tariqasida "xiyonat" qilish — faqat kulgi uchun, hech qanday
    o'yin ta'siri yo'q (nikoh buzilmaydi, pul/ball o'zgarmaydi)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    ok, uid, partner_id, partner_name, err = _require_partner_reply(message)
    if not ok:
        bot.send_message(message.chat.id, err)
        return
    text = random.choice(BETRAYAL_JOKES).format(
        a=mention(uid, message.from_user.first_name), b=mention(partner_id, partner_name),
    )
    bot.send_message(message.chat.id, text)


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
    bot.send_message(
        message.chat.id,
        f"🎁 {mention(sender.id, sender.first_name)} — {mention(target.id, target.first_name)}ga {amount} {icon} sovg'a qildi!",
    )
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
#  🔄 /tiklash, /restart — botni xavfsiz qayta ishga tushirish (faqat bot egasi)
#  Aktiv o'yinlar holati diskka saqlanadi, guruhlarga ogohlantirish yuboriladi,
#  so'ng bot jarayoni o'zini xuddi shu joyda (os.execv) qayta ishga tushiradi.
#  Qayta ishga tushgach, load_games_state() avtomatik chaqirilib, barcha o'yinlar
#  qolgan vaqtini hisoblab davom ettiriladi.
# ================================================================================

@bot.message_handler(commands=["tiklash", "restart", "Restart", "Tiklash"])
def cmd_restart(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return

    active_chats = list(GAMES.keys())
    bot.send_message(
        message.chat.id,
        f"🔄 Bot qayta ishga tushirilmoqda...\n"
        f"Aktiv o'yinlar soni: {len(active_chats)} ta — hammasi avtomatik tiklanadi.",
    )

    # 1) hozirgi holatni diskka yozamiz
    save_games_state()

    # 2) har bir aktiv o'yin guruhiga ogohlantirish yuboramiz
    for chat_id in active_chats:
        try:
            bot.send_message(
                chat_id,
                "🔄 <b>Bot texnik ishlar tufayli bir necha soniyaga qayta ishga tushmoqda.</b>\n"
                "O'yiningiz avtomatik saqlanadi va tiklanadi — iltimos biroz kuting. ⏳",
            )
        except Exception:
            pass

    _logger.info("🔄 /tiklash buyrug'i orqali bot %s tomonidan qayta ishga tushirilmoqda.", message.from_user.id)

    # 3) jarayonni o'zini o'zi (xuddi shu PID, xuddi shu argumentlar bilan) qayta ishga tushiramiz.
    #    os.execv joriy Python jarayonini to'liq almashtiradi — shuning uchun __main__ blokidagi
    #    load_games_state() chaqiruvi avtomatik ishga tushib, saqlangan o'yinlarni tiklaydi.
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        _logger.exception("⚠️ os.execv orqali qayta ishga tushirib bo'lmadi — jarayon to'xtatiladi, "
                           "host (systemd/Railway/Docker) uni avtomatik qayta ishga tushirishi kerak.")
        os._exit(1)


# ================================================================================
#  /Guruh — faqat yaratuvchi uchun
# ================================================================================

@bot.message_handler(commands=["Guruh", "guruh"])
def cmd_guruh(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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


# ================================================================================
#  🏆 GEROYLAR — /geroyim (ko'rish + darajani oshirish), owner uchun /geroy_ber
# ================================================================================

@bot.message_handler(commands=["geroyim"])
def cmd_geroyim(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    show_hero_panel(message.chat.id, message.from_user.id)


@bot.message_handler(commands=["geroy_bashorat"])
def cmd_geroy_bashorat(message):
    """🔍 Geroy qobiliyati (Seraphine/Zephyrion "Chuqur bashorat") — o'yin davomida
    BIR MARTA, reply qilingan o'yinchining ANIQ rolini shaxsiy xabarda bildiradi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    if not hero_has_ability(uid, "role_reveal_once"):
        bot.send_message(message.chat.id, "❌ Bu qobiliyat sizda yo'q (Seraphine yoki Zephyrion geroyi, tegishli darajada kerak).")
        return
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "🔍 Guruhda, bashorat qilmoqchi bo'lgan o'yinchining xabariga reply qilib yozing.")
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game or game["phase"] not in ("night", "day"):
        bot.send_message(chat_id, "❌ Bu qobiliyat faqat faol o'yin davomida ishlaydi.")
        return
    if uid not in game["players"] or not game["players"][uid]["alive"]:
        return
    if uid in game.setdefault("hero_role_reveal_used", set()):
        safe_send(uid, "❌ Bu qobiliyatingizni shu o'yin davomida allaqachon ishlatib bo'lgansiz.")
        return
    target = message.reply_to_message.from_user
    if target.id not in game["players"]:
        bot.send_message(chat_id, "❌ Bu o'yinchi joriy o'yinda ishtirok etmayapti.")
        return
    game["hero_role_reveal_used"].add(uid)
    target_role = game["players"][target.id]["role"]
    safe_send(uid, f"🔍 Geroyingiz bashorat qildi: <b>{target.first_name}</b>ning aniq roli — <b>{target_role}</b>!\n(Bu qobiliyat endi sarflandi.)")
    announce_item_use(chat_id, uid, "🔍 Geroy bashorati")


def _find_active_game_for(uid):
    """Foydalanuvchi hozir ishtirok etayotgan (tirik) faol o'yinni topadi."""
    for cid, g in GAMES.items():
        if uid in g["players"] and g["players"][uid]["alive"]:
            return cid, g
    return None, None


def do_geroy_koz(uid):
    """👁 Geroy qobiliyati (Seraphine/Zephyrion "Tungi nazar") — qaytaradi: (ok, xabar)."""
    if not hero_has_ability(uid, "night_vision_auto"):
        return False, "❌ Bu qobiliyat sizda yo'q (Seraphine yoki Zephyrion geroyi, tegishli darajada kerak)."
    chat_id, game = _find_active_game_for(uid)
    if not game or game["phase"] != "night":
        return False, "❌ Bu qobiliyat faqat tun davomida ishlaydi."
    active_count = len(game.get("responded_tonight", set()))
    safe_send(uid, f"👁 Geroyingiz sizga pichirlaydi: bu tun hozircha <b>{active_count}</b> ta o'yinchi faol harakat qildi.")
    announce_item_use(chat_id, uid, "👁 Geroy tungi nazari")
    return True, f"👁 Bu tun hozircha {active_count} ta o'yinchi faol harakat qildi."


def do_geroy_daromad(uid):
    """💎 Geroy qobiliyati (Elandriel/Zephyrion "Boylik siri") — qaytaradi: (ok, xabar)."""
    if not hero_has_ability(uid, "diamond_trickle"):
        return False, "❌ Bu qobiliyat sizda yo'q (Elandriel yoki Zephyrion geroyi, tegishli darajada kerak)."
    chat_id, game = _find_active_game_for(uid)
    if not game:
        return False, "❌ Bu qobiliyat faqat faol o'yin davomida ishlaydi."
    if uid in game.setdefault("hero_income_claimed", set()):
        return False, "❌ Bu o'yin uchun bu qobiliyatni allaqachon ishlatib bo'lgansiz."
    game["hero_income_claimed"].add(uid)
    add_balance(uid, diamond=1)
    safe_send(uid, "💎 Geroyingiz sizga +1 Olmos in'om qildi! (Bu o'yin uchun sarflandi.)")
    announce_item_use(chat_id, uid, "💎 Geroy boyligi")
    return True, "💎 +1 Olmos oldingiz!"


@bot.message_handler(commands=["geroy_koz"])
def cmd_geroy_koz(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    ok, msg = do_geroy_koz(message.from_user.id)
    if not ok:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["geroy_daromad"])
def cmd_geroy_daromad(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    ok, msg = do_geroy_daromad(message.from_user.id)
    if not ok:
        bot.send_message(message.chat.id, msg)


def build_hero_panel(uid):
    """Geroy kartochkasi uchun (matn, tugmalar, rasm_yoli) qaytaradi — /geroyim, asosiy
    menyu tugmasi va darajani oshirishdan keyingi yangilanish uchun umumiy funksiya.
    SODDA VA TUSHUNARLI: har bir mahorat holati (✅ ochiq / 🔒 yopiq) aniq ko'rsatiladi,
    qo'lda ishlatiladigan mahoratlar uchun to'g'ridan-to'g'ri tugma beriladi."""
    hero = get_hero(uid)
    if not hero:
        text = (
            "🏆 <b>Sizda hali geroy yo'q</b>\n\n"
            "💎 Olmos do'konidan <b>🏆 Afsonaviy Sandiq</b> (110 💎) sotib oling — "
            "ichidan 5 xil noyob geroydan biri chiqishi mumkin:\n\n"
            + "\n".join(f"• {h['name']}" for h in HEROES.values())
        )
        return text, None, None

    level = hero["level"]
    lines = [
        f"🏆 <b>{hero['name']}</b>",
        f"📅 Faol: <b>{hero['days_active']}</b> kundan beri",
        f"📊 Daraja: <b>{level} / {HERO_MAX_LEVEL}</b>",
        "",
        "✨ <b>Mahoratlar:</b>",
    ]
    kb = types.InlineKeyboardMarkup()
    for ab in hero["abilities"]:
        unlocked = level >= ab["unlock"]
        if unlocked:
            if "base" in ab:
                val = _ability_power(level, ab["unlock"], ab["base"], ab["cap"])
                val_txt = f"{val*100:.0f}%" if val < 1 else f"{int(val)}"
                lines.append(f"✅ <b>{ab['name']}</b> — hozirgi kuchi: {val_txt}")
            else:
                lines.append(f"✅ <b>{ab['name']}</b>")
            lines.append(f"   <i>{ab['desc']}</i>")
        else:
            lines.append(f"🔒 <b>{ab['name']}</b> — {ab['unlock']}-darajada ochiladi")

    lines.append("")
    lines.append("🕹 <b>Qo'lda ishlatish:</b> pastdagi tugmalar yoki mos buyruqlar orqali "
                  "(faqat faol o'yin ichida ishlaydi — geroylar avtomatik ISHLAMAYDI!):")
    if any(a["key"] in ("survive", "revive_once") and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  🛡 Himoya — har TUN, bot avtomatik yuboradigan tugma orqali")
    if any(a["key"] == "vote_shield_once" and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  🗳 Xalq himoyasi — har KUN, bot avtomatik yuboradigan tugma orqali")
    if any(a["key"] == "role_reveal_once" and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  🔍 Bashorat — kimningdir xabariga reply qilib /geroy_bashorat")
    if any(a["key"] == "compass_free" and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  🧭 Kompas — kimningdir xabariga reply qilib /kompas (bepul)")
    if any(a["key"] == "night_vision_auto" and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  👁 Tungi nazar — pastdagi tugma yoki /geroy_koz")
        kb.add(types.InlineKeyboardButton("👁 Tungi nazarni ishlatish", callback_data=f"herouse|koz|{uid}"))
    if any(a["key"] == "diamond_trickle" and level >= a["unlock"] for a in hero["abilities"]):
        lines.append("  💎 Boylik — pastdagi tugma yoki /geroy_daromad (o'yinda 1 marta)")
        kb.add(types.InlineKeyboardButton("💎 Boylikni undirish", callback_data=f"herouse|daromad|{uid}"))

    cost = hero_level_up_cost(level)
    if cost is not None:
        lines.append(f"\n⬆️ Keyingi darajaga: <b>{cost} 💎</b>")
        kb.add(types.InlineKeyboardButton(f"⬆️ Darajani oshirish ({cost} 💎)", callback_data=f"herolvl|{uid}"))
    else:
        lines.append("\n🌟 Geroyingiz ENG YUQORI darajada!")

    return "\n".join(lines), kb, hero_image_path(hero["key"])


def show_hero_panel(chat_id, uid):
    text, kb, image_path = build_hero_panel(uid)
    if image_path:
        try:
            with open(image_path, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=text, reply_markup=kb)
            return
        except Exception:
            pass
    bot.send_message(chat_id, text, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("herouse|"))
def cb_hero_use(call):
    """🕹 Geroyim panelidagi tugmalar orqali qo'lda ishlatiladigan mahoratlar (👁 Tungi
    nazar, 💎 Boylik) — bosilganda darhol ishlaydi va natija shu yerda ko'rsatiladi."""
    maybe_capture_owner(call.from_user)
    _, kind, owner_id_s = call.data.split("|")
    owner_id = int(owner_id_s)
    uid = call.from_user.id
    if uid != owner_id:
        bot.answer_callback_query(call.id, "❌ Bu sizning geroyingiz emas.", show_alert=True)
        return
    if kind == "koz":
        ok, msg = do_geroy_koz(uid)
    elif kind == "daromad":
        ok, msg = do_geroy_daromad(uid)
    else:
        return
    bot.answer_callback_query(call.id, msg, show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith("heroarm|"))
def cb_hero_arm(call):
    """🏆 O'yinchi geroy qobiliyatini (himoya/xalq himoyasi) QO'LDA faollashtiradi.
    Faollashtirilmasa, ushbu tur/kun uchun geroy hech qanday avtomatik ta'sir qilmaydi."""
    maybe_capture_owner(call.from_user)
    _, kind, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    uid = call.from_user.id
    game = GAMES.get(chat_id)
    if not game or uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "❌ Bu tanlov endi amal qilmaydi.", show_alert=True)
        return
    if kind == "defense":
        if game["phase"] != "night":
            bot.answer_callback_query(call.id, "❌ Bu faqat tun davomida faollashtiriladi.", show_alert=True)
            return
        game.setdefault("hero_armed_defense", set()).add(uid)
        bot.answer_callback_query(call.id, "🛡 Geroy himoyasi shu tunga faollashtirildi!", show_alert=True)
        try:
            bot.edit_message_text("🛡✅ Geroy himoyasi shu tunga FAOLLASHTIRILDI.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass
    elif kind == "voteshield":
        if game["phase"] != "day":
            bot.answer_callback_query(call.id, "❌ Bu faqat kunduzi faollashtiriladi.", show_alert=True)
            return
        game.setdefault("hero_armed_vote_shield", set()).add(uid)
        bot.answer_callback_query(call.id, "🗳 Xalq himoyasi shu kunga faollashtirildi!", show_alert=True)
        try:
            bot.edit_message_text("🗳✅ Xalq himoyasi shu kunga FAOLLASHTIRILDI.", call.message.chat.id, call.message.message_id)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("herolvl|"))
def cb_hero_level_up(call):
    maybe_capture_owner(call.from_user)
    _, owner_id_s = call.data.split("|")
    owner_id = int(owner_id_s)
    uid = call.from_user.id
    if uid != owner_id:
        bot.answer_callback_query(call.id, "❌ Bu sizning geroyingiz emas.", show_alert=True)
        return
    hero = get_hero(uid)
    if not hero:
        bot.answer_callback_query(call.id, "❌ Sizda geroy yo'q.", show_alert=True)
        return
    cost = hero_level_up_cost(hero["level"])
    if cost is None:
        bot.answer_callback_query(call.id, "🌟 Geroyingiz allaqachon eng yuqori darajada!", show_alert=True)
        return
    u = user_dict(uid)
    if u["diamond"] < cost:
        bot.answer_callback_query(call.id, f"❌ Yetarli olmos yo'q ({cost} 💎 kerak).", show_alert=True)
        return
    update_user(uid, diamond=u["diamond"] - cost)
    new_level = hero["level"] + 1
    with db_lock:
        cur.execute("UPDATE heroes SET level=? WHERE user_id=?", (new_level, uid))
        conn.commit()
    bot.answer_callback_query(call.id, f"🎉 Geroyingiz {new_level}-darajaga ko'tarildi!", show_alert=True)
    try:
        text, kb, _ = build_hero_panel(uid)
        if call.message.photo:
            bot.edit_message_caption(text, call.message.chat.id, call.message.message_id, reply_markup=kb)
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        pass


@bot.message_handler(commands=["geroy_ber"])
def cmd_geroy_ber(message):
    """👑 Faqat bot egasi — istalgan foydalanuvchiga xohlagan geroyni to'g'ridan-to'g'ri beradi.
    Foydalanish: kimningdir xabariga reply qilib /geroy_ber <hero_key> (masalan: burgut)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if not message.reply_to_message or len(parts) != 2 or parts[1].lower() not in HEROES:
        keys = ", ".join(HEROES.keys())
        bot.send_message(message.chat.id, f"Foydalanish: kimningdir xabariga reply qilib <code>/geroy_ber &lt;kalit&gt;</code>\nMavjud kalitlar: {keys}")
        return
    hero_key = parts[1].lower()
    target = message.reply_to_message.from_user
    user_dict(target.id, target.first_name)
    with db_lock:
        cur.execute("INSERT OR REPLACE INTO heroes (user_id, hero_key, level, acquired_at) VALUES (?, ?, 1, ?)", (target.id, hero_key, time.time()))
        conn.commit()
    hero = HEROES[hero_key]
    bot.send_message(message.chat.id, f"👑 {mention(target.id, target.first_name)}ga <b>{hero['name']}</b> geroyi berildi!")
    safe_send(target.id, f"🏆 Bot egasi sizga <b>{hero['name']}</b> geroyini in'om qildi! /geroyim orqali ko'ring.")


# ================================================================================
#  👑 BOT EGASI (OWNER) UCHUN YANA 5 TA TO'LIQ ISHLAYDIGAN QO'SHIMCHA FUNKSIYA
# ================================================================================

@bot.message_handler(commands=["statistika"])
def cmd_owner_statistika(message):
    """👑 Butun bot bo'yicha umumiy statistika: foydalanuvchilar, o'ynalgan o'yinlar,
    muomaladagi valyutalar va hozir faol o'yinlar soni."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    with db_lock:
        cur.execute("SELECT COUNT(*), COALESCE(SUM(games),0), COALESCE(SUM(wins),0), "
                     "COALESCE(SUM(dollar),0), COALESCE(SUM(diamond),0), COALESCE(SUM(coin),0) FROM users")
        row = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM heroes")
        hero_count = cur.fetchone()[0]
    total_users, total_games, total_wins, total_dollar, total_diamond, total_coin = row
    active_games = len(GAMES)
    text = (
        "📊 <b>BOT BO'YICHA UMUMIY STATISTIKA</b>\n\n"
        f"👥 Ro'yxatdan o'tgan foydalanuvchilar: <b>{total_users}</b>\n"
        f"🎮 Jami o'ynalgan o'yinlar (yig'indi): <b>{total_games // 2 if total_games else 0}</b>\n"
        f"🏆 Jami g'alabalar: <b>{total_wins}</b>\n"
        f"💵 Muomaladagi jami dollar: <b>${total_dollar}</b>\n"
        f"💎 Muomaladagi jami olmos: <b>{total_diamond}</b>\n"
        f"🪙 Muomaladagi jami coin: <b>{total_coin}</b>\n"
        f"🏆 Geroyga ega foydalanuvchilar: <b>{hero_count}</b>\n"
        f"🕹 Hozir faol o'yinlar soni: <b>{active_games}</b>"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["ball_ber"])
def cmd_owner_ball_ber(message):
    """👑 Foydalanuvchiga qo'lda ball qo'shish/ayirish (tuzatish uchun).
    Foydalanish: kimningdir xabariga reply qilib /ball_ber <son> (manfiy ham bo'lishi mumkin)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if not message.reply_to_message or len(parts) != 2:
        bot.send_message(message.chat.id, "Foydalanish: kimningdir xabariga reply qilib <code>/ball_ber &lt;son&gt;</code> (masalan: -10 yoki 25)")
        return
    try:
        amount = int(parts[1])
    except ValueError:
        bot.send_message(message.chat.id, "❌ Son noto'g'ri kiritildi.")
        return
    target = message.reply_to_message.from_user
    user_dict(target.id, target.first_name)
    add_points(target.id, amount, "owner_manual")
    bot.send_message(message.chat.id, f"✅ {mention(target.id, target.first_name)}ga <b>{amount:+d}</b> ball qo'shildi (qo'lda).")
    safe_send(target.id, f"👑 Bot egasi tomonidan sizga <b>{amount:+d}</b> ball berildi.")


@bot.message_handler(commands=["oyinni_zorla_tugat"])
def cmd_owner_force_end(message):
    """👑 Joriy guruhdagi faol o'yinni majburan, favqulodda to'xtatadi (bot osilib
    qolganda yoki o'yin buzilganda ishlatiladigan favqulodda tugma)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    chat_id = message.chat.id
    game = GAMES.get(chat_id)
    if not game:
        bot.send_message(chat_id, "❌ Bu guruhda hozir faol o'yin yo'q.")
        return
    for t in game.get("timers", []):
        try:
            t.cancel()
        except Exception:
            pass
    del GAMES[chat_id]
    save_games_state()
    bot.send_message(chat_id, "🛑 👑 Bot egasi tomonidan o'yin favqulodda to'xtatildi. Hech kimga mukofot/jarima berilmadi.")


@bot.message_handler(commands=["royxat_faol"])
def cmd_owner_active_list(message):
    """👑 Hozir botda faol bo'lgan barcha o'yinlarning ro'yxati (guruh ID, bosqich, kun raqami, o'yinchilar soni)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    if not GAMES:
        bot.send_message(message.chat.id, "📭 Hozir hech qanday faol o'yin yo'q.")
        return
    lines = ["🕹 <b>HOZIR FAOL O'YINLAR</b>\n"]
    for i, (cid, g) in enumerate(GAMES.items(), 1):
        phase_label = {"night": "🌙 Tun", "day": "☀️ Kun", "lobby": "🛋 Lobbi"}.get(g.get("phase"), g.get("phase"))
        lines.append(f"{i}. <code>{cid}</code> — {phase_label}, {g.get('day_number', 0)}-kun, {len(g.get('players', {}))} o'yinchi")
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["valyuta_ber"])
def cmd_owner_currency_grant(message):
    """👑 Foydalanuvchiga qo'lda dollar/olmos/coin berish (yoki ayirish, manfiy son bilan).
    Foydalanish: kimningdir xabariga reply qilib /valyuta_ber <dollar|olmos|coin> <son>."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if not message.reply_to_message or len(parts) != 3 or parts[1].lower() not in ("dollar", "olmos", "coin"):
        bot.send_message(message.chat.id, "Foydalanish: kimningdir xabariga reply qilib <code>/valyuta_ber &lt;dollar|olmos|coin&gt; &lt;son&gt;</code>")
        return
    kind = parts[1].lower()
    try:
        amount = int(parts[2])
    except ValueError:
        bot.send_message(message.chat.id, "❌ Son noto'g'ri kiritildi.")
        return
    target = message.reply_to_message.from_user
    user_dict(target.id, target.first_name)
    kwargs = {"dollar": amount} if kind == "dollar" else ({"diamond": amount} if kind == "olmos" else {"coin": amount})
    add_balance(target.id, **kwargs)
    label = {"dollar": "💵$", "olmos": "💎", "coin": "🪙"}[kind]
    bot.send_message(message.chat.id, f"✅ {mention(target.id, target.first_name)}ga {amount:+d}{label} berildi.")
    safe_send(target.id, f"👑 Bot egasi tomonidan sizga {amount:+d}{label} berildi.")


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
    add(ch.get("compass", 0) > 0, f"🧭 Sirli kompas: {ch.get('compass', 0)} ta")
    add(ch.get("antidote", 0) > 0, f"🩹 Kichik Aptechka (zaharga qarshi): {ch.get('antidote', 0)} ta")
    add(ch.get("hidden_vote", 0) > 0, f"💼 Shubhali sumka (ovozni yashirish): {ch.get('hidden_vote', 0)} ta")
    add(ch.get("revote", 0) > 0, f"⚡️ Energiya ichimligi (qayta ovoz berish): {ch.get('revote', 0)} ta")
    add(ch.get("smoke_bomb", 0) > 0, f"💣 Tutunli bomba: {ch.get('smoke_bomb', 0)} ta")
    add(ch.get("flash_light", 0) > 0, f"🔦 Katta Fonar: {ch.get('flash_light', 0)} ta")
    add(ch.get("cloak", 0) > 0, f"🧥 Yashirin plash: {ch.get('cloak', 0)} ta")
    add(ch.get("duel_adv", 0) > 0, f"⚔️ Olmos Qilich (duel ustunligi): {ch.get('duel_adv', 0)} ta")
    add(ch.get("golden_bullet", 0) > 0, f"🟡 Oltin o'q: {ch.get('golden_bullet', 0)} ta")
    add(ch.get("radar", 0) > 0, f"📡 Maxfiy radar: {ch.get('radar', 0)} ta")
    add(ch.get("revive", 0) > 0, f"⚡️ Tezkor jonlanish: {ch.get('revive', 0)} ta")
    add(ch.get("role_choice", 0) > 0, f"🎭 Rol tanlash huquqi: {ch.get('role_choice', 0)} marta")
    add(ch.get("watch_eyes", 0) > 0, f"👁 Kuzatish ko'zi: {ch.get('watch_eyes', 0)} ta")
    add(ch.get("day_shield", 0) > 0, f"🛡🌞 Kunduzgi himoya: {ch.get('day_shield', 0)} ta")

    imp_until = ch.get("imperator_until", 0)
    if imp_until and imp_until > time.time():
        rem = int(imp_until - time.time())
        add(True, f"👑 Imperator maqomi: {rem // 3600} soat {(rem % 3600) // 60} daqiqa qoldi")

    elite_until_line = ch.get("vip_until", 0)
    if elite_until_line and elite_until_line > time.time():
        rem_days = int((elite_until_line - time.time()) // 86400)
        add(True, f"👑 HUNTER ELITE: {rem_days} kun qoldi")

    admin_until = ch.get("temp_admin_until", 0)
    if admin_until and admin_until > time.time():
        rem = int(admin_until - time.time())
        add(True, f"⚡️ Vaqtinchalik admin huquqi: {rem // 3600} soat qoldi")

    night_vision_left = ch.get("night_vision", 0)  # (yuqorida "🥽 Tungi ko'zoynak" bilan bir xil hisoblanadi)

    hero = get_hero(uid)
    if hero:
        add(True, f"{hero['name']} — {hero['level']}-lvl (/geroyim)")

    def _rem_days(key):
        until = ch.get(key, 0)
        return int((until - time.time()) // 86400) + 1 if until > time.time() else 0

    ramka_days = _rem_days("ramka_until")
    add(ramka_days > 0, f"🖼 Mifik ramka: {ramka_days} kun qoldi")
    toj_days = _rem_days("toj_until")
    add(toj_days > 0, f"👑 Hukmdor toj: {toj_days} kun qoldi")
    qirol_days = _rem_days("qirol_until")
    add(qirol_days > 0, f"🐉 Hunter Mafia Qiroli unvoni: {qirol_days} kun qoldi")
    dgw = ch.get("duel_guaranteed_win", 0)
    if dgw > 0:
        add(True, f"🗡 Kafolatlangan duel g'alabasi — {dgw} marta qoldi")
    shadow_days = _rem_days("shadow_until")
    add(shadow_days > 0, f"👤 Shadow status: {shadow_days} kun qoldi (reytingda yashirin)")
    add(ch.get("klan_license", 0) > 0, f"🏛 Klan litsenziyasi: {ch.get('klan_license', 0)} marta ishlatish mumkin")

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
    partner = get_partner_mention(uid)
    marriage_line = f"💍 Oilaviy holat: Nikohda ({partner})" if partner else "💍 Oilaviy holat: Bo'ydoq"
    duel_total = u["duel_wins"] + u["duel_losses"]
    duel_rate = f"{(u['duel_wins'] / duel_total * 100):.1f}%" if duel_total else "0.0%"
    elite_line = elite_status_line(uid)
    text = (
        "👤 <b>SHAXSIY KABINET</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{elite_line}\n"
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
    """📦 SODDA VA TUSHUNARLI inventar: har bir buyum alohida tugma, bosilganda
    tavsifi va (mavjud bo'lsa) ishlatish/yoqish-o'chirish tugmasi chiqadi."""
    u = user_dict(uid)
    try:
        items = json.loads(u["inventory"] or "[]")
    except Exception:
        items = []
    ch = get_charges(uid)
    voucher_count = len(ch.get("osh_vouchers", []))
    hero = get_hero(uid)

    if not items and voucher_count == 0 and not hero:
        bot.send_message(chat_id, "📦 Sizning inventaringiz hozircha bo'sh.\n🛒 Do'kondan buyum sotib oling — /market")
        return

    counts = {}
    for it in items:
        counts[it] = counts.get(it, 0) + 1

    kb = types.InlineKeyboardMarkup()
    lines = ["📦 <b>SIZNING INVENTARINGIZ</b>", "", "Har bir buyum haqida to'liq ma'lumot va uni ISHLATISH "
             "yoki YOQISH/O'CHIRISH uchun mos tugmani bosing:", ""]

    if hero:
        lines.append(f"🏆 {hero['name']} — {hero['level']}-lvl")
        kb.add(types.InlineKeyboardButton(f"🏆 {hero['name']}", callback_data=f"menu|hero"))

    for name, n in counts.items():
        shopkey = ITEM_NAME_TO_SHOPKEY.get(name)
        label = f"{name} — {n} ta" if n > 1 else name
        lines.append(f"• {name}" + (f" ({n} ta)" if n > 1 else ""))
        if shopkey:
            kb.add(types.InlineKeyboardButton(label, callback_data=f"invitem|{shopkey[0]}|{shopkey[1]}"))
        else:
            kb.add(types.InlineKeyboardButton(label, callback_data="invitem_noop"))

    if voucher_count:
        lines.append(f"• 🥘 Tortiq qilinadigan osh — {voucher_count} ta")
        kb.add(types.InlineKeyboardButton(f"🥘 Osh tortiqlari ({voucher_count} ta)", callback_data="invitem_osh_info"))

    bot.send_message(chat_id, "\n".join(lines), reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "invitem_osh_info")
def cb_invitem_osh_info(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🥘 <b>Osh tortiqlari</b>\n\nBularni sotib olgan bo'lsangiz, pul o'rniga boshqa bir "
        "o'yinchiga TORTIQ qilish huquqiga ega bo'lasiz.\n\n"
        "Ishlatish: guruhda, tortiq qilmoqchi bo'lgan kishining xabariga <b>reply</b> qilib "
        "<code>/oshtortiq</code> deb yozing.",
    )


# charge_key -> (target kerakmi, do_* funksiya, foydalanuvchiga ko'rsatiladigan tugma nomi)
_INV_TARGET_ACTIONS = {
    "poison": ("target", do_zahar, "🧪 Zaharlash uchun tanlang"),
    "gps": ("target", do_gps, "📍 Kimni tekshiramiz?"),
    "compass": ("target", do_kompas, "🧭 Kimni tekshiramiz?"),
    "flash_light": ("target", do_fonar, "🔦 Kimni yoritamiz?"),
    "smoke_bomb": ("self", do_tutun, "💨 Hozir ishlatish"),
    "radar": ("self", do_qayta_tanlash, "📡 Hozir ishlatish"),
}

# 🕹 Buyruq orqali ishlatiladigan buyumlar uchun ANIQ ko'rsatma (inventarda chalkash
# "tegishli buyruq orqali" degan umumiy matn o'rniga)
_INV_COMMAND_HINT = {
    "role_choice": "/rolni_tanla &lt;rol nomi&gt;",
    "klan_license": "/klan &lt;nomi&gt;",
}

# ⚙️ Passiv (o'zi avtomatik ishlaydigan, alohida tugma kerak bo'lmaydigan) buyumlar
# uchun ANIQ tushuntirish matni
_INV_PASSIVE_INFO = {
    "day_shield": "⚙️ Bu buyum AVTOMATIK ishlaydi — kunduzgi ovoz berishda eng ko'p ovoz olib "
                  "qolsangiz, o'zi avtomatik sizni himoya qiladi (alohida buyruq kerak emas).",
    "revote": "⚙️ Bu buyum AVTOMATIK ishlaydi — ovoz berishda fikringizni o'zgartirmoqchi bo'lsangiz, "
              "shunchaki qayta boshqa odamga ovoz bering, zaxira avtomatik ishlatiladi.",
    "cloak": "⚙️ Bu buyum AVTOMATIK ishlaydi — komissar yoki boshqa tekshiruvlar sizni "
             "tekshirganda, natijani avtomatik yashiradi.",
    "duel_guaranteed_win": "⚔️ Bu buyum AVTOMATIK ishlaydi — /duel bilan kimgadir chaqiruv "
                            "yuborganingizda, zaxirangiz bo'lsa g'alaba avtomatik kafolatlanadi.",
}


@bot.callback_query_handler(func=lambda c: c.data == "invitem_noop")
def cb_invitem_noop(call):
    bot.answer_callback_query(call.id, "ℹ️ Bu buyum haqida qo'shimcha ma'lumot yo'q.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("invitem|"))
def cb_invitem_detail(call):
    """Inventardagi buyum tugmasi bosilganda — tavsifi va (mavjud bo'lsa) yoqish/
    o'chirish TUGMASI yoki to'g'ridan-to'g'ri ISHLATISH tugmasi ko'rsatiladi."""
    maybe_capture_owner(call.from_user)
    _, cat, key = call.data.split("|")
    _, items = SHOP_CATEGORIES[cat]
    item = items.get(key)
    uid = call.from_user.id
    if not item:
        bot.answer_callback_query(call.id, "❌ Buyum topilmadi.")
        return
    bot.answer_callback_query(call.id)
    charge_key = item.get("charge_key")
    left = get_charges(uid).get(charge_key, 0) if charge_key else 0
    text = f"<b>{item['name']}</b>\n{item.get('desc', '')}"
    if charge_key and item.get("mode") == "charge":
        text += f"\n\n📦 Qolgan miqdor: {left} ta."
    kb = types.InlineKeyboardMarkup()

    if charge_key in _INV_TARGET_ACTIONS and left > 0:
        kind, _fn, label = _INV_TARGET_ACTIONS[charge_key]
        chat_id, game = find_active_game_for(uid)
        if not game:
            text += "\n\n⚠️ Buyumni ishlatish uchun hozir faol o'yinda tirik ishtirokchi bo'lishingiz kerak."
        elif kind == "self":
            kb.add(types.InlineKeyboardButton(label, callback_data=f"invuse_self|{charge_key}|{chat_id}"))
        else:
            kb.add(types.InlineKeyboardButton(label, callback_data=f"invuse_pick|{charge_key}|{chat_id}"))
    elif charge_key and charge_key in TOGGLABLE_ITEMS and left > 0:
        state = "✅ FAOL" if is_item_active(uid, charge_key) else "⛔ O'CHIQ"
        kb.add(types.InlineKeyboardButton(f"Holat: {state} — bosib almashtiring", callback_data=f"toggleitem|{charge_key}"))
    elif charge_key in _INV_COMMAND_HINT:
        text += f"\n\n🕹 Ishlatish: {_INV_COMMAND_HINT[charge_key]}"
    elif charge_key in _INV_PASSIVE_INFO:
        text += f"\n\n{_INV_PASSIVE_INFO[charge_key]}"
    elif item.get("mode") == "charge" and charge_key:
        text += "\n\nℹ️ Bu buyum avtomatik yoki tegishli buyruq orqali ishlaydi."

    bot.send_message(call.message.chat.id, text, reply_markup=kb if kb.keyboard else None)


@bot.callback_query_handler(func=lambda c: c.data.startswith("invuse_self|"))
def cb_invuse_self(call):
    """Inventardan to'g'ridan-to'g'ri o'ziga ishlatiladigan buyum (Tutun, Radar)."""
    maybe_capture_owner(call.from_user)
    _, charge_key, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    uid = call.from_user.id
    game = GAMES.get(chat_id)
    if not game or uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "❌ Bu o'yin endi faol emas.", show_alert=True)
        return
    _, fn, _ = _INV_TARGET_ACTIONS[charge_key]
    ok, msg = fn(chat_id, game, uid)
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id)
    except Exception:
        bot.send_message(call.message.chat.id, msg)


@bot.callback_query_handler(func=lambda c: c.data.startswith("invuse_pick|"))
def cb_invuse_pick(call):
    """Nishon tanlash kerak bo'lgan buyum (Zahar/GPS/Kompas/Fonar) — tirik
    o'yinchilar ro'yxatini ko'rsatadi."""
    maybe_capture_owner(call.from_user)
    _, charge_key, chat_id_s = call.data.split("|")
    chat_id = int(chat_id_s)
    uid = call.from_user.id
    game = GAMES.get(chat_id)
    if not game or uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "❌ Bu o'yin endi faol emas.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    kb = types.InlineKeyboardMarkup()
    for target_id, p in game["players"].items():
        if target_id == uid:
            continue
        kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"invuse_target|{charge_key}|{chat_id}|{target_id}"))
    try:
        bot.edit_message_text("🎯 Kimga ishlatasiz?", call.message.chat.id, call.message.message_id, reply_markup=kb)
    except Exception:
        bot.send_message(call.message.chat.id, "🎯 Kimga ishlatasiz?", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("invuse_target|"))
def cb_invuse_target(call):
    maybe_capture_owner(call.from_user)
    _, charge_key, chat_id_s, target_s = call.data.split("|")
    chat_id, target_id = int(chat_id_s), int(target_s)
    uid = call.from_user.id
    game = GAMES.get(chat_id)
    if not game or uid not in game["players"] or not game["players"][uid]["alive"]:
        bot.answer_callback_query(call.id, "❌ Bu o'yin endi faol emas.", show_alert=True)
        return
    target_name = game["players"].get(target_id, {}).get("name", "?")
    _, fn, _ = _INV_TARGET_ACTIONS[charge_key]
    ok, msg = fn(chat_id, game, uid, target_id, target_name)
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id)
    except Exception:
        bot.send_message(call.message.chat.id, msg)


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

    elif action == "birja":
        open_diamond_shop_menu(call.message.chat.id, uid)  # 🔧 TUZATILDI: eski Birja/VIP o'rniga — Olmos do'koni
        bot.answer_callback_query(call.id)

    elif action == "elite":
        open_elite_menu(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "lang":
        open_lang_menu(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "dollarshop":
        open_dollar_shop(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "d2c":
        open_diamond_to_coin_menu(call.message.chat.id, uid)
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
        bot.send_message(call.message.chat.id, build_top_text())
        bot.answer_callback_query(call.id)

    elif action == "inventory":
        show_inventory(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "hero":
        show_hero_panel(call.message.chat.id, uid)
        bot.answer_callback_query(call.id)

    elif action == "points_top":
        kb2 = types.InlineKeyboardMarkup()
        kb2.add(
            types.InlineKeyboardButton("📅 Kunlik", callback_data="ptop|kun"),
            types.InlineKeyboardButton("🗓 Haftalik", callback_data="ptop|hafta"),
        )
        kb2.add(
            types.InlineKeyboardButton("📆 Oylik", callback_data="ptop|oy"),
            types.InlineKeyboardButton("♾ Mutlaq", callback_data="ptop|mutlaq"),
        )
        bot.send_message(call.message.chat.id, "🏅 Qaysi davr bo'yicha reytingni ko'rmoqchisiz?", reply_markup=kb2)
        bot.answer_callback_query(call.id)

    elif action == "market_info":
        bot.send_message(
            call.message.chat.id,
            "🛒 <b>QORA BOZOR</b>\n\n"
            "Bu yerda o'yinchilar o'z inventaridagi buyumlarni dollar, olmos yoki "
            "Hunter Coin evaziga — o'zi tanlagan narxda bir-biriga sotishlari mumkin.\n\n"
            "📦 <code>/sell</code> — inventaringizni raqamlangan holda ko'rish\n"
            "📦 <code>/sell &lt;raqam&gt; &lt;dollar|diamond|coin&gt; &lt;narx&gt;</code> — buyumni bozorga qo'yish\n"
            "🛒 <code>/market</code> — faol e'lonlarni ko'rish\n"
            "🛒 <code>/buy &lt;ID&gt;</code> — e'londagi buyumni sotib olish\n\n"
            "<i>Eslatma: qora bozor faqat maxsus savdo guruhida ishlaydi: "
            "https://t.me/+v9bYoMk-0hAyZTcy</i>",
        )
        bot.answer_callback_query(call.id)

    elif action == "tournament":
        t = TOURNAMENTS.get(call.message.chat.id)
        if t and t["status"] != "finished":
            remaining = len(t["participants"]) - len(t["eliminated"])
            bot.send_message(
                call.message.chat.id,
                f"🏆 <b>{t['name']}</b> — holat: {t['status']}\n"
                f"👥 Ishtirokchilar: {len(t['participants'])} (qolgan: {remaining})\n\n"
                "📋 /turnir_royxat — to'liq ro'yxat",
            )
        else:
            bot.send_message(
                call.message.chat.id,
                "🏆 <b>MUSOBAQALAR (Turnirlar)</b>\n\n"
                "👑 FAQAT bot egasi <code>/turnir_boshla &lt;nomi&gt;</code> orqali yangi turnir ochadi.\n"
                "O'yinchilar tugma orqali qo'shiladi, so'ng tashkilotchi ikkitadan tanlab "
                "⚔️ <b>Turnir Jangi</b> (elimination, duel'dan farqli) o'tkazadi — oxirida "
                "bitta CHEMPION qoladi va katta mukofot (+500$, +20💎, +50 ball) oladi!\n\n"
                "📜 Buyruqlar: /turnir_boshla, /turnir_royxat, /turnir_yopish, /turnir_jang, /turnir_tugat",
            )
        bot.answer_callback_query(call.id)

    elif action == "nikoh_info":
        partner = get_partner_mention(uid)
        if partner:
            bot.send_message(call.message.chat.id, f"💍 <b>Oilaviy holat:</b> Nikohda ❤️\nJuftingiz: {partner}\n\nAjrashish uchun /ajrashish deb yozing.")
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
            "/duel (reply) &lt;tikish summasi&gt; — duelga chaqirish (masalan: /duel 250)\n"
            "/duel_stat (yoki reply) — duel statistikasi\n"
            "/nikoh (reply) — turmush taklifi\n"
            "/juftim — oilaviy holatingiz\n"
            "/ajrashish — ajrashish\n"
            "/OilaInfo — nikoh davomiyligi (qancha vaqtdan beri birgasiz)\n"
            "/Quchoqla, /Opich (reply, faqat juftingizga) — erkalash\n"
            "/OilaTop — eng mustahkam oilalar reytingi\n"
            "/Sovgla &lt;atirgul|yurak|shokolad&gt; (reply, faqat juftingizga) — virtual sovg'a\n"
            "/Xiyonat (reply, faqat juftingizga) — hazilomuz \"xiyonat\"\n"
            "/inventar — buyumlaringiz ro'yxati\n"
            "/sell, /sell &lt;raqam&gt; &lt;narx&gt; — 🛒 Qora bozorga buyum qo'yish\n"
            "/osh (reply) &lt;turi&gt; — do'stingizga milliy osh ziyofat qiling (unga himoya+bonus beradi)\n"
            "/market, /buy &lt;ID&gt; — 🛒 Qora bozordan xarid qilish\n"
            "/birja — 💎 Olmos do'koni (Stars orqali sotib olish / HunterCoin↔Olmos)\n"
            "/Givde, /GivdeMoney, /GivdeCoin (reply) — sovg'a berish\n"
            "/klan &lt;nomi&gt;, /klanim — klan yaratish / holatini ko'rish\n"
            "/klanga_qoshil &lt;egasi_ID&gt; — klanga qo'shilish so'rovi yuborish\n"
            "/klan_tark, /klan_chetlash (reply) — klandan chiqish / chiqarish\n"
            "/klan_orinbosar (reply) — o'rinbosar tayinlash\n"
            "/klan_azo_daraja (reply) &lt;son&gt; — a'zo darajasini oshirish/pasaytirish\n"
            "/klan_lvl — klanni yangi darajaga ko'tarish\n"
            "/klan_nomi &lt;yangi nomi&gt; — klan nomini o'zgartirish ($5000)\n"
            "/klan_maqom (reply) ritsar|sehrgar — maqom berish\n"
            "/klan_hazna, /klan_taqsimla (reply) &lt;dollar&gt; — klan xazinasi\n"
            "/klanlar — top klanlar ro'yxati\n"
            "/klanjang &lt;raqib_egasi_ID&gt; — klanlar jangi e'lon qilish\n"
            "/promo &lt;KOD&gt; — promo-kodni ishlatish\n"
            "/profile — shaxsiy kabinet\n"
            "/tark_et — o'yinni tark etish (avtomatik mag'lub, -10 ball)\n\n"
            "<b>🏆 Geroylar va ballar:</b>\n"
            "/geroyim — geroyingizni ko'rish (rasm bilan) va darajasini oshirish\n"
            "/geroy_bashorat, /geroy_koz, /geroy_daromad — geroy mahoratlarini qo'lda ishlatish\n"
            "/balltop_kun, /balltop_hafta, /balltop_oy, /balltop_mutlaq — faollik ballari reytingi\n\n"
            "<b>🏆 Musobaqalar (turnirlar) — FAQAT BOT EGASI boshqaradi:</b>\n"
            "/turnir_boshla &lt;nomi&gt; — yangi turnir ochish (faqat owner)\n"
            "/turnir_royxat — ishtirokchilar ro'yxati\n"
            "/turnir_yopish — ro'yxatni yopib boshlash (faqat owner)\n"
            "/turnir_jang — navbatdagi ⚔️ Turnir Jangini tanlab boshlash (faqat owner)\n"
            "/turnir_tugat — turnirni bekor qilish (faqat owner)\n\n"
            "<b>Faqat bot yaratuvchisi / adminlar:</b>\n"
            "/Guruh, /mirkamilovic, /sendall, /addmoney, /adddiamond, /addcoin, /ban, /unban\n"
            "/promo_create &lt;KOD&gt; &lt;dollar&gt; &lt;diamond&gt; &lt;coin&gt; &lt;limit&gt; — promo-kod yaratish\n"
            "/promo_yarat &lt;KOD&gt; (reply) — eng faol o'yinchi uchun shaxsiy promo-kod (har ishlatilganda unga +$10)\n"
            "/klan_mukofot — 3 oylik TOP klanlar mukofotini tarqatish\n"
            "/tarqatish &lt;dollar|diamond|coin&gt; &lt;miqdor&gt; &lt;kishi&gt; — sovg'a tarqatish (faqat bot yaratuvchisi)\n"
            "/shu_bozor — joriy guruhni qora bozor qilib belgilash\n"
            "/bozor_holati — qora bozor sozlamasini tekshirish\n"
            "/guruh_id — joriy guruh ID'sini ko'rish\n"
            "/jufti &lt;guruh_ID&gt; — 2 guruhni Qizil vs Ko'k musobaqasiga bog'lash\n"
            "/jufti_bekor — juftlikni bekor qilish\n"
            "/hisob — Qizil vs Ko'k umumiy hisobini ko'rish\n"
            "/paralar — nikohdagi juftliklar ro'yxati (admin)\n"
            "/tiklash (yoki /restart) — botni xavfsiz qayta ishga tushirish, aktiv "
            "o'yinlar avtomatik saqlanib tiklanadi (faqat bot yaratuvchisi)\n"
            "/bazani_tikla — bazani avvalgi zaxira nusxa (.json) fayldan tiklash (faqat bot yaratuvchisi)\n"
            "/statistika, /ball_ber, /oyinni_zorla_tugat, /royxat_faol, /valyuta_ber, /geroy_ber — "
            "qo'shimcha owner funksiyalari (⚙️ Admin panelda tugmalar bilan)\n"
            "/guruh_ban (reply), /guruh_unban_hammasi — Telegram guruh darajasidagi ban/unban (guruh admini)\n"
            "/emoji_test — PREMIUM_EMOJI lug'atini sinab ko'rish (faqat bot yaratuvchisi)"
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
        hero_extra = hero_bonus_extra_dollar(uid)  # 🏆 Geroy (Elandriel / Zephyrion)
        if roll < 95:
            reward = int(10 * mult) + hero_extra
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
    elif mode == "gamble_ability":
        # 🎲 Pul emas — tasodifiy ABILITY beriladi (do'kondagi hech bir buyum pul qaytarmaydi)
        if key == "zar":
            options = [("shield", None), ("night_vision", 1)]
        else:  # "quti"
            options = [("gps", 1), ("compass", 1), ("shield", None)]
        picked_key, picked_amount = random.choice(options)
        if picked_key == "shield":
            add_shield(uid, 1)
            result_note = "🛡 Chiqdi: Himoya (+1 shield)!"
        else:
            add_charge(uid, picked_key, picked_amount)
            result_note = f"✨ Chiqdi: {TOGGLABLE_ITEMS.get(picked_key, picked_key)} ({picked_amount} ta)!"
    elif mode == "charge":
        add_charge(uid, item["charge_key"], item.get("charge_amount", 1))
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
    elif mode == "hero_chest":
        existing = get_hero(uid)
        if existing:
            refund = item["price"] // 2
            add_balance(uid, diamond=refund)
            result_note = f"📦 Sizda allaqachon geroy bor ({existing['name']})! Sandiq {refund} 💎 ga aylantirildi."
        else:
            hero_key = roll_hero()
            with db_lock:
                cur.execute("INSERT OR REPLACE INTO heroes (user_id, hero_key, level, acquired_at) VALUES (?, ?, 1, ?)", (uid, hero_key, time.time()))
                conn.commit()
            hero = HEROES[hero_key]
            extra = "\n🎊🎊 NODIR TUSHISH! Siz eng kuchli geroyni qo'lga kiritdingiz! 🎊🎊" if hero_key == "burgut" else ""
            result_note = f"🎉 Sandiqdan chiqdi: <b>{hero['name']}</b> (1-lvl)!{extra}\n{hero['desc']}\n/geroyim orqali ko'ring va rivojlantiring."

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
        parts = payload.split("_")
        kind = parts[0]
    except Exception:
        return

    if kind == "hc":
        _, uid_s, qty_s = parts
        uid, qty = int(uid_s), int(qty_s)
        add_balance(uid, coin=qty)
        bot.send_message(message.chat.id, f"✅ To'lov muvaffaqiyatli o'tdi! +{qty} 🪙 Hunter Coin hisobingizga qo'shildi.\nRahmat!")

    elif kind == "diamondbuy":
        # 💎 Yangi: Olmosni to'g'ridan-to'g'ri Stars orqali sotib olish (7⭐️ = 1💎)
        _, uid_s, qty_s = parts
        uid, qty = int(uid_s), int(qty_s)
        add_balance(uid, diamond=qty)
        bot.send_message(message.chat.id, f"✅ To'lov muvaffaqiyatli o'tdi! +{qty} 💎 Olmos hisobingizga qo'shildi.\nRahmat!")

    elif kind == "elitepay":
        # 👑 HUNTER ELITE — tarifli (1 hafta — 3 oy) obuna, Stars orqali to'langanda shu yerga tushadi
        _, uid_s, days_s = parts
        uid, days = int(uid_s), int(days_s)
        new_until = grant_elite_days(uid, days)
        bot.send_message(
            message.chat.id,
            elite_success_text(days, new_until),
        )


# ================================================================================
#  💎 OLMOS DO'KONI — to'g'ridan-to'g'ri Telegram Stars orqali Olmos sotib olish
#  (🔧 TUZATILDI: eski "Birja / VIP" tizimi olib tashlandi — botda endi HECH
#  QANDAY "VIP" nomli buyum yoki xizmat yo'q, faqat 👑 HUNTER ELITE bor.
#  Narx: 1 💎 Olmos = 7 ⭐️ Stars.)
# ================================================================================

DIAMOND_STARS_RATE = 7  # 1 💎 Olmos narxi = 7 ⭐️ Stars
DIAMOND_PACKAGES = [10, 30, 50, 100, 200]


def open_diamond_shop_menu(chat_id, uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for qty in DIAMOND_PACKAGES:
        price = qty * DIAMOND_STARS_RATE
        kb.add(types.InlineKeyboardButton(f"💎 {qty} Olmos — {price} ⭐️ Stars", callback_data=f"buydiamond|{qty}"))
    kb.add(types.InlineKeyboardButton("🪙 10 Coin ➜ 60-100 💎 Olmos almashtirish", callback_data="exchange_to_diamond"))
    bot.send_message(
        chat_id,
        "💎✨ <b>OLMOS DO'KONI</b> ✨💎\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"⭐️ 1 💎 Olmos narxi: <b>{DIAMOND_STARS_RATE} Stars</b>\n\n"
        "Kerakli miqdorni tanlang yoki Hunter Coin orqali almashtiring:",
        reply_markup=kb,
    )


@bot.message_handler(commands=["almazdokon", "birja"])
def cmd_diamond_shop(message):
    """💎 Olmos do'koni — /birja eski nomi ham ishlaydi (o'rgangan foydalanuvchilar
    uchun qulaylik), lekin endi bu yerda HECH QANDAY "VIP" mavjud emas — faqat
    to'g'ridan-to'g'ri Olmos sotib olish (7⭐️ = 1💎)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    open_diamond_shop_menu(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("buydiamond|"))
def cb_buy_diamond_stars(call):
    try:
        maybe_capture_owner(call.from_user)
        uid = call.from_user.id
        qty = int(call.data.split("|")[1])
        if qty not in DIAMOND_PACKAGES:
            bot.answer_callback_query(call.id, "❌ Noto'g'ri miqdor.", show_alert=True)
            return
        price = qty * DIAMOND_STARS_RATE
        bot.send_invoice(
            call.message.chat.id,
            title=f"💎 {qty} Olmos",
            description=f"{qty} ta Olmos sotib olish ({price} ⭐️ Stars)",
            invoice_payload=f"diamondbuy_{uid}_{qty}",
            provider_token="",  # Telegram Stars uchun bo'sh qoldiriladi
            currency="XTR",
            prices=[types.LabeledPrice(label=f"{qty} Olmos", amount=price)],
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        _logger.warning("cb_buy_diamond_stars xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "❌ To'lov tizimida xatolik. Keyinroq urinib ko'ring.", show_alert=True)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data == "exchange_to_diamond")
def cb_exchange_to_diamond(call):
    try:
        maybe_capture_owner(call.from_user)
        uid = call.from_user.id
        u = user_dict(uid, call.from_user.first_name)
        dynamic_diamond_rate = random.randint(60, 100)

        if u["coin"] < 10:
            bot.answer_callback_query(call.id, "❌ Hisobingizda Hunter Coin yetarli emas! (Kamida 10 🪙 kerak)", show_alert=True)
            return

        add_balance(uid, coin=-10, diamond=dynamic_diamond_rate)
        bot.answer_callback_query(call.id, "✅ Muvaffaqiyatli almashtirildi!", show_alert=True)
        try:
            bot.edit_message_text(
                f"💱 <b>Ayirboshlash bajarildi!</b>\n\n"
                f"➖ 10 🪙 Hunter Coin sarflandi.\n"
                f"➕ Hisobingizga <b>{dynamic_diamond_rate}</b> ta 💎 Olmos qo'shildi!",
                call.message.chat.id, call.message.message_id,
            )
        except Exception:
            pass
    except Exception as e:
        _logger.warning("cb_exchange_to_diamond xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Xatolik yuz berdi.", show_alert=True)
        except Exception:
            pass


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
    kb.add(types.InlineKeyboardButton("🔄 Bazani tiklash (restore)", callback_data="admin|restore"))
    # --- 👑 Yangi qo'shilgan 5 ta owner funksiyasi ---
    kb.add(types.InlineKeyboardButton("📈 To'liq bot statistikasi", callback_data="admin|full_stats"))
    kb.add(types.InlineKeyboardButton("🏅 Ball qo'lda qo'shish/ayirish", callback_data="admin|ball_info"))
    kb.add(types.InlineKeyboardButton("🛑 Joriy guruh o'yinini zudlik bilan to'xtatish", callback_data="admin|force_end_info"))
    kb.add(types.InlineKeyboardButton("🕹 Hozir faol o'yinlar ro'yxati", callback_data="admin|active_list"))
    kb.add(types.InlineKeyboardButton("💎 Valyuta qo'lda berish", callback_data="admin|currency_info"))
    kb.add(types.InlineKeyboardButton("🏆 Geroy qo'lda berish", callback_data="admin|hero_give_info"))
    # --- 👑 Yangi qo'shilgan 3 ta owner funksiyasi (Almex tahlili asosida) ---
    kb.add(types.InlineKeyboardButton("🔍 Foydalanuvchi profilini qidirish", callback_data="admin|user_lookup_info"))
    kb.add(types.InlineKeyboardButton("🚪 Botni guruhdan chiqarish", callback_data="admin|leave_group_info"))
    kb.add(types.InlineKeyboardButton("👑 ELITE qo'lda, muddatli berish", callback_data="admin|elite_give_info"))
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


@bot.callback_query_handler(func=lambda c: c.data == "admin|full_stats")
def cb_admin_full_stats(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    with db_lock:
        cur.execute("SELECT COUNT(*), COALESCE(SUM(games),0), COALESCE(SUM(wins),0), "
                     "COALESCE(SUM(dollar),0), COALESCE(SUM(diamond),0), COALESCE(SUM(coin),0) FROM users")
        row = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM heroes")
        hero_count = cur.fetchone()[0]
    total_users, total_games, total_wins, total_dollar, total_diamond, total_coin = row
    text = (
        "📊 <b>BOT BO'YICHA UMUMIY STATISTIKA</b>\n\n"
        f"👥 Ro'yxatdan o'tgan foydalanuvchilar: <b>{total_users}</b>\n"
        f"🎮 Jami o'ynalgan o'yinlar (yig'indi): <b>{total_games // 2 if total_games else 0}</b>\n"
        f"🏆 Jami g'alabalar: <b>{total_wins}</b>\n"
        f"💵 Muomaladagi jami dollar: <b>${total_dollar}</b>\n"
        f"💎 Muomaladagi jami olmos: <b>{total_diamond}</b>\n"
        f"🪙 Muomaladagi jami coin: <b>{total_coin}</b>\n"
        f"🏆 Geroyga ega foydalanuvchilar: <b>{hero_count}</b>\n"
        f"🕹 Hozir faol o'yinlar soni: <b>{len(GAMES)}</b>"
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda c: c.data == "admin|active_list")
def cb_admin_active_list(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    if not GAMES:
        bot.send_message(call.message.chat.id, "📭 Hozir hech qanday faol o'yin yo'q.")
        return
    lines = ["🕹 <b>HOZIR FAOL O'YINLAR</b>\n"]
    for i, (cid, g) in enumerate(GAMES.items(), 1):
        phase_label = {"night": "🌙 Tun", "day": "☀️ Kun", "lobby": "🛋 Lobbi"}.get(g.get("phase"), g.get("phase"))
        lines.append(f"{i}. <code>{cid}</code> — {phase_label}, {g.get('day_number', 0)}-kun, {len(g.get('players', {}))} o'yinchi")
    bot.send_message(call.message.chat.id, "\n".join(lines))


@bot.callback_query_handler(func=lambda c: c.data == "admin|ball_info")
def cb_admin_ball_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🏅 <b>Ball qo'lda qo'shish/ayirish:</b>\n\n"
        "Kimningdir xabariga reply qilib:\n<code>/ball_ber &lt;son&gt;</code> (masalan: 25 yoki -10)",
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|force_end_info")
def cb_admin_force_end_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🛑 <b>Joriy guruh o'yinini zudlik bilan to'xtatish:</b>\n\n"
        "Bu buyruqni faol o'yin ketayotgan GURUHNING ICHIDA yozing:\n<code>/oyinni_zorla_tugat</code>",
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|currency_info")
def cb_admin_currency_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "💎 <b>Valyuta qo'lda berish:</b>\n\n"
        "Kimningdir xabariga reply qilib:\n<code>/valyuta_ber &lt;dollar|olmos|coin&gt; &lt;son&gt;</code>",
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin|hero_give_info")
def cb_admin_hero_give_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    keys = ", ".join(f"<code>{k}</code> ({v['name']})" for k, v in HEROES.items())
    bot.send_message(
        call.message.chat.id,
        "🏆 <b>Geroy qo'lda berish:</b>\n\n"
        "Kimningdir xabariga reply qilib:\n<code>/geroy_ber &lt;kalit&gt;</code>\n\n"
        f"Mavjud kalitlar:\n{keys}",
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


# ================================================================================
#  🔄 BAZANI TIKLASH (RESTORE) — /bazani_tikla
#  Admin panel: "🔄 Bazani tiklash (restore)" tugmasi → /bazani_tikla buyrug'i →
#  keyingi yuborilgan .json fayl (admin|backup natijasi) o'qilib, ustuniga
#  qarab (INSERT OR REPLACE) joriy bazadagi mos foydalanuvchilar yangilanadi,
#  bazada yo'q foydalanuvchilar esa yangi qator sifatida qo'shiladi.
# ================================================================================

# Bot egasidan .json faylni kutayotgan (shaxsiy chatdagi) userlar to'plami
ADMIN_AWAITING_RESTORE = set()


@bot.callback_query_handler(func=lambda c: c.data == "admin|restore")
def cb_admin_restore_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🔄 <b>Bazani tiklash:</b>\n\n"
        "/bazani_tikla deb yozing, so'ng bot so'ragan joyga avvalgi zaxira nusxa (.json) faylni yuboring.",
    )


@bot.message_handler(commands=["bazani_tikla"])
def cmd_bazani_tikla(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    ADMIN_AWAITING_RESTORE.add(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "📥 Endi zaxira nusxa (.json) faylni shu yerga <b>fayl</b> sifatida yuboring.\n\n"
        "⚠️ <b>Diqqat:</b> bu amal joriy bazadagi mos foydalanuvchilarning ma'lumotini backup "
        "fayldagi qiymatlar bilan almashtiradi (ustma-ust yozadi). Backup faylda yo'q "
        "foydalanuvchilarga tegmaydi.",
    )


@bot.message_handler(content_types=["document"])
def handle_restore_document(message):
    maybe_capture_owner(message.from_user)
    uid = message.from_user.id
    # faqat bot egasidan, faqat /bazani_tikla dan keyin va faqat shaxsiy chatda kutamiz —
    # aks holda bu handler guruhlardagi oddiy fayl yuborishlarga aralashmasligi kerak
    if message.chat.type != "private" or uid not in ADMIN_AWAITING_RESTORE:
        return
    ADMIN_AWAITING_RESTORE.discard(uid)

    doc = message.document
    if not doc or not (doc.file_name or "").lower().endswith(".json"):
        bot.send_message(message.chat.id, "❌ Bu .json fayl emas. Tiklash bekor qilindi — qaytadan /bazani_tikla deb yozing.")
        return

    try:
        file_info = bot.get_file(doc.file_id)
        raw = bot.download_file(file_info.file_path)
        data = json.loads(raw.decode("utf-8"))
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Faylni o'qib bo'lmadi: {e}")
        return

    if not isinstance(data, list):
        bot.send_message(message.chat.id, "❌ Fayl formati noto'g'ri — JSON ro'yxat (list) bo'lishi kerak.")
        return

    restored = 0
    skipped = 0
    placeholders = ",".join(["?"] * len(USER_COLS))
    col_list = ",".join(USER_COLS)

    with db_lock:
        for entry in data:
            if not isinstance(entry, dict) or entry.get("user_id") in (None, ""):
                skipped += 1
                continue
            try:
                row_values = [entry.get(col) for col in USER_COLS]
                row_values[0] = int(entry["user_id"])  # user_id har doim int bo'lishi shart
                cur.execute(f"INSERT OR REPLACE INTO users ({col_list}) VALUES ({placeholders})", row_values)
                restored += 1
            except Exception:
                skipped += 1
        conn.commit()

    bot.send_message(
        message.chat.id,
        "✅ <b>Tiklash yakunlandi!</b>\n"
        f"👥 Tiklangan/yangilangan: {restored} ta\n"
        f"⚠️ O'tkazib yuborilgan (noto'g'ri format): {skipped} ta",
    )


@bot.message_handler(commands=["sendall"])
def cmd_sendall(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/unban &lt;user_id&gt;</code>")
        return
    target_id = int(parts[1])
    unban_user(target_id)
    bot.send_message(message.chat.id, f"✅ Foydalanuvchi <code>{target_id}</code> blokdan chiqarildi.")


# ================================================================================
#  🚫 GURUH-DARAJASIDAGI TELEGRAM BAN/UNBAN TIZIMI
#  ⚠️ MUHIM TEXNIK CHEKLOV: Telegram Bot API'da guruhdagi BARCHA bloklangan
#  foydalanuvchilar ro'yxatini olish (getChatBannedUsers) UMUMAN MAVJUD EMAS —
#  bu Telegram platformasining o'zi qo'ygan cheklov, hech qanday kod bilan
#  aylanib o'tib bo'lmaydi (faqat MTProto-asoslangan userbot — Pyrogram/Telethon —
#  orqali VA faqat administrator huquqi bilan mumkin, oddiy Bot API orqali emas).
#
#  Shuning uchun bu yerda ISHLAYDIGAN, halol yechim taqdim etiladi: bot o'zi
#  /guruh_ban orqali kimnidir bloklasa, uni mahalliy bazaga yozib boradi va
#  keyin /guruh_unban_hammasi ANIQ SHU RO'YXATNI (bot o'zi bloklaganlarni)
#  birma-bir, FloodWait'dan qochish uchun orada kutish bilan, unban qiladi.
# ================================================================================

cur.execute("""
CREATE TABLE IF NOT EXISTS chat_bans (
    chat_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (chat_id, user_id)
)
""")
conn.commit()


def _is_real_group_admin(chat_id, user_id):
    """Foydalanuvchi shu GURUHNING (Telegram darajasida) admini yoki egasi ekanini tekshiradi."""
    if is_owner(user_id):
        return True
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False


@bot.message_handler(commands=["guruh_ban"])
def cmd_guruh_ban(message):
    """🚫 Guruh admini — kimningdir xabariga reply qilib, uni Telegram guruhidan
    bloklaydi (haqiqiy chat ban) VA keyinchalik ommaviy unban qilish uchun ro'yxatga yozadi."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not _is_real_group_admin(message.chat.id, message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat guruh administratori uchun.")
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        bot.send_message(message.chat.id, "🚫 Kimnidir bloklash uchun uning xabariga <b>reply</b> qilib /guruh_ban deb yozing.")
        return
    target = message.reply_to_message.from_user
    try:
        bot.ban_chat_member(message.chat.id, target.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Bloklab bo'lmadi: {e}")
        return
    with db_lock:
        cur.execute("INSERT OR IGNORE INTO chat_bans (chat_id, user_id) VALUES (?, ?)", (message.chat.id, target.id))
        conn.commit()
    bot.send_message(message.chat.id, f"🚫 {target.first_name} guruhdan bloklandi.")


@bot.message_handler(commands=["guruh_unban_hammasi"])
def cmd_guruh_unban_hammasi(message):
    """✅ Guruh admini — ushbu bot ORQALI bloklangan barcha foydalanuvchilarni
    birma-bir, FloodWait'dan saqlanish uchun orada kutish bilan, unban qiladi.
    (Bot orqali emas, boshqa usulda bloklanganlar bu ro'yxatda bo'lmaydi — bu
    Telegram Bot API'ning texnik cheklovi, yuqoridagi izohga qarang.)"""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if message.chat.type not in ("group", "supergroup"):
        return
    if not _is_real_group_admin(message.chat.id, message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat guruh administratori uchun.")
        return

    with db_lock:
        cur.execute("SELECT user_id FROM chat_bans WHERE chat_id=?", (message.chat.id,))
        rows = [r[0] for r in cur.fetchall()]

    if not rows:
        bot.send_message(
            message.chat.id,
            "📭 Ushbu bot orqali bloklangan hech kim topilmadi.\n\n"
            "ℹ️ Eslatma: Telegram Bot API guruhdagi BARCHA bloklanganlar ro'yxatini "
            "berish imkoniyatini umuman taqdim etmaydi — faqat ushbu bot o'zi "
            "/guruh_ban bilan bloklaganlarni kuzatib boradi.",
        )
        return

    status_msg = bot.send_message(message.chat.id, f"⏳ {len(rows)} ta foydalanuvchi unban qilinmoqda...")
    success, failed = 0, 0
    for i, uid in enumerate(rows, 1):
        try:
            bot.unban_chat_member(message.chat.id, uid, only_if_banned=True)
            success += 1
        except Exception:
            failed += 1
        # 🕐 FloodWait'dan saqlanish uchun har bir amaldan keyin qisqa tanaffus
        time.sleep(0.6)
        if i % 15 == 0:
            try:
                bot.edit_message_text(f"⏳ Jarayonda... {i}/{len(rows)}", message.chat.id, status_msg.message_id)
            except Exception:
                pass

    with db_lock:
        cur.execute("DELETE FROM chat_bans WHERE chat_id=?", (message.chat.id,))
        conn.commit()

    try:
        bot.edit_message_text(
            f"✅ <b>Tugallandi!</b>\n\n🟢 Muvaffaqiyatli unban: {success} ta\n🔴 Xatolik: {failed} ta",
            message.chat.id, status_msg.message_id,
        )
    except Exception:
        bot.send_message(message.chat.id, f"✅ Tugallandi! Muvaffaqiyatli: {success}, xatolik: {failed}")


# ================================================================================
#  PROMO-KODLAR (qoshimchakod8.py "Promo-kod Yaratish" g'oyasi asosida)
# ================================================================================

@bot.message_handler(commands=["promo_create"])
def cmd_promo_create(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
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


@bot.message_handler(commands=["promo_yarat"])
def cmd_promo_personal(message):
    """🎁 Eng faol o'yinchilar uchun shaxsiylashtirilgan promo-kod (ism/nik asosida).
    Kimdir shu kodni ishlatsa, kod egasiga +$10 bonus tushadi (referal tizimi)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    if message.chat.type not in ("group", "supergroup") or not message.reply_to_message:
        bot.send_message(message.chat.id, "❌ Promo-kod bermoqchi bo'lgan o'yinchining xabariga reply qilib, kodni yozing.")
        return
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Foydalanish: <code>/promo_yarat KOD</code> (o'yinchining xabariga reply qiling)")
        return
    code = parts[1].upper()
    target = message.reply_to_message.from_user
    user_dict(target.id, target.first_name)
    with db_lock:
        cur.execute(
            "INSERT OR REPLACE INTO promo_codes (code, dollar, diamond, coin, max_uses, used_count, owner_id) "
            "VALUES (?,20,0,0,100000,0,?)",
            (code, target.id),
        )
        conn.commit()
    bot.send_message(
        message.chat.id,
        f"✅ Shaxsiy promo-kod yaratildi: <code>{code}</code> — egasi: {mention(target.id, target.first_name)}\n"
        f"👥 Har bir ishlatilganda: foydalanuvchiga +$20, {target.first_name}ga +$10 bonus.",
    )
    safe_send(target.id, f"🎉 Sizga shaxsiy promo-kod berildi: <code>{code}</code>! Uni do'stlaringizga tarqating — har bir ishlatilishi sizga +$10 olib keladi.")


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
        cur.execute("SELECT dollar, diamond, coin, max_uses, used_count, owner_id FROM promo_codes WHERE code=?", (code,))
        row = cur.fetchone()
        if not row:
            bot.send_message(message.chat.id, "❌ Bunday promo-kod topilmadi.")
            return
        dollar, diamond, coin, max_uses, used_count, owner_id = row
        cur.execute("SELECT 1 FROM promo_redemptions WHERE code=? AND user_id=?", (code, uid))
        if cur.fetchone():
            bot.send_message(message.chat.id, "❌ Siz bu promo-kodni allaqachon ishlatgansiz.")
            return
        if used_count >= max_uses:
            bot.send_message(message.chat.id, "❌ Bu promo-kodning ishlatish limiti tugagan.")
            return
        if owner_id == uid:
            bot.send_message(message.chat.id, "❌ O'zingizning promo-kodingizni ishlata olmaysiz.")
            return
        cur.execute("INSERT INTO promo_redemptions (code, user_id) VALUES (?,?)", (code, uid))
        cur.execute("UPDATE promo_codes SET used_count=used_count+1 WHERE code=?", (code,))
        conn.commit()
    add_balance(uid, dollar=dollar, diamond=diamond, coin=coin)
    extra_note = ""
    if owner_id:
        add_balance(owner_id, dollar=10)
        extra_note = "\n\n🎁 Kod egasiga +$10 referal bonusi yuborildi."
        safe_send(owner_id, f"🎁 Sizning promo-kodingizdan foydalanildi — +$10 bonus tushdi!")
    bot.send_message(
        message.chat.id,
        f"🎁 <b>Promo-kod muvaffaqiyatli ishlatildi!</b>\n💵 +{dollar}$ 💎 +{diamond} 🪙 +{coin}{extra_note}",
    )


# ================================================================================
#  SOVG'A TARQATISH / GIVEAWAY — /tarqatish
#  (qoshimchakod6.py g'oyasi asosida, aiogram'dan telebot'ga moslashtirildi)
# ================================================================================

GIVEAWAYS = {}
GIVEAWAY_CURRENCY_ICON = {"dollar": "💵", "diamond": "💎", "coin": "🪙"}


@bot.message_handler(commands=["tarqatish"])
@bot.channel_post_handler(commands=["tarqatish"])
def cmd_tarqatish(message):
    # Diamond/dollar/coin tarqatish huquqi FAQAT bot yaratuvchisiga tegishli —
    # guruh admini yoki vaqtinchalik admin buyumi bu buyruqqa yetarli emas.
    if is_owner_channel(message.chat):
        pass  # tasdiqlangan owner kanalidan — ruxsat berilgan
    else:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        if not is_owner(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ Bu buyruqni faqat bot yaratuvchisi ishlatishi mumkin.")
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
#  /top — reyting (matn buyrug'i sifatida ham, avval faqat tugma orqali ishlar edi)
# ================================================================================

@bot.message_handler(commands=["top", "reyting"])
@bot.channel_post_handler(commands=["top", "reyting"])
def cmd_top(message):
    if is_owner_channel(message.chat):
        bot.send_message(message.chat.id, build_top_text())
        return
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if is_banned(message.from_user.id):
        return
    bot.send_message(message.chat.id, build_top_text())


@bot.message_handler(commands=["topalmaz"])
@bot.channel_post_handler(commands=["topalmaz"])
def cmd_top_diamond(message):
    if is_owner_channel(message.chat):
        bot.send_message(message.chat.id, build_top_diamond_text())
        return
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if is_banned(message.from_user.id):
        return
    bot.send_message(message.chat.id, build_top_diamond_text())


@bot.message_handler(commands=["topdollar"])
@bot.channel_post_handler(commands=["topdollar"])
def cmd_top_dollar(message):
    if is_owner_channel(message.chat):
        bot.send_message(message.chat.id, build_top_dollar_text())
        return
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if is_banned(message.from_user.id):
        return
    bot.send_message(message.chat.id, build_top_dollar_text())


@bot.message_handler(commands=["topguruh"])
@bot.channel_post_handler(commands=["topguruh"])
def cmd_top_groups(message):
    if is_owner_channel(message.chat):
        bot.send_message(message.chat.id, build_top_groups_text())
        return
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ Bu buyruq faqat bot egasi uchun.")
        return
    bot.send_message(message.chat.id, build_top_groups_text())


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
        uid = message.from_user.id
        if uid not in game["players"]:
            safe_delete(message)
            return
        # 🕵️ MAXFIY MISSIYA KUZATUVI — kunduzgi xabarlar shu yerda hisoblanadi
        track_mission_activity(game, uid, message.text or "")
        return


def track_mission_activity(game, uid, text):
    """Butun o'yin davomidagi guruh xabarlari asosida maxfiy missiyalarni tekshirish
    uchun kerakli statistikani to'playdi (birinchi gapiruvchi, xabarlar soni,
    aniq iboralar, ovoz ochilishidan oldin gapirganlar)."""
    game.setdefault("msg_count_total", {})
    game["msg_count_total"][uid] = game["msg_count_total"].get(uid, 0) + 1
    if game.get("ever_first_speaker") is None:
        game["ever_first_speaker"] = uid
    low = text.lower()
    said = game.setdefault("said_phrases", {}).setdefault(uid, set())
    if "xayrli tun" in low:
        said.add("xayrli_tun")
    if "men tinch aholiman" in low:
        said.add("men_tinch_aholiman")
    if "men ham shunday" in low:
        said.add("men_ham_shunday")
    if not game.get("voting_open"):
        game.setdefault("spoke_before_vote_today", set()).add(uid)


def check_mission_completed(game, uid, mission_key):
    """Har bir missiya turi uchun to'plangan statistika asosida bajarilgan-bajarilmaganini tekshiradi."""
    if mission_key == "first_speaker":
        return game.get("ever_first_speaker") == uid
    if mission_key == "vote_skip":
        return uid in game.get("skip_vote_ever", set())
    if mission_key == "self_vote":
        return uid in game.get("self_vote_ever", set())
    if mission_key == "say_xayrli_tun":
        return "xayrli_tun" in game.get("said_phrases", {}).get(uid, set())
    if mission_key == "talk_atleast_once":
        return game.get("msg_count_total", {}).get(uid, 0) >= 1
    if mission_key == "first_voter":
        return uid in game.get("first_voter_ever", set())
    if mission_key == "last_voter":
        return uid in game.get("last_voter_ever", set())
    if mission_key == "never_say_tinch":
        return "men_tinch_aholiman" not in game.get("said_phrases", {}).get(uid, set())
    if mission_key == "vote_against_mafia_kill":
        return uid in game.get("anti_mafia_vote_ever", set())
    if mission_key == "active_5msg":
        return game.get("msg_count_total", {}).get(uid, 0) >= 5
    if mission_key == "say_men_ham":
        return "men_ham_shunday" in game.get("said_phrases", {}).get(uid, set())
    if mission_key == "silent_until_vote":
        return uid in game.get("silent_before_vote_ever", set())
    if mission_key == "vote_majority":
        return uid in game.get("majority_vote_ever", set())
    if mission_key == "max3_msg":
        return game.get("msg_count_total", {}).get(uid, 0) <= 3
    if mission_key == "survive_night":
        return game["players"].get(uid, {}).get("alive", False)
    return False


# ================================================================================
#  👑 HUNTER ELITE — a'zolik (tarifli), shaxsiy laqab, til sozlamalari,
#     olmos sovg'a qilish tizimi.
#
#  (Almex Black Bot'da ko'rilgan "PRO obuna", "Til tanlash", "Laqab tasdiqlash
#   ovoz berishi" va "Birovga olmos sovg'a qilish" funksiyalaridan ilhomlanib,
#   Hunter Mafia botiga moslab, MAVJUD infratuzilma ustiga — charges JSON'i,
#   add_balance, Telegram Stars invoice tizimi — qurilgan. Yangi DB ustuni
#   TALAB QILINMAYDI: hammasi allaqachon mavjud "charges" ustunida saqlanadi,
#   shuning uchun eski foydalanuvchilarning hech qanday ma'lumoti yo'qolmaydi.
#
#  ESLATMA: botning asosiy interfeysi (menyular, o'yin matnlari) o'zbek tilida
#  qoladi — /til orqali tanlangan til faqat ELITE, laqab va sovg'a bo'limining
#  shaxsiy tasdiqlash xabarlarida ishlatiladi (pastda ochiq yozilgan). Bu — soxta
#  "to'liq tarjima" va'da qilmaslik uchun ataylab shunday cheklangan.)
# ================================================================================

ELITE_PLANS = [
    # {kun: (necha kunlik obuna), diamond: (Olmos narxi), stars: (Telegram Stars narxi)}
    # 🔧 YANGILANDI: 1 hafta = 100⭐/40💎 dan boshlanadi, 3 oygacha (uzoq muddat
    # olganda foizli chegirma bilan) sotib olish mumkin.
    {"days": 7,  "diamond": 40,  "stars": 100},   # 1 hafta
    {"days": 15, "diamond": 70,  "stars": 180},   # 15 kun
    {"days": 30, "diamond": 130, "stars": 320},   # 1 oy
    {"days": 60, "diamond": 230, "stars": 580},   # 2 oy
    {"days": 90, "diamond": 320, "stars": 800},   # 3 oy (eng katta chegirma)
]

LANG_LIST = [
    ("tr", "🇹🇷 Türkçe"),
    ("en", "🇺🇸 English"),
    ("ru", "🇷🇺 Русский"),
    ("uk", "🇺🇦 Українська"),
    ("kk", "🇰🇿 Қазақша"),
    ("uz", "🇺🇿 Oʻzbekcha"),
    ("id", "🇮🇩 Bhasa Indonesia"),
]

LANG_STRINGS = {
    "lang_set": {
        "tr": "✅ Dil başarıyla değiştirildi!",
        "en": "✅ Language changed successfully!",
        "ru": "✅ Язык успешно изменён!",
        "uk": "✅ Мову успішно змінено!",
        "kk": "✅ Тіл сәтті өзгертілді!",
        "uz": "✅ Til muvaffaqiyatli o'zgartirildi!",
        "id": "✅ Bahasa berhasil diubah!",
    },
    "nickname_ok": {
        "tr": "✅ Takma adınız onaylandı ve ayarlandı!",
        "en": "✅ Your nickname has been approved and set!",
        "ru": "✅ Ваш никнейм одобрен и установлен!",
        "uk": "✅ Ваш нікнейм схвалено та встановлено!",
        "kk": "✅ Лақап атыңыз мақұлданды және орнатылды!",
        "uz": "✅ Laqabingiz tasdiqlandi va o'rnatildi!",
        "id": "✅ Nama panggilan Anda telah disetujui dan diatur!",
    },
    "gift_sent": {
        "tr": "🎁 Hediye başarıyla gönderildi!",
        "en": "🎁 Gift sent successfully!",
        "ru": "🎁 Подарок успешно отправлен!",
        "uk": "🎁 Подарунок успішно надіслано!",
        "kk": "🎁 Сыйлық сәтті жіберілді!",
        "uz": "🎁 Sovg'a muvaffaqiyatli yuborildi!",
        "id": "🎁 Hadiah berhasil dikirim!",
    },
}


def T(uid, key):
    """Foydalanuvchi tanlagan tilda (agar shu kalit uchun tarjima bo'lsa) matn qaytaradi,
    aks holda standart o'zbekcha variantga qaytadi (hech qachon xato bermaydi)."""
    lang = get_lang(uid)
    table = LANG_STRINGS.get(key, {})
    return table.get(lang) or table.get("uz") or ""


def get_lang(uid):
    ch = get_charges(uid)
    return ch.get("lang", "uz")


def set_lang(uid, code):
    set_charge_value(uid, "lang", code)


def get_nickname(uid):
    ch = get_charges(uid)
    return (ch.get("nickname") or "").strip()


def set_nickname(uid, nickname):
    set_charge_value(uid, "nickname", nickname.strip()[:32])


def is_elite(uid):
    ch = get_charges(uid)
    until = ch.get("vip_until", 0)
    return bool(until) and until > time.time()


def elite_days_left(uid):
    ch = get_charges(uid)
    until = ch.get("vip_until", 0)
    if not until or until <= time.time():
        return 0
    return max(0, int((until - time.time()) // 86400) + 1)


def grant_elite_days(uid, days):
    """Yangi ELITE kunlarni qo'shadi — agar hozir ham faol ELITE bo'lsa, qolgan
    muddat ustiga QO'SHILADI (ya'ni 15 kun qolganida yana 30 kun sotib olsa, 45 kun bo'ladi),
    aks holda hozirdan boshlab hisoblanadi. Yangi umumiy tugash vaqtini (unix) qaytaradi."""
    ch = get_charges(uid)
    current_until = ch.get("vip_until", 0)
    base = current_until if current_until and current_until > time.time() else time.time()
    new_until = base + days * 86400
    set_charge_value(uid, "vip_until", new_until)
    return new_until


def elite_status_line(uid):
    if is_elite(uid):
        nick = get_nickname(uid)
        nick_part = f" | 🏷 Laqab: {nick}" if nick else ""
        return f"𝓔𝓵𝓲𝓽𝓮 👑 <b>HUNTER ELITE faol</b> — {elite_days_left(uid)} kun qoldi{nick_part}"
    return "👑 HUNTER ELITE: faol emas — /elite orqali oling"


ELITE_STYLED_WORD = "𝓔𝓵𝓲𝓽𝓮"  # 🔧 YANGI: maxsus (kursiv-kalligrafik) shriftdagi "Elite" so'zi, emojidan OLDIN yoziladi


def elite_success_text(days, until):
    return (
        f"🎉 {ELITE_STYLED_WORD} 👑 <b>TABRIKLAYMIZ! HUNTER ELITE FAOLLASHTIRILDI!</b> 👑 {ELITE_STYLED_WORD} 🎉\n\n"
        f"⏳ Qo'shilgan muddat: <b>{_elite_days_label(days)}</b>\n"
        f"📅 Amal qilish muddati: <b>{time.strftime('%d.%m.%Y', time.localtime(until))}</b> gacha\n\n"
        "✨ Endi sizga ochiq:\n"
        f"• {ELITE_STYLED_WORD} 👑 Ismingiz yonida oltin ELITE nishoni\n"
        "• 🏷 Shaxsiy laqab (/taxallus)\n"
        "• 🚪 O'yin lobbysidan istalgan payt chiqish huquqi\n"
        "• 💎 Kunlik ELITE Sirli Sandiq (/elite_sandiq)\n"
        "• 👁 Kengaytirilgan profil va reytingdagi maxsus ko'rinish\n\n"
        "Rahmat! 💎"
    )


def _elite_days_label(d):
    """Kunlar sonini o'qish oson formatga o'giradi: 7->'1 hafta', 30->'1 oy' va h.k."""
    if d == 7:
        return "1 hafta"
    if d % 30 == 0:
        months = d // 30
        return f"{months} oy" if months > 1 else "1 oy"
    return f"{d} kun"


def open_elite_menu(chat_id, uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for plan in ELITE_PLANS:
        d = plan["days"]
        label = _elite_days_label(d)
        kb.add(types.InlineKeyboardButton(
            f"⭐️ {label} — {plan['stars']} Stars",
            callback_data=f"elitebuy|{d}|stars",
        ))
        kb.add(types.InlineKeyboardButton(
            f"💎 {label} — {plan['diamond']} Olmos",
            callback_data=f"elitebuy|{d}|diamond",
        ))
    status = elite_status_line(uid)
    bot.send_message(
        chat_id,
        "𝓔𝓵𝓲𝓽𝓮 👑✨ <b>HUNTER ELITE A'ZOLIGI</b> ✨👑\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{status}\n\n"
        "👑 ELITE sizga quyidagilarni beradi:\n"
        "• ⭐️ Ism yonida oltin ELITE nishoni\n"
        "• 🏷 Shaxsiy laqab o'rnatish — /taxallus <laqab>\n"
        "• 🚪 Lobbydan istalgan payt chiqish — /chiqish\n"
        "• 🎁 Olmos sovg'a qilish imkoniyati — /sovga\n"
        "• 💎 Kunlik ELITE Sirli Sandiq — /elite_sandiq\n"
        "• 👑 Reyting va profilda maxsus (oltin) ko'rinish\n\n"
        "💳 <b>1 haftalikdan 3 oygacha</b> — o'zingizga qulay muddatni tanlang.\n"
        "Uzoqroq muddat olsangiz — <b>foizli chegirma</b> avtomatik qo'llanadi!\n"
        "⭐️ Telegram Stars orqali (100⭐️dan) yoki 💎 Olmos orqali (40💎dan) to'lang:",
        reply_markup=kb,
    )


@bot.message_handler(commands=["elite"])
def cmd_elite(message):
    """👑 HUNTER ELITE menyusini ochadi. To'liq try/except bilan himoyalangan —
    hech qanday holatda bot "javobsiz qolib" ketmaydi."""
    try:
        maybe_capture_owner(message.from_user)
        safe_delete(message)
        open_elite_menu(message.chat.id, message.from_user.id)
    except Exception as e:
        _logger.warning("cmd_elite xatolik: %s", e)
        try:
            bot.send_message(message.chat.id, "⚠️ ELITE menyusini ochishda xatolik yuz berdi. Qaytadan urinib ko'ring: /elite")
        except Exception:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("elitebuy|"))
def cb_elite_buy(call):
    """👑 HUNTER ELITE sotib olish. 🔧 TUZATILDI: avval bu funksiyada umumiy
    try/except YO'Q edi — agar biror joyda kutilmagan xatolik chiqsa (masalan
    DB bilan bog'liq), Telegram tugmani "bosilgan" deb belgilamas edi va
    foydalanuvchiga HECH QANDAY javob ko'rinmas edi (xuddi bot "javob
    bermayapti"gandek tuyulardi). Endi har qanday holatda ham foydalanuvchiga
    aniq javob (muvaffaqiyat yoki xatolik xabari) ko'rsatiladi."""
    try:
        maybe_capture_owner(call.from_user)
        uid = call.from_user.id
        parts = call.data.split("|")
        if len(parts) != 3:
            bot.answer_callback_query(call.id, "⚠️ Noto'g'ri so'rov, qaytadan /elite deb urinib ko'ring.", show_alert=True)
            return
        _, days_s, currency = parts
        try:
            days = int(days_s)
        except ValueError:
            bot.answer_callback_query(call.id, "⚠️ Noto'g'ri tarif.", show_alert=True)
            return

        plan = next((p for p in ELITE_PLANS if p["days"] == days), None)
        if not plan:
            bot.answer_callback_query(call.id, "❌ Bu tarif topilmadi. Yangi menyu uchun /elite deb yozing.", show_alert=True)
            return

        if currency == "diamond":
            price = plan["diamond"]
            u = user_dict(uid, call.from_user.first_name)
            if u["diamond"] < price:
                bot.answer_callback_query(
                    call.id,
                    f"❌ Olmosingiz yetarli emas! Kerak: {price} 💎, sizda: {u['diamond']} 💎.\n"
                    f"💎 Olmos sotib olish uchun: /almazdokon",
                    show_alert=True,
                )
                return
            add_balance(uid, diamond=-price)
            new_until = grant_elite_days(uid, days)
            bot.answer_callback_query(call.id, "✅ HUNTER ELITE faollashtirildi!", show_alert=True)
            bot.send_message(call.message.chat.id, elite_success_text(days, new_until))

        elif currency == "stars":
            price = plan["stars"]
            try:
                bot.send_invoice(
                    call.message.chat.id,
                    title=f"👑 HUNTER ELITE ({_elite_days_label(days)})",
                    description=f"{_elite_days_label(days)} HUNTER ELITE obunasi ({price} ⭐️ Stars)",
                    invoice_payload=f"elitepay_{uid}_{days}",
                    provider_token="",   # Telegram Stars uchun bo'sh qoldiriladi
                    currency="XTR",
                    prices=[types.LabeledPrice(label=f"HUNTER ELITE ({_elite_days_label(days)})", amount=price)],
                )
                bot.answer_callback_query(call.id)
            except Exception as inv_err:
                _logger.warning("send_invoice xatolik (elite/stars): %s", inv_err)
                bot.answer_callback_query(
                    call.id,
                    "❌ To'lov tizimida xatolik. Bu ko'pincha botda Telegram Stars to'lovlari "
                    "yoqilmagan bo'lsa yuz beradi — bot egasi @BotFather'da to'lovlarni tekshirsin.",
                    show_alert=True,
                )
        else:
            bot.answer_callback_query(call.id, "❌ Noma'lum to'lov turi. Qaytadan /elite deb urinib ko'ring.", show_alert=True)
    except Exception as e:
        _logger.warning("cb_elite_buy xatolik: %s", e)
        try:
            bot.answer_callback_query(call.id, "⚠️ Kutilmagan xatolik yuz berdi. Qaytadan /elite deb urinib ko'ring.", show_alert=True)
        except Exception:
            pass


# --------------------------------------------------------------------------------
#  🌐 TIL / LANGUAGE
# --------------------------------------------------------------------------------

def open_lang_menu(chat_id, uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for code, label in LANG_LIST:
        mark = " ✅" if get_lang(uid) == code else ""
        kb.add(types.InlineKeyboardButton(f"{label}{mark}", callback_data=f"setlang|{code}"))
    bot.send_message(
        chat_id,
        "🌐 <b>Til / Language sozlamalari</b>\n\n"
        "Tanlangan til shaxsiy ELITE, laqab va sovg'a xabarlaringizda ishlatiladi.\n"
        "Botning asosiy o'yin matnlari hozircha o'zbek tilida qoladi.\n\n"
        "Kerakli tilni tanlang:",
        reply_markup=kb,
    )


@bot.message_handler(commands=["til", "lang"])
def cmd_til(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    open_lang_menu(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("setlang|"))
def cb_set_lang(call):
    maybe_capture_owner(call.from_user)
    uid = call.from_user.id
    code = call.data.split("|")[1]
    if code not in dict(LANG_LIST):
        bot.answer_callback_query(call.id, "❌ Noma'lum til.", show_alert=True)
        return
    set_lang(uid, code)
    bot.answer_callback_query(call.id, T(uid, "lang_set"), show_alert=True)
    try:
        bot.edit_message_text(
            f"{T(uid, 'lang_set')}\n\n" + dict(LANG_LIST)[code],
            call.message.chat.id, call.message.message_id,
        )
    except Exception:
        pass


# --------------------------------------------------------------------------------
#  🏷 SHAXSIY LAQAB (taxallus) — faqat HUNTER ELITE a'zolari uchun.
#     Guruhda chaqirilsa — Almex Black Bot'dagidek 👍/👎 tasdiqlash ovoz berishi
#     ochiladi (30 soniya, ko'pchilik "yoqlab" ovoz bersa tasdiqlanadi).
#     Shaxsiy (DM) chatda chaqirilsa — auditoriya yo'qligi uchun darhol o'rnatiladi.
# --------------------------------------------------------------------------------

PENDING_NICKNAMES = {}   # vote_id -> {"uid":, "nickname":, "yes": set(), "no": set(), "chat_id":, "message_id":}
_NICK_VOTE_SECONDS = 30
_nick_vote_counter = [0]


def _resolve_nickname_vote(vote_id):
    data = PENDING_NICKNAMES.pop(vote_id, None)
    if not data:
        return
    yes, no = len(data["yes"]), len(data["no"])
    approved = yes >= no  # teng bo'lsa ham — laqab zararsiz bo'lgani uchun tasdiqlanadi
    try:
        if approved:
            set_nickname(data["uid"], data["nickname"])
            result_text = (
                f"✅ <b>Laqab tasdiqlandi!</b>\n"
                f"👤 Yangi laqab: <b>{data['nickname']}</b>\n"
                f"📊 Ovozlar: {yes} 👍 | {no} 👎"
            )
        else:
            result_text = (
                f"❌ <b>Laqab rad etildi.</b>\n"
                f"📊 Ovozlar: {yes} 👍 | {no} 👎"
            )
        bot.edit_message_text(result_text, data["chat_id"], data["message_id"])
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("nickvote|"))
def cb_nickname_vote(call):
    maybe_capture_owner(call.from_user)
    _, vote_id_s, choice = call.data.split("|")
    vote_id = int(vote_id_s)
    data = PENDING_NICKNAMES.get(vote_id)
    if not data:
        bot.answer_callback_query(call.id, "⏱ Bu ovoz berish tugagan.", show_alert=True)
        return
    voter = call.from_user.id
    data["yes"].discard(voter)
    data["no"].discard(voter)
    if choice == "yes":
        data["yes"].add(voter)
    else:
        data["no"].add(voter)
    bot.answer_callback_query(call.id, "✅ Ovozingiz qabul qilindi!")
    try:
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton(f"👍 {len(data['yes'])}", callback_data=f"nickvote|{vote_id}|yes"),
            types.InlineKeyboardButton(f"👎 {len(data['no'])}", callback_data=f"nickvote|{vote_id}|no"),
        )
        bot.edit_message_reply_markup(data["chat_id"], data["message_id"], reply_markup=kb)
    except Exception:
        pass


@bot.message_handler(commands=["taxallus", "nickname"])
def cmd_taxallus(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id

    if not is_elite(uid):
        bot.send_message(
            message.chat.id,
            "❌ Bu funksiya faqat 👑 <b>HUNTER ELITE</b> a'zolari uchun!\n"
            "/elite orqali ELITE a'zolikni oling.",
        )
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        bot.send_message(message.chat.id, "✏️ Foydalanish: <code>/taxallus Yangi_Laqabim</code>")
        return

    nickname = parts[1].strip()[:32]

    if message.chat.type == "private":
        set_nickname(uid, nickname)
        bot.send_message(message.chat.id, T(uid, "nickname_ok") + f"\n👤 {nickname}")
        return

    # Guruhda — jamoaviy tasdiqlash ovoz berishi
    _nick_vote_counter[0] += 1
    vote_id = _nick_vote_counter[0]
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("👍 0", callback_data=f"nickvote|{vote_id}|yes"),
        types.InlineKeyboardButton("👎 0", callback_data=f"nickvote|{vote_id}|no"),
    )
    sent = bot.send_message(
        message.chat.id,
        f"❓ Rostdan ham {mention(uid, message.from_user.first_name)} uchun\n"
        f"👤 yangi laqab: <b>{nickname}</b> — o'rnatilishini xohlaysizmi?\n\n"
        f"⏰ Tasdiqlash uchun vaqt: {_NICK_VOTE_SECONDS} soniya",
        reply_markup=kb,
    )
    PENDING_NICKNAMES[vote_id] = {
        "uid": uid, "nickname": nickname, "yes": set(), "no": set(),
        "chat_id": message.chat.id, "message_id": sent.message_id,
    }
    t = threading.Timer(_NICK_VOTE_SECONDS, lambda: _resolve_nickname_vote(vote_id))
    t.daemon = True
    t.start()


# --------------------------------------------------------------------------------
#  🎁 OLMOS SOVG'A QILISH — /sovga
#     Ishlatish: kimningdir xabariga REPLY qilib  /sovga <miqdor>
#            yoki reply'siz:                       /sovga <user_id> <miqdor>
# --------------------------------------------------------------------------------

def user_exists(uid):
    with db_lock:
        cur.execute("SELECT 1 FROM users WHERE user_id=?", (uid,))
        return cur.fetchone() is not None


@bot.message_handler(commands=["sovga", "gift"])
def cmd_sovga(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    sender_id = message.from_user.id
    parts = message.text.split()

    target_id = None
    target_name = None

    if message.reply_to_message and len(parts) == 2:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        amount_s = parts[1]
    elif len(parts) == 3:
        if not parts[1].lstrip("-").isdigit():
            bot.send_message(message.chat.id, "❌ Foydalanuvchi ID raqam bo'lishi kerak.")
            return
        target_id = int(parts[1])
        amount_s = parts[2]
    else:
        bot.send_message(
            message.chat.id,
            "🎁 <b>Olmos sovg'a qilish</b>\n\n"
            "Foydalanish:\n"
            "• Kimningdir xabariga REPLY qilib: <code>/sovga &lt;miqdor&gt;</code>\n"
            "• Yoki to'g'ridan-to'g'ri: <code>/sovga &lt;Telegram_ID&gt; &lt;miqdor&gt;</code>\n\n"
            "❗️ Qabul qiluvchi avval botga kamida bir marta <code>/start</code> bosgan bo'lishi kerak.",
        )
        return

    if target_id == sender_id:
        bot.send_message(message.chat.id, "❌ O'zingizga sovg'a qila olmaysiz 🙂")
        return

    try:
        amount = int(amount_s)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Miqdor butun son bo'lishi kerak.")
        return
    if amount <= 0:
        bot.send_message(message.chat.id, "❌ Miqdor musbat bo'lishi kerak.")
        return

    if target_name:
        user_dict(target_id, target_name)  # reply orqali kelgan — mavjud emas bo'lsa ro'yxatdan o'tkazamiz
    elif not user_exists(target_id):
        bot.send_message(message.chat.id, "❌ Bu foydalanuvchi hali botdan foydalanmagan (avval botga /start bosishi kerak).")
        return

    sender = user_dict(sender_id, message.from_user.first_name)
    if sender["diamond"] < amount:
        bot.send_message(message.chat.id, f"❌ Olmosingiz yetarli emas! Sizda: {sender['diamond']} 💎")
        return

    add_balance(sender_id, diamond=-amount)
    add_balance(target_id, diamond=amount)

    target_row = user_dict(target_id)
    bot.send_message(
        message.chat.id,
        T(sender_id, "gift_sent") + f"\n{mention(sender_id, message.from_user.first_name)} ➜ "
        f"{mention(target_id, target_row['name'])}: <b>{amount} 💎</b>",
    )
    safe_send(target_id, f"🎁 Sizga {mention(sender_id, message.from_user.first_name)} tomonidan <b>{amount} 💎</b> Olmos sovg'a qilindi!")


# --------------------------------------------------------------------------------
#  🚪 /chiqish — HUNTER ELITE a'zolari uchun lobbydan istalgan payt chiqish huquqi
#     (Almex Black Bot'dagi PRO-only /leave bilan bir xil mantiq)
# --------------------------------------------------------------------------------

@bot.message_handler(commands=["chiqish"])
def cmd_chiqish(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    uid = message.from_user.id
    chat_id = message.chat.id
    game = GAMES.get(chat_id)

    if not game or game["phase"] != "waiting" or uid not in game["players"]:
        bot.send_message(chat_id, "❌ Siz hozir chiqib bo'ladigan faol lobbyda emassiz.")
        return

    if not is_elite(uid):
        bot.send_message(
            chat_id,
            "❌ Lobbydan chiqish faqat 👑 <b>HUNTER ELITE</b> a'zolari uchun!\n"
            "/elite orqali ELITE a'zolikni oling.",
        )
        return

    del game["players"][uid]
    if game.get("join_msg_id"):
        try:
            bot.edit_message_text(build_join_text(game), chat_id, game["join_msg_id"], reply_markup=build_join_markup(chat_id, game))
        except Exception:
            pass
    bot.send_message(chat_id, f"🚪 {mention(uid, message.from_user.first_name)} lobbydan chiqdi (👑 ELITE huquqi).")


# --------------------------------------------------------------------------------
#  💵 DOLLAR DO'KONI — Olmosga o'yin-ichi Dollar sotib olish
#     (Almex Black Bot'dagi "Dollar sotib olish uchun variantni tanlang" bilan
#      bir xil paket tuzilishi, sizning Olmos/Dollar balansingizga moslashtirilgan)
# --------------------------------------------------------------------------------

DOLLAR_PACKAGES = [
    {"dollar": 300,   "diamond": 1},
    {"dollar": 600,   "diamond": 2},
    {"dollar": 800,   "diamond": 3},
    {"dollar": 1500,  "diamond": 4},
    {"dollar": 5000,  "diamond": 15},
    {"dollar": 10000, "diamond": 30},
]


def open_dollar_shop(chat_id, uid):
    kb = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(f"{p['dollar']}💵 — {p['diamond']}💎", callback_data=f"buydollar|{p['diamond']}")
        for p in DOLLAR_PACKAGES
    ]
    for i in range(0, len(buttons), 2):
        kb.add(*buttons[i:i + 2])
    u = user_dict(uid)
    bot.send_message(
        chat_id,
        "💵 <b>DOLLAR DO'KONI</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💎 Sizda: {u['diamond']} Olmos\n\n"
        "Olmosga o'yin-ichi Dollar sotib olish uchun paketni tanlang:",
        reply_markup=kb,
    )


@bot.message_handler(commands=["dollar_dokon"])
def cmd_dollar_dokon(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    open_dollar_shop(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("buydollar|"))
def cb_buy_dollar(call):
    maybe_capture_owner(call.from_user)
    uid = call.from_user.id
    diamond_cost = int(call.data.split("|")[1])
    pkg = next((p for p in DOLLAR_PACKAGES if p["diamond"] == diamond_cost), None)
    if not pkg:
        bot.answer_callback_query(call.id, "❌ Bu paket topilmadi.", show_alert=True)
        return
    u = user_dict(uid, call.from_user.first_name)
    if u["diamond"] < diamond_cost:
        bot.answer_callback_query(
            call.id, f"❌ Olmosingiz yetarli emas! Kerak: {diamond_cost} 💎, sizda: {u['diamond']} 💎.",
            show_alert=True,
        )
        return
    add_balance(uid, diamond=-diamond_cost, dollar=pkg["dollar"])
    bot.answer_callback_query(call.id, "✅ Xarid muvaffaqiyatli!", show_alert=True)
    try:
        bot.edit_message_text(
            f"💱 <b>Xarid bajarildi!</b>\n\n"
            f"➖ {diamond_cost} 💎 Olmos sarflandi.\n"
            f"➕ Hisobingizga <b>{pkg['dollar']}</b> 💵 Dollar qo'shildi!",
            call.message.chat.id, call.message.message_id,
        )
    except Exception:
        pass


# --------------------------------------------------------------------------------
#  💎↔🪙 OLMOS ↔ ALMEX-COIN QAT'IY KURSDA AYIRBOSHLASH (2 💎 = 1 🪙)
#     (Almex Black Bot'dagi "Olmos → Almex Coin, Kurs: 2💎 = 1" bilan bir xil —
#      sizning botingizdagi mavjud "coin→diamond, tasodifiy kurs" ayirboshlashdan
#      FARQLI — bu ANIQ, DOIMIY 2:1 kursda, TESKARI yo'nalishda ishlaydi)
# --------------------------------------------------------------------------------

DIAMOND_TO_COIN_RATE = 2  # 2 💎 = 1 🪙
DIAMOND_TO_COIN_PRESETS = [10, 20, 50, 100, 200, 500]


def open_diamond_to_coin_menu(chat_id, uid):
    u = user_dict(uid)
    kb = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for d in DIAMOND_TO_COIN_PRESETS:
        c = d // DIAMOND_TO_COIN_RATE
        buttons.append(types.InlineKeyboardButton(f"{d}💎 → {c}🪙", callback_data=f"d2c|{d}"))
    for i in range(0, len(buttons), 2):
        kb.add(*buttons[i:i + 2])
    bot.send_message(
        chat_id,
        "💎➜🪙 <b>Olmos → Hunter Coin ayirboshlash</b>\n\n"
        f"💎 Sizda: {u['diamond']} Olmos\n"
        f"📌 Qat'iy kurs: <b>{DIAMOND_TO_COIN_RATE} 💎 = 1 🪙</b>\n\n"
        "Qancha ayirboshlashni tanlang:",
        reply_markup=kb,
    )


@bot.message_handler(commands=["olmos_coin"])
def cmd_olmos_coin(message):
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    open_diamond_to_coin_menu(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("d2c|"))
def cb_diamond_to_coin(call):
    maybe_capture_owner(call.from_user)
    uid = call.from_user.id
    diamond_amount = int(call.data.split("|")[1])
    coin_amount = diamond_amount // DIAMOND_TO_COIN_RATE
    u = user_dict(uid, call.from_user.first_name)
    if u["diamond"] < diamond_amount:
        bot.answer_callback_query(
            call.id, f"❌ Olmosingiz yetarli emas! Kerak: {diamond_amount} 💎, sizda: {u['diamond']} 💎.",
            show_alert=True,
        )
        return
    add_balance(uid, diamond=-diamond_amount, coin=coin_amount)
    bot.answer_callback_query(call.id, "✅ Ayirboshlash muvaffaqiyatli!", show_alert=True)
    try:
        bot.edit_message_text(
            f"💱 <b>Ayirboshlash bajarildi!</b>\n\n"
            f"➖ {diamond_amount} 💎 Olmos sarflandi.\n"
            f"➕ Hisobingizga <b>{coin_amount}</b> 🪙 Hunter Coin qo'shildi!",
            call.message.chat.id, call.message.message_id,
        )
    except Exception:
        pass


# ================================================================================
#  👑 BOT EGASI (OWNER) UCHUN YANA 3 TA YANGI, TO'LIQ ISHLAYDIGAN FUNKSIYA
#  (Almex Black Bot skrinshotlari tahlili asosida so'ralgan qo'shimcha)
#
#   1) /useri <user_id yoki reply> — istalgan foydalanuvchining TO'LIQ profilini
#      (balans, statistika, ELITE holati, oila, geroy, ban holati) ko'rish.
#   2) /guruhdan_chiq <chat_id> — botni istalgan guruhdan majburan chiqarish
#      (haqiqiy Telegram API leave_chat chaqiruvi) + known_groups'dan o'chirish.
#   3) /elite_ber <kun> (reply) — istalgan foydalanuvchiga qo'lda, muddatli
#      HUNTER ELITE (VIP) berish — mavjud grant_elite_days() ustiga qurilgan,
#      shuning uchun sotib olingan ELITE bilan TO'LIQ mos (muddatlar qo'shiladi).
# ================================================================================

@bot.callback_query_handler(func=lambda c: c.data == "admin|user_lookup_info")
def cb_admin_user_lookup_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🔍 <b>Foydalanuvchi profilini ko'rish:</b>\n\n"
        "<code>/useri &lt;user_id&gt;</code> — ID bo'yicha\n"
        "yoki kimningdir xabariga <b>reply</b> qilib <code>/useri</code> deb yozing.",
    )


@bot.message_handler(commands=["useri", "user_lookup"])
def cmd_owner_user_lookup(message):
    """🔍 Bot egasi — istalgan foydalanuvchining TO'LIQ profilini (balans,
    statistika, ELITE/VIP holati, oila, geroy, ban holati, klan) bir zumda ko'radi.
    Foydalanish: /useri <user_id>  YOKI  kimningdir xabariga reply qilib /useri."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return

    target_id = None
    target_name = None
    parts = message.text.split()
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
    elif len(parts) == 2 and parts[1].lstrip("-").isdigit():
        target_id = int(parts[1])
    else:
        bot.send_message(
            message.chat.id,
            "Foydalanish: <code>/useri &lt;user_id&gt;</code> yoki kimningdir xabariga reply qilib <code>/useri</code>.",
        )
        return

    with db_lock:
        cur.execute("SELECT * FROM users WHERE user_id=?", (target_id,))
        row = cur.fetchone()
    if row is None:
        bot.send_message(message.chat.id, f"❌ <code>{target_id}</code> ID'li foydalanuvchi bazada topilmadi.")
        return

    u = dict(zip(USER_COLS, row))
    name = target_name or u.get("name") or str(target_id)
    try:
        inv = json.loads(u.get("inventory") or "[]")
    except Exception:
        inv = []
    banned = bool(u.get("banned"))
    elite_active = is_elite(target_id)
    elite_line = f"👑 Faol — {elite_days_left(target_id)} kun qoldi" if elite_active else "❌ Faol emas"
    nick = get_nickname(target_id)

    with db_lock:
        cur.execute("SELECT hero_key, level FROM heroes WHERE user_id=?", (target_id,))
        hero_row = cur.fetchone()
    hero_line = "—"
    if hero_row:
        hkey, hlvl = hero_row
        hname = HEROES.get(hkey, {}).get("name", hkey)
        hero_line = f"{hname} ({hlvl}-daraja)"

    married_line = "❌ Turmush qurmagan"
    if u.get("married_to"):
        with db_lock:
            cur.execute("SELECT name FROM users WHERE user_id=?", (u["married_to"],))
            mrow = cur.fetchone()
        mname = mrow[0] if mrow else str(u["married_to"])
        married_line = f"💍 {mname} bilan (ID: <code>{u['married_to']}</code>)"

    text = (
        f"🔍 <b>FOYDALANUVCHI PROFILI</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 Ism: <b>{name}</b>\n"
        f"🆔 ID: <code>{target_id}</code>\n"
        f"🏷 Laqab: {nick or '—'}\n\n"
        f"💵 Dollar: <b>${u['dollar']}</b>\n"
        f"💎 Olmos: <b>{u['diamond']}</b>\n"
        f"🪙 Hunter Coin: <b>{u['coin']}</b>\n"
        f"🛡 Qalqon: <b>{u['shield']}</b>\n"
        f"🎒 Inventar: <b>{len(inv)} ta buyum</b>\n\n"
        f"🎮 O'yinlar: <b>{u['games']}</b> | 🏆 G'alabalar: <b>{u['wins']}</b>\n"
        f"⚔️ Duel: {u.get('duel_wins', 0)} G' / {u.get('duel_losses', 0)} M\n"
        f"🏆 Geroy: {hero_line}\n"
        f"{married_line}\n\n"
        f"👑 HUNTER ELITE: {elite_line}\n"
        f"🚫 Ban holati: {'⛔ BLOKLANGAN' if banned else '✅ Erkin'}"
    )
    kb = types.InlineKeyboardMarkup()
    if banned:
        kb.add(types.InlineKeyboardButton("✅ Unban qilish", callback_data=f"adminuser|unban|{target_id}"))
    else:
        kb.add(types.InlineKeyboardButton("🚫 Ban qilish", callback_data=f"adminuser|ban|{target_id}"))
    kb.add(types.InlineKeyboardButton("👑 30 kun ELITE berish", callback_data=f"adminuser|elite30|{target_id}"))
    bot.send_message(message.chat.id, text, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("adminuser|"))
def cb_admin_user_quick_action(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    _, action, uid_s = call.data.split("|")
    target_id = int(uid_s)
    if action == "ban":
        update_user(target_id, banned=1)
        bot.answer_callback_query(call.id, "🚫 Foydalanuvchi bloklandi.", show_alert=True)
    elif action == "unban":
        update_user(target_id, banned=0)
        bot.answer_callback_query(call.id, "✅ Foydalanuvchi blokdan chiqarildi.", show_alert=True)
    elif action == "elite30":
        new_until = grant_elite_days(target_id, 30)
        bot.answer_callback_query(call.id, "👑 30 kunlik ELITE berildi.", show_alert=True)
        safe_send(target_id, elite_success_text(30, new_until))
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "admin|leave_group_info")
def cb_admin_leave_group_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    groups = list_known_groups()
    lines = ["🚪 <b>Botni guruhdan chiqarish:</b>\n",
             "<code>/guruhdan_chiq &lt;chat_id&gt;</code>\n"]
    if groups:
        lines.append("📋 <b>Mavjud guruhlar:</b>")
        for cid, title in groups:
            lines.append(f"• {title} — <code>{cid}</code>")
    bot.send_message(call.message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["guruhdan_chiq"])
def cmd_owner_leave_group(message):
    """🚪 Bot egasi — botni istalgan guruhdan (masalan qoidabuzar/keraksiz
    guruhdan) HAQIQIY ravishda, Telegram API orqali chiqaradi va ro'yxatdan o'chiradi.
    Foydalanish: /guruhdan_chiq <chat_id>"""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].lstrip("-").isdigit():
        bot.send_message(message.chat.id, "Foydalanish: <code>/guruhdan_chiq &lt;chat_id&gt;</code>")
        return
    target_chat_id = int(parts[1])
    try:
        bot.leave_chat(target_chat_id)
        remove_known_group(target_chat_id)
        GAMES.pop(target_chat_id, None)
        bot.send_message(message.chat.id, f"🚪 Bot <code>{target_chat_id}</code> guruhidan muvaffaqiyatli chiqdi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Guruhdan chiqib bo'lmadi: {e}")


@bot.callback_query_handler(func=lambda c: c.data == "admin|elite_give_info")
def cb_admin_elite_give_info(call):
    maybe_capture_owner(call.from_user)
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Ruxsat yo'q.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "👑 <b>HUNTER ELITE qo'lda, muddatli berish:</b>\n\n"
        "Kimningdir xabariga reply qilib:\n<code>/elite_ber &lt;kun&gt;</code>\n\n"
        "Masalan: <code>/elite_ber 30</code> — 30 kunlik ELITE beradi.\n"
        "<i>Agar foydalanuvchida allaqachon faol ELITE bo'lsa, muddat USTIGA QO'SHILADI "
        "(sotib olingan ELITE bilan bir xil mantiq).</i>",
    )


@bot.message_handler(commands=["elite_ber"])
def cmd_owner_elite_ber(message):
    """👑 Bot egasi — istalgan foydalanuvchiga qo'lda, xohlagan muddatga
    HUNTER ELITE (VIP) beradi. Mavjud grant_elite_days() funksiyasidan
    foydalanadi — shu sababli sotib olingan ELITE bilan 100% mos (qo'shiladi).
    Foydalanish: kimningdir xabariga reply qilib /elite_ber <kun>."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    parts = message.text.split()
    if not message.reply_to_message or len(parts) != 2 or not parts[1].lstrip("-").isdigit():
        bot.send_message(
            message.chat.id,
            "Foydalanish: kimningdir xabariga reply qilib <code>/elite_ber &lt;kun&gt;</code>",
        )
        return
    days = int(parts[1])
    if days <= 0 or days > 3650:
        bot.send_message(message.chat.id, "❌ Kunlar soni 1 dan 3650 gacha bo'lishi kerak.")
        return
    target = message.reply_to_message.from_user
    user_dict(target.id, target.first_name)
    new_until = grant_elite_days(target.id, days)
    bot.send_message(
        message.chat.id,
        f"👑 {mention(target.id, target.first_name)}ga <b>{days} kunlik</b> HUNTER ELITE berildi!\n"
        f"📅 Amal qilish muddati: <b>{time.strftime('%d.%m.%Y', time.localtime(new_until))}</b> gacha.",
    )
    safe_send(target.id, elite_success_text(days, new_until))


# ================================================================================
#  📜 BOTFATHER UCHUN BUYRUQLAR MENYUSI — ENDI FAQAT 2 XIL (uchga emas!):
#
#   1) FOYDALANUVCHILAR uchun (USER_COMMANDS) — GURUHDA HAM, SHAXSIY CHATDA HAM
#      bir xil to'liq ro'yxat ko'rinadi (shu jumladan /newgame, /startgame,
#      /povtorgame, /start_team, /parastart kabi barcha "guruhda kerak
#      bo'ladigan" buyruqlar — avval bular GROUP_COMMANDS ro'yxatida yo'q edi,
#      shuning uchun guruhda "/" bosilganda ko'rinmas edi — TUZATILDI).
#   2) BOT EGASI (5588583777) uchun (OWNER_EXTRA_COMMANDS) — YUQORIDAGI
#      BARCHA USER_COMMANDS + faqat egaga tegishli qo'shimcha buyruqlar.
#      Owner uchun ikkalasi BIRLASHTIRILIB ko'rsatiladi — ya'ni owner
#      botning MUTLAQO BARCHA buyruqlarini ko'radi.
#
#  Bot ishga tushganda set_bot_commands_for_all_scopes() avtomatik chaqiriladi.
# ================================================================================

USER_COMMANDS = [
    ("start", "🚀 Botni ishga tushirish"),
    ("join", "➕ O'yinga qo'shilish"),
    ("rolni_tanla", "🎭 Maxsus rolni tanlash"),
    ("profile", "👤 Profilim / kabinet"),
    ("inventar", "🎒 Inventarim"),
    ("kuchlarim", "⚡ Menda mavjud effektlar"),
    ("top", "🏆 Reyting"),
    ("topalmaz", "💎 Olmos reytingi"),
    ("topdollar", "💵 Dollar reytingi"),
    ("balltop_kun", "📅 Kunlik ball reytingi"),
    ("balltop_hafta", "📆 Haftalik ball reytingi"),
    ("balltop_oy", "🗓 Oylik ball reytingi"),
    ("balltop_mutlaq", "🏅 Umumiy ball reytingi"),
    ("heros", "🦸 Geroylar ro'yxati"),
    ("geroyim", "🦸 Mening geroyim"),
    ("geroy_bashorat", "🔮 Geroy bashorati"),
    ("geroy_koz", "👁 Geroy ko'zi"),
    ("geroy_daromad", "💰 Geroy daromadi"),
    ("hisob", "💳 Hisobim"),
    ("almazdokon", "💎 Olmos do'koni"),
    ("dollar_dokon", "🏪 Dollar do'koni"),
    ("olmos_coin", "💎 Olmos ↔ Coin ayirboshlash"),
    ("sell", "🛒 Sotuvga qo'yish"),
    ("buy", "🛍 Sotib olish"),
    ("market", "🏬 Bozor"),
    ("osh", "🍲 Osh (o'yin ichi funksiyasi)"),
    ("elite", "👑 HUNTER ELITE olish"),
    ("elite_sandiq", "💎 ELITE Sirli Sandiq (faqat ELITE)"),
    ("taqdir", "🔮 Taqdir G'ildiragi (kunlik omad)"),
    ("til", "🌐 Tilni tanlash"),
    ("taxallus", "🏷 Laqab o'rnatish (ELITE)"),
    ("sovga", "🎁 Sovg'a yuborish"),
    ("chiqish", "🚪 O'yindan chiqish (ELITE)"),
    ("duel", "⚔️ Duelga chaqirish"),
    ("duel_stat", "📈 Duel statistikam"),
    ("nikoh", "💍 Turmush qurish taklifi"),
    ("juftim", "💑 Juftim"),
    ("ajrashish", "💔 Ajrashish"),
    ("oilainfo", "👨‍👩‍👧 Oila haqida ma'lumot"),
    ("oilatop", "🏆 Oilalar reytingi"),
    ("quchoqla", "🤗 Quchoqlash / o'pish"),
    ("sovgla", "🎁 Juftga sovg'a"),
    ("xiyonat", "💔 Xiyonat qilish (hazil)"),
    ("givde", "🎁 Sovg'a berish (reply)"),
    ("givdemoney", "💵 Pul sovg'a berish (reply)"),
    ("givdecoin", "🪙 Coin sovg'a berish (reply)"),
    ("klan", "🏛 Klan yaratish / bo'limi"),
    ("klanim", "🏛 Mening klanim"),
    ("klanga_qoshil", "➕ Klanga qo'shilish"),
    ("klan_tark", "🚪 Klandan chiqish"),
    ("klan_chetlash", "❌ Klandan a'zo chiqarish (klan egasi)"),
    ("klan_orinbosar", "🥈 O'rinbosar tayinlash (klan egasi)"),
    ("klan_azo_daraja", "⭐ A'zo darajasini oshirish (klan egasi)"),
    ("klan_lvl", "📈 Klan darajasi"),
    ("klan_nomi", "✏️ Klan nomini o'zgartirish"),
    ("klan_maqom", "🎖 Klan maqomi"),
    ("klan_hazna", "💰 Klan xazinasi"),
    ("klan_taqsimla", "🤝 Klan xazinasini taqsimlash"),
    ("klanlar", "📋 Klanlar ro'yxati"),
    ("klanjang", "⚔️ Klanlar jangi"),
    ("tark_et", "🚪 O'yinni tark etish"),
    ("turnir_royxat", "📋 Turnir ishtirokchilari ro'yxati"),
    ("promo", "🎟 Promo-kodni ishlatish"),
    ("jamoa", "💬 Mafiya jamoasiga yashirin xabar"),
    ("adolat", "💬 Qonun jamoasiga yashirin xabar"),
    ("zahar", "☠️ Zahar ishlatish (buyum)"),
    ("gps", "📍 GPS (buyum)"),
    ("kompas", "🧭 Kompas (buyum)"),
    ("tutun", "💨 Tutun bombasi (buyum)"),
    ("fonar", "🔦 Fonar (buyum)"),
    ("qayta_tanlash", "🔁 Rolni qayta tanlash (buyum)"),
    ("newgame", "🎮 Yangi o'yin ochish (admin)"),
    ("povtorgame", "🔁 Yopilgan qo'shilishni qayta ochish (admin)"),
    ("startgame", "▶️ O'yinni majburan boshlash (admin)"),
    ("sotop", "🛑 O'yinni to'xtatish (admin)"),
    ("paralar", "💍 Para juftliklar ro'yxati (admin)"),
    ("zayafka_soni", "📥 A'zolik so'rovlari soni (admin)"),
    ("zayafka_qabul", "✅ A'zolik so'rovlarini qabul qilish (admin)"),
    ("zayafka_hammasi", "✅ Barcha so'rovlarni qabul qilish (admin)"),
    ("zayafka_rad", "❌ A'zolik so'rovlarini rad etish (admin)"),
    ("start_team", "🐺🦅 Jamoaviy o'yinni boshlash (admin)"),
    ("stop_team", "🏁 Jamoaviy o'yinni yakunlash (admin)"),
    ("parastart", "💍 Para o'yinga ro'yxat ochish (admin)"),
    ("paraforce", "💍 Para o'yinni majburiy boshlash (admin)"),
    ("parastop", "🛑 Para o'yinni to'xtatish (admin)"),
    ("guruh_ban", "🚫 Guruhda bloklash (admin)"),
    ("guruh_unban_hammasi", "✅ Guruhda hammani unban qilish (admin)"),
]

OWNER_EXTRA_COMMANDS = [
    ("ban", "🚫 Foydalanuvchini bloklash"),
    ("unban", "✅ Blokdan chiqarish"),
    ("addmoney", "💵 Dollar qo'shish/ayirish"),
    ("adddiamond", "💎 Olmos qo'shish/ayirish"),
    ("addcoin", "🪙 Coin qo'shish/ayirish"),
    ("valyuta_ber", "💱 Valyuta qo'lda berish (reply)"),
    ("geroy_ber", "🏆 Geroy qo'lda berish (reply)"),
    ("ball_ber", "🏅 Ball qo'lda qo'shish/ayirish (reply)"),
    ("promo_create", "🎁 Promo-kod yaratish"),
    ("promo_yarat", "🎟 Shaxsiy promo-kod yaratish"),
    ("tarqatish", "🎉 Ommaviy sovg'a tarqatish"),
    ("sendall", "📢 Barchaga global xabar"),
    ("statistika", "📊 Bot bo'yicha to'liq statistika"),
    ("bazani_tikla", "🔄 Bazani zaxira nusxadan tiklash"),
    ("oyinni_zorla_tugat", "🛑 Joriy o'yinni zudlik bilan to'xtatish"),
    ("royxat_faol", "📋 Faol ro'yxatga olishlar"),
    ("useri", "🔍 Foydalanuvchi profilini qidirish"),
    ("guruhdan_chiq", "🚪 Botni guruhdan chiqarish"),
    ("elite_ber", "👑 ELITE qo'lda berish"),
    ("turnir_boshla", "🏆 Yangi turnir ochish"),
    ("turnir_yopish", "🔒 Turnir ro'yxatini yopish"),
    ("turnir_jang", "⚔️ Turnir jangini boshlash"),
    ("turnir_tugat", "🛑 Turnirni bekor qilish"),
    ("topguruh", "🏘 Top guruhlar (maxfiy statistika)"),
    ("mirkamilovic", "👑 Owner maxsus paneli"),
    ("shu_kanal", "📢 Yangiliklar kanalini bog'lash"),
    ("shu_bozor", "🏪 Qora bozor guruhini bog'lash"),
    ("bozor_holati", "📦 Qora bozor holati"),
    ("guruh_id", "🆔 Guruh ID raqami"),
    ("guruh", "ℹ️ Guruh haqida ma'lumot"),
    ("jufti", "💍 (texnik) juftlik testi"),
    ("jufti_bekor", "💔 (texnik) juftlik testini bekor qilish"),
    ("klan_mukofot", "🏆 3 oylik top klanlar mukofoti"),
    ("emoji_test", "🧪 Premium emojilarni sinash"),
    ("tiklash", "🔁 Botni qayta ishga tushirish"),
    ("teamgame", "🐺🦅 Jamoaviy o'yin rejimini yoqish/o'chirish"),
    ("parateam", "💍 Para o'yin rejimini yoqish/o'chirish"),
    ("setting", "⚙️ Guruh sozlamalari paneli"),
    ("menyu_yangila", "🔄 Buyruqlar menyusini qayta o'rnatish"),
]


def set_bot_commands_for_all_scopes():
    """🤖 Bot ishga tushganda avtomatik chaqiriladi — Telegram'ga 2 xil scope
    bo'yicha 2 xil buyruqlar ro'yxatini yuboradi:
      • Hammaga (guruh HAM, shaxsiy chat HAM) — USER_COMMANDS (to'liq, hech
        narsa tashlab ketilmagan — guruhda /newgame, /startgame va h.k. ENDI
        albatta ko'rinadi)
      • Bot egasining shaxsiy chati (5588583777) — USER_COMMANDS +
        OWNER_EXTRA_COMMANDS — ya'ni BARCHA buyruqlar birgalikda
    Bu — Telegram Bot API'ning rasmiy imkoniyati (setMyCommands + scope);
    boshqa hech bir foydalanuvchi owner buyruqlarini o'z menyusida KO'RMAYDI."""
    try:
        user_cmds = [types.BotCommand(c, d) for c, d in USER_COMMANDS]
        bot.set_my_commands(commands=user_cmds, scope=types.BotCommandScopeAllGroupChats())
        bot.set_my_commands(commands=user_cmds, scope=types.BotCommandScopeAllPrivateChats())
        bot.set_my_commands(commands=user_cmds)  # scope'siz — standart/fallback ro'yxat sifatida ham o'rnatiladi
    except Exception as e:
        _logger.warning("Foydalanuvchi buyruqlar menyusini o'rnatishda xatolik: %s", e)

    try:
        seen = set()
        owner_cmds = []
        for c, d in USER_COMMANDS + OWNER_EXTRA_COMMANDS:
            if c in seen:
                continue
            seen.add(c)
            owner_cmds.append(types.BotCommand(c, d))
        owner_cmds = owner_cmds[:100]  # Telegram cheklovi: bitta scope uchun maks. 100 ta buyruq
        bot.set_my_commands(
            commands=owner_cmds,
            scope=types.BotCommandScopeChat(chat_id=OWNER_ID_FROM_ENV),
        )
    except Exception as e:
        _logger.warning("Owner buyruqlar menyusini o'rnatishda xatolik: %s", e)


@bot.message_handler(commands=["menyu_yangila"])
def cmd_menyu_yangila(message):
    """🔄 Bot egasi — 2 xil buyruqlar menyusini (foydalanuvchi/owner) istalgan
    vaqt qo'lda qayta o'rnatadi (masalan USER_COMMANDS/OWNER_EXTRA_COMMANDS
    ro'yxatlariga o'zgartirish kiritilgandan keyin)."""
    maybe_capture_owner(message.from_user)
    safe_delete(message)
    if not is_owner(message.from_user.id):
        return
    set_bot_commands_for_all_scopes()
    bot.send_message(message.chat.id, "✅ Buyruqlar menyusi (foydalanuvchilar / owner) qayta o'rnatildi.")



# ================================================================================
#  ISHGA TUSHIRISH
# ================================================================================

if __name__ == "__main__":
    print("Hunter Mafia bot v5 (telebot, do'kon + Stars + promo + tarqatish + qora bozor + klan jangi) ishga tushmoqda...")
    with db_lock:
        cur.execute("SELECT COUNT(*) FROM users")
        _existing_users = cur.fetchone()[0]
    _logger.info(f"📂 Baza fayli: {DB_PATH}")
    _logger.info(f"👥 Bazadagi mavjud foydalanuvchilar soni: {_existing_users} ta")
    if _existing_users == 0 and _users_table_existed is False:
        _logger.warning("⚠️ Bu — 'users' jadvali birinchi marta yaratilyapti (yangi/bo'sh baza). Agar avval "
                         "foydalanuvchilar bo'lgan bo'lsa, bot boshqa papkadan yoki boshqa hunter_mafia.db "
                         "fayli bilan ishga tushirilayotgan bo'lishi mumkin — DB_PATH qatorini tekshiring.")
    _state_restored = False
    while True:
        try:
            BOT_USERNAME = bot.get_me().username
            _logger.info("Bot ishga tushdi: @%s", BOT_USERNAME)
            if not _state_restored:
                # 🔄 oldingi ishga tushishda (xatolik/deploy/`/tiklash`) saqlangan aktiv
                # o'yinlar bo'lsa, shu yerda tiklanadi — faqat 1 marta, tarmoq uzilib
                # qayta ulanganda emas (chunki fayl birinchi muvaffaqiyatli tiklashda o'chiriladi).
                load_games_state()
                _state_restored = True
                _check_clan_inactivity()  # 🏛 klan faolsizlik tekshiruvini fon rejimida ishga tushiramiz
                set_bot_commands_for_all_scopes()  # 📜 3 xil buyruqlar menyusini (guruh/shaxsiy/owner) o'rnatish
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            # Tarmoq uzilishi yoki Telegram API vaqtinchalik ishlamay qolishi kabi hollarda
            # bot butunlay o'chib qolmasin — 5 soniya kutib qayta ulanadi.
            _logger.exception("Polling to'xtadi, 5 soniyadan keyin qayta urinilmoqda: %s", e)
            time.sleep(5)
