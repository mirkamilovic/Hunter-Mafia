import os
import sqlite3

# Railway'da Volume ulangan bo'lsa, ma'lumotlar o'sha yerda saqlanadi.
# Agar localda ishlatayotgan bo'lsangiz, oddiy papkaga saqlaydi.
DB_DIR = "data"
if not os.path.exists(DB_DIR):
  os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, "mafia_bot.db")

# Bazaga ulanish
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Jadvalni yaratish (hamma narsa shu yerda saqlanadi)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance INTEGER DEFAULT 0,
    inventory TEXT DEFAULT '',
    matches_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0
)
"""
)
conn.commit()


# Foydalanuvchini bazaga qo'shish yoki borligini tekshirish
def get_or_create_user(user_id, username):
  cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
  user = cursor.fetchone()
  if not user:
    cursor.execute(
        "INSERT INTO players (user_id, username, balance, inventory,"
        " matches_played, wins) VALUES (?, ?, 0, '', 0, 0)",
        (user_id, username),
    )
    conn.commit()
    cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
  return user


# Balansni yangilash
def update_balance(user_id, amount):
  cursor.execute(
      "UPDATE players SET balance = balance + ? WHERE user_id = ?",
      (amount, user_id),
  )
  conn.commit()


# Inventarga buyum qo'shish
def add_item(user_id, item_name):
  cursor.execute("SELECT inventory FROM players WHERE user_id = ?", (user_id,))
  res = cursor.fetchone()
  if res:
    current_inv = res[0]
    new_inv = f"{current_inv},{item_name}" if current_inv else item_name
    cursor.execute(
        "UPDATE players SET inventory = ? WHERE user_id = ?",
        (new_inv, user_id),
    )
    conn.commit()


# O'yin statistikalarini yangilash (masalan, o'yin sonini oshirish)
def add_match_played(user_id):
  cursor.execute(
      "UPDATE players SET matches_played = matches_played + 1 WHERE user_id = ?",
      (user_id,),
  )
  conn.commit()
