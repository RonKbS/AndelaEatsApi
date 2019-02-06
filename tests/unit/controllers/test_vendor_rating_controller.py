'''Unit tests for the app.controllers.vendor_rating_controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.vendor_rating_controller import VendorRatingController
from app.models.vendor_rating import VendorRating
from app.repositories.meal_item_repo import MealItemRepo
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
