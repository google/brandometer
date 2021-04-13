from google.cloud import firestore
from flask import render_template, request, flash, redirect, url_for, jsonify, send_file
from .forms import QuestionForm
from . import app
import zipfile
import io
import os
import pathlib

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
          u'Question1Type' : form.question1type.data,
          u'Question2Type' : form.question2type.data,
          u'Question3Type' : form.question3type.data,
          u'Question4Type' : form.question4type.data,
          u'Question5Type' : form.question5type.data,
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
          u'Question3': form.question3.data,
          u'Answer3a': form.answer3a.data,
          u'Answer3b': form.answer3b.data,
          u'Answer3c': form.answer3c.data,
          u'Answer3d': form.answer3d.data,
          u'Answer1aNext': form.answer1anext.data,
          u'Answer1bNext': form.answer1bnext.data,
          u'Answer1cNext': form.answer1cnext.data,
          u'Answer1dNext': form.answer1dnext.data,
          u'Answer2aNext': form.answer2anext.data,
          u'Answer2bNext': form.answer2bnext.data,
          u'Answer2cNext': form.answer2cnext.data,
          u'Answer2dNext': form.answer2dnext.data,
          u'Answer3aNext': form.answer3anext.data,
          u'Answer3bNext': form.answer3bnext.data,
          u'Answer3cNext': form.answer3cnext.data,
          u'Answer3dNext': form.answer3dnext.data
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
        survey_id=survey_id,
        manual_responses=True,
        show_back_button = True,
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
    question_type = survey.get('Question' + str(i) + 'Type')
    if question_text:
      question = {
          'id': i,
          'type': question_type,
          'text': question_text,
          'options': options,
          'next_question': next_question
      }
      for j in ['a', 'b', 'c', 'd']:
        answer_text = survey.get('Answer' + str(i) + j, '')
        if answer_text:
          answer_id = j.capitalize()
          options.append({
              'id': answer_id,
              'role': 'option',
              'text': answer_text
          })
          next_question[answer_id] = survey.get('Answer' + str(i) + j + 'Next','')
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
        form.question2.data = edit_doc.get('Question2',)
        form.answer2a.data = edit_doc.get('Answer2a',)
        form.answer2b.data = edit_doc.get('Answer2b',)
        form.answer2c.data = edit_doc.get('Answer2c',)
        form.answer2d.data = edit_doc.get('Answer2d',)
        form.question3.data = edit_doc.get('Question3',)
        form.answer3a.data = edit_doc.get('Answer3a',)
        form.answer3b.data = edit_doc.get('Answer3b',)
        form.answer3c.data = edit_doc.get('Answer3c',)
        form.answer3d.data = edit_doc.get('Answer3d',)
        form.question1type.data = edit_doc.get('Question1Type',)
        form.question2type.data = edit_doc.get('Question2Type',)
        form.question3type.data = edit_doc.get('Question3Type',)
        form.question4type.data = edit_doc.get('Question4Type',)
        form.question5type.data = edit_doc.get('Question5Type',)
        form.answer1anext.data = edit_doc.get('Answer1aNext',)
        form.answer1bnext.data = edit_doc.get('Answer1bNext',)
        form.answer1cnext.data = edit_doc.get('Answer1cNext',)
        form.answer1dnext.data = edit_doc.get('Answer1dNext',)
        form.answer2anext.data = edit_doc.get('Answer2aNext',)
        form.answer2bnext.data = edit_doc.get('Answer2bNext',)
        form.answer2cnext.data = edit_doc.get('Answer2cNext',)
        form.answer2dnext.data = edit_doc.get('Answer2dNext',)
        form.answer3anext.data = edit_doc.get('Answer3aNext',)
        form.answer3bnext.data = edit_doc.get('Answer3bNext',)
        form.answer3cnext.data = edit_doc.get('Answer3cNext',)
        form.answer3dnext.data = edit_doc.get('Answer3dNext',)
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
          u'Question3': form.question3.data,
          u'Answer3a': form.answer3a.data,
          u'Answer3b': form.answer3b.data,
          u'Answer3c': form.answer3c.data,
          u'Answer3d': form.answer3d.data,
          u'Question1Type': form.question1type.data,
          u'Question2Type': form.question2type.data,
          u'Question3Type': form.question3type.data,
          u'Question4Type': form.question4type.data,
          u'Question5Type': form.question5type.data,
          u'Answer1aNext': form.answer1anext.data,
          u'Answer1bNext': form.answer1bnext.data,
          u'Answer1cNext': form.answer1cnext.data,
          u'Answer1dNext': form.answer1dnext.data,
          u'Answer2aNext': form.answer2anext.data,
          u'Answer2bNext': form.answer2bnext.data,
          u'Answer2cNext': form.answer2cnext.data,
          u'Answer2dNext': form.answer2dnext.data,
          u'Answer3aNext': form.answer3anext.data,
          u'Answer3bNext': form.answer3bnext.data,
          u'Answer3cNext': form.answer3cnext.data,
          u'Answer3dNext': form.answer3dnext.data
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
        survey_html = render_template('creative.html',
                                      survey=survey,
                                      survey_id=survey_id,
                                      show_back_button = False,
                                      all_question_json=get_question_json(survey))
        z.writestr("index.html", survey_html)

    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='surveycreative.zip')

@app.context_processor
def inject_receiver_params():
  return {
      'receiver_url':
          os.environ.get(
              'RECEIVER_URL',
              'https://us-central1-jerraldwee-testing.cloudfunctions.net/receiver'
          )
  }
