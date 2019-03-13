import datetime
from tests.base_test_case import BaseTestCase
from factories import VendorRatingFactory


class TestReportsEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_report(self):
        recent_date = datetime.datetime.now().date() + datetime.timedelta(7)

        ratings = VendorRatingFactory.create_batch(3, service_date=recent_date)
        response = self.client().get(self.make_url('/reports/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 200)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertJSONKeyPresent(response_json['payload'][0], 'vendor')
        self.assertEqual(type(payload), list)
