from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "db/budgetbook.db"


# DB初期化（1回だけ実行）
def init_db():
    if not os.path.exists("db"):
        os.makedirs("db")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount INTEGER
                )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS expense (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    shop TEXT,
                    category TEXT,
                    payment TEXT,
                    amount INTEGER
                )"""
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "Kakeibo App is running!"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
