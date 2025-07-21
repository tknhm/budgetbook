from flask import Blueprint, request
from budgetbook.models import Income, Expense
from sqlalchemy import func
from budgetbook.extensions import db

summary_bp = Blueprint("summary", __name__)


def apply_date_filter(query, start, end):
    """共通の期間フィルタ"""
    if start:
        query = query.filter(Expense.date >= start)
    if end:
        query = query.filter(Expense.date <= end)
    return query


@summary_bp.route("/income/summary/category", methods=["GET"])
def income_summary_by_category():
    """カテゴリ別の収入集計"""
    start = request.args.get("start")
    end = request.args.get("end")

    query = db.session.query(Income.category, func.sum(Income.amount).label("total"))
    if start:
        query = query.filter(Income.date >= start)
    if end:
        query = query.filter(Income.date <= end)
    query = query.group_by(Income.category)

    result = [{"category": category, "total": total} for category, total in query.all()]
    return result, 200


@summary_bp.route("/expense/summary/category", methods=["GET"])
def expense_summary_by_category():
    """カテゴリ別の支出集計"""
    start = request.args.get("start")
    end = request.args.get("end")

    query = db.session.query(Expense.category, func.sum(Expense.amount).label("total"))
    query = apply_date_filter(query, start, end)
    query = query.group_by(Expense.category)

    result = [{"category": category, "total": total} for category, total in query.all()]
    return result, 200


@summary_bp.route("/expense/summary/payment", methods=["GET"])
def expense_summary_by_payment():
    """カテゴリ別の支出集計"""
    start = request.args.get("start")
    end = request.args.get("end")

    query = db.session.query(Expense.payment, func.sum(Expense.amount).label("total"))
    query = apply_date_filter(query, start, end)
    query = query.group_by(Expense.payment)

    result = [{"payment": payment, "total": total} for payment, total in query.all()]
    return result, 200
