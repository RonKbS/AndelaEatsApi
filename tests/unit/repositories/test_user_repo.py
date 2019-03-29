from tests.base_test_case import BaseTestCase
from app.models.user import User
from factories.user_factory import UserFactory
from app.repositories.user_repo import UserRepo


class TestUserRoleRepo(BaseTestCase):

  def setUp(self):
    self.BaseSetUp()
    self.repo = UserRepo()

  def test_new_user_method_returns_new_user_object(self):
    user = UserFactory.build()

    new_user = self.repo.new_user(user.slack_id, user.first_name, user.last_name, user.user_id, user.image_url)
    self.assertIsInstance(new_user, User)
    self.assertEqual(str(new_user.slack_id), str(user.slack_id))
    self.assertEqual(new_user.first_name, user.first_name)
    self.assertEqual(new_user.image_url, user.image_url)
