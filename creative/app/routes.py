from google.cloud import firestore
from flask import render_template, request, flash, redirect, url_for, jsonify
from .forms import QuestionForm
from . import app

db=firestore.Client()
doc_ref=db.collection(u'Surveys')

@app.route('/index')
def index():
    all_surveys= doc_ref.stream()

    return render_template('index.html', all_surveys = all_surveys)

@app.route('/surveycreation',methods=['GET','POST'])
def surveycreation():
    form = QuestionForm()

    if form.validate_on_submit():
        data = {
                u'SurveyName': form.surveyname.data,
                u'Question1': form.question1.data,
                u'Answer1a': form.answer1a.data,
                u'Answer1b': form.answer1b.data,
                u'Answer1c': form.answer1c.data,
                u'Answer1d': form.answer1d.data,
                u'Question2': form.question2.data,
                u'Answer2a': form.answer2a.data
                }

        doc_ref = db.collection(u'Surveys').document()
        doc_ref.set(data)
        # Then query for documents
        users_ref = db.collection(u'Surveys')

        for doc in users_ref.stream():
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

        return redirect(url_for('index'))

    return render_template('questions.html', title='Survey Creation', form=form)

@app.route('/delete',methods=["GET","DELETE"])
def delete():
    if request.method =="GET":
        docref_id = request.args.get('id')
        doc_ref.document(docref_id).delete()
    return redirect(url_for('index'))

@app.route('/edit', methods=["POST","PUT","GET"])
def edit():
    form = QuestionForm()
    docref_id = request.args.get('id')
    edit_doc = doc_ref.document(docref_id).get()
    if request.method == 'GET':
        form.surveyname.data = edit_doc.get('SurveyName',)
        form.question1.data = edit_doc.get('Question1',)
        form.answer1a.data = edit_doc.get('Answer1a',)
        form.answer1b.data = edit_doc.get('Answer1b',)
        form.answer1c.data = edit_doc.get('Answer1c',)
        form.answer1d.data = edit_doc.get('Answer1d',)
    if form.validate_on_submit():
        data = {
                u'SurveyName': form.surveyname.data,
                u'Question1': form.question1.data,
                u'Answer1a': form.answer1a.data,
                u'Answer1b': form.answer1b.data,
                u'Answer1c': form.answer1c.data,
                u'Answer1d': form.answer1d.data
                }
        edit_doc = db.collection(u'Surveys').document(docref_id)
        edit_doc.update(data)
        return redirect(url_for('index'))
    return render_template('questions.html', form=form)
