from app.utils.auth import Auth
from flask import jsonify, make_response
from app.utils.snake_case import SnakeCaseConversion

class BaseController:
	
	def __init__(self, request):
		self.request = request
		
	def user(self, *keys):
		return Auth.user(*keys)
		
	def request_params(self, *keys):
		_json = self.get_json()
		if keys:
			values = list()
			for key in keys:
				values.append(_json.get(key))
			return values
		
		return _json

	def request_params_dict(self, *keys):
		params = {}

		for key in keys:
			value = self.get_json().get(key)
			params.__setitem__(SnakeCaseConversion.camel_to_snake(key), value) if value else None

		if not keys:
			for key, value in self.get_json().items():
				params.__setitem__(SnakeCaseConversion.camel_to_snake(key), value)

		return params

	
	def post_params(self, *keys):
		values = list()
		for key in keys:
			values.append(self.request.data.get(key))
		return values
	
	def get_params(self, *keys):
		values = list()
		for key in keys:
			values.append(self.request.args.get(key))
		return values

	def get_params_dict(self):
		args = {}
		for key in self.request.args:
			args.__setitem__(SnakeCaseConversion.camel_to_snake(key), self.request.args.get(key))

		return args
	
	def get_json(self):
		return self.request.get_json()
	
	def get_int_params(self):
		params = self.get_params_dict()
		for key, value in params.items():
			try:
				params[key] = int(value)
			except ValueError:
				raise ValueError(f'{key} must an integer')
		return params
				
	
	def handle_response(self, msg='OK', payload=None, status_code=200, slack_response=None):
		
		# If there is no specific slack formatted response, default to WEB API Response format
		if slack_response is None:
			data = {'msg': msg}
			if payload is not None:
				data['payload'] = payload
		else:
			data = slack_response
		
		response = jsonify(data)
		response.status_code = status_code
		return response
	
	def missing_required(self, params):
		return True if None in params or '' in params else False
	
	def missing_response(self, msg='Missing Required Parameters'):
		return self.handle_response(msg=msg, status_code=400)
	
	def pagination_meta(self, paginator):
		return {'total_rows': paginator.total, 'total_pages': paginator.pages, 'current_page': paginator.page,
				'next_page': paginator.next_num, 'prev_page': paginator.prev_num}
	
	def prettify_response_dates(self, created_at, updated_at=None):
		return {'created_at': created_at, 'updated_at': updated_at,
				'date_pretty_short': created_at.strftime('%b %d, %Y'), 'date_pretty': created_at.strftime('%B %d, %Y')}

	@staticmethod
	def return_transformed_enum_items(enums, items):
		"""Transform enum types to strings of returned paginated items

			: param1 target(tuple): A tuple of keys corresponding to dictionary values that are enum types
			: param2 items(list): A list of items in a paginator

			: return(list): list of transformed items
		"""
		transformed_items = []

		for activity in items:

			activity_item = activity.serialize()

			for each_enum in enums:
				activity_item[each_enum] = activity_item[each_enum].value

			transformed_items.append(activity_item)

		return transformed_items
