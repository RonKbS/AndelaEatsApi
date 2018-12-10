""" Andela API Gateway Service Wrappe """

import requests
from config import get_env
from app.utils.Cache import Cache


class AndelaService:
	
	def __init__(self):
		self.API_URL = 'http://api.andela.com/api/v1'
		self.API_TOKEN = get_env('ANDELA_API_TOKEN')
		self.HEADERS = {'api-token': self.API_TOKEN}
		
		self.cache = Cache()
		
	def call(self, method, url_path, **kwargs):
		url = self.create_request_url(url_path)
		
		r = requests.request(method, url, headers=self.HEADERS, **kwargs)
		if r.status_code in [200, 201]:
			return r.json()
		else:
			raise Exception('Service Error: {}'.format(r.json()))
			
	def create_request_url(self, url_path):
		if url_path[0] == '/':
			url_path = url_path[1:]
			
			return f'{self.API_URL}/{url_path}'
	
	def get_user_by_email_or_id(self, key):
		
		if key.find('@') > -1:
			url_path = f'/users?email={key}'
			cache_key = key.replace('@', '')
		else:
			url_path = f'/users?ids={key}'
			cache_key = key

		user = self.cache.get(cache_key)

		if user is None:
			user_data = self.call('GET', url_path)
			user = user_data['values'][0]
			self.cache.set(cache_key, user)
		return user
