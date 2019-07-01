from tests.base_test_case import BaseTestCase
from app.models.vendor_engagement import VendorEngagement
from factories.vendor_engagement_factory import VendorEngagementFactory
from app.repositories.vendor_engagement_repo import VendorEngagementRepo

class TestVendorEngagementRepo(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		self.repo = VendorEngagementRepo()
		
	def test_new_vendor_engagement_method_returns_new_vendor_engagement_object(self):
		engagement = VendorEngagementFactory.build()
		new_engagement = self.repo.new_vendor_engagement(engagement.vendor.id, engagement.start_date, engagement.location_id, engagement.end_date, 1,1)

		self.assertIsInstance(new_engagement, VendorEngagement)
		self.assertEqual(engagement.vendor_id, new_engagement.vendor_id)
		self.assertEqual(new_engagement.status, 1)
		self.assertEqual(engagement.start_date, new_engagement.start_date)
		self.assertEqual(engagement.end_date, new_engagement.end_date)

	def test_get_existing_engagement_when_engagment_exists(self):
		engagement = VendorEngagementFactory.build()
		self.repo.new_vendor_engagement(engagement.vendor.id, engagement.start_date,
														 engagement.location_id, engagement.end_date, 1, 1)

		count = self.repo.get_existing_engagement(engagement.start_date, engagement.end_date)

		self.assertEqual(count, 1)

	def test_get_existing_engagement_when_engagment_does_not_exists(self):
		engagement = VendorEngagementFactory.build()

		count = self.repo.get_existing_engagement(engagement.start_date, engagement.end_date)

		self.assertEqual(count, 0)

	def test_get_engagement_by_date_when_engagment_does_exists(self):
		engagement = VendorEngagementFactory.build()

		new_engagement = self.repo.new_vendor_engagement(engagement.vendor.id, engagement.start_date,
										engagement.location_id, engagement.end_date, 1, 1)

		paginated_result = self.repo.get_engagement_by_date()

		self.assertIsInstance(paginated_result.items[0], VendorEngagement)
		self.assertEqual(paginated_result.items[0], new_engagement)

	def test_new_vendor_engagement_raises_exception_with_invalid_date_format(self):
		engagement = VendorEngagementFactory.build()

		invalid_start_date = 'invalid date format'

		with self.assertRaises(Exception) as e:
			self.repo.new_vendor_engagement(engagement.vendor.id, invalid_start_date,
														 engagement.location_id, engagement.end_date, 1, 1)


		