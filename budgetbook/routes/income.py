from flask import Blueprint, request
from marshmallow import ValidationError
from budgetbook.models import Income
from budgetbook.schemas import income_schema, incomes_schema
from budgetbook.extensions import db

income_bp = Blueprint("income", __name__)


@income_bp.route("/income", methods=["POST"])
def add_income():
    data = request.get_json()

    try:
        data = income_schema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    income = Income(**data)
    db.session.add(income)
    db.session.commit()

    return income_schema.dump(income), 201


@income_bp.route("/income", methods=["GET"])
def list_income():
    """収入データ取得（期間フィルタ付き）"""
    start = request.args.get("start")
    end = request.args.get("end")

    query = Income.query
    if start:
        query = query.filter(Income.date >= start)
    if end:
        query = query.filter(Income.date <= end)

    # デフォルトは全件、フィルタがあれば適用
    incomes = query.order_by(Income.date.desc()).all()

    return incomes_schema.dump(incomes), 200


@income_bp.route("/income/<int:income_id>", methods=["GET"])
def get_income(income_id):
    inc = Income.query.get_or_404(income_id)
    return income_schema.dump(inc), 200


@income_bp.route("/income/<int:income_id>", methods=["PATCH"])
def update_income(income_id):
    inc = Income.query.get_or_404(income_id)
    try:
        # partial=True で部分更新を許可
        data = income_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    for key, value in data.items():
        setattr(inc, key, value)
    db.session.commit()
    return income_schema.dump(inc), 200


@income_bp.route("/income/<int:income_id>", methods=["DELETE"])
def delete_income(income_id):
    inc = Income.query.get_or_404(income_id)
    db.session.delete(inc)
    db.session.commit()
    return "", 204
