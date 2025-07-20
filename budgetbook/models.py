from budgetbook.extensions import db


class Income(db.Model):
    __tablename__ = "income"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)


class Expense(db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    shop = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment = db.Column(db.String)
