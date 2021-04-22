from flask import render_template, flash
from . import survey_collection
import io
import datetime
import zipfile
import os

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
    # prepare data
    survey_doc = get_doc_by_id(id)
    survey_dict = survey_doc.to_dict()
    current_datetime = datetime.datetime.now().strftime("%Y%m%d")
    surveyName = survey_dict['surveyName'].replace(" ", "-")
    prefix_filename = current_datetime+'_'+surveyName
    seg_types = ['default_control','default_expose']

    # create zip
    write_html_template(id, survey_dict, prefix_filename, seg_types)
    zip_dir(prefix_filename, seg_types)

    # make data response
    filename = prefix_filename +'.zip'
    with open(filename, 'rb') as file:
        file_data = io.BytesIO(file.read())
    delete_tmp_zip_files(prefix_filename, seg_types)
    return filename, file_data

def zip_dir(filename, seg_types):
    zipdir = zipfile.ZipFile(filename+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for seg_type in seg_types:
        zipdir.write(filename+'_'+seg_type+'.zip')

def write_html_template(id, survey_dict, prefix_filename, seg_types):
    
    for seg_type in seg_types:
        dir_name = prefix_filename+'_'+seg_type 
        # write html file
        zip_write_file = zipfile.ZipFile(dir_name+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zip_write_file.writestr('index.html', get_html_template(survey_dict, seg_type))
        

def get_html_template(survey_dict, seg_type):
    return render_template('creative.html',
                            survey=survey_dict,
                            survey_id=id,
                            show_back_button = False,
                            all_question_json=get_question_json(survey_dict),
                            seg=seg_type)

def delete_tmp_zip_files(filename, seg_types):
    for seg_type in seg_types:
        os.remove(filename+'_'+seg_type+'.zip')
    os.remove(filename+'.zip')

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