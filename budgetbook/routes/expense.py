from flask import Blueprint, request
from budgetbook.db import get_db_connection
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_amount, is_valid_date

expense_bp = Blueprint("expense", __name__)


@expense_bp.route("/expense", methods=["POST"])
def add_expense():
    data = request.json or {}

    # 日付バリデーション
    if not is_valid_date(data.get("date")):
        return json_response(
            {"error": "Invalid date format (YYYY-MM-DD required)"}, 400
        )

    # カテゴリ必須チェック
    if not data.get("category"):
        return json_response({"error": "category is required"}, 400)

    # 店名必須チェック
    if not data.get("shop"):
        return json_response({"error": "shop is required"}, 400)

    # 支払い方法必須チェック
    if not data.get("payment"):
        return json_response({"error": "payment is required"}, 400)

    # 金額バリデーション
    if not is_valid_amount(data.get("amount")):
        return json_response({"error": "amount must be a number"}, 400)

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expense (date, shop, category, amount, payment) VALUES (?, ?, ?, ?, ?)",
        (
            data["date"],
            data.get("shop"),
            data["category"],
            int(data["amount"]),
            data.get("payment"),
        ),
    )
    conn.commit()
    conn.close()

    return json_response({"message": "Expense added successfully"}, status=201)


@expense_bp.route("/expense", methods=["GET"])
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
