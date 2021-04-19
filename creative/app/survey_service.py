from flask import render_template, flash
from . import survey_collection
import io
import datetime
import zipfile

def get_all():
    return survey_collection.get_all()

def get_doc_by_id(id):
    return survey_collection.get_doc_by_id(id)

def get_by_id(id):
    return survey_collection.get_by_id(id)

def delete_by_id(id):
    return survey_collection.delete_by_id(id)

def create(form):
    doc_ref = survey_collection.create(form.data)
    flash(f"{form.surveyName.data} is created as {doc_ref.id}")

def update_by_id(id, form):
    edit_doc = survey_collection.update_by_id(id, form.data)
    flash(f"Survey with ID: {id} is edited")

def set_form_data(form, edit_doc):
    edit_doc_dict = edit_doc.to_dict()
    for key, value in edit_doc_dict.items():
        form[key].data = edit_doc.get(key,)

def zip_file(id):
    data = io.BytesIO()
    survey_doc = get_doc_by_id(id)
    survey_dict = survey_doc.to_dict()
    write_html_template(id, survey_dict, data)
    data.seek(0)
    filename = datetime.datetime.now().strftime("%Y%m%d")+'_'+survey_dict['surveyName']+'.zip'
    return filename, data

def write_html_template(id, survey_dict, data):
    with zipfile.ZipFile(data, mode='w') as z:
        survey_html = render_template('creative.html',
                                  survey=survey_dict,
                                  survey_id=id,
                                  show_back_button = False,
                                  all_question_json=get_question_json(survey_dict))
        z.writestr("index.html", survey_html)

def get_question_json(survey):
  all_question_json = []
  for i in range(1, 5):
    question_text = survey.get('question' + str(i), '')
    options = []
    next_question = {}
    question_type = survey.get('question' + str(i) + 'Type')
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
          options.append({
              'id': answer_id,
              'role': 'option',
              'text': answer_text
          })
          next_question[answer_id] = survey.get('answer' + str(i) + j + 'Next','')
      all_question_json.append(question)
  return all_question_json