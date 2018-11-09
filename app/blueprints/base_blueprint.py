from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth



class BaseBlueprint:
	
	base_url_prefix = '/api/v1'
	
	def __init__(self, app):
		self.app = app
	
	def register(self):
		
		''' Register All App Blue Prints Here '''
		
		from app.blueprints.meal_item_blueprint import meal_item_blueprint
		from app.blueprints.vendor_blueprint import vendor_blueprint
		from app.blueprints.location_blueprint import location_blueprint
		from app.blueprints.role_blueprint import role_blueprint
		from app.blueprints.menu_blueprint import menu_blueprint
		from app.blueprints.order_blueprint import order_blueprint
		from app.blueprints.vendor_rating_blueprint import rating_blueprint
		from app.blueprints.vendor_engagement_blueprint import engagement_blueprint
		
		self.app.register_blueprint(meal_item_blueprint)
		self.app.register_blueprint(vendor_blueprint)
		self.app.register_blueprint(engagement_blueprint)
		self.app.register_blueprint(rating_blueprint)
		self.app.register_blueprint(location_blueprint)
		self.app.register_blueprint(role_blueprint)
		self.app.register_blueprint(menu_blueprint)
		self.app.register_blueprint(order_blueprint)

