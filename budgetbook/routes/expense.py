from flask import Blueprint, request
from budgetbook.models import Expense
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_amount, is_valid_date
from budgetbook.extensions import db

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

    expense = Expense(
        date=data["date"],
        shop=data.get("shop"),
        category=data["category"],
        amount=data["amount"],
        payment=data.get("payment"),
    )
    db.session.add(expense)
    db.session.commit()
    return json_response({"message": "Expense added successfully"}, status=201)


@expense_bp.route("/expense", methods=["GET"])
def list_expense():
    """全支出データを取得"""
    expenses = Expense.query.all()
    result = [
        {
            "id": e.id,
            "date": e.date,
            "shop": e.shop,
            "category": e.category,
            "amount": e.amount,
            "payment": e.payment,
        }
        for e in expenses
    ]
    return json_response(result)


@expense_bp.route("/expense", methods=["GET"])
def list_expense_filtered():
    start = request.args.get("start")
    end = request.args.get("end")

    query = Expense.query
    if start and end:
        query = query.filter(Expense.date.between(start, end))

    expenses = query.all()
    result = [
        {
            "id": e.id,
            "date": e.date,
            "shop": e.shop,
            "category": e.category,
            "amount": e.amount,
            "payment": e.payment,
        }
        for e in expenses
    ]
    return json_response(result)
