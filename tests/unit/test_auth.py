from tests.base_test_case import BaseTestCase
from app.utils.auth import Auth
from factories.role_factory import RoleFactory
from factories.user_role_factory import UserRoleFactory
from factories.permission_factory import PermissionFactory
from ppretty import ppretty

class TestAuth(BaseTestCase):
	
	def setUp(self):
		self.BaseSetUp()
	
	def test_get_user_method_return_dict_of_user_data_if_valid_header_present(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			user_data = Auth._get_user()
			
			self.assertIsInstance(user_data, dict)
			self.assertIsNotNone(user_data)
			self.assertJSONKeysPresent(user_data, 'id', 'first_name', 'last_name', 'email')
	
	def test_user_method_return_list_of_user_data_based_on_supplied_keys(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			decoded = Auth.decode_token(self.get_valid_token())
			
			values = Auth.user('id', 'first_name', 'last_name', 'email')
			id, first_name, last_name, email = values
			
			self.assertIsInstance(values, list)
			self.assertEquals(decoded['UserInfo']['id'], id)
			self.assertEquals(decoded['UserInfo']['first_name'], first_name)
			self.assertEquals(decoded['UserInfo']['last_name'], last_name)
			self.assertEquals(decoded['UserInfo']['email'], email)
	
	def test_get_token_throws_exception_when_auth_header_missing(self):
		try:
			Auth.get_token()
			assert False
		except Exception as e:
			assert True
	
	def test_get_token_return_token_if_valid_header_present(self):
		
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			token = Auth.get_token()
			
			self.assertIsInstance(token, str)
			self.assertIsNotNone(token)
			
			
	def test_decode_token_throws_exception_on_invalid_token(self):
		try:
			Auth.decode_token(self.get_invalid_token())
			assert False
		except Exception as e:
			assert True
	
	def test_decode_token_returns_dict_on_valid_token(self):
		token = Auth.decode_token(self.get_valid_token())
		if type(token) is dict:
			assert True
		else:
			assert False
			
	def test_get_location_throws_exception_when_location_header_missing(self):
		try:
			Auth.get_location()
			assert False
		except Exception as e:
			assert True
			
	def test_get_location_header_returns_int_value_when_location_header_present(self):
		with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
			location = Auth.get_location()
			self.assertIsInstance(location, int)
			self.assertIsNotNone(location)
			

	# def test_has_permission_checks_valid_permissions(self):
	# 	'''To test the has_permission method, We need to create a mock role, user role maping and role-permission mapping '''
	#
	#
	# 	with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
	# 		user_id = Auth.user('id')
	#
	# 		role = RoleFactory(id=1)
	# 		user_role = UserRoleFactory(role_id=role.id, user_id=user_id)
	# 		perm = PermissionFactory(id=1, role_id=role.id, keyword='login')
	#
	# 		r = Auth.has_permission('create_account')
	#
	#
	# 		# print(user_id, role.id, role.name, user_role.role_id, user_role.user_id, perm.role_id, r.data.decode('utf-8'))
	#
	# 		assert False