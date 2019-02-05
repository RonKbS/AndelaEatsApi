'''Unit tests for the app.controllers.vendor_rating_controller.
'''
from unittest.mock import patch

from app.controllers.vendor_rating_controller import VendorRatingController
from app.repositories.vendor_rating_repo import VendorRatingRepo
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
