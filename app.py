from flask import Flask, request, jsonify
import sqlite3
import os
import json

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


@app.route("/income", methods=["POST"])
def add_income():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO income (date, category, amount) VALUES (?, ?, ?)",
        (data["date"], data["category"], data["amount"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Income added"}), 201


@app.route("/income", methods=["GET"])
def get_income():
    start = request.args.get("start")
    end = request.args.get("end")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM income WHERE date BETWEEN ? AND ?", (start, end))
    rows = c.fetchall()
    conn.close()
    return app.response_class(
        response=json.dumps(rows, ensure_ascii=False), mimetype="application/json"
    )


@app.route("/expense", methods=["POST"])
def add_expense():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO expense (date, shop, category, payment, amount)
        VALUES (?, ?, ?, ?, ?)
    """,
        (data["date"], data["shop"], data["category"], data["payment"], data["amount"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense added"}), 201


@app.route("/expense", methods=["GET"])
def get_expense():
    start = request.args.get("start")
    end = request.args.get("end")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM expense WHERE date BETWEEN ? AND ?", (start, end))
    rows = c.fetchall()
    conn.close()

    # 整形（オプション）
    results = [
        {
            "id": row[0],
            "date": row[1],
            "shop": row[2],
            "category": row[3],
            "payment": row[4],
            "amount": row[5],
        }
        for row in rows
    ]

    return app.response_class(
        response=json.dumps(results, ensure_ascii=False), mimetype="application/json"
    )


@app.route("/expense/summary", methods=["GET"])
def expense_summary():
    start = request.args.get("start")
    end = request.args.get("end")
    group_by = request.args.get("group_by")

    # 必須パラメータの確認
    if not all([start, end, group_by]):
        return jsonify({"error": "start, end, and group_by are required"}), 400

    if group_by not in ["category", "payment"]:
        return jsonify({"error": "group_by must be 'category' or 'payment'"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 動的に GROUP BY を切り替える
    query = f"""
        SELECT {group_by}, SUM(amount)
        FROM expense
        WHERE date BETWEEN ? AND ?
        GROUP BY {group_by}
    """
    c.execute(query, (start, end))
    rows = c.fetchall()
    conn.close()

    # JSON形式に整形
    result = [{group_by: row[0], "total": row[1]} for row in rows]

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False), mimetype="application/json"
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
