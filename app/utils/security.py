from functools import wraps
from datetime import datetime
from flask import request, make_response, jsonify

class Security:
	
	@staticmethod
	def validator(rules):
		"""
		:rules: list -  The sets of keys and rules to be appliesd
		example: [username|required:max-255:min-120, email|required:email]
		"""
		
		def real_validate_request(f):
			
			@wraps(f)
			def decorated(*args, **kwargs):
				if not request.json:
					return make_response(jsonify({'msg':'Bad Request - Request Must be JSON Formatted'})), 400
				
				payload = request.get_json()
				
				if payload:
					#Loop through all validation rules
					for rule in rules:
						rule_array = rule.split('|')
						
						request_key = rule_array[0]
						validators = rule_array[1].split(':')
							
						# If the key is not in the request payload, and required is not part of the validator rules,
						# Continue the loop to avoid key errors.
						if request_key not in payload and 'required' not in validators:
							continue
						
						#Loop all validators specified in the current rule
						for validator in validators:
							
							if validator == 'int' and type(payload[request_key]) is str and not payload[request_key].isdigit():
								return make_response(jsonify({'msg': 'Bad Request - {} must be integer'.format(request_key)})), 400
							
							if validator == 'float':
								try:
									float(payload[request_key])
								except Exception as e:
									return make_response(jsonify({'msg': 'Bad Request - {} must be float'.format(request_key)})), 400
							
							if (validator == 'required' and request_key not in payload) or payload[request_key] == '':
								return make_response(jsonify({'msg': 'Bad Request - {} is required'.format(request_key)})), 400
							
							if validator.find('max') > -1:
								pass
							
							if validator.find('min') > -1:
								pass
							
							if validator == 'date':
								try:
									datetime.strptime(payload[request_key], '%Y-%m-%d')
								except Exception as e:
									return make_response(jsonify({'msg': 'Bad Request - {} should be valid date. Format: YYYY-MM-DD'.format(request_key)})), 400

							if validator == 'list' and type(payload[request_key]) is not list:
								return make_response(jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400
							
				return f(*args, **kwargs)
			
			return decorated
		
		return real_validate_request