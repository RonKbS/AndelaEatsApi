from tests.base_test_case import BaseTestCase
from factories import MealItemFactory, RoleFactory, PermissionFactory, UserRoleFactory


class TestMealItemEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_create_meal_item_endpoint_without_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build()
		data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image,
				'mealType': meal_item.meal_type}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_create_meal_item_endpoint_with_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build()
		data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image,
				'mealType': meal_item.meal_type}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assertEqual(response.status_code, 201)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['mealItem']['name'], meal_item.name)
		self.assertEqual(payload['mealItem']['description'], meal_item.description)
		self.assertEqual(payload['mealItem']['image'], meal_item.image)
		self.assertEqual(payload['mealItem']['mealType'], meal_item.meal_type)

	def test_create_meal_item_endpoint_with_missing_description(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build()
		data = {'mealName': meal_item.name, 'mealType': meal_item.meal_type, 'image': meal_item.image}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request - description is required')

	def test_create_meal_item_endpoint_with_missing_meal_type(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build()
		data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request - mealType is required')

	def test_create_meal_item_endpoint_with_missing_meal_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build()
		data = {'mealType': meal_item.meal_type, 'description': meal_item.description, 'image': meal_item.image}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request - mealName is required')

	def test_create_meal_item_endpoint_with_invalid_meal_type(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.build(meal_type='wrong_type')
		data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image,
				'mealType': meal_item.meal_type}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid meal type. Must be main, protein or side')

	def test_create_meal_item_endpoint_with_existing_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='create_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		MealItemFactory.create(name='sweet item')
		meal_item = MealItemFactory.build(name='sweet item')
		data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image,
				'mealType': meal_item.meal_type}
		response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Meal item with this name already exists')

	def test_list_meal_item_endpoint_right_permission(self):
		# Create Three Dummy Vendors
		meals = MealItemFactory.create_batch(3)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/meal-items/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['mealItems']), 3)
		self.assertJSONKeysPresent(payload['mealItems'][0], 'name', 'description', 'mealType', 'image')

	def test_list_meal_item_endpoint_wrong_permission(self):
		# Create Three Dummy Vendors
		meals = MealItemFactory.create_batch(3)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().get(self.make_url('/meal-items/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_get_specific_meal_item_enpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().get(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'mealItem')
		self.assertJSONKeysPresent(payload['mealItem'], 'name', 'description', 'mealType', 'image')
		self.assertEqual(int(payload['mealItem']['id']), meal_item.id)
		self.assertEqual(payload['mealItem']['name'], meal_item.name)
		self.assertEqual(payload['mealItem']['description'], meal_item.description)
		self.assertEqual(payload['mealItem']['mealType'], meal_item.meal_type)

	def test_get_specific_meal_item_enpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().get(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_get_specific_meal_item_enpoint_wrong_meal_item_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().get(self.make_url('/meal-items/100'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This meal id does not exist')

	def test_get_specific_meal_item_enpoint_deleted_meal_item_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='view_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create(is_deleted=True)

		response = self.client().get(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This meal item is deleted')

	def test_update_meal_item_endpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()
		data = {'mealName': 'Jollof Rice', 'description': 'tomato sautee rice', 'mealType': 'protein',
				'image': 'a new image link'}
		response = self.client().put(self.make_url('/meal-items/{}'.format(meal_item.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['mealItem']['name'], data['mealName'])
		self.assertEqual(payload['mealItem']['description'], data['description'])
		self.assertEqual(payload['mealItem']['mealType'], data['mealType'])
		self.assertEqual(payload['mealItem']['image'], data['image'])

	def test_update_meal_item_endpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()
		data = {'mealName': 'Jollof Rice', 'description': 'tomato sautee rice', 'mealType': 'protein',
				'image': 'a new image link'}
		response = self.client().put(self.make_url('/meal-items/{}'.format(meal_item.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_update_meal_item_endpoint_to_existing_name(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item1 = MealItemFactory.create(name='sweet item')
		meal_item = MealItemFactory.create()
		data = {'mealName': meal_item1.name, 'description': meal_item.description, 'image': meal_item.image,
				'mealType': meal_item.meal_type}
		response = self.client().put(self.make_url('/meal-items/{}'.format(meal_item.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Meal item with this name already exists')

	def test_update_meal_item_endpoint_invalid_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()
		data = {'mealName': 'Jollof Rice', 'description': 'tomato sautee rice', 'mealType': 'protein',
				'image': 'a new image link'}
		response = self.client().put(self.make_url('/meal-items/100'), data=self.encode_to_json_string(data),
									 headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid or incorrect meal_id provided')

	def test_update_deleted_meal_item(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='update_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create(is_deleted=True)
		data = {'mealName': 'Jollof Rice', 'description': 'tomato sautee rice', 'mealType': 'protein',
				'image': 'a new image link'}
		response = self.client().put(self.make_url('/meal-items/{}'.format(meal_item.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This meal item is deleted')

	def test_delete_meal_item_endpoint_right_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().delete(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], "success")

	def test_delete_meal_item_enpoint_wrong_permission(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='wrong_permission', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().delete(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

	def test_delete_meal_item_enpoint_wrong_meal_item_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create()

		response = self.client().delete(self.make_url('/meal-items/100'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Invalid or incorrect meal_id provided')

	def test_delete_meal_item_enpoint_deleted_meal_item_id(self):
		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_meal_item', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		meal_item = MealItemFactory.create(is_deleted=True)

		response = self.client().delete(self.make_url('/meal-items/{}'.format(meal_item.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Bad Request. This meal item is deleted')

