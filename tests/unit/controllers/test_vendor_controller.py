'''Unit tests for the vendor controller.
'''
from datetime import datetime
from unittest.mock import patch, Mock
from faker import Faker

from app.controllers.vendor_controller import VendorController
from app.models.vendor import Vendor
from tests.base_test_case import BaseTestCase


class TestVendorController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.fake = Faker()
        self.mock_vendor = Vendor(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False,
            name=self.fake.name(),
            address=self.fake.address(),
            tel=self.fake.phone_number(),
            contact_person=self.fake.name(),
            is_active=True,
            location_id=1
        )

    @patch('app.utils.auth.Auth.get_location')
    @patch('app.repositories.vendor_repo.VendorRepo.filter_by')
    @patch('app.controllers.vendor_controller.VendorController'
           '.pagination_meta')
    def test_list_vendors_ok_response(
        self,
        mock_pagination_meta,
        mock_filter_by,
        mock_get_location
    ):
        '''Test list_vendors OK response.
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
            mock_filter_by.return_value.items = [
                self.mock_vendor,
            ]
            mock_get_location.return_value = 1
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.list_vendors()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch('app.repositories.vendor_repo.VendorRepo.filter_by')
    @patch.object(VendorController, 'pagination_meta')
    def test_list_deleted_vendors_ok_response(
        self,
        mock_pagination_meta,
        mock_filter_by,
        mock_get_location
    ):
        '''Test list_deleted_vendors OK response.
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
            mock_filter_by.return_value.items = [self.mock_vendor, ]
            mock_get_location.return_value = 1
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.list_deleted_vendors()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch('app.repositories.vendor_repo.VendorRepo.filter_by')
    @patch.object(VendorController, 'pagination_meta')
    def test_list_suspended_vendors_ok_response(
        self,
        mock_pagination_meta,
        mock_filter_by,
        mock_get_location
    ):
        '''Test list_deleted_vendors OK response.
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
            mock_filter_by.return_value.items = [self.mock_vendor, ]
            mock_get_location.return_value = 1
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.list_suspended_vendors()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_get_vendor_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get
    ):
        '''Test get_vendor when the vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = None
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.get_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Bad Request - Invalid or ' \
                'Missing vendor_id'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_get_vendor_ok_response(
        self,
        mock_vendor_repo_get
    ):
        '''Test get_vendor OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = self.mock_vendor
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.get_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.utils.auth.Auth.get_location')
    @patch.object(VendorController, 'request_params')
    @patch('app.repositories.vendor_repo.VendorRepo.new_vendor')
    def test_creat_vendor_ok_response(
        self,
        mock_new_vendor,
        mock_request_params,
        mock_get_location
    ):
        '''Test create_vendor OK response.
        '''
        mock_get_location.return_value = 1
        mock_request_params.return_value = (
            self.fake.name(),
            self.fake.phone_number(),
            self.fake.address(),
            True,
            self.fake.name()
        )
        mock_new_vendor.return_value = self.mock_vendor
        vendor_controller = VendorController(self.request_context)

        # Act
        result = vendor_controller.create_vendor()

        # Assert
        assert result.status_code == 201
        assert result.get_json()['msg'] == 'OK'

    @patch.object(VendorController, 'request_params')
    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_update_vendor_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get,
        mock_request_params
    ):
        '''Test update_vendor when vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                self.fake.name(),
                self.fake.phone_number(),
                self.fake.address(),
                True,
                self.fake.name()
            )
            mock_vendor_repo_get.return_value = None
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.update_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'vendor_id provided'
