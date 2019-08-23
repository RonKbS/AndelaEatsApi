import datetime
from tests.base_test_case import BaseTestCase
from app.repositories import PermissionRepo
from factories import PermissionFactory, RoleFactory, UserRoleFactory


class TestPermissionEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_permission_without_right_permission(self):
        permission = PermissionFactory.build()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='wrong_keyword', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {'name': permission.name, 'keyword': permission.keyword, 'role_id': role.id}
        response = self.client().post(self.make_url('/roles/permissions'),
            data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        
        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')
    
    def test_create_permission_with_right_permission(self):
        permission = PermissionFactory.build()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_permissions', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {'name': permission.name, 'keyword': permission.keyword, 'role_id': role.id}
        response = self.client().post(self.make_url('/roles/permissions'),
            data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        
        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['permission']['name'], permission.name)
        self.assertEqual(payload['permission']['keyword'], permission.keyword)
        
    def test_list_permissions_without_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        for i in range(1,4):
            permission_repo.new_permission(role1.id, f'name-{i}', f'keyword-{i}')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_permissions', role_id=role1.id)
        UserRoleFactory.create(user_id=user_id, role_id=100)
        
        response = self.client().get(self.make_url('/roles/permissions'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_list_permissions_with_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        for i in range(1,4):
            permission_repo.new_permission(role1.id, f'name-{i}', f'keyword-{i}')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        
        response = self.client().get(self.make_url('/roles/permissions'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['permissions']), 4)
        self.assertJSONKeysPresent(payload['permissions'][0], 'name', 'keyword', 'roleId')
        
    def test_update_permissions_without_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission = permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role_id=100)
        data = {'name': 'New name1', 'role_id': role1.id, 'keyword': 'New eky'}
        response = self.client().put(self.make_url('/roles/permissions/{}'.format(permission.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_update_permissions_with_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission = permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        data = {'name': 'New name1', 'role_id': role1.id, 'keyword': 'New eky'}
        response = self.client().put(self.make_url('/roles/permissions/{}'.format(permission.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['permission']['name'], data['name'])

    def test_update_with_wrong_permission_id(self):

        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission = permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        data = {'name': 'New name1', 'role_id': role1.id, 'keyword': 'New eky'}

        response = self.client().put(self.make_url(f'/roles/permissions/1000'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Invalid or incorrect permission id provided')

    def test_delete_permission_endpoint_with_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission = permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().delete(self.make_url(f'/roles/permissions/{permission.id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(response_json['msg'], 'permission deleted')

    def test_delete_permission_endpoint_without_right_permission(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission = permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role_id=1000)

        response = self.client().delete(self.make_url(f'/roles/permissions/{permission.id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_delete_permission_endpoint_with_wrong_permission_id(self):
        permission_repo = PermissionRepo()
        role1 = RoleFactory.create(name='admin')
        permission_repo.new_permission(role1.id, 'name-1', 'keyword-1')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_permissions', role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        response = self.client().delete(self.make_url(f'/roles/permissions/576'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'Invalid or incorrect permission id provided')
