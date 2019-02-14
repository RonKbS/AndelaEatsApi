from tests.base_test_case import BaseTestCase
from factories.vendor_engagement_factory import VendorEngagementFactory
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from datetime import datetime, timedelta
from app.utils.cron import Cron

class TestCron(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_run_24_hourly_method(self):

        end_date = (datetime.now() - timedelta(weeks=1)).date()

        new_engagement = VendorEngagementFactory.create(end_date=end_date)
        temp_engagement_id = new_engagement.id
        Cron(self.app).run_24_hourly()

        with self.app.app_context():
            engagement = VendorEngagementRepo().get(temp_engagement_id)

        self.assertEqual(engagement.status, 0)
