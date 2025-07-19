# budgetbook

ローカル環境で動作するシンプルな家計簿アプリです。
**収入・支出の登録、期間ごとの集計、カテゴリや支払い方法ごとの可視化**をサポートします。

今後はスマホ対応やOCR入力機能も視野に入れています。

---

## ✅ 機能概要

* **収入管理**

  * 日付・カテゴリ・金額の登録
* **支出管理**

  * 日付・店名・カテゴリ・金額・支払い方法（現金/カード/PayPayなど）の登録
* **集計**

  * 月ごとや任意期間のカテゴリ別・支払い方法別の集計
  * 将来的には棒グラフ・円グラフ・サンキー図で可視化予定
* **API 提供**

  * `/income`, `/expense` でデータ登録
  * `/expense/summary` で期間集計

---

## ✅ プロジェクト構成

```
budgetbook/
├── budgetbook/
│   ├── __init__.py
│   ├── app.py               # Flaskメインアプリ
│   ├── config.py            # DBパスなど環境ごとの設定
│   ├── init_db.py           # DB初期化スクリプト
│   ├── routes/
│   │   ├── income.py        # 収入API
│   │   ├── expense.py       # 支出API
│   │   └── summary.py       # 集計API
│   └── db/                  # SQLite DBファイル保存先
├── tests/
│   ├── conftest.py          # pytest の共通設定(DB切替)
│   ├── test_income.py       # 収入APIのテスト
│   ├── test_expense.py      # 支出APIのテスト
│   └── test_summary.py      # 集計APIのテスト
├── requirements.txt         # 依存パッケージ
├── pytest.ini               # pytest設定
└── README.md
```

---

## ✅ セットアップ

```bash
git clone https://github.com/あなたのユーザ名/budgetbook.git
cd budgetbook

# Python環境（pyenv推奨）
pyenv install 3.12.x
pyenv virtualenv 3.12.x budgetbook
pyenv activate budgetbook

# 依存ライブラリをインストール
pip install -r requirements.txt

# DB初期化
python -m budgetbook.init_db
```

アプリ起動は

```bash
flask --app budgetbook.app run
```

---

## ✅ テスト

### 実行方法

```bash
pytest -v --cov=budgetbook --cov-report=term-missing
```

✅ **テスト時はローカルDB(`budgetbook.db`)ではなく、一時ファイルDBを自動で使用するので安全です。**

* `tests/conftest.py` がテスト用の一時ファイルDBを作成し、`init_db()` で初期化
* 終了後、自動で削除されます
* CI/CD(GitHub Actions)でも同じ手順で実行されます

---

### 実装済みテスト

* `tests/test_income.py`

  * `/income` の正常系・異常系
* `tests/test_expense.py`

  * `/expense` の正常系・異常系
* `tests/test_summary.py`

  * `/expense/summary` のカテゴリ別・支払い方法別の集計

---

### カバレッジ確認

```bash
pytest --cov=budgetbook --cov-report=term-missing
```

例:

```
budgetbook/app.py            65     12    82%   50-60
budgetbook/routes/summary.py 20      0   100%
```

---

## ✅ CI/CD

GitHub Actions で `pytest` が自動実行されます。
PR や main ブランチの変更時に自動テスト＆カバレッジ確認が走ります。

---

## ✅ 今後の予定

* ✅ 収入・支出・集計APIの完成
* ✅ pytest + GitHub Actions CI/CD整備
* ⬜ グラフ可視化（棒グラフ・円グラフ・サンキー図）
* ⬜ OCRによる手書き家計簿の読み込み
* ⬜ スマホ対応UI

---

## ✅ 技術スタック

* Python 3.12 + Flask
* SQLite (ローカルDB)
* pytest + coverage
* GitHub Actions (CI)
