from tests.base_test_case import BaseTestCase
from app.models.activity import Activity
from factories.activity_factory import ActivityFactory
from app.repositories.activity_repo import ActivityRepo


class TestMenuRepo(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		self.repo = ActivityRepo()

	def test_new_activity_method_returns_new_activity_object(self):
		activity = ActivityFactory.build()
		new_activity = self.repo.new_activity(
			activity.module_name, activity.ip_address, activity.user_id, activity.action_type,
			activity.action_details, activity.channel
		)

		self.assertIsInstance(new_activity, Activity)
		self.assertEqual(new_activity.module_name, activity.module_name)
		self.assertEqual(new_activity.ip_address, activity.ip_address)
		self.assertEqual(new_activity.user_id, activity.user_id)
