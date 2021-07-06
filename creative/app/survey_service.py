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
"""Various imports to be used for survey functionalites."""
import datetime
import io
import os
import zipfile
from flask import flash
from flask import render_template
from google.cloud import bigquery
from google.cloud import bigquery_storage
import google.cloud.bigquery.magics
import pandas as pd
import survey_collection


def get_all():
  return survey_collection.get_all()


def get_doc_by_id(survey_id):
  return survey_collection.get_doc_by_id(survey_id)


def get_by_id(survey_id):
  return survey_collection.get_by_id(survey_id)


def delete_by_id(survey_id):
  return survey_collection.delete_by_id(survey_id)


def create(form):
  doc_ref = survey_collection.create(form.data)
  flash(f'{form.surveyname.data} created as {doc_ref.id}')


def update_by_id(survey_id, form):
  edit_doc = survey_collection.update_by_id(survey_id, form.data)
  flash(f'{form.surveyname.data} updated')


def set_form_data(form, edit_doc):
  edit_doc_dict = edit_doc.to_dict()

  for key, value in edit_doc_dict.items():
    form[key].data = edit_doc.get(key,)


def zip_file(survey_id):
  """File download function."""
  # Make these use temp files in '/tmp/' to work around
  # App Engine read only filesystem

  # Prepare data
  survey_doc = get_doc_by_id(survey_id)
  survey_dict = survey_doc.to_dict()
  current_datetime = datetime.datetime.now().strftime('%Y%m%d')
  surveyname = survey_dict['surveyname'].replace(' ', '-')
  prefix_filename = current_datetime + '_' + surveyname
  seg_types = ['default_control', 'default_expose']

  # create zip
  template_zips = write_html_template(survey_id, survey_dict, prefix_filename,
                                      seg_types)
  combined_zip = zip_dir(prefix_filename, template_zips)

  # make data response
  with open(combined_zip.filename, 'rb') as file:
    file_data = io.BytesIO(file.read())

  # clean up tmp files
  delete_tmp_zip_files([combined_zip] + template_zips)

  return os.path.basename(combined_zip.filename), file_data


def zip_dir(filename, template_zips):
  with zipfile.ZipFile('/tmp/' + filename + '.zip', 'w',
                       zipfile.ZIP_DEFLATED) as zipdir:
    for zip in template_zips:
      zipdir.write(zip.filename)
  return zipdir


def write_html_template(survey_id, survey_dict, prefix_filename, seg_types):
  template_zips = []

  for seg_type in seg_types:
    dir_name = '/tmp/' + prefix_filename + '_' + seg_type
    # write html file
    with zipfile.ZipFile(dir_name + '.zip', 'w',
                         zipfile.ZIP_DEFLATED) as zip_write_file:
      zip_write_file.writestr(
          'index.html', get_html_template(survey_id, survey_dict, seg_type))
      template_zips.append(zip_write_file)

  return template_zips


def get_html_template(survey_id, survey_dict, seg_type):
  return render_template(
      'creative.html',
      survey=survey_dict,
      survey_id=survey_id,
      show_back_button=False,
      all_question_json=get_question_json(survey_dict),
      seg=seg_type,
      thankyou_text=get_thank_you_text(survey_dict),
      next_text=get_next_text(survey_dict),
      comment_text=get_comment_text(survey_dict))


def delete_tmp_zip_files(zipfiles):
  for zipfile in zipfiles:
    os.remove(zipfile.filename)


def get_all_question_text(survey):
  all_question_text = []
  for i in range(1, 6):
    question_text = survey.get('question' + str(i), '')
    if question_text:
      all_question_text.append(question_text)
  return all_question_text


def get_question_json(survey):
  """Retrieving questions from survey in JSON format."""
  all_question_json = []
  for i in range(1, 6):
    question_text = survey.get('question' + str(i), '')
    options = []
    next_question = {}
    question_type = survey.get('question' + str(i) + 'type')
    if question_text:
      question = {
          'id': i,
          'type': question_type,
          'text': question_text,
          'options': options,
          'next_question': next_question
      }
    for j in ['a', 'b', 'c', 'd']:
      answer_text = survey.get('answer' + str(i) + j, '')
      if answer_text:
        answer_id = j.capitalize()
        options.append({'id': answer_id, 'role': 'option', 'text': answer_text})
      next_question[answer_id] = survey.get('answer' + str(i) + j + 'next', '')
    all_question_json.append(question)
  return all_question_json


def download_results(surveyid):
  """Download survey results in a CSV format file."""
  google.cloud.bigquery.magics.context.use_bqstorage_api = True
  project_id = os.environ.get('PROJECT_ID')
  table_id = os.environ.get('TABLE_ID')
  client = bigquery.Client(project=project_id)
  bqstorageclient = bigquery_storage.BigQueryReadClient()
  query = f"""
        SELECT *
        FROM `{table_id}`
        WHERE ID = @survey_id
    """
  job_config = bigquery.QueryJobConfig(query_parameters=[
      bigquery.ScalarQueryParameter('survey_id', 'STRING', surveyid),
  ])
  query_job = client.query(query, job_config=job_config)
  df = query_job.result().to_dataframe(bqstorage_client=bqstorageclient)
  df = df[df['ID'] == surveyid]
  output = {'Date': [], 'Control/Expose': [], 'Dimension 2': []}
  outputdf = pd.DataFrame(data=output)
  outputdf['Date'] = df['CreatedAt'].values
  outputdf['Control/Expose'] = df['Segmentation'].values
  responselist = df['Response'].str.split(pat=('|'), expand=True)
  columns = list(responselist)
  for i in columns:
    responselist[i] = responselist[i].str.slice(start=2)
  responselist = responselist.rename(
      columns={
          0: 'Response 1',
          1: 'Response 2',
          2: 'Response 3',
          3: 'Response 4',
          4: 'Response 5'
      })
  responselist = responselist.reset_index(drop=True)
  outputdf = pd.concat([outputdf, responselist], axis=1)
  print(outputdf)
  csv = outputdf.to_csv()
  return csv


def get_thank_you_text(survey):
  """Multi-language support input for thank you text."""
  if survey.get('language') == 'ms':
    thankyou_text = 'Terima Kasih'
  elif survey.get('language') == 'zh':
    thankyou_text = '谢谢'
  elif survey.get('language') == 'ja':
    thankyou_text = 'ありがとうございました'
  elif survey.get('language') == 'ko':
    thankyou_text = '고맙습니다'
  else:
    thankyou_text = 'Thank You'
  return thankyou_text


def get_next_text(survey):
  """Multi-language support input for next text."""
  if survey.get('language') == 'ms':
    next_text = 'Next'
  elif survey.get('language') == 'zh':
    next_text = '下一个'
  elif survey.get('language') == 'ja':
    next_text = '次へ'
  elif survey.get('language') == 'ko':
    next_text = '다음에'
  else:
    next_text = 'Next'
  return next_text


def get_comment_text(survey):
  """Multi-language support input for comment text."""
  if survey.get('language') == 'ms':
    comment_text = 'Pilih semua yang berkenaan'
  elif survey.get('language') == 'zh':
    comment_text = '选择所有适用的'
  elif survey.get('language') == 'ja':
    comment_text = '当てはまるもの全て選択'
  elif survey.get('language') == 'ko':
    comment_text = '적용 가능한 모든 항목을 선택하십시오'
  else:
    comment_text = 'Choose all applicable'
  return comment_text
