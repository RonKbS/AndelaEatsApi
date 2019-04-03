'''Unit tests for the app.controllers.vendor_rating_controller.
'''
from datetime import datetime, timedelta
from unittest.mock import patch

from app.controllers.vendor_rating_controller import VendorRatingController
from app.models.meal_item import MealItem
from app.models.order import Order
from app.models.vendor import Vendor
from app.models.vendor_engagement import VendorEngagement
from app.models.vendor_rating import VendorRating
from app.repositories.meal_item_repo import MealItemRepo
from app.repositories.order_repo import OrderRepo
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.repositories.vendor_rating_repo import VendorRatingRepo
from app.repositories.vendor_repo import VendorRepo
from tests.base_test_case import BaseTestCase


class TestVendorRatingController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch.object(VendorRatingRepo, 'filter_by')
    def test_list_ratings_no_ratings_for_date(
        self,
        mock_vendor_rating_repo_filter_by
    ):
        '''Test list_ratings response when there are no ratings for the
        given date.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating_repo_filter_by.return_value.items = None
            mock_date = '2019-02-05'
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.list_ratings(mock_date)

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'No ratings for this date'

    @patch.object(VendorRatingRepo, 'filter_by')
    @patch.object(VendorRepo, 'get')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorRatingRepo, 'meal_average')
    def test_list_ratings_ok_response(
        self,
        mock_vendor_rating_repo_meal_average,
        mock_meal_item_repo_get,
        mock_vendor_repo_get,
        mock_vendor_rating_repo_filter_by
    ):
        '''Test list_ratings OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating = VendorRating(
                vendor_id=1,
                user_id=1,
                comment='Mock comment',
                service_date=datetime.now(),
                rating=1.0,
                channel='Mock channel',
                rating_type='engagement',
                type_id=0,
                engagement_id=1,
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                main_meal_id=1
            )
            mock_vendor_rating_repo_filter_by.return_value.items = [
                mock_vendor_rating,
            ]
            mock_vendor_repo_get.return_value.name = 'Mock vender'
            mock_meal_item_repo_get.return_value.name = 'Mock meal name'
            mock_vendor_rating_repo_meal_average.return_value = 2.0
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.list_ratings('2019-02-06')

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorRatingRepo, 'get')
    def test_get_vendor_rating_when_rating_doesnot_exist(
        self,
        mock_vendor_rating_repo_get
    ):
        '''Test get_vendor_rating when the rating does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating_repo_get.return_value = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.get_vendor_rating(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request'

    @patch.object(VendorRatingRepo, 'get')
    def test_get_vendor_rating_ok_response(
        self,
        mock_vendor_rating_repo_get
    ):
        '''Test get_vendor_rating OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating = VendorRating(
                vendor_id=1,
                user_id=1,
                comment='Mock comment',
                service_date=datetime.now(),
                rating=1.0,
                channel='Mock channel',
                rating_type='engagement',
                type_id=0,
                engagement_id=1,
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                main_meal_id=1
            )
            mock_vendor_rating_repo_get.return_value = mock_vendor_rating
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.get_vendor_rating(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorEngagementRepo, 'get')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(VendorRepo, 'get')
    def test_create_vendor_rating_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_vendor_engagement_repo_get
    ):
        '''Test create_vendor_rating when vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = None
            mock_vendor_rating_controller_request_params.return_value = (
                None, None, None, None, None
            )
            mock_auth_user.return_value = None
            mock_vendor_repo_get.return_value = None
            mock_vendor_engagement_repo_get.return_value.vendor_id = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_vendor_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid vendor_id provided'

    @patch.object(VendorRepo, 'update_vendor_average_rating')
    @patch.object(VendorRatingRepo, 'new_rating')
    @patch.object(VendorEngagementRepo, 'get')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(VendorRepo, 'get')
    def test_create_vendor_rating_ok_response(
        self,
        mock_vendor_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_vendor_engagement_repo_get,
        mock_vendor_rating_repo_new_rating,
        mock_vendor_rating_repo_update_vendor_average_rating
    ):
        '''Test create_vendor_rating OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor = Vendor(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                name='Mock vendor',
                address='Mock address',
                tel='',
                contact_person='Mock contact person',
                is_active=True,
                location_id=1
            )
            mock_vendor_rating = VendorRating(
                vendor_id=1,
                user_id=1,
                comment='Mock comment',
                service_date=datetime.now(),
                rating=1.0,
                channel='Mock channel',
                rating_type='engagement',
                type_id=0,
                engagement_id=1,
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                main_meal_id=1
            )
            mock_vendor_repo_get.return_value = mock_vendor
            mock_auth_user.return_value = 1
            mock_vendor_rating_controller_request_params.return_value = (
                'Mock comment',
                2.0,
                '2019-02-01',
                'Mock channel',
                1
            )
            mock_vendor_engagement_repo_get.return_value.vendor_id = 1
            mock_vendor_rating_repo_new_rating \
                .return_value = mock_vendor_rating
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )
            mock_vendor_rating_repo_update_vendor_average_rating.return_value = None

            # Act
            result = vendor_rating_controller.create_vendor_rating()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'Rating created'

    @patch.object(VendorRatingController, 'request_params')
    def test_create_order_rating_when_rating_invalid(
        self,
        mock_vendor_rating_controller_request_params
    ):
        '''Test create_order_rating when rating is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating_controller_request_params.return_value = (
                None, None, None, None, 6, None, None
            )
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            result.status_code == 400
            result.get_json()['msg'] == 'Rating must be between 1 and 5' \
                ', inclusive'

    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    def test_create_order_rating_when_meal_item_doesnot_exist(
        self,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params
    ):
        '''Test create_order_rating when meal item does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_rating_controller_request_params.return_value = (
                None, None, None, None, 3, None, None
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Meal item with this id not ' \
                'found'

    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get')
    def test_create_order_rating_when_engagement_doesnot_exist(
        self,
        mock_vendor_engagement_repo_get,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params
    ):
        '''Test create order rating when engagement does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_meal_item = MealItem(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                meal_type='main',
                name='Mock meal',
                description='Mock meal description',
                image='',
                location_id=1
            )
            mock_vendor_rating_controller_request_params.return_value = (
                None, None, None, None, 3, None, None
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = mock_meal_item
            mock_vendor_engagement_repo_get.return_value = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Engagement with this id is' \
                ' not found'

    @patch.object(OrderRepo, 'get')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get')
    def test_create_order_rating_when_order_doesnot_exist(
        self,
        mock_vendor_engagement_repo_get,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_order_repo_get
    ):
        '''Test create_order_rating when order doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_meal_item = MealItem(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                meal_type='main',
                name='Mock meal',
                description='Mock meal description',
                image='',
                location_id=1
            )
            mock_vendor_engagement = VendorEngagement(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                location_id=1,
                start_date=datetime.now(),
                end_date=(datetime.now() + timedelta(days=5)),
                status=1,
                termination_reason='Mock reason'
            )
            mock_vendor_rating_controller_request_params.return_value = (
                1, None, None, None, 3, None, None
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = mock_meal_item
            mock_vendor_engagement_repo_get.return_value = \
                mock_vendor_engagement
            mock_order_repo_get.return_value = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Order with this id is not' \
                ' found'

    @patch.object(OrderRepo, 'get')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get')
    def test_create_order_rating_when_order_already_rated(
        self,
        mock_vendor_engagement_repo_get,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_order_repo_get
    ):
        '''Test create_order_rating when order has already been rated.
        '''
        # Arrange
        with self.app.app_context():
            mock_meal_item = MealItem(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                meal_type='main',
                name='Mock meal',
                description='Mock meal description',
                image='',
                location_id=1
            )
            mock_vendor_engagement = VendorEngagement(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                location_id=1,
                start_date=datetime.now(),
                end_date=(datetime.now() + timedelta(days=5)),
                status=1,
                termination_reason='Mock reason'
            )
            mock_order = Order(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id='user_id',
                date_booked_for=datetime.now(),
                date_booked=datetime.now(),
                channel='web',
                meal_period='lunch',
                order_status='booked',
                has_rated=True,
                menu_id=1,
                location_id=1
            )
            mock_vendor_rating_controller_request_params.return_value = (
                1, None, None, None, 3, None, None
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = mock_meal_item
            mock_vendor_engagement_repo_get.return_value = \
                mock_vendor_engagement
            mock_order_repo_get.return_value = mock_order
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This order has been rated'

    @patch.object(VendorRatingRepo, 'get_unpaginated')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get')
    def test_create_order_rating_when_meal_already_rated(
        self,
        mock_vendor_engagement_repo_get,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_vendor_rating_repo_get_unpaginated
    ):
        '''Test create_order_rating when order has already been rated.
        '''
        # Arrange
        with self.app.app_context():
            mock_meal_item = MealItem(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                meal_type='main',
                name='Mock meal',
                description='Mock meal description',
                image='',
                location_id=1
            )
            mock_vendor_engagement = VendorEngagement(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                location_id=1,
                start_date=datetime.now(),
                end_date=(datetime.now() + timedelta(days=5)),
                status=1,
                termination_reason='Mock reason'
            )
            mock_vendor_rating = VendorRating(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                user_id='user_id',
                comment='Mock comment',
                service_date=datetime.now(),
                rating=3.0,
                channel='web',
                rating_type='meal',
                type_id=1,
                engagement_id=1,
                main_meal_id=1
            )
            service_date = datetime.strftime((datetime.now() - timedelta(1)).date(), '%Y-%m-%d')
            mock_vendor_rating_controller_request_params.return_value = (
                None, None, None, None, 3, service_date, None
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = mock_meal_item
            mock_vendor_engagement_repo_get.return_value = \
                mock_vendor_engagement
            mock_vendor_rating_repo_get_unpaginated.return_value = [
                mock_vendor_rating,
            ]
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'You have already rated' \
                ' this meal'

    @patch.object(VendorRepo, 'update_vendor_average_rating')
    @patch.object(OrderRepo, 'get')
    @patch.object(VendorRatingController, 'request_params')
    @patch('app.Auth.user')
    @patch.object(MealItemRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get')
    def test_create_order_rating_ok_response(
        self,
        mock_vendor_engagement_repo_get,
        mock_meal_item_repo_get,
        mock_auth_user,
        mock_vendor_rating_controller_request_params,
        mock_order_repo_get,
        mock_vendor_repo_update_average_rating
    ):
        '''Test create_order_rating when order has already been rated.
        '''
        # Arrange
        with self.app.app_context():
            mock_meal_item = MealItem(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                meal_type='main',
                name='Mock meal',
                description='Mock meal description',
                image='',
                location_id=1
            )
            mock_vendor_engagement = VendorEngagement(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                location_id=1,
                start_date=datetime.now(),
                end_date=(datetime.now() + timedelta(days=5)),
                status=1,
                termination_reason='Mock reason'
            )
            mock_order = Order(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id='user_id',
                date_booked_for=datetime.now(),
                date_booked=datetime.now(),
                channel='web',
                meal_period='lunch',
                order_status='booked',
                has_rated=False,
                menu_id=1,
                location_id=1
            )
            mock_vendor_rating_controller_request_params.return_value = (
                1, 1, 1, 'Mock comment', 3, '2019-02-06', 'web'
            )
            mock_auth_user.return_value = 1
            mock_meal_item_repo_get.return_value = mock_meal_item
            mock_vendor_engagement_repo_get.return_value = \
                mock_vendor_engagement
            mock_order_repo_get.return_value = mock_order
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )
            mock_vendor_repo_update_average_rating.return_value = None

            # Act
            result = vendor_rating_controller.create_order_rating()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'Rating successful'

    @patch.object(VendorRatingController, 'get_json')
    @patch.object(VendorRatingRepo, 'get')
    def test_update_vendor_rating_when_rating_is_invalid(
        self,
        mock_vendor_rating_repo_get,
        mock_vendor_rating_controller_get_json
    ):
        '''Test update_vendor_rating when rating is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_rating_id = 1
            mock_vendor_rating_controller_get_json.return_value = {
                'comment': 'Mock comment'
            }
            mock_vendor_rating_repo_get.return_value = None
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.update_vendor_rating(
                mock_rating_id
            )

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'rating_id provided'

    @patch.object(VendorRatingRepo, 'get')
    @patch.object(VendorRatingController, 'get_json')
    @patch('app.Auth.user')
    def test_update_vendor_rating_when_rating_is_forbidden(
        self,
        mock_auth_user,
        mock_vendor_rating_controller_get_json,
        mock_vendor_rating_repo_get
    ):
        '''Test update_vendor_rating when rating is forbidden.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_user.return_value = 1
            mock_vendor_rating_controller_get_json.return_value = {
                'comment': 'Mock comment'
            }
            mock_vendor_rating = VendorRating(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                user_id=2,
                comment='Mock comment',
                service_date=datetime.now(),
                rating=3.0,
                channel='web',
                rating_type='meal',
                type_id=1,
                engagement_id=1,
                main_meal_id=1
            )
            mock_vendor_rating_repo_get.return_value = mock_vendor_rating
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.update_vendor_rating(1)

            # Assert
            assert result.status_code == 403
            assert result.get_json()['msg'] == 'You are not allowed to ' \
                'update a rating that is not yours'

    @patch.object(VendorRatingRepo, 'update')
    @patch.object(VendorRatingRepo, 'get')
    @patch.object(VendorRatingController, 'get_json')
    @patch('app.Auth.user')
    def test_update_vendor_rating_ok_response(
        self,
        mock_auth_user,
        mock_vendor_rating_controller_get_json,
        mock_vendor_rating_repo_get,
        mock_vendor_rating_repo_update
    ):
        '''Test update_vendor_rating when rating is forbidden.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_user.return_value = 1
            mock_vendor_rating_controller_get_json.return_value = {
                'comment': 'Mock comment'
            }
            mock_vendor_rating = VendorRating(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                vendor_id=1,
                user_id=1,
                comment='Mock comment',
                service_date=datetime.now(),
                rating=3.0,
                channel='web',
                rating_type='meal',
                type_id=1,
                engagement_id=1,
                main_meal_id=1
            )
            mock_vendor_rating_repo_get.return_value = mock_vendor_rating
            mock_vendor_rating_repo_update.return_value = mock_vendor_rating
            vendor_rating_controller = VendorRatingController(
                self.request_context
            )

            # Act
            result = vendor_rating_controller.update_vendor_rating(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
