import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# デフォルトはTESTING環境変数で切り替え
if os.getenv("TESTING") == "1":
    DB_PATH = os.path.join(BASE_DIR, "db", "budgetbook_test.db")
else:
    DB_PATH = os.path.join(BASE_DIR, "db", "budgetbook.db")
