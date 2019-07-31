'''Unit tests for the vendor controller.
'''
from datetime import datetime
from unittest.mock import patch, Mock
from faker import Faker

from app.controllers.vendor_controller import VendorController
from app.models.vendor import Vendor
from app.models.vendor_rating import VendorRating
from app.models.vendor_engagement import VendorEngagement
from tests.base_test_case import BaseTestCase
from factories.vendor_factory import VendorFactory
from factories.location_factory import LocationFactory


class TestVendorController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.fake = Faker()
        vendor = VendorFactory()
        location = LocationFactory()
        self.mock_vendor_engagement = VendorEngagement(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            vendor_id=vendor.id,
            location_id=location.id,
            start_date=datetime.now(),
            end_date=datetime.now(),
            status=1,
            termination_reason=self.fake.text()
        )
        self.mock_rating = VendorRating(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            vendor_id=vendor.id,
            user_id=1,
            comment=self.fake.text(),
            service_date=datetime.now(),
            rating=1.2,
            channel='web',
            type_id=1,
            engagement_id=1,
            main_meal_id=1
        )
        self.mock_vendor_with_dependants = Vendor(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False,
            name=self.fake.name(),
            address=self.fake.address(),
            tel=self.fake.phone_number(),
            contact_person=self.fake.name(),
            is_active=True,
            location_id=location.id,
            ratings=[self.mock_rating, ],
            engagements=[self.mock_vendor_engagement, ]
        )
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
            location_id=location.id
        )
        self.mock_deleted_vendor = Vendor(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=True,
            name=self.fake.name(),
            address=self.fake.address(),
            tel=self.fake.phone_number(),
            contact_person=self.fake.name(),
            is_active=True,
            location_id=location.id
        )
    
    def tearDown(self):
        self.BaseTearDown()

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

    @patch.object(VendorController, 'request_params')
    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_update_vendor_ok_response(
        self,
        mock_vendor_repo_get,
        mock_request_params
    ):
        '''Test update_vendor OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_request_params.return_value = (
                self.fake.name(),
                self.fake.phone_number()[:20],
                self.fake.address(),
                True,
                self.fake.name()
            )
            mock_vendor_repo_get.return_value = self.mock_vendor
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.update_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_suspend_vendor_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get
    ):
        '''Test suspend_vendor when vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = None
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.suspend_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'vendor_id provided'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    @patch('app.repositories.vendor_repo.VendorRepo.update')
    def test_suspend_vendor_ok_response(
        self,
        mock_vendor_repo_update,
        mock_vendor_repo_get
    ):
        '''Test suspend_vendor OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = self.mock_vendor
            mock_vendor_repo_update.return_value = self.mock_vendor
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.suspend_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_un_suspend_vendor_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get
    ):
        '''Test un_suspend_vendor when vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = None
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.un_suspend_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'vendor_id provided'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    @patch('app.repositories.vendor_repo.VendorRepo.update')
    def test_un_suspend_vendor_ok_response(
        self,
        mock_vendor_repo_update,
        mock_vendor_repo_get
    ):
        '''Test un_suspend_vendor OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = self.mock_vendor
            mock_vendor_repo_update.return_value = self.mock_vendor
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.un_suspend_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_delete_vendor_when_vendor_doesnot_exist(
        self,
        mock_vendor_repo_get
    ):
        '''Test delete_vendor when vendor doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = None
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.delete_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'vendor_id provided'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_delete_vendor_when_vendor_is_already_deleted(
        self,
        mock_vendor_repo_get
    ):
        '''Test delete_vendor when vendor is already deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = self.mock_deleted_vendor
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.delete_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Vendor has already ' \
                'been deleted'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    def test_delete_vendor_when_vendor_has_dependants(
        self,
        mock_vendor_repo_get
    ):
        '''Test delete_vendor when vendor has dependants.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = \
                self.mock_vendor_with_dependants
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.delete_vendor(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Vendor cannot be deleted ' \
                'because it has a child object'

    @patch('app.repositories.vendor_repo.VendorRepo.get')
    @patch('app.repositories.vendor_repo.VendorRepo.update')
    @patch('app.repositories.vendor_engagement_repo'
           '.VendorEngagementRepo.filter_by')
    def test_delete_vendor_ok_response(
        self,
        mock_filter_by,
        mock_vendor_repo_update,
        mock_vendor_repo_get
    ):
        '''Test delete_vendor OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_vendor_repo_get.return_value = self.mock_vendor
            mock_vendor_repo_update.return_value = self.mock_vendor
            mock_filter_by.return_value.items = [self.mock_vendor_engagement, ]
            vendor_controller = VendorController(self.request_context)

            # Act
            result = vendor_controller.delete_vendor(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'Vendor deleted'
