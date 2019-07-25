import datetime
from tests.base_test_case import BaseTestCase
from tests import create_user_role
from app.repositories import RoleRepo
from factories import PermissionFactory, RoleFactory, UserRoleFactory, UserFactory, LocationFactory
from .user_role import create_user_role
from unittest.mock import Mock, patch


class TestRoleEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_role_endpoint(self):
        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='create_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)

        data = {'name': 'Jack Jones', 'help': 'A Help Message'}
        response = self.client().post(self.make_url('/roles/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['role']['name'], 'Jack Jones')
        self.assertEqual(payload['role']['help'], 'A Help Message')

    def test_list_roles_endpoint(self):
        
        RoleFactory.create_batch(3)
        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='view_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().get(self.make_url('/roles/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['roles']), 4)
        self.assertJSONKeysPresent(payload['roles'][0], 'name', 'help')

    def test_get_specific_role_enpoint(self):
        role = RoleFactory.create()
        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='view_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)
        response = self.client().get(self.make_url('/roles/{}'.format(role.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(payload, 'role')
        self.assertJSONKeysPresent(payload['role'], 'name', 'help')
        self.assertEqual(payload['role']['id'], role.id)
        self.assertEqual(payload['role']['name'], role.name)
        self.assertEqual(payload['role']['help'], role.help)

    def test_list_user_endpoint(self):
        role = RoleFactory()
        user_role = UserRoleFactory(role_id=role.id)
        user = UserFactory(slack_id='-LMnsyxrsj_TEYEAHCBk', user_type_id=user_role.id)

        create_user_role('view_users')

        response = self.client().get(self.make_url(f'/users/{user.slack_id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)

    def test_update_roles_endpoint(self):

        role = RoleFactory.create()
        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='create_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)
        data = {'name': 'Super Admin'}
        response = self.client().put(self.make_url('/roles/{}'
        .format(role.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['role']['name'], data['name'])

    def test_invalid_update(self):

        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='create_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)
        data = {'name': 'Super Admin'}
        response = self.client().put(self.make_url('/roles/1000'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert400(response)

    def test_delete_role_endpoint_with_right_permission(self):
        role = RoleFactory.create()

        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword='delete_roles', role=role1)
        user_role = UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().delete(self.make_url(f'/roles/{role.id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(response_json['msg'], 'role deleted')

    def test_delete_role_endpoint_without_right_permission(self):
        role = RoleFactory.create()

        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_roless', role_id=100)
        UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().delete(self.make_url(f'/roles/{role.id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_delete_role_endpoint_with_wrong_role_id(self):

        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_roles', name='delete_roles', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().delete(self.make_url(f'/roles/1576'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'Invalid or incorrect role_id provided')

    def test_get_user_role_endpoint(self):

        new_role, user_id = create_user_role('view_user_roles')
        new_role.save()
        role = RoleFactory()
        user_role = UserRoleFactory(role=role)
        user = UserFactory(user_type_id=user_role.id)

        response = self.client().get(self.make_url(f'/roles/user/{user_role.user_id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user_role'][0]['id'], user_role.id)

    @patch('app.controllers.role_controller.AndelaService.get_user_by_email_or_id')
    def test_create_user_role_endpoint(self, mock_andela_get_user_by_email):
        location = LocationFactory.create()
        user = UserFactory()
        mock_andela_get_user_by_email.return_value = {'id': user.user_id}

        create_user_role('create_user_roles')

        new_role = RoleFactory.create()

        user_role_data = { 'roleId': new_role.id, 'emailAddress': self.user_email()}
        headers = self.headers()
        headers.update({'X-Location': location.id})
        response = self.client().post(self.make_url(f'/roles/user'), data=self.encode_to_json_string(user_role_data),
                                      headers=headers)

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user_role']['roleId'], new_role.id)

    def test_delete_user_role(self):
        create_user_role('delete_user_roles')

        new_role, _ = create_user_role('test_role')
        new_role.save()
        response = self.client().delete(self.make_url(f'/roles/user/delete/{new_role.id}'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'user_role deleted for user')
        self.assertEqual(response_json['payload']['status'], 'success')

    def test_disable_user_role_endpoint(self):
        create_user_role('delete_user_roles')

        new_role, _ = create_user_role('test_role')
        new_role.save()

        user_role_data = {'roleId': new_role.role_id, 'userId': new_role.user_id}

        response = self.client().post(self.make_url(f'/roles/user/disable/'), data=self.encode_to_json_string(user_role_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'user_role disabled for user')
        self.assertEqual(response_json['payload']['status'], 'success')

    def test_get_role_permissions(self):
        new_role, _ = create_user_role('view_permissions')
        new_role.save()
        response = self.client().get(self.make_url(f'/roles/{new_role.id}/permissions'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['role_id'], new_role.id)

    def test_get_single_permission_endpoint(self):
        create_user_role('view_permissions')

        new_role = RoleFactory.create()
        new_role.save()
        new_permission = PermissionFactory.create(keyword='delete_roles', name='delete_roles', role=new_role)
        new_permission.save()
        response = self.client().get(self.make_url(f'/roles/{new_role.id}/permissions/{new_permission.id}'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['permission'][0]['id'], new_permission.id)
