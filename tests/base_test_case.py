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
		return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySW5mbyI6eyJpZCI6Ii1MR19fODhzb3pPMU9HcnFkYTJ6IiwiZmlyc3RfbmFtZSI6IkVubyIsImxhc3RfbmFtZSI6IkJhc3NleSIsImZpcnN0TmFtZSI6IkVubyIsImxhc3ROYW1lIjoiQmFzc2V5IiwiZW1haWwiOiJlbm8uYmFzc2V5QGFuZGVsYS5jb20iLCJuYW1lIjoiRW5vIEJhc3NleSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLWJvM3RJS3NMYXVBL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFjL1pXSGhuT2ZLbmJNL3Bob3RvLmpwZz9zej01MCIsInJvbGVzIjp7IlRlY2hub2xvZ3kiOiItS1hIN2lNRTRlYk1FWEFFYzdIUCIsIkFuZGVsYW4iOiItS2lpaGZab3NlUWVxQzZiV1RhdSJ9fSwiaWF0IjoxNTQ2OTM4NDk4LCJleHAiOjE1NDk1MzA0OTgsImF1ZCI6ImFuZGVsYS5jb20iLCJpc3MiOiJhY2NvdW50cy5hbmRlbGEuY29tIn0.Z6zQ8dtIW1OXD8OdW2QtfHcwPvpwFzCg12zp0l6lfNv4NxIZPmM9kdzXPcTXO0y7g56HwmD-xo0wLy3AoJbfCYyZILmvrOiPMXwQyKBQPnY3XGG9p5kttTP8VWJ_4fQsRtlFJuhb5Q-nlBudiuyh2iCEdQ2_i-OGLyVqDMBse5g'

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

