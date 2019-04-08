from os import getenv, environ
import jwt
import json
from app import create_app
from app.utils import db
from app.utils.auth import Auth
from flask_testing import TestCase
from faker import Faker

config_name = 'testing'
environ['APP_ENV'] = config_name
fake = Faker()

class BaseTestCase(TestCase):

	VALID_TOKEN = None

	def BaseSetUp(self):
		"""Define test variables and initialize app"""
		self.app = self.create_app()
		self.client = self.app.test_client

		self.migrate()

	@staticmethod
	def generate_token(exp=None):
		"""
        Generates jwt tokens for testing purpose

        params:
            exp: Token Expiration. This could be datetime object or an integer
        result:
            token: This is the bearer token in this format 'Bearer token'
        """

		secret_key = getenv('JWT_SECRET_KEY')
		payload = {
			'UserInfo': User().to_dict(),
			'iss': 'accounts.andela.com',
			'aud': 'andela.com',
		}
		payload.__setitem__('exp', exp) if exp is not None else ''

		token = jwt.encode(payload, secret_key, algorithm='RS256').decode('utf-8')
		return token
		
	@staticmethod
	def get_valid_token():

		if not BaseTestCase.VALID_TOKEN:
			BaseTestCase.VALID_TOKEN = BaseTestCase.generate_token()

		return BaseTestCase.VALID_TOKEN

	@staticmethod
	def user_id():
		return Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['id']

	@staticmethod
	def user_email():
		return Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['email']

	@staticmethod
	def user_first_and_last_name():
		return (
				Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['firstName'],
				Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['lastName']
		)

	@staticmethod
	def get_invalid_token():
		return 'some.invalid.token'
		
	def create_app(self):
		"""Create the app and specify 'testing' as the environment"""
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client()
		self.request_context = self.app.test_request_context()
		self.url = '/api/v1'

		@self.app.before_request
		def check_token():
			return Auth.check_token()

		@self.app.before_request
		def check_location_header():
			return Auth.check_location_header()
		
		''' Init DB'''
		
		return self.app
	
	@staticmethod
	def encode_to_json_string(data_object):
		return json.dumps(data_object)
	
	@staticmethod
	def decode_from_json_string(data_str):
		return json.loads(data_str)
	
	def make_url(self, path):
		return '{}{}'.format(self.url, path)
	
	
	@staticmethod
	def migrate():
		db.session.close()
		db.drop_all()
		db.create_all()
	
	@staticmethod
	def headers():
		return  {
			'Content-Type': 'application/json',
			'X-Location': '1',
			'Authorization': 'Bearer {}'.format(BaseTestCase.get_valid_token()),
			}
	
	@staticmethod
	def headers_without_token():
		return {
			'Content-Type': 'application/json',
			'X-Location': '1',
		}
	
	@staticmethod
	def assertJSONKeyPresent(json_object, key):
		if type(json_object) is str:
			json_obj = BaseTestCase.decode_from_json_string(json_object)
		elif type(json_object) is dict:
			json_obj = json_object
		
		if key in json_obj:
			assert True
		else:
			assert False
				
	@staticmethod
	def assertJSONKeysPresent(json_object, *keys):
		error_flag = 0
		if type(json_object) is str:
			json_obj = BaseTestCase.decode_from_json_string(json_object)
		elif type(json_object) is dict:
			json_obj = json_object
		
		for key in keys:
			
			if key not in json_obj:
				error_flag += 1
		
		if error_flag == 0:
			assert True
		else:
			assert False

	@staticmethod
	def construct_mock_response(json_data, status_code):
		class MockResponseClass:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		return MockResponseClass(json_data, status_code)


class User:
	"""Class for creating user mocks"""

	def __init__(self):
		self.first_name = fake.first_name()
		self.id = "-LG__88sozO1OGrqda2z"
		self.last_name = fake.last_name()
		self.firstName = self.first_name
		self.lastName = self.last_name
		self.email = fake.email()
		self.name = f'{self.first_name} {self.last_name}'
		self.picture = fake.image_url(height=None, width=None)
		self.roles = {
			"Technology": "-KXH7iME4ebMEXAEc7HP",
			"Andelan": "-KiihfZoseQeqC6bWTau"
		}

	def to_dict(self):
		"""Converts the instance of this class to a dict.

        Returns:
            dict : User data dictionary.
        """
		return {
				"id": self.id,
				"first_name": self.first_name,
				"last_name": self.last_name,
				"firstName": self.firstName,
				"lastName": self.lastName,
				"email": self.email,
				"name": self.name,
				"picture": self.picture,
				"roles": self.roles
			}

