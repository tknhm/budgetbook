import pytest
from budgetbook.app import app, db
from budgetbook.db import init_db


@pytest.fixture
def client(tmp_path):
    # ✅ テスト専用のDBパスに切り替え
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    app.config["TESTING"] = True

    # ✅ Flaskアプリケーションコンテキストを使う
    with app.app_context():
        init_db(drop=True)  # ← ここがコンテキスト内

    # ✅ テストクライアントもコンテキスト内で作る
    with app.test_client() as client:
        yield client

    # ✅ 終了後にDBセッション削除
    with app.app_context():
        db.session.remove()
        db.drop_all()
