from tests.base_test_case import BaseTestCase
from app.models.meal_service import MealService
from factories.meal_service_factory import MealServiceFactory
from app.repositories.meal_service_repo import MealServiceRepo
from factories import UserRoleFactory, RoleFactory, UserFactory, LocationFactory, MealSessionFactory


class TestMealServiceRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = MealServiceRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_meal_service_method_returns_new_meal_service_object(self):
        role = RoleFactory.create()
        location = LocationFactory.create()
        user_role = UserRoleFactory.build(
            role_id=role.id,
            location=location
        )
        user = UserFactory.create(user_type=user_role)
        meal_session = MealSessionFactory(location=location)
        meal_service = MealServiceFactory( user=user, session=meal_session)
        new_meal_service = self.repo.new_meal_service(
            user_id=meal_service.user.id,
            session_id=meal_service.session.id,
            date=meal_service.date
        )
        self.assertIsInstance(new_meal_service, MealService)
        self.assertEqual(new_meal_service.user_id, meal_service.user_id)
        self.assertEqual(new_meal_service.session_id, meal_service.session_id)
        self.assertEqual(new_meal_service.date, meal_service.date)
