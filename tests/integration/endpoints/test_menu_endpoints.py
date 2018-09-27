from datetime import date, datetime, timedelta
from tests.base_test_case import BaseTestCase
from factories import VendorFactory, RoleFactory, PermissionFactory, UserRoleFactory, MenuFactory, VendorEngagementFactory, MealItemFactory
from app.utils import db
from app.models import MealItem, Menu
from app.repositories.menu_repo import MenuRepo


class MenuEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_create_menu_endpoint(self):
		menu = MenuFactory.build()
		main_meal_item = MealItemFactory.build()
		side_meal_item = MealItemFactory.build()
		protein_meal_item = MealItemFactory.build()
		vendor = VendorFactory.build()
		db.session.add(vendor)
		db.session.commit()
		vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
		db.session.add(vendor_engagement)
		db.session.add(main_meal_item)
		db.session.add(side_meal_item)
		db.session.add(protein_meal_item)
		db.session.commit()

		data = {
		'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
		'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
		'allowedProtein': menu.allowed_protein, 'sideItems': [side_meal_item.id],
		'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
		}

		response = self.client().post(self.make_url('/admin/menu/'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assertEqual(response.status_code, 201)
		self.assertJSONKeysPresent(payload, 'menu')
		self.assertJSONKeysPresent(payload['menu'], 'mainMeal', 'proteinItems', 'sideItems', 'allowedProtein', 'allowedSide',
		'date', 'id', 'mealPeriod', 'timestamps', 'vendorEngagementId'
		)

		self.assertEqual(payload['menu']['vendorEngagementId'], vendor_engagement.id)
		self.assertEqual(payload['menu']['mealPeriod'], menu.meal_period)
		self.assertEqual(payload['menu']['mainMealId'], main_meal_item.id)
		self.assertEqual(payload['menu']['allowedSide'], menu.allowed_side)
		self.assertEqual(payload['menu']['allowedProtein'], menu.allowed_protein)

	def test_delete_menu_endpoint_with_right_permission(self):
		menu = MenuFactory.create()
		# menu.save()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_menu', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/admin/menu/{menu.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], "success")

	def test_delete_menu_endpoint_without_right_permission(self):
		menu = MenuFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_menu', role_id=100)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/admin/menu/{menu.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)

	def test_list_menu_endpoint(self):
		'''Test that users with the right permission can view list of menus'''

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='view_menu', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)
		current_date = str(datetime.now().date())

		m = MenuFactory()
		results = Menu.query.all()
		
		response = self.client().get(self.make_url(f'/admin/menu/lunch/{current_date}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		print(results[0].date.date())
		# payload = response_json['payload']
		# print(payload)
		# print(f'/admin/menu/lunch/{current_date}')
		# print(m.date.date())
		# print(type(current_date))
		# print(m.meal_period)


		# print('<><><><><><><><><><><><><', payload)
		# print('<><><><><><><><><><><><><', results)
		# print('+++++++++++++++++', results[1].date.date(), date1.date())
		# print('+++++++++++++++++', results[0].meal_period)


		self.assert200(response)
		self.assertEqual(len(payload['menuList']), 1)
		# self.assertJSONKeysPresent(payload['ratings'][0], 'vendorId', 'userId', 'id', 'comment', 'rating','channel')
