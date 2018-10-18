from sqlalchemy import and_
from app.controllers.base_controller import BaseController
from app.repositories import OrderRepo
from app.repositories.meal_item_repo import MealItemRepo
from app.models import Order
from datetime import datetime
from app.utils.auth import Auth


class OrderController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.order_repo = OrderRepo()
        self.meal_item_repo = MealItemRepo()

    def list_orders(self):
        orders = self.order_repo.filter_by(is_deleted=False)
        orders_list = [order.serialize() for order in orders.items]
        return self.handle_response('OK', payload={'orders': orders_list, 'meta': self.pagination_meta(orders)})

    def get_order(self, order_id):
        order = self.order_repo.get(order_id)
        if order:
            order = order.serialize()
            return self.handle_response('OK', payload={'order': order})
        else:
            return self.handle_response('Bad Request', status_code=400)

    def create_order(self):
        """
        Creates a new order
        """

        user_id = Auth.user('id')
        date_booked, date_booked_for, channel, meal_items = self.request_params('dateBooked', 'dateBookedFor', 'channel', 'mealItems')
        orders = self.order_repo.filter_by(is_deleted=False).items
        if orders and any(order.user_id == user_id and order.date_booked_for == datetime.strptime(date_booked_for, '%Y-%m-%d').date() for order in orders):
            return self.handle_response('you have already booked for this date.', status_code=400)

        meal_object_items = []
            
        for meal_item_id in meal_items:
            meal_item = self.meal_item_repo.get(meal_item_id)
            meal_object_items.append(meal_item)

        new_order = self.order_repo.create_order(user_id, date_booked_for, date_booked, meal_object_items, channel).serialize()
        new_order['mealItems'] = [item.name for item in meal_object_items]
        return self.handle_response('OK', payload={'order': new_order})


    def update_order(self, order_id):

        user_id, date_booked_for, channel, meal_items = self.request_params('userId', 'dateBookedFor', 'channel', 'mealItems')

        meal_object_items = []
        for meal_item_id in meal_items:
            meal_item = self.meal_item_repo.get(meal_item_id)
            meal_object_items.append(meal_item)

        order = self.order_repo.get(order_id)
        if order:
            updates = {}
            if user_id:
                updates['user_id'] = user_id
            if date_booked_for:
                updates['date_booked_for'] = datetime.strptime(date_booked_for, '%Y-%m-%d')
            if channel:
                updates['channel'] = channel
            if meal_items:
                updates['meal_item_orders'] = meal_object_items

            self.order_repo.update(order, **updates)
            return self.handle_response('OK', payload={'order': order.serialize()})

        return self.handle_response('Invalid or incorrect order_id provided', status_code=400)

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
