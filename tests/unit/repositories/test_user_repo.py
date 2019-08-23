from tests.base_test_case import BaseTestCase
from app.models.user import User
from factories.user_factory import UserFactory
from factories.user_role_factory import UserRoleFactory
from factories.role_factory import RoleFactory
from app.repositories.user_repo import UserRepo


class TestUserRoleRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = UserRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_method_returns_new_user_object(self):
        user = UserFactory.build(slack_id='-Lcel5YdCjsvKOG3zsrV')
        role = RoleFactory()
        user_role = UserRoleFactory(role_id=role.id)

        new_user = self.repo.new_user(user.first_name, user.last_name, user.image_url,
                                      user_id=user.user_id,  slack_id=user.slack_id, user_type=user_role)
        self.assertIsInstance(new_user, User)
        self.assertEqual(str(new_user.slack_id), str(user.slack_id))
        self.assertEqual(new_user.first_name, user.first_name)
        self.assertEqual(new_user.image_url, user.image_url)
