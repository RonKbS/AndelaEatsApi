from flask import Blueprint, request
from app.utils.security import Security


class BaseBlueprint:
	
	base_url_prefix = '/api/v1'
	
	def __init__(self, app):
		self.app = app
	
	def register(self):
		
		''' Register All App Blue Prints Here '''
		
		from .meal_blueprint import meal_blueprint
		from .vendor_blueprint import vendor_blueprint, engagement_blueprint
		
		self.app.register_blueprint(meal_blueprint)
		self.app.register_blueprint(vendor_blueprint)
		self.app.register_blueprint(engagement_blueprint)