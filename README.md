# budgetbook

家計簿管理アプリ（Flask + SQLite）。  
ローカルで動作し、収入・支出の登録、期間ごとの集計、可視化が可能です。  
将来的にはスマホ対応やOCR読み取り機能も追加予定。

---

## ✅ セットアップ

```bash
git clone https://github.com/<yourname>/budgetbook.git
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

## ✅ テスト

### テスト実行（ローカル）

テストは `pytest` を使用しています。
**テスト専用DB** を使うため、環境変数 `TESTING=1` を指定してください。

```bash
# テストDB初期化
TESTING=1 python -m budgetbook.init_db

# テスト実行
TESTING=1 pytest -v
```

テストカバレッジも確認できます：

```bash
TESTING=1 pytest --cov=budgetbook --cov-report=term-missing
```

HTMLレポートを生成したい場合：

```bash
TESTING=1 pytest --cov=budgetbook --cov-report=html
open htmlcov/index.html
```

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

```
