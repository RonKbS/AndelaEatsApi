from datetime import date, datetime, timedelta
from tests.base_test_case import BaseTestCase
from factories import VendorFactory, RoleFactory, PermissionFactory, UserRoleFactory, MenuFactory, VendorEngagementFactory, MealItemFactory
from app.utils import db
from app.models import MealItem, Menu
from app.repositories import MenuRepo, MealItemRepo
from app.utils.enums import MealPeriods
import pdb


class MenuEndpoints(BaseTestCase):
	"""A test class for menu endpoints"""

	def setUp(self):
		self.BaseSetUp()

	def test_create_menu_endpoint_without_permission(self):
		""" Test for creation of a new menu without permmission """
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

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
			'allowedProtein': menu.allowed_protein,
			'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id],
			'vendorEngagementId': vendor_engagement.id
		}

		response = self.client().post(self.make_url('/admin/menus/'), \
									  data=self.encode_to_json_string(data), headers=self.headers())

		self.assert400(response)

	def test_create_menu_endpoint(self):
		"""Test for creation of new menu"""
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

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)


		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
			'allowedProtein': menu.allowed_protein,
			'sideItems': [side_meal_item.id], 
			'proteinItems': [protein_meal_item.id], 
			'vendorEngagementId': vendor_engagement.id
		}

		response = self.client().post(self.make_url('/admin/menus/'), \
			data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assertEqual(response.status_code, 201)
		self.assertJSONKeysPresent(payload, 'menu')
		self.assertJSONKeysPresent(payload['menu'], 'mainMeal', 
		'proteinItems', 'sideItems', 'allowedProtein', 'allowedSide',
			'date', 'id', 'mealPeriod', 'timestamps', 'vendorEngagementId'
		)

		self.assertEqual(
			payload['menu']['vendorEngagementId'], vendor_engagement.id
			)
		self.assertEqual(payload['menu']['mealPeriod'], menu.meal_period)
		self.assertEqual(payload['menu']['mainMealId'], main_meal_item.id)
		self.assertEqual(payload['menu']['allowedSide'], menu.allowed_side)
		self.assertEqual(payload['menu']['allowedProtein'], menu.allowed_protein)

		'''Test invalid main item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': 1000, 'allowedSide': menu.allowed_side,
			'allowedProtein': menu.allowed_protein, 'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
		}
		response = self.client().post(self.make_url('/admin/menus/'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

		'''Test invalid side item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
			'allowedProtein': menu.allowed_protein, 'sideItems': [side_meal_item.id, 1000],
			'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
		}
		response = self.client().post(self.make_url('/admin/menus/'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

		'''Test invalid protein item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
			'allowedProtein': menu.allowed_protein, 'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id, 1000], 'vendorEngagementId': vendor_engagement.id
		}
		response = self.client().post(self.make_url('/admin/menus/'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

	def test_delete_menu_endpoint_with_right_permission(self):
		"""Test that a user with permission to delete menu can successfully do so"""
		menu = MenuFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/admin/menus/{menu.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], "success")

	def test_delete_menu_endpoint_without_right_permission(self):
		"""Test that a user without permission to delete menu cannot successfully do so"""
		menu = MenuFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_menu', role_id=100)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/admin/menus/{menu.id}'), headers=self.headers())

		self.assert400(response)


	def test_list_menu_endpoint_without_right_permission(self):
		"""Test that users without the right permission cannot view list of menus"""

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_menu', role_id=100)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)
		current_date = datetime.now().date()

		MenuFactory.create_batch(5)
		Menu.query.all()

		response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{current_date}'), headers=self.headers())

		self.assert400(response)

	def test_list_menu_endpoint_with_right_permission(self):
		"""Test that users with the right permission can view list of menus"""

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)
		current_date = datetime.now().date()

		MenuFactory.create_batch(5)

		response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{current_date}'),
					headers=self.headers())

		self.assert200(response)

	def test_list_menu_range_endpoint_without_right_permission(self):
		""" Test that users without the right permission cannot view list of menus with date range """
		start_date = datetime.now().date()
		end_date = datetime.now().date() + timedelta(days=7)

		MenuFactory.create_batch(5)

		response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'),
									 headers=self.headers())

		self.assert400(response)

	def test_list_menu_range_endpoint_with_right_permission(self):
		""" Test that users with right permission can view list of menu with date range """
		# pass
		meal_item_repo = MealItemRepo()
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)
		current_date = datetime.now().date()
		start_date = current_date.strftime('%Y-%m-%d')
		end_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')

		side_meal_item = meal_item_repo.new_meal_item(name="side1", description="descr11", image="image11", meal_type="side")
		protein_meal_item = meal_item_repo.new_meal_item(name="protein1", description="descr11", image="image12", meal_type="protein")
		MenuFactory.create_batch(5, side_items=side_meal_item.id, protein_items=protein_meal_item.id)
		
		response = self.client()\
			.get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'), headers=self.headers())
		
		self.assert200(response)

	def test_list_menu_range_endpoint_with_right_permission_wrong_range(self):
		""" Test that users with right permission but wrong range cannot view """
		pass
		# role = RoleFactory.create(name='admin')
		# user_id = BaseTestCase.user_id()
		# PermissionFactory.create(keyword='view_menu', role_id=role.id)
		# UserRoleFactory.create(user_id=user_id, role_id=role.id)
		#
		# start_date = datetime.now().date()
		# end_date = datetime.now().date()+ timedelta(days=-7)
		#
		# MenuFactory.create_batch(5)
		#
		# response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'),
		# 							 headers=self.headers())
		# response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		# self.assert404(response)
		# self.assertEqual(response_json['msg'], 'Start Date [{}] must be less than End Date[{}]'.format(start_date, end_date))

	def test_list_menu_range_endpoint_with_right_permission_wrong_period(self):
		pass

	def test_update_menu_endpoint(self):
		"""Test update of a menu"""
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_menu', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item_repo = MealItemRepo()

		main_meal_item = meal_item_repo.new_meal_item(name="main1", description="descr1", image="image1", meal_type="main")
		side_meal_item = meal_item_repo.new_meal_item(name="side1", description="descr11", image="image11", meal_type="side")
		protein_meal_item = meal_item_repo.new_meal_item(name="protein1", description="descr11", image="image12", meal_type="protein")
		vendor = VendorFactory.build()
		db.session.add(vendor)
		db.session.commit()
		vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
		db.session.add(vendor_engagement)
		db.session.add(main_meal_item)
		db.session.add(side_meal_item)
		db.session.add(protein_meal_item)
		db.session.commit()
		menu = MenuFactory.create(main_meal_id=main_meal_item.id,
			side_items = side_meal_item.id, protein_items=protein_meal_item.id)
		menu.vendor_engagement_id = vendor_engagement.id
		db.session.add(menu)
		db.session.commit()

		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': 2,
			'allowedProtein': 2, 'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
    	}

		response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['menu']['allowedProtein'], data['allowedProtein'])
		self.assertEqual(payload['menu']['allowedSide'], data['allowedSide'])

		'''Test invalid update request'''
		response = self.client().put(self.make_url('/admin/menus/100'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 404)

		'''Test invalid main item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': 100, 'allowedSide': 2,
			'allowedProtein': 2, 'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
		}
		response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

		'''Test invalid side item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': 2,
			'allowedProtein': 2, 'sideItems': [1000],
			'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
		}
		response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

		'''Test invalid protein item id request'''
		data = {
			'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
			'mainMealId': main_meal_item.id, 'allowedSide': 2,
			'allowedProtein': 2, 'sideItems': [side_meal_item.id],
			'proteinItems': [protein_meal_item.id, 1000], 'vendorEngagementId': vendor_engagement.id
		}

		response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)), data=self.encode_to_json_string(data), headers=self.headers())
		self.assertEqual(response.status_code, 400)

	def test_update_menu_endpoint_with_wrong_values(self):
		pass

	def test_update_menu_endpoint_with_wrong_permission(self):
		pass

