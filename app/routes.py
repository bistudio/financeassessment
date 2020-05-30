from flask import render_template, redirect, request, url_for, flash
from app.forms import AssessmentForm, SummaryForm
from app import app, db
from app.models import Assessment, Summary


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/aboutyou')
def aboutyou():
    return render_template('aboutyou.html', title='About You')


@app.route('/loaninfo')
def loaninfo():
    return render_template('loaninfo.html', title='About the loan')


@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        details = Assessment(age_band=form.age_band.data
                             , job_security=form.job_security.data
                             , country=form.country.data
                             , available_savings=form.available_savings.data
                             , monthly_income=form.monthly_income.data
                             , monthly_expenses=form.monthly_expenses.data
                             , lender=form.lender.data
                             , loan_reason=form.loan_reason.data
                             , loan_term=form.loan_term.data
                             , loan_apr=form.loan_apr.data
                             , loan_amount=form.loan_amount.data)
        db.session.add(details)
        db.session.commit()
        flash('Thank you for completing the assessment', 'success')
        return redirect(url_for('home'))
    return render_template('assessment.html', title='Assessment', form=form)


# @app.route('/summary', methods=['GET', 'POST'])
# def summary():
#     form = SummaryForm()
#     if form.submit():
#         print('Submitted')
#     if form.validated():
#         print('Validated')
#
#     print(form.errors)
#     return render_template('summary.html', title='Summary', form=form)
