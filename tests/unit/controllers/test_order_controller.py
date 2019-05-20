'''Unit tests for the OrderController.
'''
from datetime import datetime, date
from unittest.mock import Mock, patch
from faker import Faker
from faker.providers import date_time

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
            user_id=1,
            date_booked_for=date.today(),
            date_booked=date.today(),
            channel='web',
            meal_period='lunch',
            order_status='booked',
            has_rated=True,
            menu_id=1,
            location_id=1
        )
        self.mock_deleted_order = Order(
            is_deleted=True,
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
        self.mock_collected_order = Order(
            is_deleted=False,
            created_at=datetime.now(),
            id=1,
            user_id='mock',
            date_booked_for=date.today(),
            date_booked=date.today(),
            channel='web',
            meal_period='lunch',
            order_status='collected',
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
        self.faker = Faker()
        self.faker.add_provider(date_time)

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
    @patch('app.utils.check_date_current_vs_date_for')
    @patch('app.utils.datetime')
    @patch('app.controllers.order_controller.datetime')
    def test_create_order_when_booked_late(
        self,
        mock_order_controller_datetime,
        mock_datetime,
        mock_check_date_current_vs_date_for,
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
            mock_order_controller_datetime.now = Mock(
                return_value=datetime(2019, 2, 13, 15, 0, 0)
            )
            mock_order_controller_datetime.strptime = Mock(
                return_value=datetime(2019, 2, 14, 13, 0, 0)
            )
            mock_datetime.utcnow = Mock(
                return_value=datetime(2019, 2, 13, 16, 0, 0)
            )
            mock_auth_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            mock_get_location.return_value = 1
            mock_request_params.return_value = (
                Mock(), 'web', 'lunch', [self.mock_meal_item, ], 1
            )
            mock_user_has_order.return_value = False
            mock_location_repo_get.return_value = Location(
                id=1,
                created_at=datetime.now,
                updated_at=datetime.now(),
                is_deleted=False,
                name='mock',
                zone='+3'
            )
            mock_check_date_current_vs_date_for.return_value = True
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.create_order()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'It is too late to book a ' \
                'meal for the selected date '

    @patch('app.Auth.user')
    @patch('app.Auth.get_location')
    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.user_has_order')
    @patch('app.repositories.location_repo.LocationRepo.get')
    @patch('app.utils.check_date_current_vs_date_for')
    @patch('app.utils.datetime')
    @patch('app.repositories.meal_item_repo.MealItemRepo'
           '.get_meal_items_by_ids')
    @patch('app.repositories.order_repo.OrderRepo.create_order')
    @patch('app.controllers.order_controller.datetime')
    def test_create_order_ok_response(
        self,
        mock_order_controller_datetime,
        mock_create_order,
        mock_get_meals_by_ids,
        mock_datetime,
        mock_check_date_current_vs_date_for,
        mock_location_repo_get,
        mock_user_has_order,
        mock_request_params,
        mock_get_location,
        mock_auth_user
    ):
        '''Test create_order OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_order_controller_datetime.now = Mock(
                return_value=datetime(2019, 2, 13, 15, 0, 0)
            )
            mock_order_controller_datetime.strptime = Mock(
                return_value=datetime(2019, 2, 14, 13, 0, 0)
            )
            mock_datetime.utcnow = Mock(
                return_value=datetime(2019, 2, 13, 9, 0, 0)
            )
            mock_auth_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com',
                'first_name': 'Joseph',
                'last_name': 'Serunjogi'
            }
            mock_get_location.return_value = 1
            mock_date_booked = Mock()
            mock_request_params.return_value = (
                mock_date_booked, 'web', 'lunch', [self.mock_meal_item, ], 1
            )
            mock_user_has_order.return_value = False
            mock_location_repo_get.return_value = Location(
                id=1,
                created_at=datetime.now,
                updated_at=datetime.now(),
                is_deleted=False,
                name='mock',
                zone='+3'
            )
            mock_check_date_current_vs_date_for.return_value = False
            mock_get_meals_by_ids.return_value = [self.mock_meal_item, ]
            mock_create_order.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.create_order()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.meal_item_repo.MealItemRepo.get')
    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_update_order_when_order_doesnot_exist(
        self,
        mock_order_repo_get,
        mock_meal_item_repo_get,
        mock_request_params
    ):
        '''Test update_order when the order doesnot exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                '2019-02-12', 'web', [], None
            )
            mock_meal_item_repo_get.return_value = Mock()
            mock_order_repo_get.return_value = None
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.update_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect order_id ' \
                'provided'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.meal_item_repo.MealItemRepo.get')
    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_update_order_when_order_has_been_deleted(
        self,
        mock_order_repo_get,
        mock_meal_item_repo_get,
        mock_request_params
    ):
        '''Test update_order when the order has been deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                '2019-02-12', 'web', [], None
            )
            mock_meal_item_repo_get.return_value = Mock()
            mock_order_repo_get.return_value.is_deleted = True
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.update_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Order has already been deleted'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.meal_item_repo.MealItemRepo.get')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.controllers.order_controller.datetime')
    def test_update_order_when_updated_booking_is_late(
        self,
        mock_datetime,
        mock_order_repo_get,
        mock_meal_item_repo_get,
        mock_request_params
    ):
        '''Test update_order when the updated booking is late.
        '''
        # Arrange
        with self.app.app_context():
            mock_datetime.now = Mock(
                return_value=datetime(2019, 2, 12, 15, 45, 0)
            )
            mock_datetime.strptime = Mock(
                return_value=datetime(2019, 2, 12, 15, 45, 0)
            )
            mock_request_params.return_value = (
                '2019-02-12', 'web', [], None
            )
            mock_meal_item_repo_get.return_value = [self.mock_meal_item, ]
            mock_order_repo_get.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.update_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'It is too late to book meal ' \
                'for the selected date '

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.meal_item_repo.MealItemRepo.get')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.controllers.order_controller.datetime')
    @patch('app.repositories.order_repo.OrderRepo.update')
    def test_update_order_ok_response(
        self,
        mock_order_repo_update,
        mock_order_controller_datetime,
        mock_order_repo_get,
        mock_meal_item_repo_get,
        mock_request_params
    ):
        '''Test update_order OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_order_controller_datetime.now = Mock(
                return_value=datetime(2019, 2, 12, 12, 45, 0)
            )
            mock_order_controller_datetime.strptime = Mock(
                return_value=datetime(2019, 2, 13, 0, 0, 0)
            )
            mock_date_booked = Mock()
            mock_request_params.return_value = (
                mock_date_booked, 'web', [self.mock_meal_item, ], '1'
            )
            mock_meal_item_repo_get.return_value = [self.mock_meal_item, ]
            mock_order_repo_get.return_value = self.mock_order
            mock_order_repo_update.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.update_order(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.find_first')
    def test_collect_order_when_user_has_no_order_for_date(
        self,
        mock_find_first,
        mock_request_params
    ):
        '''Test collect_order when user has no order for date.
        '''
        # Arrange
        with self.app.app_context():
            mock_find_first.return_value = None
            mock_user_id = Mock(return_value=1)
            fake_order_id = Mock(return_value=1)
            mock_request_params.return_value = (
                mock_user_id,
                fake_order_id,
                '2019-02-13'
            )
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.collect_order()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == f'User has no {fake_order_id}' \
                ' order for the date.'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.find_first')
    def test_collect_order_when_order_already_collected(
        self,
        mock_find_first,
        mock_request_params
    ):
        '''Test collect_order when order is already collected.
        '''
        # Arrange
        with self.app.app_context():
            mock_find_first.return_value = self.mock_collected_order
            mock_request_params.return_value = (
                1,
                'mock',
                '2019-02-13'
            )
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.collect_order()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Order already collected'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.find_first')
    @patch('app.repositories.order_repo.OrderRepo.update')
    def test_collect_order_ok_response(
        self,
        mock_order_repo_update,
        mock_find_first,
        mock_request_params
    ):
        '''Test collect_order OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_find_first.return_value = self.mock_order
            mock_request_params.return_value = (
                1,
                'mock',
                '2019-02-13'
            )
            mock_order_repo_update.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.collect_order()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'Order successfully collected'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.find_first')
    def test_check_order_when_order_doesnot_exist(
        self,
        mock_find_first,
        mock_request_params
    ):
        '''Test check_order when the order doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_find_first.return_value = None
            mock_request_params.return_value = (
                1,
                'breakfast',
                '2019-02-13'
            )
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.check_order()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'User has no breakfast order for this date'

    @patch('app.controllers.order_controller.OrderController.request_params')
    @patch('app.repositories.order_repo.OrderRepo.find_first')
    def test_check_order_ok_response(
        self,
        mock_find_first,
        mock_request_params
    ):
        '''Test check_order OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_find_first.return_value = self.mock_order
            mock_request_params.return_value = (
                1,
                'mock',
                '2019-02-13'
            )
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.check_order()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_delete_order_when_order_doesnot_exist(
        self,
        mock_order_repo_get
    ):
        '''Test delete_order when the order doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_order_repo_get.return_value = None
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.delete_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'order_id provided'

    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_delete_order_when_order_is_already_deleted(
        self,
        mock_order_repo_get
    ):
        '''Test delete_order when the order is already deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_order_repo_get.return_value = self.mock_deleted_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.delete_order(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Order has already been' \
                ' deleted'

    @patch('app.utils.auth.Auth.user')
    @patch('app.repositories.order_repo.OrderRepo.get')
    def test_delete_order_when_user_deleting_order_is_not_the_owner(
        self,
        mock_order_repo_get,
        mock_auth_user
    ):
        '''Test delete_order when the user deleting the order is not
        the owner.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_user.return_value = 2
            mock_order_repo_get.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.delete_order(1)

            # Assert
            assert result.status_code == 403
            assert result.get_json()['msg'] == 'You cannot delete an order' \
                ' that is not yours'

    @patch('app.utils.auth.Auth.user')
    @patch('app.repositories.order_repo.OrderRepo.get')
    @patch('app.repositories.order_repo.OrderRepo.update')
    def test_delete_order_ok_response(
        self,
        mock_order_repo_update,
        mock_order_repo_get,
        mock_auth_user
    ):
        '''Test delete_order when the user deleting the order is not
        the owner.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_user.return_value = 1
            mock_order_repo_get.return_value = self.mock_order
            mock_order_repo_update.return_value = self.mock_order
            order_controller = OrderController(self.request_context)

            # Act
            result = order_controller.delete_order(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'Order deleted'
