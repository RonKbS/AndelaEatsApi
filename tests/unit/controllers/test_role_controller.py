'''Unit tests for the role controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.role_controller import RoleController
from app.models.role import Role
from app.repositories.role_repo import RoleRepo
from app.repositories.user_role_repo import UserRoleRepo
from app.repositories.permission_repo import PermissionRepo
from app.services.andela import AndelaService
from tests.base_test_case import BaseTestCase


class TestRoleController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.mock_role = Role(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                name='Mock role',
                help='Mock help'
            )

    @patch.object(RoleController, 'pagination_meta')
    @patch.object(RoleRepo, 'filter_by')
    def test_list_roles_ok_response(
        self,
        mock_role_repo_filter_by,
        mock_role_controller_pagination_meta
    ):
        '''Test list_roles OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': False,
                'prev_page': False
            }
            mock_role_repo_filter_by.return_value.items = [self.mock_role, ]
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.list_roles()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleRepo, 'get')
    def test_get_role_when_invalid_or_missing(
        self,
        mock_role_repo_get
    ):
        '''Test get_role invalid repo response.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = None
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.get_role(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or Missing role_id'

    @patch.object(RoleRepo, 'get')
    def test_get_role_ok_response(
        self,
        mock_role_repo_get
    ):
        '''Test get_role OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = self.mock_role
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.get_role(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleController, 'request_params')
    @patch.object(RoleRepo, 'find_first')
    def test_create_role_when_name_already_exists(
        self,
        mock_role_repo_find_first,
        mock_role_controller_request_params
    ):
        '''Test create_role when role name already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                'Mock name',
                'Mock help'
            )
            mock_role_repo_find_first.return_value = self.mock_role
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.create_role()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Role with this name already' \
                ' exists'

    @patch.object(RoleController, 'request_params')
    @patch.object(RoleRepo, 'find_first')
    def test_create_role_ok_response(
        self,
        mock_role_repo_find_first,
        mock_role_controller_request_params
    ):
        '''Test create_role OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                'Mock name',
                'Mock help'
            )
            mock_role_repo_find_first.return_value = None
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.create_role()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleController, 'request_params')
    @patch.object(RoleRepo, 'get')
    def test_update_role_when_role_doesnot_exist(
        self,
        mock_role_repo_get,
        mock_role_controller_request_params
    ):
        '''Test update_role when role doesn't exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = None
            mock_role_controller_request_params.return_value = (None, None)
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.update_role(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'role_id provided'

    @patch.object(RoleRepo, 'find_first')
    @patch.object(RoleController, 'request_params')
    @patch.object(RoleRepo, 'get')
    def test_update_role_when_name_is_already_taken(
        self,
        mock_role_repo_get,
        mock_role_controller_request_params,
        mock_role_repo_find_first
    ):
        '''Test update_role when role doesn't exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = self.mock_role
            mock_role_repo_find_first.return_value = self.mock_role
            mock_role_controller_request_params.return_value = (
                'Mock name',
                'Mock help'
            )
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.update_role(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Role with this name' \
                ' already exists'

    @patch.object(RoleRepo, 'find_first')
    @patch.object(RoleController, 'request_params')
    @patch.object(RoleRepo, 'get')
    def test_update_role_ok_response(
        self,
        mock_role_repo_get,
        mock_role_controller_request_params,
        mock_role_repo_find_first
    ):
        '''Test update_role when role doesn't exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = self.mock_role
            mock_role_repo_find_first.return_value = None
            mock_role_controller_request_params.return_value = (
                'Mock name',
                'Mock help'
            )
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.update_role(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleRepo, 'get')
    def test_delete_role_when_role_is_invalid(
        self,
        mock_role_repo_get
    ):
        '''Test delete_role when the role is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.delete_role(1)

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'role_id provided'

    @patch.object(RoleRepo, 'get')
    @patch.object(RoleRepo, 'update')
    def test_delete_role_ok_response(
        self,
        mock_role_repo_update,
        mock_role_repo_get
    ):
        '''Test delete_role when the role is invalid.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_repo_get.return_value = self.mock_role
            mock_role_repo_update.return_value = self.mock_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.delete_role(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'role deleted'
