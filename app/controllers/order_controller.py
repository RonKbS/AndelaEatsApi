from app.controllers.base_controller import BaseController
from app.repositories.order_repo import OrderRepo
from app.repositories.meal_item_repo import MealItemRepo
from datetime import datetime


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

        user_id, date_booked_for, channel, meal_items = self.request_params('userId', 'dateBookedFor', 'channel', 'mealItems')

        meal_object_items = []
        for meal_item_id in meal_items:
            meal_item = self.meal_item_repo.get(meal_item_id)
            meal_object_items.append(meal_item)

        new_order = self.order_repo.create_order(user_id, date_booked_for, channel, meal_object_items).serialize()

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
        updates = {}
        if order:
            updates['is_deleted'] = True

            self.order_repo.update(order, **updates)
            return self.handle_response('OK', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect order_id provided', status_code=400)
