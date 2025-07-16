import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "budgetbook.db")

schema = """
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    shop TEXT,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT
);
"""


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.close()
    print(f"✅ Initialized DB at {DB_PATH}")


if __name__ == "__main__":
    init_db()
