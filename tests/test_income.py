import pytest
from budgetbook.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_income_post_and_get(client):
    # POST
    res = client.post(
        "/income",
        json={
            "date": "2025-07-16",
            "category": "テスト給料",
            "amount": 1234,
        },
    )
    assert res.status_code == 200

    # GET
    res = client.get("/income?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()

    # 追加したデータが含まれていることを確認
    assert any(item["category"] == "テスト給料" for item in data)


def test_income_post_invalid_data(client):
    # 金額が文字列 -> 400エラーになるはず
    res = client.post(
        "/income",
        json={"date": "2025-07-16", "category": "テスト給料", "amount": "abc"},
    )
    assert res.status_code == 400

    # 日付が空 -> 400エラー
    res = client.post(
        "/income",
        json={"date": "", "category": "テスト給料", "amount": 1234},
    )
    assert res.status_code == 400
