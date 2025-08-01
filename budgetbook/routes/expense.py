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
    """支出データ取得（期間フィルタ付き）"""
    start = request.args.get("start")
    end = request.args.get("end")

    query = Expense.query
    if start:
        query = query.filter(Expense.date >= start)
    if end:
        query = query.filter(Expense.date <= end)

    # デフォルトは全件、フィルタがあれば適用
    expenses = query.order_by(Expense.date.desc()).all()

    return expenses_schema.dump(expenses), 200


@expense_bp.route("/expense/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    inc = Expense.query.get_or_404(expense_id)
    return expense_schema.dump(inc), 200


@expense_bp.route("/expense/<int:expense_id>", methods=["PATCH"])
def update_expense(expense_id):
    inc = Expense.query.get_or_404(expense_id)
    try:
        # partial=True で部分更新を許可
        data = expense_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    for key, value in data.items():
        setattr(inc, key, value)
    db.session.commit()
    return expense_schema.dump(inc), 200


@expense_bp.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    inc = Expense.query.get_or_404(expense_id)
    db.session.delete(inc)
    db.session.commit()
    return "", 204
