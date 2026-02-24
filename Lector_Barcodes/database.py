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
            description TEXT,
            price REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

def get_item(code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price FROM inventory WHERE code = ?", (code,))
    item = cursor.fetchone()
    conn.close()
    return item

def add_item(code, name, price, description="No description"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventory (code, name, price, description) VALUES (?, ?, ?, ?)", (code, name, price, description))
        conn.commit()
    except sqlite3.IntegrityError:
        # If it exists, we could update or just pass. User wants to edit name specifically.
        pass
    conn.close()

def update_item_name(code, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET name = ? WHERE code = ?", (name, code))
    conn.commit()
    conn.close()

def update_item_price(code, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET price = ? WHERE code = ?", (price, code))
    conn.commit()
    conn.close()

def delete_item(code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE code = ?", (code,))
    conn.commit()
    conn.close()
