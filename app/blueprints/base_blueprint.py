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
		from app.blueprints.menu_blueprint import user_menu_blueprint
		from app.blueprints.order_blueprint import order_blueprint
		from app.blueprints.vendor_rating_blueprint import rating_blueprint
		from app.blueprints.vendor_engagement_blueprint import engagement_blueprint
		from app.blueprints.bot_blueprint import bot_blueprint
		from app.blueprints.user_blueprint import user_blueprint
		from app.blueprints.faq_blueprint import faq_blueprint
		from app.blueprints.reports_blueprint import reports_blueprint
		from app.blueprints.activity_blueprint import activity_blueprint
		from app.blueprints.about_blueprint import about_blueprint
		from app.blueprints.meal_session_blueprint import meal_session_blueprint
		from app.blueprints.menu_template_blueprint import menu_template_blueprint
		
		self.app.register_blueprint(meal_item_blueprint)
		self.app.register_blueprint(vendor_blueprint)
		self.app.register_blueprint(engagement_blueprint)
		self.app.register_blueprint(rating_blueprint)
		self.app.register_blueprint(location_blueprint)
		self.app.register_blueprint(role_blueprint)
		self.app.register_blueprint(menu_blueprint)
		self.app.register_blueprint(user_menu_blueprint)
		self.app.register_blueprint(order_blueprint)
		self.app.register_blueprint(bot_blueprint)
		self.app.register_blueprint(user_blueprint)
		self.app.register_blueprint(faq_blueprint)
		self.app.register_blueprint(reports_blueprint)
		self.app.register_blueprint(activity_blueprint)
		self.app.register_blueprint(about_blueprint)
		self.app.register_blueprint(meal_session_blueprint)
		self.app.register_blueprint(menu_template_blueprint)
