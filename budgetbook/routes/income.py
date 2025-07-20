from flask import Blueprint, request
from budgetbook.db import get_db
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_amount, is_valid_date

income_bp = Blueprint("income", __name__)


@income_bp.route("/income", methods=["POST"])
def add_income():
    data = request.json or {}

    # 日付バリデーション
    if not is_valid_date(data.get("date")):
        return json_response(
            {"error": "Invalid date format (YYYY-MM-DD required)"}, 400
        )

    # カテゴリ必須チェック
    if not data.get("category"):
        return json_response({"error": "category is required"}, 400)

    # 金額バリデーション
    if not is_valid_amount(data.get("amount")):
        return json_response({"error": "amount must be a number"}, 400)

    amount = float(data["amount"])

    db = get_db()
    db.execute(
        "INSERT INTO income (date, category, amount) VALUES (?, ?, ?)",
        (data["date"], data["category"], amount),
    )
    db.commit()
    db.close()

    return json_response({"message": "Income added successfully"}, status=201)


@income_bp.route("/income", methods=["GET"])
def get_income():
    start = request.args.get("start")
    end = request.args.get("end")
    db = get_db()
    rows = db.execute(
        "SELECT * FROM income WHERE date BETWEEN ? AND ? ORDER BY date", (start, end)
    ).fetchall()
    db.close()
    result = [dict(row) for row in rows]
    return json_response(result)
