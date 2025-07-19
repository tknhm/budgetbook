import pytest


# 正常系
def test_expense_post_and_get(client):
    """支出APIの正常系テスト"""
    res = client.post(
        "/expense",
        json={
            "date": "2025-07-18",
            "shop": "スーパー",
            "category": "食費",
            "amount": 1500,
            "payment": "現金",
        },
    )
    assert res.status_code == 201

    # GET で取得確認
    res_get = client.get("/expense?start=2025-07-01&end=2025-07-31")
    assert res_get.status_code == 200
    data = res_get.get_json()
    assert any(item["category"] == "食費" and item["amount"] == 1500 for item in data)


# 異常系
@pytest.mark.parametrize(
    "payload",
    [
        # 金額が文字列
        {
            "date": "2025-07-18",
            "shop": "スーパー",
            "category": "食費",
            "amount": "abc",
            "payment": "現金",
        },
        # 日付が空
        {
            "date": "",
            "shop": "スーパー",
            "category": "食費",
            "amount": 1000,
            "payment": "カード",
        },
        # 店名がない
        {
            "date": "2025-07-18",
            "category": "食費",
            "amount": 1000,
            "payment": "PayPay",
        },
    ],
)
def test_expense_post_invalid_data(client, payload):
    """支出APIの異常系テスト"""
    res = client.post("/expense", json=payload)
    assert res.status_code == 400
