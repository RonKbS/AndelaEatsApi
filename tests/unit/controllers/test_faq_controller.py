'''Unit tests for faq_controller module.
'''

from unittest.mock import patch

from app.controllers.faq_controller import FaqController
from app.repositories.faq_repo import FaqRepo
from factories.faq_factory import FaqFactory
from tests.base_test_case import BaseTestCase
from sqlalchemy.exc import DataError


class TestFaqController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_list_faq_method_captures_invalid_dates(self):

        with self.app.app_context():
            faq_controller = FaqController(self.request_context)

            response = faq_controller.list_faqs(created_at='2019-04-04-invalid')

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'], 'Bad Request - created_at should be valid date. Format: YYYY-MM-DD'
            )

    def test_list_faq_method_returns_faqs(self):
        with self.app.app_context():
            new_faq = FaqFactory.create()
            faq_controller = FaqController(self.request_context)

            response = faq_controller.list_faqs()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], 'OK')
            self.assertEqual(
                response.get_json()['payload']['faqs'][0]['id'], new_faq.id
            )

    @patch.object(FaqRepo, 'filter_by')
    def test_list_faq_method_captures_invalid_category_values(self, mock_filter_by):
        with self.app.app_context():
            mock_filter_by.side_effect = DataError('statement', 'params', 'orig')

            faq_controller = FaqController(self.request_context)

            response = faq_controller.list_faqs(category='2019-04-04-invalid')

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'], "Category should be one of these values ['user_faq', 'admin_faq']"
            )

    @patch.object(FaqController, 'request_params')
    def test_create_faq_method_succeeds(self, mock_request_params):
        with self.app.app_context():
            faq = FaqFactory.build()

            mock_request_params.return_value = [faq.category, faq.question, faq.answer]

            faq_controller = FaqController(self.request_context)

            response = faq_controller.create_faq()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json()['msg'], 'OK')
            self.assertEqual(
                response.get_json()['payload']['faq']['question'], faq.question
            )
            self.assertEqual(
                response.get_json()['payload']['faq']['answer'], faq.answer
            )

    @patch.object(FaqController, 'request_params')
    def test_create_faq_method_handles_duplicate_faq_creation(self, mock_request_params):
        with self.app.app_context():
            faq = FaqFactory()

            mock_request_params.return_value = [faq.category, faq.question, faq.answer]

            faq_controller = FaqController(self.request_context)

            response = faq_controller.create_faq()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'],
                "Question '{}' already exists".format(faq.question)
            )

    @patch.object(FaqController, 'request_params_dict')
    def test_update_faq_method_succeeds(self, mock_request_params_dict):
        with self.app.app_context():
            faq = FaqFactory()
            update_faq_info = FaqFactory.build()

            mock_request_params_dict.return_value = {'question': update_faq_info.question}

            faq_controller = FaqController(self.request_context)

            response = faq_controller.update_faq(faq.id)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json()['msg'], 'OK')
            self.assertEqual(response.get_json()['payload']['faq']['question'], update_faq_info.question)

    @patch.object(FaqController, 'request_params_dict')
    def test_update_faq_method_handle_not_found(self, mock_request_params_dict):
        with self.app.app_context():
            faq = FaqFactory()
            update_faq_info = FaqFactory.build()

            mock_request_params_dict.return_value = {'question': update_faq_info.question}

            faq_controller = FaqController(self.request_context)

            response = faq_controller.update_faq(1000)

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json()['msg'], 'FAQ Not Found')
