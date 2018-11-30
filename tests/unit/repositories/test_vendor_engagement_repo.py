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
		new_engagement = self.repo.new_vendor_engagement(engagement.vendor.id, engagement.start_date, engagement.location_id, engagement.end_date, 1)

		self.assertIsInstance(new_engagement, VendorEngagement)
		self.assertEqual(engagement.vendor_id, new_engagement.vendor_id)
		self.assertEqual(new_engagement.status, 1)
		self.assertEqual(engagement.start_date, new_engagement.start_date)
		self.assertEqual(engagement.end_date, new_engagement.end_date)

		