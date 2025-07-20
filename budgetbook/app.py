import os
from flask import Flask
from budgetbook.config import DB_PATH
from budgetbook.routes.income import income_bp
from budgetbook.routes.expense import expense_bp
from budgetbook.routes.summary import summary_bp
from budgetbook.db import get_db, close_db

app = Flask(__name__)

# デフォルト設定
app.config.from_mapping(
    DB_PATH=os.environ.get("DB_PATH", "budgetbook.db"),
    TESTING=False,
)


# リクエスト終了時にDBを閉じる
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


# Blueprint 登録
app.register_blueprint(income_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(summary_bp)

if __name__ == "__main__":
    app.run(debug=True)
