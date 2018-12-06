from sqlalchemy import and_
from app.controllers.base_controller import BaseController
from app.repositories import OrderRepo, LocationRepo
from app.repositories.meal_item_repo import MealItemRepo
from datetime import datetime, timedelta, date
from app.utils.enums import OrderStatus
from app.utils.auth import Auth
from app.utils import current_time_by_zone, check_date_current_vs_date_for


class OrderController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.order_repo = OrderRepo()
		self.meal_item_repo = MealItemRepo()

	def list_orders(self):
		"""
		List all orders in the application: should rarely be should
		:return:
		"""
		location_id = Auth.get_location()
		current_date = datetime.now()
		current_date += timedelta(days=1)
		orders = self.order_repo.filter_by(
			is_deleted=False, date_booked_for=current_date.strftime('%Y-%m-%d'), location_id=location_id
		)
		orders_list = [order.serialize() for order in orders.items]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list, 'meta': self.pagination_meta(orders)})

	def list_orders_date(self, start_date):
		"""
		List all orders for a particular date
		:param start_date:
		:return:
		"""
		location_id = Auth.get_location()
		orders = self.order_repo.get_unpaginated(is_deleted=False, date_booked_for=start_date, location_id=location_id)
		orders_list = [order.serialize() for order in orders]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list})

	def list_orders_date_range(self, start_date, end_date):
		"""
		List all orders for a particular date
		:param start_date:
		:param end_date:
		:return:
		"""
		location_id = Auth.get_location()
		orders = self.order_repo.get_range_paginated_options_all(
			start_date=start_date, end_date=end_date, location_id=location_id
		)

		orders_list = [order.serialize() for order in orders.items]

		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list})

	def get_order(self, order_id):
		"""
		Gets all orders for an order_id
		:param order_id:
		:return:
		"""
		order = self.order_repo.get(order_id)
		if order:
			order_serialized = order.serialize()
			order_serialized['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in order.meal_item_orders]
			return self.handle_response('OK', payload={'order': order_serialized})
		return self.handle_response('Order not found', status_code=400)

	def get_order_by_user_id(self, user_id):
		"""
		Gets all orders for a user by the user id
		:param user_id:
		:return: list of orders in json model
		"""
		orders = self.order_repo.filter_by(user_id=user_id, is_deleted=False)
		orders_list = [order.serialize() for order in orders.items]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list})

	def get_order_by_user_id_date_range(self, user_id, start_date, end_date):
		"""

		:param user_id:
		:param start_date:
		:param end_date:
		:return:
		"""
		orders = self.order_repo.get_range_paginated_options(user_id=user_id, start_date=start_date, end_date=end_date)
		orders_list = [order.serialize() for order in orders.items]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list})

	def create_order(self):
		"""
		creates an order
		:return: order object
		"""
		user_id = Auth.user('id')
		location_id = Auth.get_location()
		date_booked_for, channel, meal_period, meal_items, menu_id = self.request_params(
			'dateBookedFor', 'channel', 'mealPeriod', 'mealItems', 'menuId'
		)
		if self.order_repo.user_has_order(user_id, date_booked_for, meal_period):
			return self.handle_response('You have already booked for this meal period.', status_code=400)
		
		location = LocationRepo().get(location_id)
		current_time = current_time_by_zone(location.zone)

		if datetime.strptime(date_booked_for, "%Y-%m-%d") < datetime.now():
			return self.handle_response('You are not allowed to book for a date in the past', status_code=400)


		if int(current_time_by_zone(location.zone).strftime('%H')) > 15:
			if check_date_current_vs_date_for(current_time, datetime.strptime(date_booked_for, "%Y-%m-%d")):
				return self.handle_response('It is too late to book a meal for the selected date ', status_code=400)

		meal_object_items = self.meal_item_repo.get_meal_items_by_ids(meal_items)
		
		new_order = self.order_repo.create_order(
			user_id, date_booked_for, meal_object_items, location_id, menu_id, channel, meal_period).serialize()
		
		new_order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in meal_object_items]
		return self.handle_response('OK', payload={'order': new_order})

	def update_order(self, order_id):
		"""
		updates an order based on the order Id
		:param order_id:
		:return:
		"""

		date_booked_for, channel, meal_items = self.request_params('dateBookedFor', 'channel', 'mealItems')
		meal_object_items = []
		for meal_item_id in meal_items:
			meal_item = self.meal_item_repo.get(meal_item_id)
			meal_object_items.append(meal_item)

		order = self.order_repo.get(order_id)
		if order:
			if order.is_deleted:
				return self.handle_response('Order has already been deleted', status_code=400)
			updates = {}
			if date_booked_for:
				order_date_midnight = datetime.strptime(date_booked_for, '%Y-%m-%d').replace(hour=00).replace(
					minute=00).replace(second=00)
				current_time = datetime.now()
				if order_date_midnight - current_time < timedelta('hours' == 7):
					return self.handle_response('It is too late to book meal for the selected date ', status_code=400)
				updates['date_booked_for'] = datetime.strptime(date_booked_for, '%Y-%m-%d')
			if channel:
				updates['channel'] = channel
			if meal_items:
				updates['meal_item_orders'] = meal_object_items

			updated_order = self.order_repo.update(order, **updates).serialize()
			updated_order['mealItems'] = [{'name': item.name, 'image': item.image, 'id': item.id} for item in order.meal_item_orders]
			return self.handle_response('OK', payload={'order': updated_order})

		return self.handle_response('Invalid or incorrect order_id provided', status_code=400)

	def collect_order(self):
		"""
		Collects order and mark as collected for a user Id
		:param user_id:
		:param order_type:
		:param order_date:
		:return:
		"""
		user_id, order_type, order_date = self.request_params('userId', 'orderType', 'orderDate')

		order = self.order_repo.find_first(user_id=user_id, meal_period=order_type, date_booked_for=order_date, is_deleted=False)
		if not order:
			return self.handle_response('Invalid or incorrect details provided', status_code=400)

		if order.order_status == OrderStatus.collected:
			return self.handle_response('Order already collected', status_code=409)

		order.order_status = OrderStatus.collected
		order.save()
		return self.handle_response('OK', payload={'order': order.serialize()})

	def check_order(self):
		"""
		Checks if a user has an order for a particular date and period

		:return:
		"""
		user_id, order_type, order_date = self.request_params('userId', 'orderType', 'orderDate')
		# get user_id from another method and reform to db's user id
		order = self.order_repo.find_first(user_id=user_id, meal_period=order_type, date_booked_for=order_date, is_deleted=False)
		if not order:
			return self.handle_response('Invalid or incorrect details provided', status_code=400)
		return self.handle_response('OK', payload={'order': order.serialize()})

	def delete_order(self, order_id):

		order = self.order_repo.get(order_id)

		if order:
			if order.is_deleted:
				return self.handle_response('Order has already been deleted', status_code=400)
			if Auth.user('id') != order.user_id:
				return self.handle_response('You cannot delete an order that is not yours', status_code=403)

			updates = {}
			updates['is_deleted'] = True

			self.order_repo.update(order, **updates)
			return self.handle_response('Order deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect order_id provided', status_code=400)
