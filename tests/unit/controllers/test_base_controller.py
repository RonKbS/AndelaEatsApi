"""Unit tests for  app.controllers.base_controller
"""
from datetime import datetime as dt
from unittest.mock import patch

from faker import Faker

from app.controllers.base_controller import BaseController
from app.utils.auth import Auth
from tests.base_test_case import BaseTestCase


class TestBaseController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_post_params_returns_non_empty_list(self):
        with self.app.app_context():
            fake = Faker()
            fake_key = fake.name()
            fake_value = fake.name()

            # modify request object of the request context
            self.request_context.request.data.add(fake_key, fake_value)

            base_controller = BaseController(self.request_context.request)

            assert base_controller.post_params(fake_key)[0] == fake_value

    def test_get_params_returns_empty_list(self):
        with self.app.app_context():
            fake = Faker()
            fake_key = fake.name()

            base_controller = BaseController(self.request_context.request)
            assert base_controller.get_params(fake_key)[0] is None

    def test_missing_required_returns_true(self):
        with self.app.app_context():
            base_controller = BaseController(self.request_context.request)

            assert base_controller.missing_required([None]) is True
            assert base_controller.missing_required(['']) is True

    def test_missing_response_returns_correct_response(self):
        with self.app.app_context():
            base_controller = BaseController(self.request_context.request)

            response = base_controller.missing_response()
            assert response.status_code == 400
            assert response.get_json()["msg"] == "Missing Required Parameters"

    def test_prettify_response_dates_returns_correctly(self):
        with self.app.app_context():
            created_at = dt.now()
            base_controller = BaseController(self.request_context.request)

            pretty_date = base_controller.prettify_response_dates(
                created_at
            )

            assert pretty_date.get('created_at') == created_at
            assert pretty_date.get('updated_at') is None
            assert pretty_date.get('date_pretty_short') == created_at.strftime('%b %d, %Y')
            assert pretty_date.get('date_pretty') == created_at.strftime('%B %d, %Y')

    @patch.object(Auth, 'get_token')
    def test_user_returns_valid_user(self, mock_get_token):
        with self.app.app_context():
            mock_get_token.return_value = self.get_valid_token()

            base_controller = BaseController(self.request_context.request)
            return_value = base_controller.user()

            assert return_value.get("id") == Auth.decode_token(self.get_valid_token())['UserInfo']["id"]
            assert return_value.get("first_name") == Auth.decode_token(self.get_valid_token())['UserInfo']["first_name"]
            assert return_value.get("last_name") == Auth.decode_token(self.get_valid_token())['UserInfo']["last_name"]
            assert return_value.get("firstName") == Auth.decode_token(self.get_valid_token())['UserInfo']["firstName"]
            assert return_value.get("lastName") == Auth.decode_token(self.get_valid_token())['UserInfo']["lastName"]
            assert return_value.get("email") == Auth.decode_token(self.get_valid_token())['UserInfo']["email"]
            assert return_value.get("name") == Auth.decode_token(self.get_valid_token())['UserInfo']["name"]
            assert return_value.get("picture") == Auth.decode_token(self.get_valid_token())['UserInfo']["picture"]
            assert return_value.get("roles") == Auth.decode_token(self.get_valid_token())['UserInfo']["roles"]

    def test_request_params_returns_json(self):
        with self.app.app_context():
            base_controller = BaseController(self.request_context.request)

            return_value = base_controller.request_params()

            assert return_value is None
