"""
Description of QuestionForm: Generates a survey name field input and
5 questions and answers for customers to fill out. It would capture the
input of the customers and create a survey based on user input.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question1type = SelectField('Question1Type', choices=('SINGLE_OPTION','MULTIPLE_OPTION'))
    question2type = SelectField('Question2Type', choices=('SINGLE_OPTION','MULTIPLE_OPTION'))
    question3type = SelectField('Question3Type', choices=('SINGLE_OPTION','MULTIPLE_OPTION'))
    question4type = SelectField('Question4Type', choices=('SINGLE_OPTION','MULTIPLE_OPTION'))
    question5type = SelectField('Question5Type', choices=('SINGLE_OPTION','MULTIPLE_OPTION'))
    surveyname = StringField('SurveyName',validators=[DataRequired()])
    question1 = StringField('Question1',validators=[DataRequired()])
    answer1a = StringField('Answer1a', validators=[DataRequired()])
    answer1b = StringField('Answer1b', validators=[DataRequired()])
    answer1c = StringField('Answer1c', validators=[DataRequired()])
    answer1d = StringField('Answer1d', validators=[DataRequired()])
    answer1anext = StringField('Answer1aNext', default='end', validators=[DataRequired()])
    answer1bnext = StringField('Answer1bNext', default='end', validators=[DataRequired()])
    answer1cnext = StringField('Answer1cNext', default='end', validators=[DataRequired()])
    answer1dnext = StringField('Answer1dNext', default='end', validators=[DataRequired()])
    answer2anext = StringField('Answer2aNext',default='end')
    answer2bnext = StringField('Answer2bNext',default='end')
    answer2cnext = StringField('Answer2cNext',default='end')
    answer2dnext = StringField('Answer2dNext',default='end')
    answer3anext = StringField('Answer3aNext',default='end')
    answer3bnext = StringField('Answer3bNext',default='end')
    answer3cnext = StringField('Answer3cNext',default='end')
    answer3dnext = StringField('Answer3dNext',default='end')
    question2 = StringField('Question2')
    answer2a = StringField('Answer2a')
    answer2b = StringField('Answer2b')
    answer2c = StringField('Answer2c')
    answer2d = StringField('Answer2d')
    question3 = StringField('Question3')
    answer3a = StringField('Answer3a')
    answer3b = StringField('Answer3b')
    answer3c = StringField('Answer3c')
    answer3d = StringField('Answer3d')
    question4 = StringField('Question4')
    answer4a = StringField('Answer4a')
    answer4b = StringField('Answer4b')
    answer4c = StringField('Answer4c')
    answer4d = StringField('Answer4d')
    question5 = StringField('Question5')
    answer5a = StringField('Answer5a')
    answer5b = StringField('Answer5b')
    answer5c = StringField('Answer5c')
    answer5d = StringField('Answer5d')
    submit = SubmitField('Submit')
