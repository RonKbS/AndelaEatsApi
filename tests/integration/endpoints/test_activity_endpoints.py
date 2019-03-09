from tests.base_test_case import BaseTestCase
from factories.activity_factory import ActivityFactory
import datetime


class TestActivityEndpoints(BaseTestCase):
    """Test class for Activity endpoints"""

    def setUp(self):
        self.BaseSetUp()

    def test_get_range_correct_date_range_succeeds(self):

        activity = ActivityFactory.create()

        create_date = activity.created_at.date()
        create_date_ahead = activity.created_at.date() + datetime.timedelta(days=3)

        first_date = str(create_date.year) + "-" + \
                     str(create_date.month).zfill(2) + \
                     "-" + str(create_date.day).zfill(2)

        second_date = str(create_date_ahead.year) + "-"\
                      + str(create_date_ahead.month).zfill(2) + "-" + \
                      str(create_date_ahead.day).zfill(2)

        response = self.client().get(
            self.make_url("/activities/range"),
            query_string={'date_range': first_date + ":" + second_date}, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['activities'][0]['id'], activity.id)
        self.assertEqual(response_json['payload']['activities'][0]['isDeleted'], activity.is_deleted)
        self.assertEqual(response_json['payload']['activities'][0]['ipAddress'], activity.ip_address)
        self.assertEqual(response_json['payload']['activities'][0]['actionType'], activity.action_type)
        self.assertEqual(response_json['payload']['activities'][0]['actionDetails'], activity.action_details)
        self.assertEqual(response_json['payload']['activities'][0]['channel'], activity.channel)

    def test_get_range_with_wrong_date_range_order_fails(self):

        activity = ActivityFactory.create()

        create_date = activity.created_at.date()
        create_date_ahead = activity.created_at.date() + datetime.timedelta(days=3)

        first_date = str(create_date.year) + "-" + \
                     str(create_date.month).zfill(2) + \
                     "-" + str(create_date.day).zfill(2)

        second_date = str(create_date_ahead.year) + "-"\
                      + str(create_date_ahead.month).zfill(2) + "-" + \
                      str(create_date_ahead.day).zfill(2)

        response = self.client().get(
            self.make_url("/activities/range"),
            query_string={'date_range': second_date + ":" + first_date}, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("Bad Request - Start Date", response_json['msg'])

    def test_get_range_with_invalid_dates_fails(self):

        response = self.client().get(
            self.make_url("/activities/range"),
            query_string={'date_range': "inndaf" + ":" + "dfaeavd"}, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("should be valid dates", response_json['msg'])

    def test_get_range_incorrect_range_separator_fails(self):

        response = self.client().get(
            self.make_url("/activities/range"),
            query_string={'date_range': "inndaf dfaeavd"}, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("Bad Request - There must be a `:` separating the dates", response_json['msg'])

    def test_get_range_no_provision_of_query_params_fails(self):

        response = self.client().get(
            self.make_url("/activities/range"), headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("Bad Request - Request Must be Properly Formatted", response_json['msg'])

    def test_get_action_range_correct_values_succeeds(self):

        activity = ActivityFactory.create()

        create_date = activity.created_at.date()
        create_date_ahead = activity.created_at.date() + datetime.timedelta(days=3)

        first_date = str(create_date.year) + "-" + \
                     str(create_date.month).zfill(2) + \
                     "-" + str(create_date.day).zfill(2)

        second_date = str(create_date_ahead.year) + "-"\
                      + str(create_date_ahead.month).zfill(2) + "-" + \
                      str(create_date_ahead.day).zfill(2)

        response = self.client().get(
            self.make_url("/activities/action_range"),
            query_string={
                'date_range': first_date + ":" + second_date,
                'action_type': 'create'
            }, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['activities'][0]['id'], activity.id)
        self.assertEqual(response_json['payload']['activities'][0]['isDeleted'], activity.is_deleted)
        self.assertEqual(response_json['payload']['activities'][0]['ipAddress'], activity.ip_address)
        self.assertEqual(response_json['payload']['activities'][0]['actionType'], activity.action_type)
        self.assertEqual(response_json['payload']['activities'][0]['actionDetails'], activity.action_details)
        self.assertEqual(response_json['payload']['activities'][0]['channel'], activity.channel)

    def test_get_action_range_invalid_enum_options_fails(self):

        activity = ActivityFactory.create()

        create_date = activity.created_at.date()
        create_date_ahead = activity.created_at.date() + datetime.timedelta(days=3)

        first_date = str(create_date.year) + "-" + \
                     str(create_date.month).zfill(2) + \
                     "-" + str(create_date.day).zfill(2)

        second_date = str(create_date_ahead.year) + "-"\
                      + str(create_date_ahead.month).zfill(2) + "-" + \
                      str(create_date_ahead.day).zfill(2)

        response = self.client().get(
            self.make_url("/activities/action_range"),
            query_string={
                'date_range': first_date + ":" + second_date,
                'action_type': 'insert'  # an invalid enum option
            }, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("can only have options:", response_json['msg'])

    def test_get_action_range_required_query_param_not_supplied_fails(self):

        response = self.client().get(
            self.make_url("/activities/action_range"),
            query_string={
                'date_range': '2019-01-01' + ":" + '2019-10-10',
                'action_typq': 'insert'  # Supplying a non existing query parameter ie action_typq
            }, headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertIn("Bad Request - action_type is required", response_json['msg'])
