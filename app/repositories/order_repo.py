from app.repositories.base_repo import BaseRepo
from app.models.order import Order
from datetime import datetime
from app.repositories.meal_item_repo import MealItemRepo
from app.utils.enums import OrderStatus


class OrderRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, Order)
		self.meal_item_repo = MealItemRepo()

	def create_order(self, user_id, date_booked_for, meal_items, menu_id, channel='web', meal_period='lunch'):
		order = Order(user_id=user_id, date_booked_for=datetime.strptime(date_booked_for, '%Y-%m-%d'),
					  date_booked=datetime.now(), channel=channel, order_status=OrderStatus.booked,
					  meal_period=meal_period, menu_id=menu_id)

		for meal_item in meal_items:
			order.meal_item_orders.append(meal_item)

		order.save()
		return order

	def update_order(self, user_id, date_booked_for, date_booked, meal_items, channel='web', meal_period='lunch'):
		order = Order(user_id=user_id, date_booked_for=datetime.strptime(date_booked_for, '%Y-%m-%d'),
					  date_booked=datetime.strptime(date_booked, '%Y-%m-%d'), channel=channel, meal_period=meal_period)

		for meal_item in meal_items:
			order.meal_item_orders.append(meal_item)

		order.save()
		return order

	def get_range_paginated_options(self, user_id, start_date, end_date):
		return Order.query.filter(
			Order.date_booked_for >= start_date, Order.date_booked_for <= end_date,
			Order.user_id == user_id, Order.is_deleted.is_(False)
		).order_by(Order.date_booked_for.desc()).paginate(error_out=False)

	def get_range_paginated_options_all(self, start_date, end_date):
		return Order.query.filter(
			Order.date_booked_for >= start_date, Order.date_booked_for <= end_date,
			Order.is_deleted.is_(False)
		).order_by(Order.date_booked_for.desc()).paginate(error_out=False)
