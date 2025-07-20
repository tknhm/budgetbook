from flask import Blueprint, request
from budgetbook.models import Income
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_amount, is_valid_date
from budgetbook.extensions import db

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

    income = Income(
        date=data["date"],
        category=data["category"],
        amount=amount,
    )
    db.session.add(income)
    db.session.commit()

    return json_response({"message": "Income added successfully"}, status=201)


@income_bp.route("/income", methods=["GET"])
def list_income():
    """全収入データを取得"""
    incomes = Income.query.all()
    result = [
        {
            "id": i.id,
            "date": i.date,
            "category": i.category,
            "amount": i.amount,
        }
        for i in incomes
    ]
    return json_response(result)


@income_bp.route("/income", methods=["GET"])
def list_income_filtered():
    start = request.args.get("start")
    end = request.args.get("end")

    query = Income.query
    if start and end:
        query = query.filter(Income.date.between(start, end))

    incomes = query.all()
    result = [
        {
            "id": i.id,
            "date": i.date,
            "category": i.category,
            "amount": i.amount,
        }
        for i in incomes
    ]
    return json_response(result)
