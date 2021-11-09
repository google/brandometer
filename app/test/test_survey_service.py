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

import csv
import datetime
import math
import os
import tempfile
import unittest
from unittest import mock
import zipfile

from google.cloud import bigquery
from mockfirestore import MockFirestore
import pandas
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

  def test_zip_file_returns_user_readable_filename(self):
    survey_id = 'some_test_id'
    survey_dict = {
        'surveyname': 'test survey',
        'question1': 'q1 text',
    }

    filename, _ = survey_service.zip_file(survey_id, survey_dict)
    self.assertRegex(filename, '.*_test-survey.zip$')

  def test_zip_file_returns_nested_zips_with_content(self):
    survey_id = 'some_test_id'
    survey_dict = {
        'surveyname': 'test survey',
        'question1': 'q1 text',
    }

    _, data = survey_service.zip_file(survey_id, survey_dict)
    zf = zipfile.ZipFile(data)
    names = sorted([nzf.filename for nzf in zf.filelist])
    self.assertRegex(names[0], '.*_test-survey_default_control.zip$')
    self.assertRegex(names[1], '.*_test-survey_default_expose.zip$')

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
      zip1 = zipfile.ZipFile(tmpdir + 'mock-file-name.zip', 'w')
      zip2 = zipfile.ZipFile(tmpdir + 'mock-file-name2.zip', 'w')

      survey_service.delete_tmp_zip_files([zip1, zip2])

      expected_calls = [mock.call(zip1.filename), mock.call(zip2.filename)]
      os.remove.assert_has_calls(expected_calls)
      assert os.remove.call_count == 2

  def test_get_all_question_text(self):
    survey_dict = {
        'question1': 'q1 text',
        'question2': 'q2 text',
    }

    result = survey_service.get_all_question_text(survey_dict)

    self.assertEqual(result, ['q1 text', 'q2 text'])

  def test_get_all_question_text_includes_text_after_missed_questions(self):
    survey_dict = {
        'question1': 'q1 text',
        'question2': 'q3 text',
    }

    result = survey_service.get_all_question_text(survey_dict)

    self.assertEqual(result, ['q1 text', 'q3 text'])

  def test_get_question_json_converts_to_format_expected_by_creative(self):
    survey = {
        'question1': 'q1 text',
        'question1type': 'q1type',
        'question1order': 'ORDERED',
        'answer1a': 'a1a',
        'answer1anext': 'end',
        'answer1b': 'a1b',
        'answer1bnext': '2',
        'question2': 'q2 text',
    }
    json = survey_service.get_question_json(survey)
    self.assertDictEqual(
        json[0], {
            'answersOrder': 'ORDERED',
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

  def test_get_survey_responses_limits_to_given_survey(self):
    mock_bigquery_client = mock.create_autospec(bigquery.Client)

    survey_service.get_survey_responses(12345, client=mock_bigquery_client)

    query_call = mock_bigquery_client.query.mock_calls[0]
    sql = query_call.args[0]
    survey_param = query_call.kwargs['job_config'].query_parameters[0]
    self.assertRegex(sql, 'WHERE ID = @survey_id')
    self.assertEqual(survey_param.name, 'survey_id')
    self.assertEqual(survey_param.value, 12345)

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_download_responses(self, responses_mock):
    t1 = datetime.datetime.now()
    t2 = t1 + datetime.timedelta(hours=-1)
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': [t1, t2],
        'Segmentation': ['seg1', 'seg2'],
        'Response': ['1:r1a', '1:r2b']
    })

    raw_csv = survey_service.download_responses(1)
    responses = list(csv.DictReader(raw_csv.splitlines()))

    self.assertEqual(responses[0]['Date'], str(t1))
    self.assertEqual(responses[0]['Control/Expose'], 'seg1')
    self.assertEqual(responses[0]['Response 1'], 'r1a')
    self.assertEqual(responses[1]['Date'], str(t2))
    self.assertEqual(responses[1]['Control/Expose'], 'seg2')
    self.assertEqual(responses[1]['Response 1'], 'r2b')

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_download_responses_with_multi_question_responses(
      self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': [datetime.datetime.now()],
        'Segmentation': ['seg1'],
        'Response': ['1:r1a|2:r1b||4:r1e|']
    })

    raw_csv = survey_service.download_responses(surveyid=1234)
    responses = list(csv.DictReader(raw_csv.splitlines()))

    self.assertEqual(responses[0]['Response 1'], 'r1a')
    self.assertEqual(responses[0]['Response 2'], 'r1b')
    self.assertEqual(responses[0]['Response 3'], '')
    self.assertEqual(responses[0]['Response 4'], 'r1e')
    self.assertEqual(responses[0]['Response 5'], '')

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_download_responses_returns_empty_csv_with_no_responses(
      self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': [],
        'Segmentation': [],
        'Response': []
    })

    raw_csv = survey_service.download_responses(surveyid=1234)
    self.assertEqual(raw_csv.strip(), 'Date,Control/Expose,Dimension 2')

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_get_brand_lift_results(self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': 4 * [datetime.datetime.now()],
        'Segmentation': ['expose', 'expose', 'control', 'control'],
        'Response': ['1:A', '1:A', '1:A', '1:B']
    })

    results = survey_service.get_brand_lift_results(1)
    q1_expose_lift = results[0][0]
    q1_control_lift = results[0][1]
    q1_lift = results[0][2]

    # Expose group has A for 2/2 of answers
    self.assertEqual(1, q1_expose_lift[0])
    # Expose group has B for 0/2 of answers
    self.assertEqual(0, q1_expose_lift[1])

    # Control group has A for 1/2 of answers
    self.assertEqual(0.5, q1_control_lift[0])
    # Control group has B for 1/2 of answers
    self.assertEqual(0.5, q1_control_lift[1])

    # Answer A is 100% more likely in expose group
    self.assertEqual(1, q1_lift[0])
    # Answer B is 100% less likely in expose group
    self.assertEqual(-1, q1_lift[1])

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_get_brand_lift_results_with_multi_question_responses(
      self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': 4 * [datetime.datetime.now()],
        'Segmentation': ['expose', 'expose', 'control', 'control'],
        'Response': ['1:A|2:A', '1:A|2:B', '1:A|2:B', '1:B|2:B']
    })

    results = survey_service.get_brand_lift_results(1)
    q2_expose_lift = results[1][0]
    q2_control_lift = results[1][1]
    q2_lift = results[1][2]

    # Expose group has A for 1/2 of answers
    self.assertEqual(0.5, q2_expose_lift[0])
    # Expose group has B for 1/2 of answers
    self.assertEqual(0.5, q2_expose_lift[1])

    # Control group has A for 0/2 of answers
    self.assertEqual(0, q2_control_lift[0])
    # Control group has B for 2/2 of answers
    self.assertEqual(1, q2_control_lift[1])

    # Answer A is infinitely more likely in expose group (since 0 in control)
    self.assertEqual(math.inf, q2_lift[0])
    # Answer B is 50% less likely in expose group
    self.assertEqual(-0.5, q2_lift[1])

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_get_brand_lift_results_with_no_responses(self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': [],
        'Segmentation': [],
        'Response': []
    })

    results = survey_service.get_brand_lift_results(1)

    self.assertEqual(results, [])

  @mock.patch.object(survey_service, 'get_survey_responses')
  def test_get_brand_lift_results_corrects_segment_names(self, responses_mock):
    responses_mock.return_value = pandas.DataFrame({
        'CreatedAt': 3 * [datetime.datetime.now()],
        'Segmentation': ['default_expose', 'default_expose', 'default_control'],
        'Response': ['1:A', '1:A', '1:B']
    })

    results = survey_service.get_brand_lift_results(1)
    q1_expose_lift = results[0][0]
    q1_control_lift = results[0][1]

    # Expose group has A for 2/2 of answers
    self.assertEqual(1, q1_expose_lift[0])
    # Expose group has B for 0/2 of answers
    self.assertEqual(0, q1_expose_lift[1])

    # Control group has A for 0/1 of answers
    self.assertEqual(0, q1_control_lift[0])
    # Control group has B for 1/1 of answers
    self.assertEqual(1, q1_control_lift[1])
