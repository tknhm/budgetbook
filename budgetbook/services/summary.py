from budgetbook.models import Expense
from sqlalchemy import extract
from collections import defaultdict
from datetime import datetime
from budgetbook.extensions import db


def get_payment_method_summary():
    summary = defaultdict(lambda: defaultdict(int))
    expenses = db.session.query(Expense).all()

    for exp in expenses:
        year_monthh = exp.date.strftime("%Y-%m")
        summary[exp.payment][year_monthh] += exp.amount

    # そーとしてリストに整形する
    sorted_summary = {
        payment: dict(sorted(months.items())) for payment, months in summary.items()
    }

    return sorted_summary
