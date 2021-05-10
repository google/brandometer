import datetime

from flask import Flask
from flask import render_template, request, flash, redirect, url_for, jsonify, send_file, Response
import pathlib
import os
from flask_bootstrap import Bootstrap

import forms
import survey_collection
import survey_service

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
Bootstrap(app)


@app.route('/')
def root():
  return redirect(url_for('index'))


@app.route('/index')
def index():
  all_surveys = survey_service.get_all()
  return render_template('index.html', all_surveys=all_surveys)


@app.route('/survey/create', methods=['GET', 'POST'])
def create():
  form = forms.QuestionForm()
  if form.validate_on_submit():
    survey_service.create(form)
    return redirect(url_for('index'))
  return render_template('questions.html', title='Survey Creation', form=form)


@app.route('/survey/preview/<string:survey_id>', methods=['GET'])
def preview(survey_id):
  survey_doc = survey_service.get_doc_by_id(survey_id)
  if survey_doc.exists:
    survey_info = survey_doc.to_dict()
    return render_template(
        'creative.html',
        survey=survey_info,
        survey_id=survey_id,
        manual_responses=True,
        show_back_button=True,
        all_question_json=survey_service.get_question_json(survey_info),
        seg='default')
  else:
    flash('Survey not found')
    return redirect(url_for('index'))


@app.route('/survey/delete', methods=['GET', 'DELETE'])
def delete():
  if request.method == 'GET':
    docref_id = request.args.get('survey_id')
    survey_service.delete_by_id(docref_id)
    flash(f'Survey with ID: {docref_id} is deleted')
  return redirect(url_for('index'))


@app.route('/survey/edit', methods=['POST', 'PUT', 'GET'])
def edit():
  form = forms.QuestionForm()
  docref_id = request.args.get('survey_id')
  edit_doc = survey_service.get_doc_by_id(docref_id)
  if request.method == 'GET':
    survey_service.set_form_data(form, edit_doc)
  if form.validate_on_submit():
    survey_service.update_by_id(docref_id, form)
    return redirect(url_for('index'))
  return render_template('questions.html', form=form)


@app.route('/survey/download_zip/<string:survey_id>', methods=['GET'])
def download_zip(survey_id):
  filename, data = survey_service.zip_file(survey_id)
  return send_file(
      data,
      mimetype='application/zip',
      as_attachment=True,
      attachment_filename=filename)


@app.route('/survey/download_results/<string:survey_id>', methods=['GET'])
def download_results(survey_id):
  if request.method == 'GET':
    csv = survey_service.download_results(survey_id)
    return Response(
        csv,
        mimetype='text/csv',
        headers={'Content-disposition': 'attachment; filename=surveydata.csv'})


@app.context_processor
def inject_receiver_params():
  return {
      'receiver_url':
          os.environ.get(
              'RECEIVER_URL',
              'https://us-central1-jerraldwee-testing.cloudfunctions.net/receiver'
          )
  }


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)