import redis
import json
from datetime import datetime
from config import get_env


class Cache:
	
	def __init__(self, adapter='redis', redis_connection={'host': get_env('REDIS_HOST'), 'port': get_env('REDIS_PORT'), 'db': get_env('REDIS_DB')}):
		self.cache_obj = None
		if adapter == 'redis':
			pool = redis.ConnectionPool(**redis_connection)
			self.cache_obj = redis.StrictRedis(connection_pool=pool)
	
	def _handle(self, obj):
		if isinstance(obj, datetime):
			return obj.__str__()
	
	def set(self, key, value):
		self.cache_obj.set(key, json.dumps(value, default=self._handle))
	
	def get(self, key):
		obj = self.cache_obj.get(key)
		if obj:
			return json.loads(obj)
		return obj

