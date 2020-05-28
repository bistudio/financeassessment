from flask import render_template, redirect, request, url_for, flash
from app.forms import AssessmentForm, SummaryForm
from app import app


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
    print(form.errors)
    if form.validate_on_submit():
        flash('Thank you for completing the assessment', 'success')
        return redirect(url_for('summary'))
    return render_template('assessment.html', title='Assessment', form=form)


@app.route('/summary', methods=['GET', 'POST'])
def summary():
    return render_template('summary.html', title='Summary')
