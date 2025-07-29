from budgetbook.extensions import ma
from marshmallow import fields, validate, Schema


class IncomeSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    category = fields.Str(required=True)
    amount = fields.Int(required=True, validate=validate.Range(min=1))


income_schema = IncomeSchema()
incomes_schema = IncomeSchema(many=True)


class ExpenseSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    shop = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True)
    amount = fields.Int(required=True, validate=validate.Range(min=1))
    payment = fields.Str(
        required=True, validate=validate.OneOf(["現金", "カード", "PayPay", "ルミネカード"])
    )


expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)


# カテゴリ別集計用
class SummaryCategorySchema(Schema):
    category = fields.Str(required=True)
    total = fields.Int(required=True)


# 支払い方法別集計用
class SummaryPaymentSchema(Schema):
    payment = fields.Str(required=True)
    total = fields.Int(required=True)


summary_category_schema = SummaryCategorySchema(many=True)
summary_payment_schema = SummaryPaymentSchema(many=True)
