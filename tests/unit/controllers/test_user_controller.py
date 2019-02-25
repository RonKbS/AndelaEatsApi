'''
Unit tests for the User Controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.user_controller import UserController
from app.models.user_role import UserRole
from tests.base_test_case import BaseTestCase


class TestUserController(BaseTestCase):
    '''
    UserController test class.
    '''

    def setUp(self):
        self.BaseSetUp()
        self.mock_user_role = UserRole(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            role_id=1,
            location_id=1,
            user_id='mock',
            is_active=True
        )

    @patch('app.repositories.user_role_repo.UserRoleRepo.filter_by')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_list_admin_users_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_filter_by
    ):
        '''
        Test list_admin_users OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [self.mock_user_role, ]
            mock_get_user_by_email_or_id.return_value = {
                "id": "-LXTuXlk2W4Gskt8KTte",
                "email": "joseph.serunjogi@andela.com",
                "first_name": "Joseph",
                "last_name": "Serunjogi",
                "name": "Joseph Serunjogi"
            }
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.list_admin_users()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
