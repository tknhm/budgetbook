from budgetbook.extensions import db


def init_db(drop=False):
    """DB初期化。drop=Trueなら既存テーブル削除"""
    from budgetbook.models import Income, Expense  # モデル読み込み

    if drop:
        db.drop_all()
    db.create_all()
    print(f"✅ Initialized DB → {db.engine.url}")
