from unittest.mock import patch
from datetime import datetime
from tests.base_test_case import BaseTestCase
from app.controllers import BotController
from factories import LocationFactory, MenuFactory
from tests.mock import (
    center_selected,
    date_selected,
    period_selected,
    action_selected_menu,
    action_selected_order,
    menu_list_rate,
)


class TestBotEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.bot_controller = BotController(self.request_context)
        self.menu_factory = MenuFactory

    def test_bot(self):
        with self.app.app_context():
            response = self.client().post(self.make_url(f'/bot/'), headers=self.headers())

            response_json = self.decode_from_json_string(response.data.decode('utf-8'))
            self.assert200(response)
            self.assertEqual(response_json['text'], 'Welcome To Andela Eats')
            self.assertEqual(type(response_json['attachments']), list)
            self.assertEqual(response_json['attachments'][0]['callback_id'], 'center_selector')
            self.assertEqual(response_json['attachments'][0]['attachment_type'], 'default')
            self.assertEqual(len(response_json['attachments'][0]['actions']), 0)

    @patch('app.controllers.bot_controller.LocationRepo')
    @patch('app.controllers.bot_controller.json.loads')
    @patch('app.controllers.bot_controller.BotController.get_menu_start_end_on')
    def test_interactions_after_selecting_location(self, mock_get_menu_start_end_on, mock_json_loads, mock_locationrepo_get):
        mock_json_loads.return_value = center_selected
        mock_get_menu_start_end_on.return_value = (datetime(2019, 2, 15), datetime(2019, 2, 15))
        mock_locationrepo_get.get.return_value = LocationFactory.create(id=1)

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_date(self, mock_json_loads):
        mock_json_loads.return_value = date_selected

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_period(self, mock_json_loads):
        mock_json_loads.return_value = period_selected

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_menu_list(self, mock_json_loads):
        mock_json_loads.return_value = action_selected_menu

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_order(self, mock_json_loads):
        mock_json_loads.return_value = action_selected_order

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menulist_rate(self, mock_json_loads):
        mock_json_loads.return_value = menu_list_rate

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_sunday(self, mock_get):

        mock_get.return_value = datetime.strptime('2019-02-10', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 11, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_sunday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-10 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 12).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_monday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-11', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())


        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 12, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_monday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-11 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 13).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_tuesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-12', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 13, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_tuesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-12 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 14).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_wednesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-13', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 14, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_wednesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-13 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 15).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_thursday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-14', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 15, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_thursday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-14 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 18).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 18).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_friday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-15', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 18, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 22, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_saturday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-16 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 18).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 22).date())