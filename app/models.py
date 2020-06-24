from app import db


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    age_band = db.Column(db.String(10), nullable=False)
    job_security = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(10), nullable=False)
    available_savings = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    monthly_income = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    monthly_expenses = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    lender = db.Column(db.String(100), nullable=True)
    loan_reason = db.Column(db.String(10), nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    loan_apr = db.Column(db.Float(precision=2, asdecimal=True, decimal_return_scale=5), nullable=False)
    loan_amount = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=0), nullable=False)
    monthly_capital_repayments = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    monthly_interest_repayments = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    monthly_repayments = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    total_amount_payable = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    total_capital_payable = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    total_interest_payable = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    new_monthly_expenses = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    new_monthly_surplus = db.Column(db.Float(precision=18, asdecimal=True, decimal_return_scale=2), nullable=False)
    loan_reason_score = db.Column(db.Float(precision=5, asdecimal=True, decimal_return_scale=2), nullable=False)
    loan_term_score = db.Column(db.Float(precision=5, asdecimal=True, decimal_return_scale=2), nullable=False)

    def __repr__(self):
        return f" '{self.id}'" \
               f", '{self.available_savings}'" \
               f", '{self.monthly_income}'" \
               f", '{self.monthly_expenses}'" \
               f",'{self.loan_term}'" \
               f",'{self.loan_apr}'" \
               f",'{self.loan_amount}'" \
               f",'{self.monthly_repayments}'" \
               f",'{self.monthly_repayments}'" \
               f",'{self.total_amount_payable}'" \
               f",'{self.total_interest_payable}'"


