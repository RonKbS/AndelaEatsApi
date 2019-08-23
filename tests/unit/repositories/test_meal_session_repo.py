"""
Unit test for the meal session repo
"""
from datetime import time, date

from app.models.meal_session import MealSession
from app.repositories.location_repo import LocationRepo
from factories.meal_session_factory import MealSessionFactory
from factories.location_factory import LocationFactory
from app.repositories.meal_session_repo import MealSessionRepo
from factories.meal_session_factory import MealSessionFactory
from tests.base_test_case import BaseTestCase


class TestMealSessionRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = MealSessionRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_meal_session_method_returns_new_meal_session_object(self):
        location = LocationFactory()
        meal_session = MealSessionFactory(location=location)

        new_meal_session = self.repo.new_meal_session(
            name=meal_session.name,
            start_time=meal_session.start_time,
            stop_time=meal_session.stop_time,
            date=meal_session.date,
            location_id=meal_session.location.id
        )

        self.assertIsInstance(new_meal_session, MealSession)
        self.assertEqual(new_meal_session.location_id, meal_session.location_id)
        self.assertEqual(new_meal_session.name, meal_session.name)
        self.assertEqual(new_meal_session.start_time, meal_session.start_time)
        self.assertEqual(new_meal_session.stop_time, meal_session.stop_time)

    def test_get_meal_sessions(self):
        # Arrange
        mock_location_id = LocationRepo().new_location('Lagos', '+1').id
        MealSessionRepo().new_meal_session(
            name='breakfast',
            start_time=time(hour=8, minute=0, second=0),
            stop_time=time(hour=9, minute=0, second=0),
            date=date.today(),
            location_id=mock_location_id)
        MealSessionRepo().new_meal_session(
            name='lunch',
            start_time=time(hour=12, minute=30, second=0),
            stop_time=time(hour=14, minute=0, second=0),
            date=date.today(),
            location_id=mock_location_id)

        # Act
        result = MealSessionRepo().get_by_date_location(
            meal_date=date.today(), location_id=mock_location_id)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

