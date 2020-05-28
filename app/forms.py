from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


age_band_choices = [(None, 'Select'), ('0', '16 - 25'), ('1', '26 - 39'), ('2', '40 - 49')
    , ('3', '50 - 59'), ('4', '60 - 65'), ('5', 'Over 65')]

job_security_choices = [(None, 'Select')
    , ('0', 'Uneasy / Starting Out'), ('1', 'Unsure'), ('2', 'Stable'), ('3', 'Good'), ('4', 'Very secure')]

country_choices = [(None, 'Select')]
country_id = []
country = []

with open('./app/static/countrylist.txt', 'r') as f:
    lines = f.readlines()
    for i in range(1, len(lines)):
        x = lines[i].strip()
        country.append(x[(x.find(',')+1):])
        country_id.append(str(i))

country_list = list(zip(country_id, country))


for k in range(len(country_list)):
    country_choices.append(country_list[k])

loan_reason_choices = [(None, 'Select'), ('0', 'Debt Consolidation'), ('1', 'Car Purchase'), ('2', 'Home Improvements'),
                       ('3', 'Investment'), ('4', 'Personal Development'),
                       ('5', 'Holiday , Travel & Excursion'), ('6', 'Other Purchase')]


class AssessmentForm(FlaskForm):
    age_band = SelectField('Age Band', validators=[DataRequired()]
                           , choices=age_band_choices, default=age_band_choices[0])
    job_security = SelectField('Job Security', validators=[DataRequired()]
                               , choices=job_security_choices, default=job_security_choices[0])
    country = SelectField('Country', validators=[DataRequired()], choices=country_choices, default=country_choices[0])
    available_savings = IntegerField('Available Savings £', validators=[DataRequired()])
    monthly_income = IntegerField('Monthly Income £', validators=[DataRequired()])
    monthly_expenses = IntegerField('Monthly Expenses £', validators=[DataRequired()])
    lender = StringField('Lender', validators=[DataRequired()])
    loan_reason = SelectField('Reason for Loan', validators=[DataRequired()]
                                  , choices=loan_reason_choices, default=loan_reason_choices[0])
    loan_term = IntegerField('Loan Term', validators=[DataRequired()])
    loan_apr = FloatField('% APR', validators=[DataRequired()])
    loan_amount = IntegerField('Loan Amount £', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SummaryForm(FlaskForm):
    no_of_payments = IntegerField('Number of Payments', validators=[DataRequired()])
    monthly_capital_repayments = IntegerField('Monthly Capital Repayments £', validators=[DataRequired()])
    monthly_interest_repayments = IntegerField('Monthly Interest Repayments £', validators=[DataRequired()])
    monthly_repayments = IntegerField('Monthly Repayments £', validators=[DataRequired()])
    total_amount_payable = IntegerField('Total Amount Payable (incl. interest) £', validators=[DataRequired()])
    total_capital_payable = IntegerField('Total Capital Payable (excl. interest) £', validators=[DataRequired()])
    total_interest_payable = IntegerField('Total Interest Payable £', validators=[DataRequired()])
    new_monthly_expenses = IntegerField('New Monthly Expenses £', validators=[DataRequired()])
    new_monthly_surplus = IntegerField('New Monthly Surplus £', validators=[DataRequired()])
    submit = SubmitField('Download')
