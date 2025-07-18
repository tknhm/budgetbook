# budgetbook

家計簿管理アプリ（Flask + SQLite）。  
ローカルで動作し、収入・支出の登録、期間ごとの集計、可視化が可能です。  
将来的にはスマホ対応やOCR読み取り機能も追加予定。

---

## ✅ セットアップ

```bash
git clone https://github.com/tknhm/budgetbook.git
cd budgetbook
pyenv local 3.12.x  # 任意のバージョン
pip install -r requirements.txt
````

---

## ✅ データベース初期化

ローカル開発用DB:

```bash
python -m budgetbook.init_db
```

テスト用DB:

```bash
TESTING=1 python -m budgetbook.init_db
```

---

## ✅ サーバ起動

```bash
flask --app budgetbook.app run --debug
```

API例:

```bash
curl -X POST "http://127.0.0.1:5000/income" \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-07-16","category":"給料","amount":300000}'
```

---

## 🧪 テスト

このプロジェクトは `pytest` を利用して自動テストを行っています。  
テスト実行時は **本番DB(`budgetbook.db`) ではなく、一時ファイルのSQLite DB** を使うため、  
ローカルデータを汚す心配はありません。

### 実行方法

```bash
# 1. 依存パッケージが入っていない場合はインストール
pip install -r requirements.txt

# 2. テストを実行
pytest -v --cov=budgetbook --cov-report=term-missing
````

✅ **テスト時のポイント**

* `tests/conftest.py` がテスト用の一時ファイルDBを作成し、`init_db()` で初期化します
* `init_db()` は `current_app.config["DB_PATH"]` を見てDBを作るので、
  テスト・開発・本番で別のDBを使えます
* テスト終了後、一時ファイルDBは削除されます

---

### CI/CD（GitHub Actions）

GitHub Actions でもテストが実行されます。
CI環境でも同じく一時ファイルDBが使われるので、
PR や main ブランチの変更でもローカルDBは影響を受けません。

---

## ✅ DBの動作環境

| 環境    | DBの種類      | パス                              |
| ----- | ---------- | ------------------------------- |
| ローカル  | SQLiteファイル | `budgetbook/db/budgetbook.db`   |
| テスト   | 一時ファイルDB   | `tempfile.mkstemp()` で作られ、終了後削除 |
| CI/CD | 一時ファイルDB   | GitHub Actions 内の一時ディレクトリ       |

---

## ✅ これまでの改善点

* `init_db()` が `current_app.config["DB_PATH"]` を参照するようになり、環境ごとにDB切替が可能
* `pytest` のテストDBは一時ファイルに自動切替
* `conftest.py` がアプリケーションコンテキスト内でDBを初期化
* CI/CDでもローカルと同じ手順で動作


---

### 異常系テストについて

`tests/test_api.py` には、APIの正常系だけでなく **異常系テスト** も追加しています。
例:

```python
def test_income_post_invalid_data(client):
    res = client.post(
        "/income",
        json={"date": "", "category": "給料", "amount": 300000}
    )
    assert res.status_code == 400
```

異常系テストを追加し、バリデーションが正しく動作するか確認します。

---

## ✅ GitHub Actions (CI)

本プロジェクトは GitHub Actions による自動テストを実行しています。
CIの設定ファイルは `.github/workflows/ci.yml` にあり、以下を実行します：

* Pythonセットアップ
* 依存関係インストール
* **テスト用DB初期化 (`TESTING=1 python -m budgetbook.init_db`)**
* `pytest` による自動テスト

push や PR 時に自動でテストが走ります ✅

---

## ✅ 今後の開発タスク

* [ ] APIの異常系テスト拡充（income, expense, summary）
* [ ] バリデーション強化
* [ ] 集計APIの詳細テスト
* [ ] 可視化グラフ（棒/円/サンキー図）の実装
* [ ] OCR入力機能（低優先度）

## 🗂 タスク管理
GitHub Projectsでタスクを管理しています  
→ [開発タスクボード](https://github.com/users/tknhm/projects/2)

---

## ✅ 参考

* [Flask ドキュメント](https://flask.palletsprojects.com/)
* [pytest ドキュメント](https://docs.pytest.org/)
* [GitHub Actions ワークフロー](https://docs.github.com/ja/actions)
