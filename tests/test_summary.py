def test_income_summary_group_by_category(client):
    """summary API でカテゴリごとの集計ができること"""

    # 収入を登録
    client.post(
        "/income",
        json={
            "date": "2025-07-20",
            "category": "給料",
            "amount": 5000,
        },
    )
    client.post(
        "/income",
        json={
            "date": "2025-07-10",
            "category": "賞与",
            "amount": 50000,
        },
    )

    # カテゴリごとの集計
    res = client.get("/income/summary/category?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()

    assert any(item["category"] == "給料" and item["total"] == 5000 for item in data)
    assert any(item["category"] == "賞与" and item["total"] == 50000 for item in data)


def test_expense_summary_group_by_category(client):
    """summary API でカテゴリごとの集計ができること"""

    # 収入を登録
    client.post(
        "/income",
        json={
            "date": "2025-07-10",
            "category": "給料",
            "amount": 5000,
        },
    )

    # 支出を登録
    client.post(
        "/expense",
        json={
            "date": "2025-07-11",
            "shop": "スーパー",
            "category": "食費",
            "amount": 1000,
            "payment": "現金",
        },
    )
    client.post(
        "/expense",
        json={
            "date": "2025-07-12",
            "shop": "ドラッグストア",
            "category": "日用品",
            "amount": 500,
            "payment": "カード",
        },
    )

    # カテゴリごとの集計
    res = client.get("/expense/summary/category?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()

    # 食費:1000, 日用品: 500 が含まれるはず
    assert any(item["category"] == "食費" and item["total"] == 1000 for item in data)
    assert any(item["category"] == "日用品" and item["total"] == 500 for item in data)


def test_expense_summary_group_by_payment(client):
    """summary API で支払い方法ごとの集計ができること"""

    # 支出を登録
    client.post(
        "/expense",
        json={
            "date": "2025-07-15",
            "shop": "カフェ",
            "category": "交際費",
            "amount": 800,
            "payment": "PayPay",
        },
    )
    client.post(
        "/expense",
        json={
            "date": "2025-07-31",
            "shop": "書店",
            "category": "教養",
            "amount": 1200,
            "payment": "カード",
        },
    )

    # 支払い方法ごとの集計
    res = client.get("/expense/summary/payment?start=2025-07-01&end=2025-07-31")
    assert res.status_code == 200
    data = res.get_json()

    # PayPay:800, カード: 12000 が含まれるはず
    assert any(item["payment"] == "PayPay" and item["total"] == 800 for item in data)
    assert any(item["payment"] == "カード" and item["total"] == 1200 for item in data)
