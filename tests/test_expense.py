import pytest
from budgetbook.app import app, DB_PATH


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_add_and_get_expense(client):
    # 支出登録
    payload = {
        "date": "2025-07-20",
        "shop": "コンビニ",
        "category": "食費",
        "payment": "現金",
        "amount": 450,
    }
    res = client.post("/expense", json=payload)
    assert res.status_code == 200
    assert res.get_json() == {"message": "Expense added"}

    # 支出取得
    res = client.get("/expense?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list) and len(data) == 1
    item = data[0]
    for k, v in payload.items():
        assert item[k] == v
