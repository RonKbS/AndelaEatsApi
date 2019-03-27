"""Integration tests for the User Blueprint.
"""
from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from app.utils.auth import PermissionRepo, UserRoleRepo
from factories import UserFactory, RoleFactory, PermissionFactory, UserRoleFactory


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

    def test_list_users_endpoint(self):
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_users', role_id=role.id)
        UserRoleFactory.create(user_id=user_id, role_id=role.id)

        # Create ten Dummy users
        UserFactory.create_batch(10)

        response = self.client().get(self.make_url('/users/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['users']), 10)
        self.assertJSONKeysPresent(payload['users'][0], 'firstName', 'lastName', 'slackId', 'email')

