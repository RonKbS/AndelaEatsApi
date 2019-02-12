'''Unit tests for the OrderController.
'''
from datetime import datetime, date
from unittest.mock import Mock, patch

from app.controllers.order_controller import OrderController
from app.models.location import Location
from app.models.order import Order
from app.models.meal_item import MealItem
from tests.base_test_case import BaseTestCase


class TestOrderController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.mock_order = Order(
            is_deleted=False,
            created_at=datetime.now(),
            id=1,
            user_id='mock',
            date_booked_for=date.today(),
            date_booked=date.today(),
            channel='web',
            meal_period='lunch',
            order_status='booked',
            has_rated=True,
            menu_id=1,
            location_id=1
        )
        self.mock_meal_item = MealItem(
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            id=1,
            meal_type='main',
            name='mock',
            description='mock',
            image='mock',
            location_id=1
        )
        self.pagination_meta = {
            'total_rows': 1,
            'total_pages': 1,
            'current_page': 1,
            'next_page': False,
            'prev_page': False
        }

    @patch('app.controllers.order_controller.OrderController.pagination_meta')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.repositories.OrderRepo.filter_by')
    @patch('app.utils.auth.Auth.get_location')
    def test_list_orders_ok_response(
        self,
        mock_get_location,
        mock_filter_by,
        mock_get,
        mock_get_user_by_email_or_id,
        mock_pagination_meta
    ):
        '''Test list_orders OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [self.mock_order, ]
            mock_get_location.return_value = 1
            mock_get.return_value.meal_item_orders = [self.mock_meal_item, ]
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            mock_pagination_meta.return_value = self.pagination_meta
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.list_orders()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch('app.repositories.order_repo.OrderRepo'
           '.get_range_paginated_options_all')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_list_orders_date_range_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_get,
        mock_get_range_paginated_options_all,
        mock_get_location
    ):
        '''Test list_orders_date
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_get_range_paginated_options_all.return_value.items = [
                self.mock_order,
            ]
            mock_get.return_value.meal_item_orders = [self.mock_meal_item, ]
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.list_orders_date_range(
                '2019-02-11', '2019-02-12'
            )

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch('app.repositories.order_repo.OrderRepo.get_unpaginated')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_list_orders_date_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_get,
        mock_get_unpaginated,
        mock_get_location
    ):
        '''Test list_orders_date OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_get_unpaginated.return_value = [self.mock_order, ]
            mock_get.return_value.meal_item_orders = [self.mock_meal_item, ]
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.list_orders_date('2019-02-11')

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_get_order_when_order_doesnot_exist(
        self,
        mock_get
    ):
        '''Test get_order when order doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = None
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.get_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Order not found'

    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_get_order_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_get
    ):
        '''Test get_order OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = self.mock_order
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.get_order(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.order_repo.OrderRepo.filter_by')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_get_order_by_user_id_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_get,
        mock_filter_by
    ):
        '''Test get_order_by_user_id OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [self.mock_order, ]
            mock_get.return_value.meal_item_orders = [self.mock_meal_item, ]
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.get_order_by_user_id(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.order_repo.OrderRepo'
           '.get_range_paginated_options')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_get_order_by_user_id_date_range_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_get,
        mock_get_range_paginated_options
    ):
        '''Test get_order_user_id_date_range OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_range_paginated_options.return_value.items = [
                self.mock_order,
            ]
            mock_get.return_value.meal_item_orders = [self.mock_meal_item, ]
            mock_get_user_by_email_or_id.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.get_order_by_user_id_date_range(
                1, '2019-01-11', '2019-02-11'
            )

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.user')
    @patch('app.utils.auth.Auth.get_location')
    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.user_has_order')
    def test_create_order_when_meal_period_is_already_booked(
        self,
        mock_user_has_order,
        mock_request_params,
        mock_get_location,
        mock_user
    ):
        '''Test create_order when meal period is already booked.
        '''
        # Arrange
        with self.app.app_context():
            mock_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            mock_get_location.return_value = 1
            mock_request_params.return_value = (
                '2019-02-01', 'web', 'lunch', [self.mock_meal_item, ], 1
            )
            mock_user_has_order.return_value = True
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.create_order()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'You have already booked for ' \
                'this meal period.'

    @patch('app.utils.auth.Auth.user')
    @patch('app.utils.auth.Auth.get_location')
    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.user_has_order')
    @patch('app.repositories.location_repo.LocationRepo.get')
    @patch('app.utils.current_time_by_zone')
    def test_create_order_when_date_booked_is_in_past(
        self,
        mock_current_time_by_zone,
        mock_get,
        mock_user_has_order,
        mock_request_params,
        mock_get_location,
        mock_user
    ):
        '''Test create_date when the date booked is in the past.
        '''
        mock_user.return_value = {
            'id': 1,
            'mail': 'joseph@mail.com',
            'first_name': 'Joseph',
            'last_name': 'Serunjogi'
        }
        mock_get_location.return_value = Mock()
        mock_request_params.return_value = (
            '2019-02-01', 'web', 'lunch', [self.mock_meal_item, ], 1
        )
        mock_user_has_order.return_value = False
        mock_get.return_value = Location(
            id=1,
            created_at=datetime.now,
            updated_at=datetime.now(),
            is_deleted=False,
            name='mock',
            zone='+3'
        )
        mock_current_time_by_zone.return_value = Mock()
        order_controller = OrderController(self.request_context)

        # Act
        result = order_controller.create_order()

        # Assert
        assert result.status_code == 400
        assert result.get_json()['msg'] == 'You are not allowed to book for ' \
            'a date in the past'

    @patch('app.Auth.user')
    @patch('app.Auth.get_location')
    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.user_has_order')
    @patch('app.repositories.location_repo.LocationRepo.get')
    @patch('app.utils.current_time_by_zone')
    @patch('app.utils.check_date_current_vs_date_for')
    def test_create_order_when_booked_late(
        self,
        mock_check_date_current_vs_date_for,
        mock_current_time_by_zone,
        mock_location_repo_get,
        mock_user_has_order,
        mock_request_params,
        mock_get_location,
        mock_auth_user
    ):
        '''Testing create_order when booked late.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            mock_get_location.return_value = 1
            mock_request_params.return_value = (
                '2019-02-12', 'web', 'lunch', [self.mock_meal_item, ], 1
            )
            mock_user_has_order.return_value = False
            mock_location_repo_get.return_value = Mock()
            mock_datetime = datetime(2019, 2, 12, 16, 00, 00)
            mock_current_time_by_zone.return_value = mock_datetime
            mock_check_date_current_vs_date_for.return_value = True
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.create_order()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'It is too late to book a ' \
                'meal for the selected date'
