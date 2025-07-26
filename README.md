# 💰 BudgetBook  

シンプルな家計簿アプリ。  
Flask + SQLite で動作し、収入・支出の登録・一覧・集計が可能です。  

## 🚀 機能一覧  

- **収入・支出の登録フォーム**（Flask API 経由で保存）
- **収入・支出の一覧表示**
  - 日付順に並び、ヘッダー固定・スクロール対応
  - 10件を超えるとスクロール可能
- **期間フィルタ**
  - ダッシュボード上部のフィルタで、収入・支出をまとめて絞り込み可能
- **UI 改善**
  - フィルタボタンの位置調整
  - テーブルデザイン（ホバー時の背景色、偶数行の背景色）
- **REST API**
  - `/expense` `/income` の登録・取得
  - `/summary/...` でカテゴリや支払い方法ごとの集計取得  

---

## 🛠️ セットアップ  

### 1. 仮想環境の作成 & 有効化  

```bash
pyenv virtualenv 3.12.11 budgetbook
pyenv activate budgetbook
````

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. DB 初期化

```bash
flask shell
>>> from budgetbook.extensions import db
>>> from budgetbook.models import *
>>> db.create_all()
```

### 4. 開発サーバー起動

```bash
flask --app budgetbook.app run --debug
```

デフォルトでは **[http://127.0.0.1:5000](http://127.0.0.1:5000)** でアクセスできます。

---

## 📂 ディレクトリ構成

```
budgetbook/
├── budgetbook/
│   ├── app.py            # Flaskアプリのエントリーポイント
│   ├── extensions.py     # DBなどの拡張機能
│   ├── models.py         # DBモデル
│   ├── schemas.py        # Marshmallowスキーマ
│   ├── routes/           # APIルート
│   │   ├── expense.py
│   │   ├── income.py
│   │   └── summary.py
│   └── templates/
│       └── dashboard.html  # ダッシュボード画面
│       └── ...
├── tests/                # pytest テスト
│   ├── test_expense.py
│   ├── test_income.py
│   └── test_summary.py
├── requirements.txt
└── README.md
```

---

## ✅ テスト実行

```bash
TESTING=1 pytest -v
```

---

## ✨ 更新履歴

### 2025-07-26

* **支出・収入のフォームを実装**し、Flask API と連携
* **支出・収入一覧の表示機能を追加**（日付順に並ぶ）
* 一覧テーブルの **デザインを改善**（ヘッダー固定、スクロール対応、ホバー時の背景色追加）
* **期間フィルタ機能を追加**
  * ダッシュボード上部から **開始日/終了日を指定して収入・支出をまとめて絞り込み**可能
* UI の改善（フィルタボタンの位置や高さ調整）

---

## 📌 今後の予定

* グラフ表示（支出カテゴリ別、月ごとの推移）
* FastAPI 化の検討
* TypeScript + フロント分離版の検討
* Docker 化
