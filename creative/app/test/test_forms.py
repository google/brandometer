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

import unittest
from flask import Flask
import forms

COMPLETE_QUESTION1 = {
    'question1': 'question',
    'answer1a': 'answerA',
    'answer1b': 'answerB',
    'answer1c': 'answerC',
    'answer1d': 'answerD',
    'answer1anext': '2',
    'answer1bnext': '2',
    'answer1cnext': '2',
    'answer1dnext': '2'
}
class QuestionFormTest(unittest.TestCase):
    def create_form(self, data):
        app = Flask(__name__)
        with app.app_context():
            app.config['WTF_CSRF_ENABLED'] = False
            return forms.QuestionForm(data=data)

    def test_question_section_is_empty_when_question_has_2_or_more_answers(self):
        cases = [COMPLETE_QUESTION1,
            dict(COMPLETE_QUESTION1, answer1d=None, answer1dnext=None),
            dict(COMPLETE_QUESTION1, answer1c=None, answer1cnext=None,
                answer1d=None, answer1dnext=None),
        ]
 
        for valid_question in cases:
            valid_form = self.create_form(valid_question)
            test_valid = forms.question_section_is_empty(valid_form, '1')
            self.assertFalse(test_valid)

    def test_question_section_is_empty_when_question_is_invalid(self):
        invalid_question_cases = [dict(COMPLETE_QUESTION1, question1=None),
            dict(COMPLETE_QUESTION1, answer1a=None),
            dict(COMPLETE_QUESTION1, answer1b=None),
            dict(COMPLETE_QUESTION1, answer1anext=None),
            dict(COMPLETE_QUESTION1, answer1bnext=None),
        ]

        for invalid_question in invalid_question_cases:
            invalid_form = self.create_form(invalid_question)
            test_invalid = forms.question_section_is_empty(invalid_form, '1')
            self.assertTrue(test_invalid)

