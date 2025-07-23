import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from budgetbook.routes.income import income_bp
from budgetbook.routes.expense import expense_bp
from budgetbook.routes.summary import summary_bp
from budgetbook.extensions import db, ma

app = Flask(__name__)

# デフォルトのDBパス
default_db_path = os.environ.get("DB_PATH", "budgetbook.db")

# SQLite 接続設定
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{default_db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# テストモード判定
if os.environ.get("TESTING") == "1":
    app.config["TESTING"] = True

db.init_app(app)
ma.init_app(app)

# Blueprint 登録
app.register_blueprint(income_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(summary_bp)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
