"""Integration tests for the User Blueprint.
"""
from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from app.utils.auth import PermissionRepo, UserRoleRepo


class TestUserEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch.object(PermissionRepo,'get_unpaginated')
    @patch.object(UserRoleRepo, 'find_first')
    def test_get_admin_user_endpoint_with_right_permission(
        self,
        mock_user_role_repo_find_first,
        mock_permission_repo_get_unpaginated
        ):

        class MockUserRoleRep:
            def __init__(self, role_id):
                self.role_id = role_id

        class MockPermissionRepo:
            def __init__(self, keyword):
                self.keyword = keyword

        mock_user_role_repo = MockUserRoleRep(1)
        mock_user_perms = MockPermissionRepo("create_user_roles")

        with self.app.app_context():
            mock_user_role_repo_find_first.return_value = mock_user_role_repo
            mock_permission_repo_get_unpaginated.return_value = [mock_user_perms]

            response = self.client().get(self.make_url('/users/admin'), headers=self.headers())
            response = response.get_json()

            assert response['msg'] == 'OK'
            assert response['payload'].get('AdminUsers') == []
