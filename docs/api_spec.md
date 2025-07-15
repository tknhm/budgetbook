# budgetbook API仕様書

---

## ✅ 概要
budgetbook は Flask + SQLite を用いた家計簿アプリです。  
現状のAPIは **収入・支出の登録/取得** および **支出の集計** をサポートしています。

---

## 1. 収入の登録

### エンドポイント
`POST /income`

---

### リクエストJSON

```json
{
  "date": "2025-07-13",
  "category": "給料",
  "amount": 250000
}
````

---

### レスポンス例

```json
{
  "message": "Income added"
}
```

---

## 2. 収入の取得

### エンドポイント

`GET /income`

---

### クエリパラメータ

| パラメータ   | 必須 | 説明                   |
| ------- | -- | -------------------- |
| `start` | ✅  | 期間開始日 (`YYYY-MM-DD`) |
| `end`   | ✅  | 期間終了日 (`YYYY-MM-DD`) |

---

### リクエスト例

```bash
GET /income?start=2025-07-01&end=2025-07-31
```

---

### レスポンス例

```json
[
  { "id": 1, "date": "2025-07-10", "category": "給料", "amount": 250000 },
  { "id": 2, "date": "2025-07-15", "category": "副収入", "amount": 10000 }
]
```

---

## 3. 支出の登録

### エンドポイント

`POST /expense`

---

### リクエストJSON

```json
{
  "date": "2025-07-13",
  "shop": "スーパーA",
  "category": "食費",
  "payment": "PayPay",
  "amount": 1500
}
```

---

### レスポンス例

```json
{
  "message": "Expense added"
}
```

---

## 4. 支出の取得

### エンドポイント

`GET /expense`

---

### クエリパラメータ

| パラメータ   | 必須 | 説明                   |
| ------- | -- | -------------------- |
| `start` | ✅  | 期間開始日 (`YYYY-MM-DD`) |
| `end`   | ✅  | 期間終了日 (`YYYY-MM-DD`) |

---

### リクエスト例

```bash
GET /expense?start=2025-07-01&end=2025-07-31
```

---

### レスポンス例

```json
[
  { "id": 1, "date": "2025-07-13", "shop": "スーパーA", "category": "食費", "payment": "PayPay", "amount": 1500 },
  { "id": 2, "date": "2025-07-14", "shop": "バス", "category": "交通費", "payment": "現金", "amount": 300 }
]
```

---

## 5. 支出の集計（カテゴリ別・支払い方法別）

### エンドポイント

`GET /expense/summary`

---

### クエリパラメータ

| パラメータ      | 必須 | 説明                       |
| ---------- | -- | ------------------------ |
| `start`    | ✅  | 期間開始日 (`YYYY-MM-DD`)     |
| `end`      | ✅  | 期間終了日 (`YYYY-MM-DD`)     |
| `group_by` | ✅  | `category` または `payment` |

---

### リクエスト例

```bash
GET /expense/summary?start=2025-07-01&end=2025-07-31&group_by=category
```

---

### レスポンス例

```json
[
  { "category": "食費", "total": 25000 },
  { "category": "交通費", "total": 8000 }
]
```

---

## TODO

* [ ] 収入も含めた月次サマリーAPI `/summary/monthly`
* [ ] カテゴリ・月ごとのグラフ描画用データ出力API
* [ ] テストコード（pytest）追加
