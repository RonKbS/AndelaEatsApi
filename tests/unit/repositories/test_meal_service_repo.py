from tests.base_test_case import BaseTestCase
from app.models.meal_service import MealService
from factories.meal_service_factory import MealServiceFactory
from app.repositories.meal_service_repo import MealServiceRepo


class TestMealServiceRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = MealServiceRepo()

    def test_new_meal_service_method_returns_new_meal_service_object(self):

        meal_service = MealServiceFactory.build()

        new_meal_service = self.repo.new_meal_service(
                user_id=meal_service.user_id, session_id=meal_service.session_id, date=meal_service.date
            )

        self.assertIsInstance(new_meal_service, MealService)
        self.assertEqual(new_meal_service.user_id, meal_service.user_id)
        self.assertEqual(new_meal_service.session_id, meal_service.session_id)
        self.assertEqual(new_meal_service.date, meal_service.date)
