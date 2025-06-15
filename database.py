import sqlite3
import os
os.makedirs("uploaded", exist_ok=True)
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    path TEXT,
    link TEXT,
    user_id INTEGER,
    phash TEXT,
    clip TEXT,
    gdrive_url TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS admins (chat_id INTEGER PRIMARY KEY)''')
conn.commit()

def init_db():
    pass

def save_data(path, link, user_id, features, gdrive_url):
    cursor.execute("INSERT INTO data (path, link, user_id, phash, clip, gdrive_url) VALUES (?, ?, ?, ?, ?, ?)",
                   (path, link, user_id, features['phash'], features['clip'], gdrive_url))
    conn.commit()

def get_user_data(user_id):
    return cursor.execute("SELECT id, path, link FROM data WHERE user_id = ?", (user_id,)).fetchall()

def delete_data_by_id(data_id):
    cursor.execute("DELETE FROM data WHERE id = ?", (data_id,))
    conn.commit()

def is_admin(chat_id):
    return cursor.execute("SELECT 1 FROM admins WHERE chat_id = ?", (chat_id,)).fetchone() is not None

def set_admin(chat_id, active=True):
    if active:
        cursor.execute("INSERT OR IGNORE INTO admins (chat_id) VALUES (?)", (chat_id,))
    else:
        cursor.execute("DELETE FROM admins WHERE chat_id = ?", (chat_id,))
    conn.commit()

def find_best_match(features):
    rows = cursor.execute("SELECT link, clip FROM data").fetchall()
    best_score = 0
    best_link = None
    for link, clip_vector in rows:
        score = compare_features_clip(features['clip'], clip_vector)
        if score > 0.85:
            return (score, link)
    return None