from flask import Blueprint, request
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_date
from budgetbook.models import Expense
from sqlalchemy import func
from budgetbook.extensions import db

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/expense/summary", methods=["GET"])
def expense_summary():
    start = request.args.get("start")
    end = request.args.get("end")
    group_by = request.args.get("group_by", "category")

    if not all([start, end, group_by]):
        return json_response({"error": "start, end, and group_by are required"}, 400)

    # 日付バリデーション
    for date in [start, end]:
        if not is_valid_date(date):
            return json_response(
                {"error": "Invalid date format (YYYY-MM-DD required)"}, 400
            )

    if group_by not in ["category", "payment"]:
        return json_response({"error": "group_by must be 'category' or 'payment'"}, 400)

    # 集計ベースのクエリ
    field = Expense.category if group_by == "category" else Expense.payment

    query = db.session.query(
        field.label(group_by), func.sum(Expense.amount).label("total")
    )

    # 日付フィルタ
    if start and end:
        query = query.filter(Expense.date.between(start, end))

    # GROUP BY
    query = query.group_by(field)

    # 実行
    results = query.all()

    # JSON形式に変換
    data = [{group_by: value, "total": total} for value, total in results]

    return json_response(data)
