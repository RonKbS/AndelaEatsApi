from datetime import date
from datetime import time
from unittest.mock import patch

from app.controllers.bot_controller import BotController
from app.models import MealItem
from app.models.menu import Menu
from app.repositories.location_repo import LocationRepo
from app.repositories.meal_item_repo import MealItemRepo
from app.repositories.meal_session_repo import MealSessionRepo
from app.repositories.menu_repo import MenuRepo
from tests.base_test_case import BaseTestCase
from factories.location_factory import LocationFactory


class TestBotController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        LocationFactory.create(name='Lagos', zone='+1')
        LocationFactory.create(name='Kampala', zone='+3')
        LocationFactory.create(name='Kigali', zone='+2')
        LocationFactory.create(name='Nairobi', zone='+3')

    def tearDown(self):
        self.BaseTearDown()

    def test_bot(self):
        with self.app.app_context():
            # Arrange
            locations = [
                ('Kampala', '+3'),
                ('Kigali', '+2'),
                ('Lagos', '+1'),
                ('Nairobi', '+3'), ]

            for location in locations:
                LocationFactory.create(
                    name=location[0],
                    zone=location[1]
                )

            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.bot()

            # Assert
            result_json = result.get_json()
            if result.status_code != 200:
                raise AssertionError()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != 'Welcome To Andela Eats':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id']\
                    != 'center_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()

            for i in range(len(locations)):
                if not any(
                        loc.get('text') == locations[i][0]
                        for loc in result_json['attachments'][0]['actions']):
                    raise AssertionError()

    def test_center_selection(self):
        # Arrange
        with self.app.app_context():
            mock_location = LocationRepo().get_unpaginated(name='Kampala')[0]
            mock_payload = {
                'actions': [{
                    'value': mock_location.id
                }]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_center_selection(mock_payload)

            # Assert
            result_json = result.get_json()
            if result.status_code != 200:
                raise AssertionError()
            if result_json['text'] != 'Select Date':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['text'] != '':
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] != 'day_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()

    def test_day_selection(self):
        with self.app.app_context():
            # Arrange
            mock_location_id = LocationRepo()\
                .get_unpaginated(name='Lagos')[0].id
            MealSessionRepo().new_meal_session(
                name='breakfast',
                start_time=time(hour=8, minute=0, second=0),
                stop_time=time(hour=10, minute=0, second=0),
                date=date.today(),
                location_id=mock_location_id)
            MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=30, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                date=date.today(),
                location_id=mock_location_id)
            mock_date = date.today().strftime('%Y-%m-%d')
            mock_payload = {
                'actions': [
                    {
                        'value': f"{mock_date}_{mock_location_id}"}
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_day_selection(mock_payload)

            # Assert
            result_json = result.get_json()
            if result.status_code != 200:
                raise AssertionError()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != 'Select Meal Period':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] \
                    != 'period_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if len(result_json['attachments'][0]['actions']) != 2:
                raise AssertionError()

    def test_handle_period_selection(self):
        with self.app.app_context():
            # Arrange
            m_date = date.today().strftime('%Y-%m-%d')
            m_location_id = LocationRepo().get_unpaginated(name='Lagos')[0].id
            m_meal_session = MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=20, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                location_id=m_location_id,
                date=m_date
            )
            m_value = f'{m_meal_session.name}_{m_date}_{m_location_id}'
            m_payload = {
                'actions': [
                    {
                        'value': m_value
                    }
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_period_selection(payload=m_payload)

            # Assert
            if result.status_code != 200:
                raise AssertionError()
            result_json = result.get_json()
            if 'attachments' not in result_json:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['text'] \
                    != 'What do you want to do?':
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] \
                    != 'action_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] \
                    != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] \
                    != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] \
                    != 'main meal':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['text'] \
                    != 'View Menu List':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['type'] \
                    != 'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['value'] \
                    != f'{m_meal_session.name}_{m_date}_menu_{m_location_id}':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['name'] \
                    != 'main meal':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['text'] \
                    != 'Place order':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['type'] \
                    != 'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['value'] \
                    != f'{m_meal_session.name}_{m_date}_order_{m_location_id}':
                raise AssertionError()

    @patch.object(BotController, '_get_meal_items_by_ids')
    @patch.object(MealItemRepo, 'get')
    @patch.object(MenuRepo, 'get_unpaginated')
    def test_handle_action_selection(self,
                                     func_get_unpaginated,
                                     func_get,
                                     func_get_meal_items_by_ids):
        with self.app.app_context():
            # Arrange
            m_menu = Menu(side_items='item 1', protein_items='item 1')
            func_get_unpaginated.return_value = [m_menu, ]
            func_get.return_value.name = 'Main meal 1'
            func_get_meal_items_by_ids.return_value = ['item 1', ]
            m_date = date.today().strftime('%Y-%m-%d')
            m_location_id = LocationRepo().get_unpaginated(name='Lagos')[0].id
            m_meal_session = MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=20, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                location_id=m_location_id,
                date=m_date
            )

            m_value = f'{m_meal_session.name}_{m_date}_menu_{m_location_id}'
            m_payload = {
                'actions': [
                    {
                        'value': m_value
                    }
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_action_selection(m_payload)

            # Assert
            if result.status_code != 200:
                raise AssertionError()
            result_json = result.get_json()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != m_meal_session.name.upper():
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if result_json['attachments'] is None:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            expected_text = 'Main meal: *Main meal 1*\n ' \
                            'Side items: item 1\n' \
                            'Protein items: item 1\n\n\n'
            if result_json['attachments'][0]['text'] != expected_text:
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] != \
                    'after_menu_list':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'] is None:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] != \
                    'main meal':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['text'] != \
                    'Rate meal':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['type'] != \
                    'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['value'] != \
                    f'{m_meal_session.name}_{m_date}_rate_{m_location_id}_{m_location_id}':
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] != \
                    'main meal':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['text'] != \
                    'Place an order':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['type'] != \
                    'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][1]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][1]['value'] != \
                    f'{m_meal_session.name}_{m_date}_order_{m_location_id}_{m_location_id}':
                raise AssertionError()

    @patch.object(MenuRepo, 'get_unpaginated')
    def test_handle_action_selection_no_menus(self, func_get_unpaginated):
        with self.app.app_context():
            # Arrange
            func_get_unpaginated.return_value = None
            m_date = date.today().strftime('%Y-%m-%d')
            m_location_id = LocationRepo().get_unpaginated(name='Lagos')[0].id
            m_meal_session = MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=20, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                location_id=m_location_id,
                date=m_date
            )
            m_value = f'{m_meal_session.name}_{m_date}_menu_{m_location_id}'
            m_payload = {
                'actions': [
                    {
                        'value': m_value
                    }
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_action_selection(m_payload)

            # Assert
            if result.status_code != 200:
                raise AssertionError()
            result_json = result.get_json()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != \
                    f'Sorry no menu found for date: {m_date}, ' \
                    f'meal period: {m_meal_session.name}':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['text'] != '':
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] != \
                    'center_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] != 'back':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['text'] != 'Back':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['type'] != 'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['value'] != \
                    f'{m_location_id}':
                raise AssertionError()

    @patch.object(MenuRepo, 'get_unpaginated')
    def test_handle_placing_order_no_menus(self, func_get_unpaginated):

        # LocationFactory.create(name='Lagos')

        with self.app.app_context():
            func_get_unpaginated.return_value = None
            m_date = date.today().strftime('%Y-%m-%d')
            m_location_id = LocationRepo().get_unpaginated(name='Lagos')[0].id
            m_meal_period = MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=20, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                location_id=m_location_id,
                date=m_date).name

            m_value = f'{m_meal_period}_{m_date}_menu_{m_location_id}'
            m_payload = {
                'actions': [
                    {
                        'value': m_value
                    }
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_placing_order(m_payload)

            # Assert
            if result.status_code != 200:
                raise AssertionError()
            result_json = result.get_json()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != f'Sorry No Menu found for ' \
                    f'Date: {m_date},Meal Period: {m_meal_period}':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if result_json['attachments'] is None:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['text'] != '':
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] != 'center_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'] is None:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] != 'back':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['text'] != 'Back':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['type'] != 'button':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['value'] != \
                    f'{m_location_id}':
                raise AssertionError()

    @patch.object(MenuRepo, 'get_unpaginated')
    def test_handle_placing_order(self, func_get_unpaginated):
        # LocationFactory.create(name='Lagos')
        with self.app.app_context():
            m_menu = Menu(id=1, main_meal=MealItem(name='Main meal 1'))
            func_get_unpaginated.return_value = [m_menu, ]
            m_date = date.today().strftime('%Y-%m-%d')
            m_location_id = LocationRepo().get_unpaginated(name='Lagos')[0].id
            m_meal_period = MealSessionRepo().new_meal_session(
                name='lunch',
                start_time=time(hour=12, minute=20, second=0),
                stop_time=time(hour=14, minute=0, second=0),
                location_id=m_location_id,
                date=m_date).name

            m_value = f'{m_meal_period}_{m_date}_menu_{m_location_id}'
            m_payload = {
                'actions': [
                    {
                        'value': m_value
                    }
                ]
            }
            bot_controller = BotController(self.request_context)

            # Act
            result = bot_controller.handle_placing_order(m_payload)

            # Assert
            if result.status_code != 200:
                raise AssertionError()
            result_json = result.get_json()
            if 'text' not in result_json:
                raise AssertionError()
            if result_json['text'] != 'Select Main Meal':
                raise AssertionError()
            if 'attachments' not in result_json:
                raise AssertionError()
            if result_json['attachments'] is None:
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['text'] != '':
                raise AssertionError()
            if 'callback_id' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['callback_id'] != \
                    'meal_action_selector':
                raise AssertionError()
            if 'color' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['color'] != '#3AA3E3':
                raise AssertionError()
            if 'attachment_type' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['attachment_type'] != 'default':
                raise AssertionError()
            if 'actions' not in result_json['attachments'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'] is None:
                raise AssertionError()
            if 'name' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['name'] != \
                    'main_meal':
                raise AssertionError()
            if 'type' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['type'] != 'button':
                raise AssertionError()
            if 'text' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['text'] != \
                    'Main meal 1':
                raise AssertionError()
            if 'value' not in result_json['attachments'][0]['actions'][0]:
                raise AssertionError()
            if result_json['attachments'][0]['actions'][0]['value'] != \
                    f'1_{m_value}':
                raise AssertionError()

