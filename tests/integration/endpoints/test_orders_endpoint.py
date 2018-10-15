from tests.base_test_case import BaseTestCase
from factories.order_factory import OrderFactory
from app.utils.enums import MealTypes, Channels
from factories.meal_item_factory import MealItemFactory
from datetime import datetime
from app.utils import db


class TestOrderEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_order_endpoint(self):
        order = OrderFactory.create()
        meal_item1 = MealItemFactory.create()
        meal_item2 = MealItemFactory.create()
        meal_item3 = MealItemFactory.create()
        meal_item1.meal_type = MealTypes.protein
        meal_item2.meal_type = MealTypes.main

        meal_items = [meal_item1.id, meal_item2.id, meal_item3.id]
        meal_item_objects = [meal_item1, meal_item2, meal_item3]

        data = {'userId': order.user_id, 'dateBookedFor': order.date_booked_for.strftime('%Y-%m-%d'), 'channel': order.channel, 'mealItems': meal_items}

        response = self.client().post(self.make_url('/orders/'), data=self.encode_to_json_string(data), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['order']['userId'], order.user_id)
        self.assertEqual(payload['order']['channel'], order.channel)

    def test_list_order_endpoint(self):
        # Create Three Dummy Vendors
        orders = OrderFactory.create_batch(3)

        response = self.client().get(self.make_url('/orders/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        self.assert200(response)
        self.assertEqual(len(payload['orders']), 3)
        self.assertJSONKeysPresent(payload['orders'][0], 'userId', 'channel', 'dateBookedFor')


    def test_get_specific_meal_item_enpoint(self):
        order = OrderFactory.create()
        print('/orders/{}/'.format(order.id))

        response = self.client().get(self.make_url('/orders/{}/'.format(order.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(payload, 'order')
        self.assertJSONKeysPresent(payload['order'], 'userId', 'channel')
        self.assertEqual(int(payload['order']['id']), order.id)
        self.assertEqual(payload['order']['userId'], order.user_id)
        self.assertEqual(payload['order']['channel'], order.channel)

    def test_update_order_endpoint(self):
        order1 = OrderFactory.create()
        order2 = OrderFactory.create()

        meal_item1 = MealItemFactory.create()
        meal_item2 = MealItemFactory.create()
        meal_item3 = MealItemFactory.create()
        meal_item1.meal_type = MealTypes.protein
        meal_item2.meal_type = MealTypes.main

        meal_items = [meal_item1.id, meal_item2.id, meal_item3.id]
        
        data = {'channel': 'slack', 'userId': 'another Id', 'dateBookedFor': order2.date_booked_for.strftime('%Y-%m-%d'), 'mealItems': meal_items}
        response = self.client().put(self.make_url('/orders/{}/'.format(order1.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['order']['channel'], data['channel'])
        self.assertEqual(payload['order']['userId'], data['userId'])

        '''Test invalid update request'''
        # User arbitrary value of 100 as the meal item ID
        response = self.client().put(self.make_url('/orders/100/'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert400(response)

    def test_delete_order_endpoint(self):
        order = OrderFactory.create()

        response = self.client().delete(self.make_url('/orders/{}/'.format(order.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
      
        self.assert200(response)
        self.assertEqual(payload['status'], "success")
