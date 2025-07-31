from flask import Blueprint, request, Response
from budgetbook.models import Income, Expense
from sqlalchemy import func, extract
from budgetbook.extensions import db
from collections import defaultdict
from datetime import datetime
import json

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


@summary_bp.route("/monthly-summary")
def monthly_summary():
    income_data = (
        db.session.query(
            extract("year", Income.date).label("year"),
            extract("month", Income.date).label("month"),
            func.sum(Income.amount).label("total_income"),
        )
        .group_by("year", "month")
        .all()
    )

    expense_data = (
        db.session.query(
            extract("year", Expense.date).label("year"),
            extract("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total_expense"),
        )
        .group_by("year", "month")
        .all()
    )

    summary = defaultdict(lambda: {"income": 0, "expense": 0})

    for year, month, total in income_data:
        key = f"{int(year)}-{int(month):02d}"
        summary[key]["income"] = total

    for year, month, total in expense_data:
        key = f"{int(year)}-{int(month):02d}"
        summary[key]["expense"] = total

    # 並び順を確定
    sorted_summary = dict(sorted(summary.items()))

    return Response(json.dumps(sorted_summary, ensure_ascii=False))


@summary_bp.route("/asset-trend")
def asset_trend():
    income_data = (
        db.session.query(
            extract("year", Income.date).label("year"),
            extract("month", Income.date).label("month"),
            func.sum(Income.amount).label("total_income"),
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    cumulative = 0
    trend = []
    for year, month, total in income_data:
        cumulative += total
        label = f"{int(year)}-{int(month):02d}"
        trend.append({"month": label, "total": cumulative})

    return Response(json.dumps(trend, ensure_ascii=False))
