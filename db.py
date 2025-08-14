import sqlite3
import os

# Define the database path within the app directory
DB_PATH = os.path.join(os.path.dirname(__file__), 'dictionary.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY,
            turkish_word TEXT UNIQUE NOT NULL,
            english_word TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_word(turkish_word):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT english_word FROM translations WHERE turkish_word=?", (turkish_word.lower(),))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_word(turkish_word, english_word):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO translations (turkish_word, english_word) VALUES (?, ?)", (turkish_word.lower(), english_word.lower()))
        conn.commit()
    except sqlite3.IntegrityError:
        # Word already exists
        pass
    finally:
        conn.close()
