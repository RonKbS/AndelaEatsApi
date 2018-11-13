from tests.base_test_case import BaseTestCase
from factories import OrderFactory, MealItemFactory, RoleFactory, PermissionFactory, UserRoleFactory
from app.utils.enums import MealTypes
from datetime import datetime, timedelta
from app.utils import db
from app.repositories import OrderRepo


class TestOrderEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_create_order_with_invalid_details_endpoint(self):
		pass

	def test_create_order_with_valid_details_endpoint(self):
		order = OrderFactory.create()
		meal_item1 = MealItemFactory.create()
		meal_item2 = MealItemFactory.create()
		meal_item3 = MealItemFactory.create()
		meal_item1.meal_type = MealTypes.protein
		meal_item2.meal_type = MealTypes.main

		meal_items = [meal_item1.id, meal_item2.id, meal_item3.id]
		data = {'userId': order.user_id, 'dateBookedFor': order.date_booked_for.strftime('%Y-%m-%d'),
				'dateBooked': order.date_booked.strftime('%Y-%m-%d'), 'channel': order.channel,
				'mealPeriod': order.meal_period, 'mealItems': meal_items}

		response = self.client().post(
			self.make_url('/orders/'), data=self.encode_to_json_string(data), headers=self.headers())

		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['order']['userId'], BaseTestCase.user_id())
		self.assertEqual(payload['order']['channel'], order.channel)

	def test_list_order_endpoint(self):
		# Create Three Dummy Vendors
		orders = OrderFactory.create_batch(3)
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='view_orders', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/orders/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		self.assert200(response)
		self.assertEqual(len(payload['orders']), 3)
		self.assertJSONKeysPresent(payload['orders'][0], 'userId', 'channel', 'dateBookedFor')

	def test_list_order_by_page_endpoint(self):
		pass

	def test_list_order_by_date_endpoint(self):
		pass

	def test_check_order_valid_endpoint(self):
		pass

	def test_check_order_valid_but_cancelled_endpoint(self):
		pass

	def test_check_order_valid_but_collected_endpoint(self):
		pass

	def test_check_order_not_valid_endpoint(self):
		pass

	def test_collect_order_valid_endpoint(self):
		pass

	def test_collect_order_not_valid_endpoint(self):
		pass

	def test_get_specific_meal_item_endpoint(self):
		order = OrderFactory.create()
		print('/orders/{}/'.format(order.id))

		response = self.client().get(self.make_url('/orders/{}'.format(order.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'order')
		self.assertJSONKeysPresent(payload['order'], 'userId', 'channel')
		self.assertEqual(int(payload['order']['id']), order.id)
		self.assertEqual(payload['order']['userId'], order.user_id)
		self.assertEqual(payload['order']['channel'], order.channel)

	def test_update_order_with_valid_order_id_endpoint(self):
		order1 = OrderFactory.create()
		order2 = OrderFactory.create()

		meal_item1 = MealItemFactory.create()
		meal_item2 = MealItemFactory.create()
		meal_item3 = MealItemFactory.create()
		meal_item1.meal_type = MealTypes.protein
		meal_item2.meal_type = MealTypes.main

		meal_items = [meal_item1.id, meal_item2.id, meal_item3.id]

		data = {
			'channel': 'slack', 'mealPeriod': 'lunch',
			'dateBookedFor': order2.date_booked_for.strftime('%Y-%m-%d'), 'mealItems': meal_items}
		response = self.client().put(
			self.make_url('/orders/{}'.format(order1.id)), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['order']['channel'], data['channel'])

		'''Test invalid update request'''
		# User arbitrary value of 100 as the meal item ID
		response = self.client().put(
			self.make_url('/orders/100'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assert400(response)

	def test_update_order_with_invalid_order_id_endpoint(self):
		pass

	def test_delete_order_endpoint_with_right_permission(self):
		user_id = BaseTestCase.user_id()
		meal = MealItemFactory.create()
		order_data = {
			'user_id': user_id,
			'date_booked_for': '2018-10-20',
			'channel': 'web', 'meal_period': 'lunch',
			'meal_items': [meal]
		}
		order_repo = OrderRepo()
		order = order_repo.create_order(**order_data)

		response = self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], 'success')
		self.assertEqual(response_json['msg'], 'Order deleted')

	def test_delete_order_not_yours(self):
		user_id = BaseTestCase.user_id()
		meal = MealItemFactory.create()
		order_data = {
			'user_id': '-UTG654RfggtdI',
			'date_booked_for': '2018-10-20',
			'channel': 'web', 'meal_period': 'lunch',
			'meal_items': [meal]
		}
		order_repo = OrderRepo()
		order = order_repo.create_order(**order_data)

		response = self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert403(response)
		self.assertEqual(response_json['msg'], 'You cannot delete an order that is not yours')

	def test_delete_order_endpoint_with_wrong_order_id(self):
		response = self.client().delete(self.make_url(f'/orders/576'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid or incorrect order_id provided')

	def test_already_deleted_order(self):
		user_id = BaseTestCase.user_id()
		meal = MealItemFactory.create()
		order_data = {
			'user_id': user_id,
			'date_booked_for': '2018-10-20',
			'channel': 'web', 'meal_period': 'lunch',
			'meal_items': [meal]
		}
		order_repo = OrderRepo()
		order = order_repo.create_order(**order_data)

		self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response = self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Order has already been deleted')
