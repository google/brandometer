from google.cloud import firestore
from flask import render_template, request, flash, redirect, url_for, jsonify
from .forms import QuestionForm
from . import app
import zipfile
import io
import pathlib
from flask import send_file

db=firestore.Client()
survey_collection=db.collection(u'Surveys')

@app.route('/index')
def index():
  all_surveys = survey_collection.stream()
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
          u'Answer2a': form.answer2a.data,
          u'Answer2b': form.answer2b.data,
          u'Answer2c': form.answer2c.data,
          u'Answer2d': form.answer2d.data,
      }

      doc_ref = survey_collection.document()
      doc_ref.set(data)
      # Then query for documents
      for doc in survey_collection.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
      flash(f"{form.surveyname.data} is created as {doc_ref.id}")

      return redirect(url_for('index'))

    return render_template('questions.html', title='Survey Creation', form=form)

@app.route('/creative/preview/<string:survey_id>', methods=['GET'])
def preview_creative(survey_id):
  doc_ref = survey_collection.document(survey_id)
  survey_doc = doc_ref.get()
  if survey_doc.exists:
    survey = survey_doc.to_dict()
    return render_template(
        'creative.html',
        survey=survey,
        all_question_json=get_question_json(survey))
  else:
    flash('Survey not found')
    return redirect(url_for('index'))

def get_question_json(survey):
  all_question_json = []
  for i in range(1, 5):
    question_text = survey.get('Question' + str(i), '')
    options = []
    next_question = {}
    if question_text:
      question = {
          'id': i,
          'type': 'SINGLE_OPTION',  # TODO handle MULTIPLE_OPTION as well
          'text': question_text,
          'options': options,
          'next_question': next_question
      }
      for j in ['a', 'b', 'c', 'd', 'e']:
        answer_text = survey.get('Answer' + str(i) + j, '')
        if answer_text:
          answer_id = j.capitalize()
          options.append({
              'id': answer_id,
              'role': 'option',
              'text': answer_text
          })
          next_question[answer_id] = 'end'
      all_question_json.append(question)

  return all_question_json

@app.route('/delete',methods=["GET","DELETE"])
def delete():
    if request.method =="GET":
        docref_id = request.args.get('id')
        survey_collection.document(docref_id).delete()
        flash(f"Survey with ID: {docref_id} is deleted")
    return redirect(url_for('index'))

@app.route('/edit', methods=["POST","PUT","GET"])
def edit():
    form = QuestionForm()
    docref_id = request.args.get('id')
    edit_doc = survey_collection.document(docref_id).get()
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
      edit_doc = survey_collection.document(docref_id)
      edit_doc.update(data)
      flash(f"Survey with ID: {docref_id} is edited")
      return redirect(url_for('index'))
    return render_template('questions.html', form=form)

@app.route('/download_zip/<string:survey_id>',methods=["GET"])
def download_zip(survey_id):
    data = io.BytesIO()

    with zipfile.ZipFile(data, mode='w') as z:
        doc_ref = survey_collection.document(survey_id)
        survey_doc = doc_ref.get()
        survey = survey_doc.to_dict()
        survey_html = render_template('creative.html',survey=survey,all_question_json=get_question_json(survey))
        z.writestr("index.html", survey_html)

    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='surveycreative.zip')
