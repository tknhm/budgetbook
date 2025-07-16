from flask import Flask, request
import sqlite3
import json
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "budgetbook.db")


# --- 共通ヘルパー ---


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def json_response(data, status=200):
    return app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        status=status,
        mimetype="application/json",
    )


# --- 収入API ---
@app.route("/income", methods=["POST"])
def add_income():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO income (date, category, amount) VALUES (?, ?, ?)",
        (data["date"], data["category"], data["amount"]),
    )
    conn.commit()
    conn.close()
    return json_response({"message": "Income added"})


@app.route("/income", methods=["GET"])
def get_income():
    start = request.args.get("start")
    end = request.args.get("end")
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM income WHERE date BETWEEN ? AND ? ORDER BY date", (start, end)
    ).fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    return json_response(result)


# --- 支出API ---
@app.route("/expense", methods=["POST"])
def add_expense():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expense (date, shop, category, payment, amount) VALUES (?, ?, ?, ?, ?)",
        (data["date"], data["shop"], data["category"], data["payment"], data["amount"]),
    )
    conn.commit()
    conn.close()
    return json_response({"message": "Expense added"})


@app.route("/expense", methods=["GET"])
def get_expense():
    start = request.args.get("start")
    end = request.args.get("end")
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM expense WHERE date BETWEEN ? AND ? ORDER BY date", (start, end)
    ).fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    return json_response(result)


@app.route("/expense/summary", methods=["GET"])
def expense_summary():
    start = request.args.get("start")
    end = request.args.get("end")
    group_by = request.args.get("group_by")

    if not all([start, end, group_by]):
        return json_response({"error": "start, end, and group_by are required"}, 400)

    if group_by not in ["category", "payment"]:
        return json_response({"error": "group_by must be 'category' or 'payment'"}, 400)

    conn = get_db_connection()
    rows = conn.execute(
        f"SELECT {group_by}, SUM(amount) AS total FROM expense WHERE date BETWEEN ? AND ? GROUP BY {group_by}",
        (start, end),
    ).fetchall()
    conn.close()

    result = [{group_by: row[group_by], "total": row["total"]} for row in rows]
    return json_response(result)


if __name__ == "__main__":
    app.run(debug=True)
