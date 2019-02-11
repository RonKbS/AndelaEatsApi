from unittest.mock import Mock, patch
from datetime import datetime
from tests.base_test_case import BaseTestCase
from app.controllers import BotController
from factories import LocationFactory


class TestBotEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.bot_controller = BotController(self.request_context)

    def test_bot(self):
        with self.app.app_context():
            response = self.bot_controller.bot()

            response_json = self.decode_from_json_string(response.data.decode('utf-8'))
            self.assert200(response)
            self.assertEqual(response_json['text'], 'Welcome To Andela Eats')
            self.assertEqual(type(response_json['attachments']), list)
            self.assertEqual(response_json['attachments'][0]['callback_id'], 'center_selector')
            self.assertEqual(response_json['attachments'][0]['attachment_type'], 'default')
            self.assertEqual(len(response_json['attachments'][0]['actions']), 0)


    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_sunday(self, mock_get):

        mock_get.return_value = datetime.strptime('2019-02-10', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 11, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_sunday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-10 16:01', '%Y-%m-%d %H:%M')

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
        mock_get.return_value = datetime.strptime('2019-02-11 16:01', '%Y-%m-%d %H:%M')

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
        mock_get.return_value = datetime.strptime('2019-02-12 16:01', '%Y-%m-%d %H:%M')

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
        mock_get.return_value = datetime.strptime('2019-02-13 16:01', '%Y-%m-%d %H:%M')

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
        mock_get.return_value = datetime.strptime('2019-02-14 16:01', '%Y-%m-%d %H:%M')

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
        mock_get.return_value = datetime.strptime('2019-02-16 16:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 18).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 22).date())