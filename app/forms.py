from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, DecimalField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField


age_band_choices = [(None, 'Select'), ('0', '16 - 25'), ('1', '26 - 39'), ('2', '40 - 49')
    , ('3', '50 - 59'), ('4', '60 - 65'), ('5', 'Over 65')]

job_security_choices = [(None, 'Select')
    , ('0', 'Uneasy / Starting Out'), ('1', 'Unsure'), ('2', 'Stable'), ('3', 'Good'), ('4', 'Very secure')]

# country_choices = [(None, 'Select')]
country_choices = [(214, 'United Kingdom')]
country_id = []
country = []

with open('./app/static/countrylist.txt', 'r') as f:
    lines = f.readlines()
    for i in range(1, len(lines)):
        x = lines[i].strip()
        country.append(x[(x.find(',') + 1):])
        country_id.append(str(i))

country_list = list(zip(country_id, country))

for k in range(len(country_list)):
    country_choices.append(country_list[k])

loan_reason_choices = [(None, 'Select'), ('0', 'Debt Consolidation'), ('1', 'Car Purchase'), ('2', 'Home Improvements'),
                       ('3', 'Investment'), ('4', 'Personal Development'),
                       ('5', 'Holiday , Travel & Excursion'), ('6', 'Other Purchase')]
loan_term_choices = [(None, 'Select')
    , ('12', 12), ('18', 18), ('24', 24), ('36', 36), ('48', 48), ('60', 60), ('72', 72), ('84', 84)]


def lender_choices_query():
    from app.models import Lenders
    return Lenders.query


class AssessmentForm(FlaskForm):
    age_band = SelectField('Age Band', validators=[DataRequired()]
                           , choices=age_band_choices, default=age_band_choices[0])
    job_security = SelectField('Job Security', validators=[DataRequired()]
                               , choices=job_security_choices, default=job_security_choices[0])
    country = SelectField('Country', validators=[DataRequired()], choices=country_choices, default=country_choices[0])
    available_savings = DecimalField('Available Savings £', validators=[DataRequired()])
    monthly_income = DecimalField('Monthly Income £', validators=[DataRequired()])
    monthly_expenses = DecimalField('Monthly Expenses £', validators=[DataRequired()])
    lender = QuerySelectField('Lender', query_factory=lender_choices_query
                              , validators=[DataRequired()], allow_blank=True, blank_text='Select', get_label='lender')
    loan_reason = SelectField('Reason for Loan', validators=[DataRequired()]
                              , choices=loan_reason_choices, default=loan_reason_choices[0])
    loan_apr = DecimalRangeField('% Apr', places=2, validators=[DataRequired(), NumberRange(min=0.05, max=45.0)])
    loan_term = SelectField('Loan Term (mths)', validators=[DataRequired()]
                            , choices=loan_term_choices, default=loan_term_choices[0])
    loan_amount = DecimalField('Loan Amount £', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SummaryForm(FlaskForm):
    no_of_payments = IntegerField('Number of Payments', validators=[DataRequired()])
    monthly_capital_repayments = DecimalField('Monthly Capital Repayments £', validators=[DataRequired()])
    monthly_interest_repayments = DecimalField('Monthly Interest Repayments £', validators=[DataRequired()])
    monthly_repayments = DecimalField('Monthly Repayments £', validators=[DataRequired()])
    total_amount_payable = DecimalField('Total Amount Payable (incl. interest) £', validators=[DataRequired()])
    total_capital_payable = DecimalField('Total Capital Payable (excl. interest) £', validators=[DataRequired()])
    total_interest_payable = DecimalField('Total Cost of Loan £', validators=[DataRequired()])
    new_monthly_expenses = DecimalField('New Monthly Expenses £', validators=[DataRequired()])
    new_monthly_surplus = DecimalField('New Monthly Surplus £', validators=[DataRequired()])
    submit = SubmitField('Download')
