import sqlite3
from budgetbook.config import DB_PATH


def get_db_connection():
    """共通のDB接続を返す"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
