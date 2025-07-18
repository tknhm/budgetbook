import pytest


# 正常系
def test_income_post_and_get(client):
    """収入APIの正常系テスト"""
    # POST
    res = client.post(
        "/income",
        json={
            "date": "2025-07-16",
            "category": "給料",
            "amount": 3000,
        },
    )
    assert res.status_code == 201

    # GET
    res = client.get("/income?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) > 0
    assert data[0]["category"] == "給料"


# 異常系
@pytest.mark.parametrize(
    "payload",
    [
        {"date": "2025-07-16", "category": "給料", "amount": "abc"},
        {"date": "", "category": "給料", "amount": 1234},
        {"date": "2025-07-16", "amount": 1234},
    ],
)
def test_income_post_invalid_data(client, payload):
    """収入APIの異常系テスト"""
    # 金額が文字列 -> 400エラーになるはず
    res = client.post(
        "/income",
        json=payload,
    )
    assert res.status_code == 400
