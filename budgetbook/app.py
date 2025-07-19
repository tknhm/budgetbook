from flask import Flask
from budgetbook.config import DB_PATH
from budgetbook.routes.income import income_bp
from budgetbook.routes.expense import expense_bp
from budgetbook.routes.summary import summary_bp

app = Flask(__name__)
app.config["DB_PATH"] = DB_PATH

# Blueprint 登録
app.register_blueprint(income_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(summary_bp)

if __name__ == "__main__":
    app.run(debug=True)
