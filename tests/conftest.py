import pytest
from budgetbook.app import app
from budgetbook.init_db import init_db


@pytest.fixture
def client(tmp_path):
    # ✅ テスト専用のDBファイルを一時ディレクトリに作る
    db_path = tmp_path / "test.db"

    # ✅ Flaskの設定をテスト用に上書き
    app.config.update(TESTING=True, DB_PATH=str(db_path))  # ← これが重要  # 一時DBに切り替え

    # ✅ 毎回テーブルをDROPして初期化する
    init_db()

    # ✅ テストクライアントを返す
    with app.test_client() as client:
        yield client
