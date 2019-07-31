"""Integration tests for the User Blueprint.
"""
from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from app.utils.auth import PermissionRepo, UserRoleRepo
from factories import UserFactory, RoleFactory, PermissionFactory, UserRoleFactory, LocationFactory
from .user_role import create_user_role


class TestUserEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

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
            assert response['payload'].get('adminUsers') == []

    def test_list_users_endpoint(self):
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_users', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        # Create ten Dummy users
        UserFactory.create_batch(10)

        response = self.client().get(self.make_url('/users/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['users']), 10)
        self.assertJSONKeysPresent(payload['users'][0], 'firstName', 'lastName', 'slackId')

    def test_delete_user_endpoint_with_right_permission(self):
        user = UserFactory.create()
        user.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_user', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/users/{user.id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(response_json['msg'], 'User deleted')

    def test_delete_already_deleted_user_with_right_permission(self):
        user = UserFactory.create(is_deleted= True)
        user.save()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_user', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/users/{user.id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assert400(response)
        self.assertEqual(400,response.status_code)
        self.assertEqual(response_json['msg'], 'User has already been deleted')

    def test_delete_vendor_endpoint_without_right_permission(self):
        user = UserFactory.create()
        user.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='wrong_permission', role_id=100)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/users/{user.id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_delete_user_endpoint_with_wrong_user_id(self):
        user = UserFactory.create()
        user.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_user', role=role)
        UserRoleFactory.create(user_id=user_id, role_id=user.id)

        response = self.client().delete(self.make_url(f'/userrs/-576A/'), headers=self.headers())

        self.assert404(response)

    def test_create_user_endpoint_succeeds1(self):
        location = LocationFactory()
        create_user_role('create_user')
        user = UserFactory.build()
        user.save()
        role = RoleFactory()
        user_data = dict(firstName=user.first_name, lastName=user.last_name, roleId=role.id)

        headers = self.headers()
        headers.update({'X-Location': location.id})

        response = self.client().post(self.make_url("/users/"), headers=headers,
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)

    def test_create_user_endpoint_succeeds2(self):
        location = LocationFactory.create()
        headers = self.headers()
        headers.update({'X-Location': location.id})

        create_user_role('view_users')
        user = UserFactory(slack_id="-LXTuXlk2W4Gskt8KTte")
        user.save()

        response = self.client().get(
            self.make_url(f'/users/{user.slack_id}/'),
            headers=headers
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)

    def test_update_user_endpoint_succeeds(self):

        create_user_role('update_user')
        role = RoleFactory()
        user_role = UserRoleFactory(role=role)
        user_role.save()
        user = UserFactory(user_type=user_role)
        user.save()
        user_data = dict(firstName="Andela", lastName="Eats", roleId=role.id)

        response = self.client().patch(
            self.make_url(f'/users/{user.id}'),
            headers=self.headers(),
            data=self.encode_to_json_string(user_data)
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)

    def test_update_user_endpoint_with_invalid_role_fails(self):
        create_user_role('update_user')
        role = RoleFactory()
        user_role = UserRoleFactory(role=role)
        user = UserFactory(user_type=user_role)
        user.save()
        user_data = dict(firstName="Andela", lastName="Eats", roleId=100)

        response = self.client().patch(self.make_url(f'/users/{user.id}'), headers=self.headers(),
                                       data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Role with id 100 doesnot exist')

    def test_update_user_endpoint_for_another_user_with_same_slack_id_fails(self):

        create_user_role('update_user')
        UserFactory.create(slack_id="slack_id_1")
        user = UserFactory.create(slack_id="slack_id_2")
        user.save()

        user_data = dict(firstName="Andela", lastName="Eats", slackId="slack_id_1")

        response = self.client().put(self.make_url("/users/" + str(user.id)), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_json['msg'], 'FAIL')
        self.assertEqual(
            response_json['payload']['user'],
            'Cannot update to the slack id of another existing user'
        )

    def test_update_user_endpoint_for_another_user_with_same_user_id_fails(self):

        create_user_role('update_user')
        UserFactory.create(user_id="user_id_1")
        user = UserFactory.create(user_id="user_id_2")
        user.save()

        user_data = dict(firstName="Andela", lastName="Eats", userId="user_id_1")

        response = self.client().put(self.make_url("/users/" + str(user.id)), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_json['msg'], "FAIL")
        self.assertEqual(
            response_json['payload']['user'],
            'Cannot update to the user id of another existing user'
        )

    def test_update_user_endpoint_for_non_existing_user_id_fails(self):

        create_user_role('update_user')
        user = UserFactory.create(user_id="user_id_2")
        user.save()

        user_data = dict(firstName="Andela", lastName="Eats", userId="user_id_1")

        response = self.client().put(self.make_url("/users/" + str(user.id + 1)), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], "FAIL")
        self.assertEqual(
            response_json['payload']['user'],
            'User not found'
        )

    def test_update_user_endpoint_for_already_deleted_user_fails(self):

        create_user_role('update_user')
        user = UserFactory.create(user_id="user_id_2", is_deleted=True)
        user.save()

        user_data = dict(firstName="Andela", lastName="Eats", userId="user_id_2")

        response = self.client().put(self.make_url("/users/" + str(user.id)), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], "FAIL")
        self.assertEqual(
            response_json['payload']['user'],
            'User already deleted'
        )
    
    def test_list_users_endpoint_without_users(self):
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_users', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().get(self.make_url('/users/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)

    def test_create_user_endpoint_succeeds(self):
        create_user_role('create_user')
        user = UserFactory.create(user_id="user_id_2", is_deleted=True)
        role = RoleFactory(name='test_role')

        location = LocationFactory.create()
        headers = self.headers()
        headers.update({'X-Location': location.id})

        user_data = dict(
            firstName=user.first_name,
            lastName=user.last_name,
            roleId=role.id
        )

        response = self.client().post(
            self.make_url("/users/"),
            headers=headers,
            data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], "OK")
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)
        self.assertEqual(response_json['payload']['user']['userRoles'][0]['name'], role.name)
        self.assertEqual(response_json['payload']['user']['userRoles'][0]['help'], role.help)

