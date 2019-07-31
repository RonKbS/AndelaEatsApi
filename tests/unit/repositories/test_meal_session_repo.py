"""
Unit test for the meal session repo
"""
from tests.base_test_case import BaseTestCase
from app.models.meal_session import MealSession
from factories.meal_session_factory import MealSessionFactory
from factories.location_factory import LocationFactory
from app.repositories.meal_session_repo import MealSessionRepo


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
