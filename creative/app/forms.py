"""
Description of QuestionForm: Generates a survey name field input and 
5 questions and answers for customers to fill out. It would capture the 
input of the customers and create a survey based on user input.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    surveyname = StringField('SurveyName',validators=[DataRequired()])
    question1 = StringField('Question1',validators=[DataRequired()])
    answer1a = StringField('Answer1a', validators=[DataRequired()])
    answer1b = StringField('Answer1b', validators=[DataRequired()])
    answer1c = StringField('Answer1c', validators=[DataRequired()])
    answer1d = StringField('Answer1d', validators=[DataRequired()])
    question2 = StringField('Question2',validators=[DataRequired()])
    answer2a = StringField('Answer2a', validators=[DataRequired()])
    answer2b = StringField('Answer2b', validators=[DataRequired()])
    answer2c = StringField('Answer2c', validators=[DataRequired()])
    answer2d = StringField('Answer2d', validators=[DataRequired()])
    question3 = StringField('Question3',validators=[DataRequired()])
    answer3a = StringField('Answer3a', validators=[DataRequired()])
    answer3b = StringField('Answer3b', validators=[DataRequired()])
    answer3c = StringField('Answer3c', validators=[DataRequired()])
    answer3d = StringField('Answer3d', validators=[DataRequired()])
    question4 = StringField('Question4',validators=[DataRequired()])
    answer4a = StringField('Answer4a', validators=[DataRequired()])
    answer4b = StringField('Answer4b', validators=[DataRequired()])
    answer4c = StringField('Answer4c', validators=[DataRequired()])
    answer4d = StringField('Answer4d', validators=[DataRequired()])   
    question5 = StringField('Question5',validators=[DataRequired()])
    answer5a = StringField('Answer5a', validators=[DataRequired()])
    answer5b = StringField('Answer5b', validators=[DataRequired()])
    answer5c = StringField('Answer5c', validators=[DataRequired()])
    answer5d = StringField('Answer5d', validators=[DataRequired()])   
    submit = SubmitField('Create')
