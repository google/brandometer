# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Import of required packages/libraries."""

import datetime
import os
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import send_file
from flask import url_for
from flask_basicauth import BasicAuth
from flask_bootstrap import Bootstrap
import forms
from forms import BRAND_TRACK
import survey_service

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
Bootstrap(app)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('AUTH_PASSWORD')
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True


@app.route('/')
def root():
  return redirect(url_for('index'))


@app.route('/index')
def index():
  all_surveys = survey_service.get_all()
  return render_template('index.html', all_surveys=all_surveys)


@app.route('/survey/create', methods=['GET', 'POST'])
def create():
  """Survey creation."""
  form = forms.QuestionForm()
  if form.validate_on_submit():
    survey_service.create(form)
    return redirect(url_for('index'))
  return render_template('questions.html', title='Survey Creation', form=form)


@app.route('/survey/preview/<string:survey_id>', methods=['GET'])
def preview(survey_id):
  """Survey preview."""
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
        seg='preview',
        thankyou_text=survey_service.get_thank_you_text(survey_info),
        next_text=survey_service.get_next_text(survey_info),
        comment_text=survey_service.get_comment_text(survey_info))
  else:
    flash('Survey not found')
    return redirect(url_for('index'))


@app.route('/survey/delete', methods=['GET', 'DELETE'])
def delete():
  """Delete survey."""
  if request.method == 'GET':
    docref_id = request.args.get('survey_id')
    survey_service.delete_by_id(docref_id)
    flash(f'Survey \'{docref_id}\' deleted')
  return redirect(url_for('index'))


@app.route('/survey/edit', methods=['POST', 'PUT', 'GET'])
def edit():
  """Edit Survey."""
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
  """Download zip of survey creative(s)."""
  survey_doc = survey_service.get_doc_by_id(survey_id)
  filename, data = survey_service.zip_file(survey_id, survey_doc.to_dict())
  return send_file(
      data,
      mimetype='application/zip',
      add_etags=False,
      cache_timeout=0,
      last_modified=datetime.datetime.now(),
      as_attachment=True,
      attachment_filename=filename)


@app.route('/survey/download_responses/<string:survey_id>', methods=['GET'])
def download_responses(survey_id):
  """Download survey responses."""
  if request.method == 'GET':
    csv = survey_service.download_responses(survey_id)
    return Response(
        csv,
        mimetype='text/csv',
        headers={'Content-disposition': 'attachment; filename=surveydata.csv'})


@app.route('/survey/reporting/<string:survey_id>', methods=['GET'])
def reporting(survey_id):
  """Survey reporting."""
  survey_doc = survey_service.get_doc_by_id(survey_id)

  if survey_doc.exists:
    survey_info = survey_doc.to_dict()
    results = survey_service.get_brand_lift_results(survey_id)
    return render_template(
        'reporting.html',
        results=results,
        survey=survey_info,
        survey_id=survey_id)
  else:
    flash('Survey not found')
    return redirect(url_for('index'))


@app.context_processor
def inject_receiver_params():
  return {
      'receiver_url':
          os.environ.get(
              'RECEIVER_URL',
              'https://us-central1-jerraldwee-testing.cloudfunctions.net/receiver'
          )
  }


@app.template_filter('get_all_question_text')
def get_all_question_text(survey):
  return survey_service.get_all_question_text(survey.to_dict())


@app.template_filter('format_percentage')
def format_percentage(num):
  return '{:.2%}'.format(num)


@app.template_filter('has_reporting')
def is_brand_track(survey):
  return survey.to_dict().get('surveytype', '') != BRAND_TRACK


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
