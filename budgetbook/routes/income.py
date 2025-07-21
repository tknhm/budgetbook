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
