import sqlite3
import os

DB_PATH = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_item(code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM inventory WHERE code = ?", (code,))
    item = cursor.fetchone()
    conn.close()
    return item

def add_item(code, name, description="No description"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventory (code, name, description) VALUES (?, ?, ?)", (code, name, description))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
