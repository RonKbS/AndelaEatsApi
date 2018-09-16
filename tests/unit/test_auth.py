from tests.base_test_case import BaseTestCase
from app.utils.auth import Auth
from config.env import app_env

class TestAuth(BaseTestCase):
	
	def setUp(self):
		self.BaseSetUp()
	
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
			
	def test_get_token_throws_exception_when_auth_header_missing(self):
		try:
			Auth.get_token()
			assert False
		except Exception as e:
			assert True
			
	def test_get_location_throws_exception_when_location_header_missing(self):
		try:
			Auth.get_location()
			assert False
		except Exception as e:
			assert True