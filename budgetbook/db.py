import sqlite3
from flask import g, current_app
from budgetbook.config import DB_PATH


def get_db():
    """リクエストごとにDB接続を作る"""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """リクエスト終了時にDBを閉じる"""
    db = g.pop("db", None)
    if db is not None:
        db.close()
