import pytest
import tempfile
import os
from budgetbook import config
from budgetbook.app import app
from budgetbook.init_db import init_db


@pytest.fixture
def client():
    # ✅ 一時ファイルDBを作成
    db_fd, db_path = tempfile.mkstemp()
    config.DB_PATH = db_path
    app.config["DB_PATH"] = db_path

    # ✅ DB初期化
    init_db()

    with app.test_client() as client:
        yield client

    # ✅ テスト終了後に削除
    os.close(db_fd)
    os.unlink(db_path)
