"""Description of QuestionForm: Generates a survey name field input and 5 questions and answers for customers to fill out.

It would capture the input of the customers and create a survey based on user
input.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
  question1Type = SelectField(
      'question1Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question2Type = SelectField(
      'question2Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question3Type = SelectField(
      'question3Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question4Type = SelectField(
      'question4Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  question5Type = SelectField(
      'question5Type', choices=('SINGLE_OPTION', 'MULTIPLE_OPTION'))
  language = SelectField('language', choices=('en', 'ms', 'zh', 'ja', 'ko'))
  surveyName = StringField('surveyName', validators=[DataRequired()])
  question1 = StringField('question1', validators=[DataRequired()])
  answer1a = StringField('answer1a', validators=[DataRequired()])
  answer1b = StringField('answer1b', validators=[DataRequired()])
  answer1c = StringField('answer1c', validators=[DataRequired()])
  answer1d = StringField('answer1d', validators=[DataRequired()])
  answer1aNext = StringField(
      'answer1aNext', default='end', validators=[DataRequired()])
  answer1bNext = StringField(
      'answer1bNext', default='end', validators=[DataRequired()])
  answer1cNext = StringField(
      'answer1cNext', default='end', validators=[DataRequired()])
  answer1dNext = StringField(
      'answer1dNext', default='end', validators=[DataRequired()])
  answer2aNext = StringField('answer2aNext', default='end')
  answer2bNext = StringField('answer2bNext', default='end')
  answer2cNext = StringField('answer2cNext', default='end')
  answer2dNext = StringField('answer2dNext', default='end')
  answer3aNext = StringField('answer3aNext', default='end')
  answer3bNext = StringField('answer3bNext', default='end')
  answer3cNext = StringField('answer3cNext', default='end')
  answer3dNext = StringField('answer3dNext', default='end')
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
