from sqlalchemy import and_
from app.controllers.base_controller import BaseController
from app.repositories import OrderRepo
from app.repositories.meal_item_repo import MealItemRepo
from datetime import datetime, timedelta
from app.utils.auth import Auth

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
		orders = self.order_repo.get_unpaginated(is_deleted=False)
		orders_list = [order.serialize() for order in orders]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [item.name for item in meal_items]
		return self.handle_response('OK', payload={'orders': orders_list})

	# def list_orders_page(self, page_id, per_page):
	# 	"""
	# 	List all orders in the application per page
	# 	:param page_id:
	# 	:param per_page:
	# 	:return:
	# 	"""
	# 	orders = self.order_repo.filter_and_order(is_deleted=False, page=page_id, per_page=per_page)
	# 	orders_list = [order.serialize() for order in orders]
	# 	for order in orders_list:
	# 		meal_items = self.order_repo.get(order['id']).meal_item_orders
	# 		order['mealItems'] = [item.name for item in meal_items]
	# 	return self.handle_response('OK', payload={'orders': orders_list})

	def list_orders_date(self, start_date):
		"""
		List all orders for a particular date
		:param start_date:
		:return:
		"""
		orders = self.order_repo.get_unpaginated(is_deleted=False, dateBookedFor=start_date)
		orders_list = [order.serialize() for order in orders]
		for order in orders_list:
			meal_items = self.order_repo.get(order['id']).meal_item_orders
			order['mealItems'] = [item.name for item in meal_items]
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
			order_serialized['mealItems'] = [item.name for item in order.meal_item_orders]
			return self.handle_response('OK', payload={'order': order_serialized})
		return self.handle_response('Order not found', status_code=400)

	def create_order(self):
		"""
		creates an order
		:return: order object
		"""

		user_id = Auth.user('id')
		date_booked_for, channel, meal_period, meal_items = self.request_params(
			'dateBookedFor', 'channel', 'mealPeriod', 'mealItems'
		)
		orders = self.order_repo.get_unpaginated(is_deleted=False)

		order_date_midnight = datetime.strptime(date_booked_for, '%Y-%m-%d').replace(hour=00).replace(
			minute=00).replace(second=00)
		current_time = datetime.now()
		if order_date_midnight - current_time < timedelta('hours' == 7):
			return self.handle_response('It is too late to book meal for the selected date ', status_code=400)

		if orders \
			and any(order.user_id == user_id and order.meal_period == meal_period
			and order.is_deleted.is_(False)
			and order.date_booked_for == datetime.strptime(
			date_booked_for, '%Y-%m-%d').date() for order in orders):
			return self.handle_response('you have already booked for this date.', status_code=400)

		meal_object_items = []

		for meal_item_id in meal_items:
			meal_item = self.meal_item_repo.get(meal_item_id)
			meal_object_items.append(meal_item)

		new_order = self.order_repo.create_order(
			user_id, date_booked_for, meal_object_items, channel, meal_period).serialize()
		new_order['mealItems'] = [item.name for item in meal_object_items]
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
			updated_order['mealItems'] = [item.name for item in order.meal_item_orders]
			return self.handle_response('OK', payload={'order': updated_order})

		return self.handle_response('Invalid or incorrect order_id provided', status_code=400)

	def collect_order(self, order_type, user_id):
		"""
		Collects order and mark as collected for a user Id
		:param order_type:
		:param user_id:
		:return:
		"""

		order = self.order_repo.filter_by(user_id=user_id)

		if order:
			return self.handle_response('OK', payload={'order': order})
		return self.handle_response('Invalid or incorrect details provided', status_code=400)

	def check_order(self, user_id, order_date, meal_period):
		"""
		Checks if a user has an order for a particular date and period
		:param user_id:
		:param order_date:
		:param meal_period:
		:return:
		"""
		pass

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
