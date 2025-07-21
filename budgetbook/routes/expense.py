from flask import Blueprint, request
from marshmallow import ValidationError
from budgetbook.models import Expense
from budgetbook.schemas import expense_schema, expenses_schema
from budgetbook.extensions import db

expense_bp = Blueprint("expense", __name__)


@expense_bp.route("/expense", methods=["POST"])
def add_expense():
    data = request.get_json()

    try:
        data = expense_schema.load(request.json)  # ✅ バリデーション
    except ValidationError as err:
        return {"errors": err.messages}, 400

    expense = Expense(**data)
    db.session.add(expense)
    db.session.commit()
    return expense_schema.dump(expense), 201


@expense_bp.route("/expense", methods=["GET"])
def list_expense():
    """全支出データを取得"""
    expenses = Expense.query.all()

    return expenses_schema.dump(expenses), 200


@expense_bp.route("/expense", methods=["GET"])
def list_expense_filtered():
    start = request.args.get("start")
    end = request.args.get("end")

    query = Expense.query
    if start:
        query = query.filter(Expense.date >= start)
    if end:
        query = query.filter(Expense.date <= end)

    expenses = query.order_by(Expense.date.desc()).all()

    return expenses_schema.dump(expenses), 200
