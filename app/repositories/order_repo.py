from app.repositories.base_repo import BaseRepo
from app.models.order import Order
from datetime import datetime
from app.repositories.meal_item_repo import MealItemRepo
from app.utils.enums import OrderStatus


class OrderRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Order)
        self.meal_item_repo = MealItemRepo()

    def create_order(self, user_id, date_booked_for, meal_items, location_id, menu_id, channel='web', meal_period='lunch'):
        order = Order(user_id=user_id, date_booked_for=datetime.strptime(date_booked_for, '%Y-%m-%d'),
                      date_booked=datetime.now(), channel=channel, order_status=OrderStatus.booked,
                      meal_period=meal_period, menu_id=menu_id, location_id=location_id)

        for meal_item in meal_items:
            order.meal_item_orders.append(meal_item)

        order.save()
        return order

    def update_order(self, user_id, date_booked_for, date_booked, meal_items, location_id, channel='web', meal_period='lunch', has_rated=False):
        order = Order(user_id=user_id, date_booked_for=datetime.strptime(date_booked_for, '%Y-%m-%d'),
                      date_booked=datetime.strptime(date_booked, '%Y-%m-%d'),
                      channel=channel, meal_period=meal_period, has_rated=has_rated,
                      location_id=location_id
                      )

        for meal_item in meal_items:
            order.meal_item_orders.append(meal_item)

        order.save()
        return order

    def get_range_paginated_options(self, user_id, start_date, end_date, **kwargs):
        return Order.query.filter(Order.date_booked_for >= start_date,
                                  Order.date_booked_for <= end_date, Order.user_id == user_id,
                                  Order.is_deleted.is_(False)).order_by(Order.date_booked_for.desc()).paginate(error_out=False, **kwargs)

    def get_range_paginated_options_all(self, start_date, end_date, location_id, **kwargs):
        return Order.query.filter(Order.date_booked_for >= start_date,
                                  Order.date_booked_for <= end_date, Order.is_deleted.is_(
                                      False),
                                  Order.location_id == location_id).order_by(
            Order.date_booked_for.desc()).paginate(error_out=False, **kwargs)

    def user_has_order(self, user_id, date_booked, meal_period):
        date_booked = datetime.strptime(date_booked, '%Y-%m-%d').date()
        return self._model.query.filter_by(**{'is_deleted': False,
                                              'user_id': user_id,
                                              'date_booked_for': date_booked,
                                              'meal_period': meal_period}).count() > 0
