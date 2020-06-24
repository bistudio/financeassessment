from flask import render_template, redirect, request, url_for, flash
from app.forms import AssessmentForm, SummaryForm
from app import app, db
from app.models import Assessment


@app.route('/')
@app.route('/home')
def home():
    assessment = Assessment.query.all()
    return render_template('home.html', title='Home', assessment=assessment)


@app.route('/aboutyou')
def aboutyou():
    return render_template('aboutyou.html', title='About You')


@app.route('/loaninfo')
def loaninfo():
    return render_template('loaninfo.html', title='About the loan')


global assessment_id


@app.route('/assessment', methods=['GET', 'POST'])
def assessment():

    form = AssessmentForm()
    if form.validate_on_submit():
        rate = (form.loan_apr.data / 100 / 12)
        monthly_repayments = round(
            (form.loan_amount.data * (rate)) / (1 - (1 + (rate)) ** (-1 * int(form.loan_term.data))), 2)
        initial_month_interest = round(form.loan_amount.data * rate, 2)
        initial_month_capital = round(monthly_repayments - initial_month_interest, 2)

        def loan_reason_score(i):
            switcher = {
                '0': 3
                , '1': 2.5
                , '2': 3
                , '3': 2
                , '4': 4
                , '5': 3
                , '6': 2.5
            }
            return switcher.get(i, 0)

        def loan_term_score(d, i):
            if int(d) < 37:
                i = '0'  # 2
            elif int(d) < 73:
                i = '1'  # 3.5
            else:
                i = '2'  # 2
            switcher = {
                '0': 2
                , '1': 3.5
                , '2': 2

            }

            return switcher.get(i, 0)

        details = Assessment(age_band=form.age_band.data
                             , job_security=form.job_security.data
                             , country=form.country.data
                             , available_savings=form.available_savings.data
                             , monthly_income=form.monthly_income.data
                             , monthly_expenses=form.monthly_expenses.data
                             , lender=form.lender.data
                             , loan_reason=form.loan_reason.data
                             , loan_term=int(form.loan_term.data)
                             , loan_apr=form.loan_apr.data
                             , loan_amount=form.loan_amount.data
                             , monthly_repayments=monthly_repayments
                             , monthly_interest_repayments=initial_month_interest
                             , monthly_capital_repayments=initial_month_capital
                             , total_amount_payable=monthly_repayments * int(form.loan_term.data)
                             , total_interest_payable=(monthly_repayments * int(form.loan_term.data))
                                                      - form.loan_amount.data
                             , new_monthly_expenses=form.monthly_expenses.data + monthly_repayments
                             , new_monthly_surplus=0.00
                             , total_capital_payable=initial_month_capital * int(form.loan_term.data)
                             , loan_reason_score=loan_reason_score(form.loan_reason.data)
                             , loan_term_score=loan_term_score(form.loan_term.data, 0)
                             )

        db.session.add(details)
        db.session.commit()
        assessment_id = details.id
        flash('Thank you for completing the assessment', 'success')
        assessment = Assessment.query.get_or_404(assessment_id)
        return render_template('summary.html', title='Assessment Summary', assessment=assessment)
        # return redirect(url_for('summary', assessment_id=details.id))
    return render_template('assessment.html', title='Assessment', form=form)
