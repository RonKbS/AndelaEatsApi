import datetime
from tests.base_test_case import BaseTestCase
from app.repositories import OrderRepo
from factories import MealItemFactory

class TestOrderEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_delete_order_endpoint_with_right_permission(self):
		
		user_id = BaseTestCase.user_id()
		meal = MealItemFactory.create()
		order_data = {
			'user_id': user_id,
			'date_booked_for': '2018-10-20',
			'date_booked': '2018-10-20',
			'channel': 'web',
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
			'date_booked': '2018-10-20',
			'channel': 'web',
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
			'date_booked': '2018-10-20',
			'channel': 'web',
			'meal_items': [meal]
			}
		order_repo = OrderRepo()
		order = order_repo.create_order(**order_data)

		self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response = self.client().delete(self.make_url(f'/orders/{order.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Order has already been deleted')
