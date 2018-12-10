import json
from app import create_app
from app.utils import db
from app.utils.auth import Auth
from flask_testing import TestCase
from flask import current_app


class BaseTestCase(TestCase):
	
	def BaseSetUp(self):
		"""Define test variables and initialize app"""
		self.app = self.create_app()
		self.client = self.app.test_client
		
		self.migrate()
		
	@staticmethod
	def get_valid_token():
		return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySW5mbyI6eyJpZCI6Ii1MNUo1Mzh5NzdXdk9uekoxRlBHIiwiZmlyc3RfbmFtZSI6IkVubyIsImxhc3RfbmFtZSI6IkJhc3NleSIsImZpcnN0TmFtZSI6IkVubyIsImxhc3ROYW1lIjoiQmFzc2V5IiwiZW1haWwiOiJlbm8uYmFzc2V5QGFuZGVsYS5jb20iLCJuYW1lIjoiRW5vIEJhc3NleSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLWJvM3RJS3NMYXVBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFjL1pXSGhuT2ZLbmJNL3Bob3RvLmpwZz9zej01MCIsInJvbGVzIjp7IkFuZGVsYW4iOiItS2lpaGZab3NlUWVxQzZiV1RhdSIsIlNlbmlvciBUZWNobmljYWwgQ29uc3VsdGFudCI6Ii1LYnVRZUkyLUtVZ1FQeFFESjh0IiwiQmVuY2ggVFRMIjoiLUxNM1JBYjE4ZGlXVUkwRjA0YVUifX0sImlhdCI6MTU0NDE5OTc4NiwiZXhwIjoxNTQ2NzkxNzg2LCJhdWQiOiJhbmRlbGEuY29tIiwiaXNzIjoiYWNjb3VudHMuYW5kZWxhLmNvbSJ9.oZj2NzAn3H_fueYUJ2o2vuMJSVozoXZiChvVdJhreIP3RAlR7rT7A1g_TneU6nWKd8NywSFVUGgNEl6wNGMkVKkdLfozhGULb-_0NpT1T9xx45bzhmphHh81ic5nKvZlwjf77Q9yGeVvY52COHWwT_Hb25o9xSLp1npSMerMln8'

	@staticmethod
	def user_id():
		return Auth.decode_token(BaseTestCase.get_valid_token())['UserInfo']['id']
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

