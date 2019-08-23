from tests.base_test_case import BaseTestCase
from app.models.user_role import UserRole
from factories.user_role_factory import UserRoleFactory
from factories.location_factory import LocationFactory
from app.repositories.user_role_repo import UserRoleRepo
from factories.role_factory import RoleFactory
from app.utils.redisset import RedisSet


class TestUserRoleRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = UserRoleRepo()
        self.redis_set = RedisSet()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_role_method_returns_new_user_role_object(self):
        role = RoleFactory.create()
        location = LocationFactory.create()
        user_role = UserRoleFactory.build(
            role_id=role.id,
            location=location
        )

        new_user_role = self.repo.new_user_role(
          user_role.role_id, user_role.user_id, user_role.location_id, user_role.email
        )

        self.assertIsInstance(new_user_role, UserRole)
        self.assertEqual(str(new_user_role.user_id), str(user_role.user_id))
        self.assertEqual(new_user_role.location.id, user_role.location.id)

    def test_exclude_works_user_role_instance(self):
        role = RoleFactory.create()
        location = LocationFactory.create()
        user_role = UserRoleFactory.build(
            role_id=role.id,
            location_id=location.id
        )

        new_user_role = self.repo.new_user_role(
          user_role.role_id, user_role.user_id, user_role.location_id, user_role.email
        )

        excluded_response = new_user_role.to_dict(exclude=["user_id"])

        self.assertFalse(excluded_response.get("user_id", False))

    def test_new_user_role_updates_cache(self):
        role = RoleFactory.create()
        location = LocationFactory.create()
        user_role = UserRoleFactory.build(
            role_id=role.id,
            location=location
        )

        self.repo.new_user_role(
          user_role.role_id,
          user_role.user_id,
          user_role.location_id,
          user_role.email
        )

        results = self.redis_set.get(user_role.email[0:1])
        self.assertTrue(user_role.email in results)

        results = self.redis_set.get(user_role.email[0:3])
        self.assertTrue(user_role.email in results)

        results = self.redis_set.get(user_role.email[0:5])
        self.assertTrue(user_role.email in results)

        results = self.redis_set.get(
            user_role.email[0:len(user_role.email)-1]
        )
        self.assertTrue(user_role.email in results)
