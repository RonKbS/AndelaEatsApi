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

	def test_get_range_action_paginated_options_method_return_paginated_results(self):
		activity = ActivityFactory.build()
		new_activity = self.repo.new_activity(
			activity.module_name, activity.ip_address, activity.user_id, activity.action_type,
			activity.action_details, activity.channel
		)

		paginated_result = self.repo.get_range_action_paginated_options(
			new_activity.action_type, new_activity.created_at, new_activity.created_at
		)

		self.assertIsInstance(paginated_result.items[0], Activity)
		self.assertEqual(paginated_result.items[0], new_activity)

	def test_get_range_paginated_options_method_return_paginated_results(self):
		activity = ActivityFactory.build()
		new_activity = self.repo.new_activity(
			activity.module_name, activity.ip_address, activity.user_id, activity.action_type,
			activity.action_details, activity.channel
		)

		paginated_result = self.repo.get_range_paginated_options(
			new_activity.created_at, new_activity.created_at
		)

		self.assertIsInstance(paginated_result.items[0], Activity)
		self.assertEqual(paginated_result.items[0], new_activity)
