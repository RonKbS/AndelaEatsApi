import jwt
import json
from flask import request, jsonify, make_response

class Auth:
	''' This class will house Authentication and Authorization Methods '''
	
	@staticmethod
	def check_token():
		try:
			token = Auth.get_token()
		except Exception as e:
			return make_response(jsonify({'msg': str(e)}),400)
		
		try:
			decoded = Auth.decode_token(token)
		except Exception as e:
			return make_response(jsonify({'msg': str(e)}), 400)
	
	@staticmethod
	def get_user():
		token = None
		try:
			token = Auth.get_token()
		except Exception as e:
			raise e
		
		try:
			if token:
				return json.loads(Auth.decode_token(token)['UserInfo'])
		except Exception as e:
			raise e
	
	@staticmethod
	def get_token():
		header = request.headers.get('Authorization', None)
		if not header:
			raise Exception('Authorization Header is Expected')
		
		header_parts = header.split()
		
		if header_parts[0].lower() != 'bearer':
			raise Exception('Authorization Header Must Start With Bearer')
		elif len(header_parts) > 1:
			return header_parts[1]
		
		raise Exception('Internal Application Error')
	
	@staticmethod
	def decode_token(token, jwtsecret=''):
		try:
			decoded = jwt.decode(token, jwtsecret, verify=False)
			return decoded
		except jwt.ExpiredSignature:
			raise Exception('Token is Expired')
		except jwt.DecodeError:
			raise Exception('Error Decoding')
		