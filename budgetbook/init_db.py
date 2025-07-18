import sqlite3
import os
from budgetbook.config import DB_PATH
from budgetbook.app import app


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
    payment TEXT
);
"""


def init_db():
    db_path = app.config["DB_PATH"]  # ← app.config から取る
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            store TEXT,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL,
            payment_method TEXT
        );
        """
    )

    conn.commit()
    conn.close()
    print(f"✅ Initialized DB at {db_path}")


if __name__ == "__main__":
    init_db()
