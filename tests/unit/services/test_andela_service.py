"""Unit tests for app.services.andela.py
"""
from unittest.mock import patch

from app.services.andela import AndelaService
from tests.base_test_case import BaseTestCase


class TestAndelaService(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    @patch('app.services.andela.requests.request')
    def test_call_returns_json(
        self,
        mock_request_class
    ):
        service = AndelaService()

        response = self.construct_mock_response({"key":"value"}, 200)

        mock_request_class.return_value = response

        assert service.call("POST", "/andelserviceapi", email="user@andela.com").get("key") == "value"

    @patch('app.services.andela.requests.request')
    def test_call_returns_exception(
        self,
        mock_request_class
    ):
        service = AndelaService()

        response = self.construct_mock_response({"key":"value"}, 400)

        mock_request_class.return_value = response

        self.assertRaises(Exception, service.call, "POST", "/andelserviceapi", email="user@andela.com")

    @patch('app.services.andela.AndelaService.call')
    @patch('app.services.andela.Cache.get')
    def test_get_user_by_email_or_id_returns_none(
        self,
        mock_Cache_get_method,
        mock_AndelaService_call_method
    ):
        mock_Cache_get_method.return_value = None
        mock_AndelaService_call_method.return_value = {"values":""}

        service = AndelaService()

        user = service.get_user_by_email_or_id("123")

        assert user is None

    @patch('app.services.andela.Cache.get')
    @patch('app.services.andela.Cache.set')
    @patch('app.services.andela.AndelaService.call')
    def test_get_user_by_email_or_id_returns_user(
        self,
        mock_AndelaService_call_method,
        mock_Catch_set_method,
        mock_Catch_get_method
    ):
        mock_AndelaService_call_method.return_value = {"values":["user_1","user_2"]}
        mock_Catch_set_method.return_value = None
        mock_Catch_get_method.return_value = None

        service = AndelaService()

        user = service.get_user_by_email_or_id("user_1@email.com")

        assert user == "user_1"

    def test_get_user_by_email_or_id_returns_none_if_a_null_key_is_supplied(self):

        user = AndelaService().get_user_by_email_or_id(key=None)

        assert user is None
