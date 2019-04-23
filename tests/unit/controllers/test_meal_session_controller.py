"""
Unit tests for the meal_session_controller
"""

from unittest.mock import patch
from datetime import datetime
import pytz

from app.controllers.meal_session_controller import MealSessionController
from app.repositories.meal_session_repo import MealSessionRepo
from app.business_logic.meal_session.meal_session_logic import MealSessionLogic
from factories.location_factory import LocationFactory
from tests.base_test_case import BaseTestCase


class TestMealSessionController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.current_date = datetime.now()

    @patch.object(MealSessionController, 'request_params')
    def test_create_session_method_succeeds(self, mock_request_params):
        with self.app.app_context():

            new_location = LocationFactory.create(id=1, name="Lagos")

            tz = pytz.timezone("Africa/Lagos")
            self.current_date = datetime.now(tz)

            mock_request_params_return_value = [
                "lunch",
                "13:10",
                "14:45",
                "".join([
                    MealSessionLogic.format_preceding(self.current_date.year),
                    "-",
                    MealSessionLogic.format_preceding(self.current_date.month),
                    "-",
                    MealSessionLogic.format_preceding(self.current_date.day)]
                ),
                new_location.id
            ]

            mock_request_params.return_value = mock_request_params_return_value

            meal_session_controller = MealSessionController(self.request_context)

            response = meal_session_controller.create_session()

            response_json = self.decode_from_json_string(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_json['msg'], 'OK')
            self.assertEqual(
                response_json['payload']['mealSession']['name'],
                mock_request_params_return_value[0])
            self.assertEqual(
                (response_json['payload']['mealSession']['startTime'])[:-3],
                mock_request_params_return_value[1])
            self.assertEqual(
                (response_json['payload']['mealSession']['stopTime'])[:-3],
                mock_request_params_return_value[2])
            self.assertEqual(
                response_json['payload']['mealSession']['date'],
                mock_request_params_return_value[3])
            self.assertEqual(
                response_json['payload']['mealSession']['locationId'],
                mock_request_params_return_value[4])
