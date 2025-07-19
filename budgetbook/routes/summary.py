from flask import Blueprint, request
from budgetbook.db import get_db_connection
from budgetbook.utils.response import json_response
from budgetbook.utils.validators import is_valid_date

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

    conn = get_db_connection()
    rows = conn.execute(
        f"SELECT {group_by}, SUM(amount) AS total FROM expense WHERE date BETWEEN ? AND ? GROUP BY {group_by}",
        (start, end),
    ).fetchall()
    conn.close()

    result = [{group_by: row[group_by], "total": row["total"]} for row in rows]
    return json_response(result)
