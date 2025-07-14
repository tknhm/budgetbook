# budgetbook 🧾

Flask + SQLite を使ったローカル家計簿アプリです。  
自分用に作成しており、後々スマホ対応やOCR機能などの拡張も検討しています。

---

## ✅ 現在の機能（2025/7/14 時点）

### 📌 API機能
- 収入の登録（POST `/income`）
- 収入の取得（GET `/income?start=YYYY-MM-DD&end=YYYY-MM-DD`）
- 支出の登録（POST `/expense`）✅ New!
- 支出の取得（GET `/expense?start=YYYY-MM-DD&end=YYYY-MM-DD`）✅ New!

### 🗂 使用技術
- **言語**: Python 3.x
- **バックエンド**: Flask
- **データベース**: SQLite
- **仮想環境管理**: pyenv + pyenv-virtualenv
- **Git管理**: Git + GitHub
- **今後追加予定**: Chart.js（グラフ可視化）、pytest（テスト）

---

## 🚀 起動方法（pyenv使用）

### 1. Python バージョンの切り替え
```bash
pyenv local 3.12.11
````

### 2. 仮想環境の作成・有効化

```bash
pyenv virtualenv 3.12.11 budgetbook-env
pyenv local budgetbook-env
```

### 3. 必要パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. アプリの起動

```bash
python app.py
```

---

## 🛠 今後の予定（To Do）

* [ ] 月・カテゴリ・支払い方法ごとの集計API
* [ ] Chart.js を使ったグラフ表示（円グラフ・棒グラフ・サンキー図）
* [ ] HTML入力フォームの作成（Flaskテンプレート）
* [ ] OCR機能で手書き家計簿の読み取り（Tesseract + pytesseract）
* [ ] テストコードの実装（pytest）

---

## 📁 ディレクトリ構成（予定）

```
budgetbook/
├── app.py            # Flaskアプリ本体
├── templates/        # HTMLテンプレート（未実装）
├── static/           # CSS/JS/Chart.jsなど（未実装）
├── db/               # SQLiteデータベースファイル
├── tests/            # テストコード（未実装）
├── .gitignore
├── README.md
└── requirements.txt  # 必要パッケージ一覧
```
