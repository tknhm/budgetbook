import pytest
from budgetbook.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def seed_expenses(client):
    samples = [
        {
            "date": "2025-07-01",
            "shop": "A",
            "category": "食費",
            "payment": "現金",
            "amount": 100,
        },
        {
            "date": "2025-07-03",
            "shop": "B",
            "category": "交通費",
            "payment": "PayPay",
            "amount": 200,
        },
        {
            "date": "2025-07-05",
            "shop": "C",
            "category": "食費",
            "payment": "現金",
            "amount": 300,
        },
    ]
    for s in samples:
        client.post("/expense", json=s)


def test_summary_by_category(client):
    seed_expenses(client)
    res = client.get(
        "/expense/summary?start=2025-07-01&end=2025-07-31&group_by=category"
    )
    assert res.status_code == 200
    data = res.get_json()
    # 食費 100+300=400, 交通費 200
    assert {"category": "食費", "total": 400} in data
    assert {"category": "交通費", "total": 200} in data


def test_summary_by_payment(client):
    seed_expenses(client)
    res = client.get(
        "/expense/summary?start=2025-07-01&end=2025-07-31&group_by=payment"
    )
    assert res.status_code == 200
    data = res.get_json()
    # 現金 100+300=400, PayPay 200
    assert {"payment": "現金", "total": 400} in data
    assert {"payment": "PayPay", "total": 200} in data


def test_summary_missing_params(client):
    res = client.get("/expense/summary?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 400
    assert "error" in res.get_json()
