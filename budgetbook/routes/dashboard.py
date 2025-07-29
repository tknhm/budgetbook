from flask import Blueprint, render_template, request
from budgetbook.services.summary import get_payment_method_summary

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
