"""Unit tests for the about_controller module.
"""

from unittest.mock import patch
import base64

from app.controllers.base_controller import BaseController
from app.controllers.about_controller import AboutController
from factories.about_factory import AboutFactory
from tests.base_test_case import BaseTestCase


class TestAboutController(BaseTestCase):
    """
    Test class for the About controller
    """

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(BaseController, 'request_params')
    def test_create_or_modify_about_page_method_creates_new_record(self, mock_request_params):
        """
        Test the create_or_modify_about_page method creates a new record if it does not find
        any record in the About table
        :param mock_request_params: this is a mock of the request_params method of the BaseController
                                    to return a list with data sent through JSON
        :return: Nothing
        """
        with self.app.app_context():
            mock_request_params.return_value = ["<html><head meta=\"utf-8\"></head></html>"]
            about_controller = AboutController(self.request_context)

            response = about_controller.create_or_modify_about_page()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.get_json()['msg'], 'OK'
            )
            self.assertEqual(
                response.get_json()['payload']['data']['isDeleted'], False
            )
            self.assertIn(
                "<head meta=\"utf-8\">",
                response.get_json()['payload']['data']['details']
            )
            self.assertIsInstance(response.get_json()['payload']['data']['timestamps'], dict)

    @patch.object(BaseController, 'request_params')
    def test_create_or_modify_about_page_method_modifies_existing_record(self, mock_request_params):
        """
        Test the create_or_modify_about_page method modifies the only existing record in the About table
        :param mock_request_params: this is a mock of the request_params method of the BaseController
                                    to return a list with data sent through JSON
        :return: Nothing
        """
        with self.app.app_context():
            AboutFactory.create(
                details=base64.b64encode("<html><head meta=\"utf-10\"></head></html>".encode('utf-8'))
            )
            mock_request_params.return_value = ["<html><head meta=\"utf-8\"></head></html>"]
            about_controller = AboutController(self.request_context)

            response = about_controller.create_or_modify_about_page()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.get_json()['msg'], 'OK'
            )
            self.assertEqual(
                response.get_json()['payload']['data']['isDeleted'], False
            )
            self.assertIn(
                "<head meta=\"utf-8\">",
                response.get_json()['payload']['data']['details']
            )
            self.assertIsInstance(response.get_json()['payload']['data']['timestamps'], dict)

    def test_get_about_page_method_returns_empty_record(self):
        """
        Test the get_about_page method returns nothing when their is no record
        :return: None
        """
        with self.app.app_context():
            about_controller = AboutController(self.request_context)

            response = about_controller.get_about_page()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json()['msg'], 'OK'
            )
            self.assertEqual(
                response.get_json()['payload']['data'], {}
            )

            self.assertIsInstance(response.get_json()['payload']['data'], dict)

    def test_get_about_page_method_returns_existing_record(self):
        """
        Test get_about_page_method returns existing records for the about Page
        :return: None
        """
        with self.app.app_context():
            AboutFactory.create(
                details=base64.b64encode("<html><head meta=\"utf-8\"></head></html>".encode('utf-8'))
            )
            about_controller = AboutController(self.request_context)

            response = about_controller.get_about_page()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json()['msg'], 'OK'
            )
            self.assertEqual(
                response.get_json()['payload']['data']['isDeleted'], False
            )
            self.assertIn(
                "<head meta=\"utf-8\">",
                response.get_json()['payload']['data']['details']
            )
            self.assertIsInstance(response.get_json()['payload']['data']['timestamps'], dict)
