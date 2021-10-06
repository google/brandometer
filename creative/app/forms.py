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
"""Description of QuestionForm: Generates a survey name field input and 5 questions and answers for customers to fill out.

It would capture the input of the customers and create a survey based on user
input.
"""
import re
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

BRAND_TRACK = 'brand_track'
BRAND_LIFT = 'brand_lift'
ANSWERS_ORDERED = 'ORDERED'
ANSWERS_SHUFFLED = 'SHUFFLED'

def question_section_is_empty(form, questionNumber):
  """Check if any field of the question input including answer is empty."""
  questionField = 'question' + questionNumber
  answerAField = 'answer' + questionNumber + 'a'
  answerBField = 'answer' + questionNumber + 'b'
  return not (form.data[questionField] and form.data[answerAField] and
              form.data[answerBField] and form.data[answerAField + 'next'] and
              form.data[answerBField + 'next'])


def validate_next_question(form, field):
  """Validate if the question is linked by any other question's answer."""
  questionNumberMatch = re.search('\d', field.name)
  questionNumber = questionNumberMatch.group()
  print('validating for question: ' + questionNumber)
  for questionIndex in range(1, 6):
    for answerChoice in ['a', 'b', 'c', 'd']:
      answerFieldName = 'answer' + str(questionIndex) + answerChoice + 'next'
      answerLinkData = form.data[answerFieldName]
      if answerLinkData == questionNumber and question_section_is_empty(
          form, questionNumber):
        raise ValidationError(
            'Answer ' + answerChoice.upper() + ' from question ' +
            str(questionIndex) +
            ' linked to this question, please fill in this section')


class QuestionForm(FlaskForm):
  """QuestionForm that takes in the survey creation parameters."""
  question1type = SelectField(
      'question1Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question2type = SelectField(
      'question2Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question3type = SelectField(
      'question3Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question4type = SelectField(
      'question4Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question5type = SelectField(
      'question5Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question_order_choices = [(ANSWERS_SHUFFLED, 'Shuffled'),
          (ANSWERS_ORDERED, 'Ordered')]
  question1order = SelectField('question1Order', choices=question_order_choices)
  question2order = SelectField('question2Order', choices=question_order_choices)
  question3order = SelectField('question3Order', choices=question_order_choices)
  question4order = SelectField('question4Order', choices=question_order_choices)
  question5order = SelectField('question5Order', choices=question_order_choices)
  language = SelectField('language', choices=('en', 'ms', 'zh', 'ja', 'ko'))
  surveytype = SelectField('surveyType', choices=[(
    BRAND_LIFT, 'Brand Lift'), (BRAND_TRACK, 'Brand Track')])
  surveyname = StringField('surveyName', validators=[DataRequired()])
  question1 = StringField('question1', validators=[DataRequired()])
  answer1a = StringField('answer1a', validators=[DataRequired()])
  answer1b = StringField('answer1b', validators=[DataRequired()])
  answer1c = StringField('answer1c')
  answer1d = StringField('answer1d')
  answer1anext = StringField(
      'answer1aNext', default='end', validators=[DataRequired()])
  answer1bnext = StringField(
      'answer1bNext', default='end', validators=[DataRequired()])
  answer1cnext = StringField('answer1cNext', default='end')
  answer1dnext = StringField('answer1dNext', default='end')
  answer2anext = StringField('answer2aNext', default='end')
  answer2bnext = StringField('answer2bNext', default='end')
  answer2cnext = StringField('answer2cNext', default='end')
  answer2dnext = StringField('answer2dNext', default='end')
  answer3anext = StringField('answer3aNext', default='end')
  answer3bnext = StringField('answer3bNext', default='end')
  answer3cnext = StringField('answer3cNext', default='end')
  answer3dnext = StringField('answer3dNext', default='end')
  answer4anext = StringField('answer4aNext', default='end')
  answer4bnext = StringField('answer4bNext', default='end')
  answer4cnext = StringField('answer4cNext', default='end')
  answer4dnext = StringField('answer4dNext', default='end')
  answer5anext = StringField('answer5aNext', default='end')
  answer5bnext = StringField('answer5bNext', default='end')
  answer5cnext = StringField('answer5cNext', default='end')
  answer5dnext = StringField('answer5dNext', default='end')
  question2 = StringField('question2')
  answer2a = StringField('answer2a')
  answer2b = StringField('answer2b')
  answer2c = StringField('answer2c')
  answer2d = StringField('answer2d')
  question3 = StringField('question3')
  answer3a = StringField('answer3a')
  answer3b = StringField('answer3b')
  answer3c = StringField('answer3c')
  answer3d = StringField('answer3d')
  question4 = StringField('question4')
  answer4a = StringField('answer4a')
  answer4b = StringField('answer4b')
  answer4c = StringField('answer4c')
  answer4d = StringField('answer4d')
  question5 = StringField('question5')
  answer5a = StringField('answer5a')
  answer5b = StringField('answer5b')
  answer5c = StringField('answer5c')
  answer5d = StringField('answer5d')
  submit = SubmitField('Submit')

  def validate_question1(form, field):
    validate_next_question(form, field)

  def validate_question2(form, field):
    validate_next_question(form, field)

  def validate_question3(form, field):
    validate_next_question(form, field)

  def validate_question4(form, field):
    validate_next_question(form, field)

  def validate_question5(form, field):
    validate_next_question(form, field)
