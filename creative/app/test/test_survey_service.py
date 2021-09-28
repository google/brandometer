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

import os
import tempfile
import unittest
from unittest import mock
import zipfile

from mockfirestore import MockFirestore
import survey_collection
import survey_service


class TestSurveyService(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.client = MockFirestore()
    self.collection = self.client.collection('test_surveys')

  def tearDown(self):
    self.client.reset()
    super().tearDown()

  def test_get_all(self):
    # given
    survey_collection.get_all = mock.Mock()
    # when
    survey_service.get_all()
    # then
    assert survey_collection.get_all.call_count == 1

  def test_get_by_id(self):
    # given
    survey_collection.get_by_id = mock.Mock()
    # when
    survey_service.get_by_id('mockSurveyId')
    # then
    survey_collection.get_by_id.assert_called_once_with('mockSurveyId')

  def test_get_doc_by_id(self):
    # given
    survey_collection.get_doc_by_id = mock.Mock()
    # when
    survey_service.get_doc_by_id('mockSurveyId')
    # then
    survey_collection.get_doc_by_id.assert_called_once_with('mockSurveyId')

  def test_delete_by_id(self):
    # given
    survey_collection.delete_by_id = mock.Mock()
    # when
    survey_service.delete_by_id('mockSurveyId')
    # then
    survey_collection.delete_by_id.assert_called_once_with('mockSurveyId')

  def test_set_form_data_copies_values_from_a_document(self):
    form = {
        'field1': mock.Mock(data=None),
        'field2': mock.Mock(data='value2'),
        'field3': mock.Mock(data='untouched')
    }

    ref = self.collection.document()
    ref.set({'field1': 'something', 'field2': 'new_value2'})
    doc = ref.get()

    survey_service.set_form_data(form, doc)
    self.assertEqual(form['field1'].data, 'something')
    self.assertEqual(form['field2'].data, 'new_value2')
    self.assertEqual(form['field3'].data, 'untouched')

  # TODO(bradx): zip_file - need to refactor to pass in survey/dict

  def test_write_html_template(self):
    segments = ['segment1', 'segment2', 'segment3']
    survey_dict = {'question1': 'q1 text', 'answer1a': 'a1a test'}
    survey_service.render_template = mock.Mock(
        return_value='<html>placeholder</html>')

    zips = survey_service.write_html_template('id1', survey_dict, 'test_prefix',
                                              segments)

    self.assertEqual(len(zips), len(segments))
    self.assertEqual(zips[0].filename, '/tmp/test_prefix_segment1.zip')
    self.assertEqual(zips[1].filename, '/tmp/test_prefix_segment2.zip')
    self.assertEqual(zips[2].filename, '/tmp/test_prefix_segment3.zip')

  def test_delete_tmp_zip_files(self):
    os.remove = mock.Mock()
    with tempfile.TemporaryDirectory() as tmpdir:
      # given
      zip1 = zipfile.ZipFile(tmpdir + 'mock-file-name.zip', 'w')
      zip2 = zipfile.ZipFile(tmpdir + 'mock-file-name2.zip', 'w')

      # when
      survey_service.delete_tmp_zip_files([zip1, zip2])

      # then
      expected_calls = [mock.call(zip1.filename), mock.call(zip2.filename)]
      os.remove.assert_has_calls(expected_calls)
      assert os.remove.call_count == 2

  def test_get_question_json_converts_to_format_expected_by_creative(self):
    survey = {
        'question1': 'q1 text',
        'question1type': 'q1type',
        'answer1a': 'a1a',
        'answer1anext': 'end',
        'answer1b': 'a1b',
        'answer1bnext': '2',
        'question2': 'q2 text',
    }
    json = survey_service.get_question_json(survey)
    self.assertDictEqual(
        json[0], {
            'id':
                1,
            'text':
                'q1 text',
            'type':
                'q1type',
            'next_question': {
                'A': 'end',
                'B': '2'
            },
            'options': [
                {
                    'id': 'A',
                    'role': 'option',
                    'text': 'a1a'
                },
                {
                    'id': 'B',
                    'role': 'option',
                    'text': 'a1b'
                },
            ]
        })
    self.assertEqual(json[1]['text'], 'q2 text')

  def test_get_thank_you_text_default(self):
    text = survey_service.get_thank_you_text({'language': 'ms'})
    self.assertEqual(text, 'Terima Kasih')

  def test_get_thank_you_text_defaults_to_english_if_no_lang(self):
    text = survey_service.get_thank_you_text({})
    self.assertEqual(text, 'Thank You')

  def test_get_thank_you_text_defaults_to_english_if_unknown_lang(self):
    text = survey_service.get_thank_you_text({'language': 'ZZ'})
    self.assertEqual(text, 'Thank You')

  def test_get_next_text_default(self):
    text = survey_service.get_next_text({'language': 'ja'})
    self.assertEqual(text, '次へ')

  def test_get_next_text_defaults_to_english_if_no_lang(self):
    text = survey_service.get_next_text({})
    self.assertEqual(text, 'Next')

  def test_get_next_text_defaults_to_english_if_unknown_lang(self):
    text = survey_service.get_next_text({'language': 'ZZ'})
    self.assertEqual(text, 'Next')

  def test_get_comment_text_default(self):
    text = survey_service.get_comment_text({'language': 'zh'})
    self.assertEqual(text, '选择所有适用的')

  def test_get_comment_text_defaults_to_english_if_no_lang(self):
    text = survey_service.get_comment_text({})
    self.assertEqual(text, 'Choose all applicable')

  def test_get_comment_text_defaults_to_english_if_unknown_lang(self):
    text = survey_service.get_comment_text({'language': 'ZZ'})
    self.assertEqual(text, 'Choose all applicable')
