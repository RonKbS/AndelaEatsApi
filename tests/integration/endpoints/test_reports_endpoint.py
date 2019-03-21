import datetime
from tests.base_test_case import BaseTestCase
from factories import OrderFactory, VendorRatingFactory, VendorFactory, VendorEngagementFactory, MenuFactory

class TestReportsEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_report(self):
        recent_date = datetime.datetime.now().date() + datetime.timedelta(7)

        VendorRatingFactory.create_batch(3, service_date=recent_date)
        response = self.client().get(self.make_url('/reports/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 200)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(type(payload), list)

    def test_report_fails_for_start_date_less_than_endDate(self):
        recent_date = datetime.datetime.now().date() + datetime.timedelta(7)

        VendorRatingFactory.create_batch(3, service_date=recent_date)
        response = self.client().get(self.make_url('/reports/?start_date=2019-03-10&end_date=2019-03-12'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Start date must not be less than end date')

    def test_all_vendor_comparison(self):
        vendor = VendorFactory.create()
        engagement = VendorEngagementFactory.create(vendor_id=vendor.id)
        menu = MenuFactory.create(vendor_engagement_id=engagement.id)
        OrderFactory.create(menu_id=menu.id)
        OrderFactory.create(menu_id=menu.id - 1)

        recent_date = datetime.datetime.now().date() + datetime.timedelta(7)

        VendorRatingFactory.create_batch(3, service_date=recent_date)
        response = self.client().get(self.make_url('/reports/?all_vendor_comparison=true'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 200)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(type(payload), list)

