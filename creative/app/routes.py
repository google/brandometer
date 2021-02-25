from flask import render_template, request, flash, redirect, url_for
from app import app
from app.forms import QuestionForm

@app.route('/index')
def index():
    return('Survey Created') #would work on getting past surveys and navigation functions
@app.route('/surveycreation',methods=['GET','POST'])
def surveycreation():
    form = QuestionForm()
    if form.validate_on_submit():
        flash("Survey created".format(form.question1.data))
        return redirect(url_for('index'))
    return render_template('questions.html', title='Survey Creation', form=form)

