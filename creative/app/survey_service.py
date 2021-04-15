from flask import render_template, flash
from . import survey_collection

def get_all():
    return survey_collection.get_all()

def get_doc_by_id(id):
    return survey_collection.get_doc_by_id(id)

def get_by_id(id):
    return survey_collection.get_by_id(id)

def delete_by_id(id):
    return survey_collection.delete_by_id(id)

def create(form):
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


    # TODO search for ==> form to_dict
    doc_ref = survey_collection.create(data)
    flash(f"{form.surveyname.data} is created as {doc_ref.id}")

def update_by_id(id, form):
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
    edit_doc = survey_collection.update_by_id(id, data)
    flash(f"Survey with ID: {id} is edited")

def set_form_data(form, edit_doc):
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