from app import db
from datetime import datetime as dt
from decimal import Decimal as D
import sqlalchemy.types as types


class SqliteNumeric(types.TypeDecorator):
    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return round(D(value), 2)


class SqliteDecimal(types.TypeDecorator):
    # This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
    # from Python to Integers which is later stored in Sqlite database.
    impl = types.Integer

    def __init__(self, scale):
        # It takes a 'scale' parameter, which specifies the number of digits
        # to the right of the decimal point of the number in the column.
        types.TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(self, value, dialect):
        # e.g. value = Column(SqliteDecimal(2)) means a value such as
        # Decimal('12.34') will be converted to 1234 in Sqlite
        if value is not None:
            value = int(D(value) * self.multiplier_int)
        return value

    def process_result_value(self, value, dialect):
        # e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None:
            value = D(value) / self.multiplier_int
        return value


Numeric = SqliteNumeric
Decimal = SqliteDecimal


class Assessment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    age_band = db.Column(db.String(10), nullable=False)
    job_security = db.Column(db.String(10), nullable=False)
    country = db.Column(db.SmallInteger, nullable=False)
    available_savings = db.Column(Numeric(18, 2), nullable=False)
    monthly_income = db.Column(Numeric(18, 2), nullable=False)
    monthly_expenses = db.Column(Numeric(18, 2), nullable=False)
    loan_reason = db.Column(db.String(10), nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    loan_apr = db.Column(Numeric(2, 5), nullable=False)
    loan_amount = db.Column(Numeric(18, 2), nullable=False)
    monthly_capital_repayments = db.Column(Numeric(18, 2), nullable=False)
    monthly_interest_repayments = db.Column(Numeric(18, 2), nullable=False)
    monthly_repayments = db.Column(Numeric(18, 2), nullable=False)
    total_amount_payable = db.Column(Numeric(18, 2), nullable=False)
    total_capital_payable = db.Column(Numeric(18, 2), nullable=False)
    total_interest_payable = db.Column(Numeric(18, 2), nullable=False)
    new_monthly_expenses = db.Column(Numeric(18, 2), nullable=False)
    new_monthly_surplus = db.Column(Numeric(18, 2), nullable=False)
    loan_reason_score = db.Column(db.Float(asdecimal=True, precision=2, decimal_return_scale=2), nullable=False)
    loan_term_score = db.Column(db.Float(asdecimal=True, precision=2, decimal_return_scale=2), nullable=False)
    final_decision = db.Column(db.String(6), nullable=True)
    lender_id = db.Column(db.Integer, db.ForeignKey('lenders.id'), nullable=False)
    # providers = db.relationship('Lenders', backref='assessment', lazy=True)
    assessment_datetime = db.Column(db.DATETIME, nullable=False, default=dt.utcnow)

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
               f",'{self.total_interest_payable}'" \
               f",'{self.loan_reason_score}'" \
               f",'{self.loan_term_score}'"


class STGMFHistoricalAprRates(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    loan_term = db.Column(db.SMALLINT, nullable=False)
    loan_amount = db.Column(Numeric(18, 0), nullable=False)
    loan_provider = db.Column(db.String(255), nullable=False)
    loan_product = db.Column(db.String(60), nullable=False)
    average_apr_rate = db.Column(db.Float(precision=2, asdecimal=True, decimal_return_scale=2), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    date_extracted = db.Column(db.DATETIME, nullable=False)

    def __init__(self, loan_term, loan_amount, loan_provider, loan_product, average_apr_rates, source, date_extracted):
        self.id = id
        self.loan_term = loan_term
        self.loan_amount = loan_amount
        self.loan_provider = loan_provider
        self.loan_product = loan_product
        self.average_apr_rate = average_apr_rates
        self.source = source
        self.date_extracted = date_extracted

    def __str__(self):
        return 'MoneyFactsAprRates(id=' + str(self.id) + ', lender=' + self.lender + ')'

    def __repr__(self):
        return f'"{self.loan_provider}", {self.loan_term}' \
               f', {self.loan_amount},{self.average_apr_rate}'


class Lenders(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    lender = db.Column(db.String(255), nullable=False)
    assessment = db.relationship('Assessment', backref='loan_provider', lazy='select')  # lazy values (dynamic, select,

    # subquery, joined)

    def __init__(self, lender):
        self.id = id
        self.lender = lender

    def __str__(self):
        return f'{self.lender}'

    def __repr__(self):
        return {id: self.id, 'lender': self.lender}
