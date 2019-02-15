from tests.base_test_case import BaseTestCase
from datetime import datetime
from unittest.mock import Mock, patch
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

    @patch('app.utils.datetime')
    def test_current_time_by_time_zone_positive_timezone(self, mock_current_time):
        mock_current_time.utcnow = Mock(
            return_value=datetime(2019, 2, 15, 6, 0, 0))
        res = current_time_by_zone('+3')

        self.assertEqual(res.hour, 9)

    @patch('app.utils.datetime')
    def test_current_time_by_time_zone_negative_timezone(self, mock_current_time):
        mock_current_time.utcnow = Mock(
             return_value=datetime(2019, 2, 15, 6, 0, 0))
        resp = current_time_by_zone('-4')

        self.assertEqual(resp.hour, 2)

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



