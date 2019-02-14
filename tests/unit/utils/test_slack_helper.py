""" Unit tests for the app.utils.slackhelper.py
"""
from unittest.mock import patch

from app.utils.slackhelper import SlackHelper
from tests.base_test_case import BaseTestCase


class TestSlackHelper(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch('app.utils.slackhelper.SlackClient.api_call')
    def test_post_message_works(
        self,
        mock_slack_api_call
    ):
        mock_slack_api_call.return_value = {
            "ok": "true",
            "channel": "Eat",
            "message": "Hi"
        }

        slack_helper = SlackHelper()

        assert slack_helper.post_message(msg="Hi", recipient="Roger").get("ok") == "true"
        assert slack_helper.post_message(msg="Hi", recipient="Roger").get("channel") == "Eat"
        assert slack_helper.post_message(msg="Hi", recipient="Roger").get("message") == "Hi"

    @patch('app.utils.slackhelper.SlackClient.api_call')
    def test_update_message_works(
        self,
        mock_slack_api_call
    ):
        mock_slack_api_call.return_value = {
            "ok": "true",
            "channel": "Eat",
            "text": "Hi again"
        }

        slack_helper = SlackHelper()

        assert slack_helper.update_message(msg="Hi", recipient="Roger").get("ok") == "true"
        assert slack_helper.update_message(msg="Hi", recipient="Roger").get("channel") == "Eat"
        assert slack_helper.update_message(msg="Hi", recipient="Roger").get("text") == "Hi again"

    @patch('app.utils.slackhelper.SlackClient.api_call')
    def test_user_info_works(
        self,
        mock_slack_api_call
    ):
        mock_slack_api_call.return_value = {
            "ok": "true",
            "user": {
                "id": "W012A3CDE",
                "name": "spengler",
                "deleted": "false",
                "is_admin": "true",
            }
        }

        slack_helper = SlackHelper()

        assert slack_helper.user_info("ururuirn4455").get("ok") == "true"
        assert slack_helper.user_info("ururuirn4455").get("user").get("id") == "W012A3CDE"
        assert slack_helper.user_info("ururuirn4455").get("user").get("name") == "spengler"
        assert slack_helper.user_info("ururuirn4455").get("user").get("deleted") == "false"
        assert slack_helper.user_info("ururuirn4455").get("user").get("is_admin") == "true"

    @patch('app.utils.slackhelper.SlackClient.api_call')
    def test_dialog_works(
        self,
        mock_slack_api_call
    ):
        mock_slack_api_call.return_value = {
            "ok": "true",
        }

        slack_helper = SlackHelper()

        dialog = {
            "callback_id": "ryde-46e2b0",
            "title": "Request a Ride",
            "submit_label": "Request",
            "state": "Limo",
            "elements": [
                {
                    "type": "text",
                    "label": "Pickup Location",
                    "name": "loc_origin"
                },
                {
                    "type": "text",
                    "label": "Dropoff Location",
                    "name": "loc_destination"
                }
            ]
        }

        assert slack_helper.dialog(dialog,"12.ab").get("ok") == "true"

    @patch('app.utils.slackhelper.SlackClient.api_call')
    def test_find_by_email_works(
        self,
        mock_slack_api_call
    ):
        slack_helper = SlackHelper()

        mock_slack_api_call.return_value = {
            "ok": "true",
            "user": {
                "id": "W012A3CDE",
                "name": "spengler",
                "deleted": "false",
                "is_admin": "true",
                "profile": {
                    "email":"eat@andela.com"
                }
            }
        }

        assert slack_helper.find_by_email("eats@andela.com").get("ok") == "true"
        assert slack_helper.find_by_email("eats@andela.com").get("user").get("id") == "W012A3CDE"
        assert slack_helper.find_by_email("eats@andela.com").get("user").get("name") == "spengler"
        assert slack_helper.find_by_email("eats@andela.com").get("user").get("deleted") == "false"
        assert slack_helper.find_by_email("eats@andela.com").get("user").get("is_admin") == "true"
        assert slack_helper.find_by_email("eats@andela.com").get("user").get("profile").get("email") == "eat@andela.com"
