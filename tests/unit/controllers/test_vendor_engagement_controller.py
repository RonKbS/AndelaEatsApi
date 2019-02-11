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

    @patch.object(VendorRepo, 'get')
    def test_list_vendor_engagements_by_vendor_when_vendor_is_disabled(
        self,
        mock_vendor_repo_get
    ):
        '''Test list_vendor_engagements when vendor is disabled.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value.is_active = False
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller. \
                list_vendor_engagements_by_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Vendor is disabled'

    @patch.object(VendorEngagementController, 'pagination_meta')
    @patch.object(VendorRepo, 'get')
    @patch.object(VendorEngagementRepo, 'filter_by')
    def test_list_vendor_engagements_by_vendor_ok_response(
        self,
        mock_vendor_engagement_repo_filter_by,
        mock_vendor_repo_get,
        mock_pagination_meta
    ):
        '''Test list_vendor_engagements OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_engagement_repo_filter_by.return_value.items = [
                self.mock_vendor_engagement,
            ]
            mock_vendor_repo_get.return_value = self.mock_vendor
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
            result = vendor_engagement_controller \
                .list_vendor_engagements_by_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch.object(VendorEngagementRepo, 'get_engagement_by_date')
    @patch.object(VendorEngagementController, 'pagination_meta')
    def test_upcoming_vendor_engagements_ok_response(
        self,
        mock_pagination_meta,
        mock_get_engagement_by_date,
        mock_get_location
    ):
        '''Test update_vendor_engagements when the request is bad.
        '''
        # Arrange
        with self.app.app_context():
            mock_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': 1,
                'prev_page': 1
            }
            mock_get_engagement_by_date.return_value.items = [
                self.mock_vendor_engagement,
            ]
            mock_get_location.return_value = 1
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller \
                .upcoming_vendor_engagements()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorEngagementRepo, 'get')
    def test_get_vendor_engagement_when_request_is_bad(
        self,
        mock_vendor_engagement_repo_get
    ):
        '''Test get_vendor_engagement when the request is bad.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_engagement_repo_get.return_value = None
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.get_vendor_engagement(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request'

    @patch.object(VendorEngagementRepo, 'get')
    def test_get_vendor_engagement_ok_response(
        self,
        mock_vendor_engagement_repo_get
    ):
        '''Test get_vendor_engagement OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_engagement_repo_get.return_value = \
                self.mock_vendor_engagement
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.get_vendor_engagement(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorEngagementController, 'request_params')
    @patch.object(VendorRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get_existing_engagement')
    def test_create_vendor_engagement_when_engagement_already_exists(
        self,
        mock_get_existing_engagement,
        mock_get,
        mock_request_params
    ):
        '''Test create_vendor_engagement when engagement already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                1, '2019-02-11', '2019-02-11', 'mock status'
            )
            mock_get.return_value = self.mock_vendor
            mock_get_existing_engagement.return_value = 1
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.create_vendor_engagement()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'An engagement already exists' \
                ' for this period. Kindly disable engagement first.'

    @patch.object(VendorEngagementController, 'request_params')
    @patch.object(VendorRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get_existing_engagement')
    def test_create_vendor_engagement_when_vendor_is_invalid(
        self,
        mock_get_existing_engagement,
        mock_get,
        mock_request_params
    ):
        '''Test create_vendor_engagement when the vendor is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_existing_engagement.return_value = 0
            mock_request_params.return_value = (
                1, '2019-02-11', '2019-02-11', 'Mock status'
            )
            mock_get.return_value = None
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.create_vendor_engagement()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid vendor_id provided'

    @patch.object(VendorEngagementController, 'request_params')
    @patch.object(VendorRepo, 'get')
    @patch.object(VendorEngagementRepo, 'get_existing_engagement')
    @patch.object(VendorEngagementRepo, 'new_vendor_engagement')
    def test_create_vendor_engagement_ok_response(
        self,
        mock_new_vendor_engagement,
        mock_get_existing_engagement,
        mock_get,
        mock_request_params
    ):
        '''Test create_vendor_engagement OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                1, '2019-02-11', '2019-02-11', 'mock status'
            )
            mock_get.return_value = self.mock_vendor
            mock_get_existing_engagement.return_value = 0
            mock_new_vendor_engagement.return_value = \
                self.mock_vendor_engagement
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.create_vendor_engagement()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorEngagementController, 'request_params')
    @patch.object(VendorEngagementRepo, 'get')
    def test_update_vendor_engagement_when_engagement_is_invalid(
        self,
        mock_get,
        mock_request_params
    ):
        '''Test update_vendor_engagement when engagement is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                1, '2019-02-11', '2019-02-11', 'mock status', 'mock_reason'
            )
            mock_get.return_value = None
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.update_vendor_engagement(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'engagement_id provided'

    @patch.object(VendorEngagementController, 'request_params')
    @patch.object(VendorEngagementRepo, 'get')
    @patch.object(VendorEngagementRepo, 'update')
    def test_update_vendor_engagement_ok_response(
        self,
        mock_update,
        mock_get,
        mock_request_params
    ):
        '''Test update_vendor_engagement when engagement is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                1, '2019-02-11', '2019-02-11', 'mock status', 'mock_reason'
            )
            mock_get.return_value = self.mock_vendor_engagement
            mock_update.return_value = self.mock_vendor_engagement
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.update_vendor_engagement(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorEngagementRepo, 'get')
    def test_delete_engagement_when_engagement_is_invalid(
        self,
        mock_get
    ):
        '''Test delete_engagement when engagement is already deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value = None
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.delete_engagement(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect' \
                ' engagement_id provided'

    @patch.object(VendorEngagementRepo, 'get')
    def test_delete_engagement_when_engagement_already_deleted(
        self,
        mock_get
    ):
        '''Test delete_engagement when engagement is already deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_get.return_value.is_deleted = True
            vendor_engagement_controller = VendorEngagementController(
                self.request_context
            )

            # Act
            result = vendor_engagement_controller.delete_engagement(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This engagement has already' \
                ' been deleted'
