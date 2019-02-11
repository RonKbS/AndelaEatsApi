from tests.base_test_case import BaseTestCase
from datetime import datetime
from app.utils import daterange, current_time_by_zone, check_date_current_vs_date_for


class TestAuth(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_daterange(self):
        d1 = datetime.strptime('2019-01-01', '%Y-%m-%d')
        d2 = datetime.strptime('2019-01-05', '%Y-%m-%d')
        res_obj = daterange(d1, d2)
        datelist = [item for item in res_obj]

        self.assertEqual(len(datelist), 5)

    def test_current_time_by_time_zone_positive_timezone(self):
        res = current_time_by_zone('+3')

        raw_utc = datetime.utcnow().hour + 3
        result = raw_utc if raw_utc < 24 else raw_utc - 24
        self.assertEqual(res.hour, result)

    def test_current_time_by_time_zone_negative_timezone(self):
        resp = current_time_by_zone('-4')

        raw_utc = datetime.utcnow().hour - 4
        result = raw_utc if raw_utc < 24 else raw_utc + 24
        self.assertEqual(resp.hour, result)

    def test_check_date_current_vs_date_for_invalid(self):
        d1 = datetime.strptime('2019-01-01', '%Y-%m-%d')
        d2 = datetime.strptime('2019-01-05', '%Y-%m-%d')

        resp = check_date_current_vs_date_for(d1, d2)

        self.assertFalse(resp)

    def test_check_date_current_vs_date_for_valid(self):
        d2 = datetime.strptime('2019-01-01', '%Y-%m-%d')
        d1 = datetime.strptime('2019-01-05', '%Y-%m-%d')

        resp = check_date_current_vs_date_for(d1, d2)

        self.assertTrue(resp)



