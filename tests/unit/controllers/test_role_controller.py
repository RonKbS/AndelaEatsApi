'''Unit tests for the role controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.role_controller import RoleController
from app.models.permission import Permission
from app.models.role import Role
from app.models.user_role import UserRole
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
        self.mock_user_role = UserRole(
            id=1,
            role_id=1,
            location_id=1,
            user_id=1,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
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

    @patch.object(UserRoleRepo, 'get_unpaginated')
    def test_get_user_roles_when_user_has_no_roles(
        self,
        mock_user_role_repo_get_unpaginated
    ):
        '''Test get_user_roles when the user has no roles.
        '''
        # Arrange
        with self.app.app_context():
            mock_user_role_repo_get_unpaginated.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.get_user_roles(1)

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'There are no roles for this user'

    @patch.object(UserRoleRepo, 'get_unpaginated')
    def test_get_user_roles_ok_response(
        self,
        mock_user_role_repo_get_unpaginated
    ):
        '''Test get_user_roles OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_user_role_repo_get_unpaginated.return_value = [
                self.mock_user_role,
            ]
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.get_user_roles(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.Auth.get_location')
    @patch.object(RoleController, 'request_params')
    @patch.object(AndelaService, 'get_user_by_email_or_id')
    def test_create_user_role_when_user_doesnot_exist(
        self,
        mock_andela_service_get_user,
        mock_role_controller_request_params,
        mock_auth_get_location
    ):
        '''Test create_user_role when user doesn't exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1,
                'joseph@mail.com'
            )
            mock_andela_service_get_user.return_value = None
            mock_auth_get_location.return_value = 1
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_user_role()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This user record does' \
                ' not exist'

    @patch.object(UserRoleRepo, 'get_unpaginated')
    @patch('app.Auth.get_location')
    @patch.object(RoleController, 'request_params')
    @patch.object(AndelaService, 'get_user_by_email_or_id')
    def test_create_user_role_when_user_already_assigned_to_role(
        self,
        mock_andela_service_get_user,
        mock_role_controller_request_params,
        mock_auth_get_location,
        mock_user_role_repo_get_unpaginated
    ):
        '''Test create_user_role when user is already assigned to the role.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1,
                'joseph@mail.com'
            )
            mock_andela_service_get_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com'
            }
            mock_auth_get_location.return_value = 1
            mock_user_role_repo_get_unpaginated.return_value = \
                self.mock_user_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_user_role()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This User ' \
                'has this Role already'

    @patch.object(UserRoleRepo, 'get')
    @patch.object(UserRoleRepo, 'get_unpaginated')
    @patch('app.Auth.get_location')
    @patch.object(RoleController, 'request_params')
    @patch.object(AndelaService, 'get_user_by_email_or_id')
    def test_create_user_role_when_role_doesnot_exist(
        self,
        mock_andela_service_get_user,
        mock_role_controller_request_params,
        mock_auth_get_location,
        mock_user_role_repo_get_unpaginated,
        mock_user_role_repo_get
    ):
        '''Test create_user_role when user is already assigned to the role.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1,
                'joseph@mail.com'
            )
            mock_andela_service_get_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com'
            }
            mock_auth_get_location.return_value = 1
            mock_user_role_repo_get_unpaginated.return_value = None
            mock_user_role_repo_get.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_user_role()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This role does not exist'

    @patch.object(UserRoleRepo, 'new_user_role')
    @patch.object(RoleRepo, 'get')
    @patch.object(UserRoleRepo, 'get_unpaginated')
    @patch('app.Auth.get_location')
    @patch.object(RoleController, 'request_params')
    @patch.object(AndelaService, 'get_user_by_email_or_id')
    def test_create_user_role_ok_response(
        self,
        mock_andela_service_get_user,
        mock_role_controller_request_params,
        mock_auth_get_location,
        mock_user_role_repo_get_unpaginated,
        mock_role_repo_get,
        mock_user_role_repo_new_user_role
    ):
        '''Test create_user_role when user is already assigned to the role.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1,
                'joseph@mail.com'
            )
            mock_andela_service_get_user.return_value = {
                'id': 1,
                'mail': 'joseph@mail.com'
            }
            mock_auth_get_location.return_value = 1
            mock_user_role_repo_get_unpaginated.return_value = None
            mock_role_repo_get.return_value = self.mock_role
            mock_user_role_repo_new_user_role.return_value = \
                self.mock_user_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_user_role()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(UserRoleRepo, 'get')
    def test_delete_user_role_when_role_doesnot_exist(
        self,
        mock_user_role_repo_get
    ):
        '''Test delete_user_role when the role does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_user_role_repo_get.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.delete_user_role(1)

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'user_role_id provided'

    @patch.object(UserRoleRepo, 'update')
    @patch.object(UserRoleRepo, 'get')
    def test_delete_user_role_ok_response(
        self,
        mock_user_role_repo_get,
        mock_user_role_repo_update
    ):
        '''Test delete_user_role when the role does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_user_role_repo_get.return_value = self.mock_user_role
            mock_user_role_repo_update.return_value = self.mock_user_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.delete_user_role(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'user_role deleted for user'

    @patch.object(RoleController, 'request_params')
    @patch.object(UserRoleRepo, 'get')
    def test_disable_user_role_when_role_doesnot_exist(
        self,
        mock_user_role_repo_get,
        mock_role_controller_request_params
    ):
        '''Test disable_user_role when the role doesnot exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = 1
            mock_user_role_repo_get.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.disable_user_role()

            # Assert
            assert result.status_code == 404
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'user_role_id provided'

    @patch.object(UserRoleRepo, 'update')
    @patch.object(RoleController, 'request_params')
    @patch.object(UserRoleRepo, 'get')
    def test_disable_user_role_ok_response(
        self,
        mock_user_role_repo_get,
        mock_role_controller_request_params,
        mock_user_role_repo_update
    ):
        '''Test disable_user_role OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = 1
            mock_user_role_repo_get.return_value = self.mock_user_role
            mock_user_role_repo_update.return_value = self.mock_user_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.disable_user_role()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'user_role disabled for user'

    @patch.object(PermissionRepo, 'get_unpaginated')
    def test_get_role_permissions_ok_response(
        self,
        mock_permission_repo_get_unpaginated
    ):
        '''Test get_role_permissions OK response.
        '''
        # Arrange
        mock_permission = Permission(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            role_id=1,
            name='Mock permission',
            keyword='mock'
        )
        mock_permission_repo_get_unpaginated.return_value = [
            mock_permission,
        ]
        role_controller = RoleController(self.request_context)

        # Act
        result = role_controller.get_role_permissions(1)

        # Assert
        assert result.status_code == 200
        assert result.get_json()['msg'] == 'OK'

    @patch.object(PermissionRepo, 'filter_by')
    def test_get_single_permission_ok_response(
        self,
        mock_permission_repo_filter_by
    ):
        '''Test get_single_permission OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_permission_repo_filter_by.return_value = mock_permission
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.get_single_permission(1,1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(PermissionRepo, 'get_unpaginated')
    def test_get_all_permissions_ok_response(
        self,
        mock_permission_repo_get_unpaginated
    ):
        '''Test get_all_permissions OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_permission_repo_get_unpaginated.return_value = [
                mock_permission,
            ]
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.get_all_permissions()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get_unpaginated')
    def test_create_role_permission_when_permission_already_exists(
        self,
        mock_permission_repo_get_unpaginated,
        mock_role_controller_request_params
    ):
        '''Test create_role_permission when permission already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            mock_permission_repo_get_unpaginated.return_value = mock_permission
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_role_permission()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This permission already exists'

    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get_unpaginated')
    @patch.object(RoleRepo, 'get')
    def test_create_role_permission_when_role_doesnot_exist(
        self,
        mock_role_repo_get,
        mock_permission_repo_get_unpaginated,
        mock_role_controller_request_params
    ):
        '''Test create_role_permission when role does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            mock_permission_repo_get_unpaginated.return_value = None
            mock_role_repo_get.return_value = None
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.create_role_permission()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'This role does not exist'

    @patch.object(PermissionRepo, 'new_permission')
    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get_unpaginated')
    @patch.object(RoleRepo, 'get')
    def test_create_role_permission_ok_response(
        self,
        mock_role_repo_get,
        mock_permission_repo_get_unpaginated,
        mock_role_controller_request_params,
        mock_permission_repo_new_permission
    ):
        '''Test create_role_permission OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_role_repo_get.return_value = self.mock_role
            mock_permission_repo_get_unpaginated.return_value = None
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            mock_permission_repo_new_permission.return_value = mock_permission
            role_controller = RoleController(self.request_context)

            # Act
            result = role_controller.create_role_permission()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get')
    def test_update_permission_when_invalid_permission(
        self,
        mock_permission_repo_get,
        mock_role_controller_request_params
    ):
        '''Test update_permission when invalid permission id is provided.
        '''
        # Arrange
        with self.app.app_context():
            mock_permission_repo_get.return_value = None
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.update_permission(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'permission id provided'

    @patch.object(PermissionRepo, 'find_first')
    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get')
    def test_update_permission_when_permission_already_updated(
        self,
        mock_permission_repo_get,
        mock_role_controller_request_params,
        mock_permission_repo_find_first
    ):
        '''Test update_permission when permission already updated.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_permission_repo_get.return_value = mock_permission
            mock_permission_repo_find_first.return_value = mock_permission
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.update_permission(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Permission with this name ' \
                'already exists'

    @patch.object(RoleRepo, 'update')
    @patch.object(PermissionRepo, 'find_first')
    @patch.object(RoleController, 'request_params')
    @patch.object(PermissionRepo, 'get')
    def test_update_permission_ok_response(
        self,
        mock_permission_repo_get,
        mock_role_controller_request_params,
        mock_permission_repo_find_first,
        mock_role_repo_update
    ):
        '''Test update_permission when permission already updated.
        '''
        # Arrange
        with self.app.app_context():
            mock_role_controller_request_params.return_value = (
                1, 'name', 'keyword'
            )
            mock_permission = Permission(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role_id=1,
                name='Mock permission',
                keyword='mock'
            )
            mock_permission_repo_get.return_value = mock_permission
            mock_permission_repo_find_first.return_value = None
            mock_role_repo_update.return_value = self.mock_role
            role_controler = RoleController(self.request_context)

            # Act
            result = role_controler.update_permission(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
