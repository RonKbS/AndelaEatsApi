from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth


class BaseBlueprint:
	
	base_url_prefix = '/api/v1'
	
	def __init__(self, app):
		self.app = app
	
	def register(self):
		
		''' Register All App Blue Prints Here '''
		
		from app.blueprints.meal_blueprint import meal_blueprint
		from app.blueprints.vendor_blueprint import vendor_blueprint, engagement_blueprint
		from app.blueprints.location_blueprint import location_blueprint
		from app.blueprints.role_blueprint import role_blueprint
		
		self.app.register_blueprint(meal_blueprint)
		self.app.register_blueprint(vendor_blueprint)
		self.app.register_blueprint(engagement_blueprint)
		self.app.register_blueprint(location_blueprint)
		self.app.register_blueprint(role_blueprint)