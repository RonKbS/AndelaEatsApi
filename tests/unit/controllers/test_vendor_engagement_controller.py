'''Unit tests for the VendorEngagementController.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.vendor_engagement_controller import \
    VendorEngagementController
from app.models.vendor import Vendor
from app.models.vendor_engagement import VendorEngagement
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.repositories.vendor_repo import VendorRepo
from app.utils.auth import Auth
from tests.base_test_case import BaseTestCase


class TestVendorEngagementController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.mock_vendor = Vendor(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name='Mock vendor',
            address='Mock address',
            tel='',
            contact_person='Mock person',
            is_active=True,
            location_id=1
        )
        self.mock_vendor_engagement = VendorEngagement(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            vendor_id=1,
            location_id=1,
            start_date=datetime.now(),
            end_date=datetime.now(),
            status=1,
            termination_reason='Mock reason',
            vendor=self.mock_vendor
        )

    @patch.object(VendorEngagementController, 'pagination_meta')
    @patch('app.utils.auth.Auth.get_location')
    @patch.object(VendorEngagementRepo, 'filter_by')
    def test_list_vendor_engagements_ok_response(
        self,
        mock_vendor_engagement_repo_filter_by,
        mock_auth_get_location,
        mock_pagination_meta
    ):
        '''Test list_vendor_engagements OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_auth_get_location.return_value = 1
            mock_vendor_engagement_repo_filter_by.return_value.items = [
                self.mock_vendor_engagement,
            ]
            mock_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': 1,
                'prev_page': 1
            }
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.list_vendor_engagements()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorRepo, 'get')
    def test_list_vendor_engagements_by_vendor_when_vendor_is_invalid(
        self,
        mock_vendor_repo_get
    ):
        '''Test list_vendor_engagement_by_vendor when the vendor is invalid
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value.is_deleted = True
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller \
                .list_vendor_engagements_by_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid Vendor'

