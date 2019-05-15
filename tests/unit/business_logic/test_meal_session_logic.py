"""Unit tests for the meal_session logic.
"""
import pytz
from datetime import datetime, time

from tests.base_test_case import BaseTestCase
from app.models.meal_session import MealSession
from factories.meal_session_factory import MealSessionFactory
from factories.location_factory import LocationFactory
from app.repositories.meal_session_repo import MealSessionRepo
from app.business_logic.meal_session.meal_session_logic import MealSessionLogic
from app.business_logic.meal_session.base_logic import BaseLogic


class TestMealSessionLogic(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.logic = MealSessionLogic()
        self.base_logic = BaseLogic()

    def test_check_two_values_are_greater_method_returns_true(self):
        return_value = self.logic.check_two_values_are_greater(2, 1)
        self.assertEqual(return_value, True)

    def test_check_two_values_are_greater_returns_false(self):
        return_value = self.logic.check_two_values_are_greater(1, 2)
        self.assertEqual(return_value, False)

    def test_check_two_values_are_greater_method_returns_false(self):
        return_value = self.logic.check_two_values_are_greater(1, 2)
        self.assertEqual(return_value, False)

    def test_format_preceding_returns_correct_formatting(self):
        return_value = self.logic.format_preceding(2)
        self.assertEqual(return_value, "02")

    def test_get_location_time_zone_raises_attribute_error(self):
        return_value = self.base_logic.get_location_time_zone(2)
        self.assertEqual(AttributeError, return_value)

    def test_get_location_time_zone_raises_unknownTimeZoneError(self):
        LocationFactory.create(id=2, name="Uganda")
        return_value = self.base_logic.get_location_time_zone(2)
        self.assertEqual(pytz.exceptions.UnknownTimeZoneError, return_value)

    def test_check_meal_session_exists_in_specified_time_method_returns_true(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        tz = pytz.timezone("Africa/Lagos")
        current_date = datetime.now(tz)

        first_meal_session = {
            "name": "lunch",
            "start_time": time(hour=13, minute=10),
            "end_time": time(hour=14, minute=40),
            "date_sent": datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            "location_id": new_location.id
        }

        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            location_id=new_location.id
        )

        return_value = self.logic.check_meal_session_exists_in_specified_time(**first_meal_session)
        self.assertEqual(return_value, True)

    def test_check_meal_session_exists_in_specified_time_method_returns_false(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        tz = pytz.timezone("Africa/Lagos")
        current_date = datetime.now(tz)

        first_meal_session = {
            "name": "lunch",
            "start_time": time(hour=12, minute=10),
            "end_time": time(hour=12, minute=40),
            "date_sent": datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            "location_id": new_location.id
        }

        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            location_id=new_location.id
        )

        return_value = self.logic.check_meal_session_exists_in_specified_time(**first_meal_session)
        self.assertEqual(return_value, False)

    def test_check_encloses_already_existing_meal_sessions_returns_true(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        tz = pytz.timezone("Africa/Lagos")
        current_date = datetime.now(tz)

        first_meal_session = {
            "name": "lunch",
            "start_time": time(hour=12, minute=10),
            "end_time": time(hour=14, minute=40),
            "date_sent": datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            "location_id": new_location.id
        }

        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            location_id=new_location.id
        )

        return_value = self.logic.check_encloses_already_existing_meal_sessions(**first_meal_session)
        self.assertEqual(return_value, True)

    def test_check_encloses_already_existing_meal_sessions_returns_false(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        tz = pytz.timezone("Africa/Lagos")
        current_date = datetime.now(tz)

        first_meal_session = {
            "name": "lunch",
            "start_time": time(hour=12, minute=10),
            "end_time": time(hour=12, minute=40),
            "date_sent": datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            "location_id": new_location.id
        }

        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            location_id=new_location.id
        )

        return_value = self.logic.check_encloses_already_existing_meal_sessions(**first_meal_session)
        self.assertEqual(return_value, False)
