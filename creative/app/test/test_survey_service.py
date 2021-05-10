from unittest import TestCase
from unittest.mock import Mock, call, patch
import os
import survey_service
import survey_collection

class TestSurveyService(TestCase):

    def test_get_all(self):
        # given
        survey_collection.get_all = Mock()
        # when
        survey_service.get_all()
        # then
        assert survey_collection.get_all.call_count == 1

    def test_get_by_id(self):
        # given
        survey_collection.get_by_id = Mock()
        # when
        survey_service.get_by_id('mockSurveyId')
        # then
        survey_collection.get_by_id.assert_called_once_with('mockSurveyId')

    def test_get_doc_by_id(self):
        # given
        survey_collection.get_doc_by_id = Mock()
        # when
        survey_service.get_doc_by_id('mockSurveyId')
        # then
        survey_collection.get_doc_by_id.assert_called_once_with('mockSurveyId')

    def test_delete_by_id(self):
        # given
        survey_collection.delete_by_id = Mock()
        # when
        survey_service.delete_by_id('mockSurveyId')
        # then
        survey_collection.delete_by_id.assert_called_once_with('mockSurveyId')

    #TODO 
    #def test_create(self):

    #TODO
    #def test_update_by_id(self):

    #TODO
    #def test_set_form_data(self):

    #TODO
    #def test_zip_file(self):

    #TODO
    #def test_zip_dir(self):

    #TODO
    #def test_write_html_template(self):

    #TODO
    #def test_get_html_template(self):

    def test_delete_tmp_zip_files(self):
        # given
        filename = "mock-file-name"
        seg_types = ["default_control","default_expose"]
        os.remove = Mock()

        # when
        survey_service.delete_tmp_zip_files(filename, seg_types)

        # then
        expected_calls = [
            call("mock-file-name_default_control.zip"),
            call("mock-file-name_default_expose.zip"),
            call("mock-file-name.zip")
        ]
        os.remove.assert_has_calls(expected_calls)
        assert os.remove.call_count == 3

    #TODO 
    #def test_get_question_json(self):

    #TODO
    #def download_results(self):