# budgetbook/utils/validators.py
from datetime import datetime


def is_valid_amount(value) -> bool:
    """数値に変換できればOK"""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def is_valid_date(value: str) -> bool:
    """YYYY-MM-DD形式の日付かチェック"""
    if not value or not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
