import sqlite3

def init_db():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY,
            turkish_word TEXT UNIQUE,
            english_word TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_word(turkish_word):
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("SELECT english_word FROM translations WHERE turkish_word=?", (turkish_word,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_word(turkish_word, english_word):
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("INSERT INTO translations (turkish_word, english_word) VALUES (?, ?)", (turkish_word, english_word))
    conn.commit()
    conn.close()
