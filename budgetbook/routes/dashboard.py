from flask import Blueprint, render_template, request, Response
from budgetbook.services.summary import get_payment_method_summary
from budgetbook.models import Expense, Income
import json

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    summary = get_payment_method_summary()

    # 集計時に使っている全ての月を収集
    all_months = set()
    for data in summary.values():
        all_months.update(data.keys())
    sorted_months = sorted(all_months)

    return render_template(
        "dashboard.html",
        payment_summary=summary,
        months=sorted_months,
    )


def get_sankey_data():
    # ノード名をユニークに集める
    income_sources = [i.category for i in Income.query.all()]
    expense_categories = [e.category for e in Expense.query.all()]
    payment_methods = [e.payment for e in Expense.query.all()]

    nodes = list(set(income_sources + expense_categories + payment_methods))

    links = []

    # 収入　→ 支出カテゴリ（仮のロジック）
    for inc in Income.query.all():
        for cat in expense_categories:
            if inc.category == cat:
                links.append(
                    {
                        "source": nodes.index(inc.category),
                        "target": nodes.index(cat),
                        "value": inc.amount,
                    }
                )

    # 支出カテゴリ　→ 支払い方法
    for exp in Expense.query.all():
        links.append(
            {
                "source": nodes.index(exp.category),
                "target": nodes.index(exp.payment),
                "value": exp.amount,
            }
        )

    return {"nodes": nodes, "links": links}


@dashboard_bp.route("/sankey-data")
def sankey_data():
    # start = request.args.get("start")
    # end = request.args.get("end")

    # query = """
    #     SELECT i.category AS income_cat, e.category AS expense_cat, SUM(e.amount) AS amount
    #     FROM income i
    #     JOIN expense e ON DATE(i.date) = DATE(e.date)
    #     WHERE 1=1
    # """
    data = get_sankey_data()
    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )
