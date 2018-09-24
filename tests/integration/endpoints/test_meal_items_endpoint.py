from tests.base_test_case import BaseTestCase
from factories.meal_item_factory import MealItemFactory


class TestMealItemEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_meal_item_endpoint(self):
        meal_item = MealItemFactory.build()
        data = {'mealName': meal_item.name, 'description': meal_item.description, 'image': meal_item.image, 'mealType': meal_item.meal_type}
        response = self.client().post(self.make_url('/meal-items/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        

        self.assert200(response)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['mealItem']['name'], meal_item.name)
        self.assertEqual(payload['mealItem']['description'], meal_item.description)
        self.assertEqual(payload['mealItem']['image'], meal_item.image)
        self.assertEqual(payload['mealItem']['mealType'], meal_item.meal_type)

    def test_list_meal_item_endpoint(self):
        # Create Three Dummy Vendors
        meals = MealItemFactory.create_batch(3)
        
        # import pdb;pdb.set_trace()

        response = self.client().get(self.make_url('/meal-items/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['mealItems']), 3)
        self.assertJSONKeysPresent(payload['mealItems'][0], 'name', 'description', 'mealType', 'image')

    def test_get_specific_meal_item_enpoint(self):
        meal_item = MealItemFactory.create()
        print('/meals/{}/'.format(meal_item.id))

        response = self.client().get(self.make_url('/meal-items/{}/'.format(meal_item.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(payload, 'mealItem')
        self.assertJSONKeysPresent(payload['mealItem'], 'name', 'description', 'mealType', 'image')
        self.assertEqual(int(payload['mealItem']['id']), meal_item.id)
        self.assertEqual(payload['mealItem']['name'], meal_item.name)
        self.assertEqual(payload['mealItem']['description'], meal_item.description)
        self.assertEqual(payload['mealItem']['mealType'], meal_item.meal_type)

    def test_update_meal_item_endpoint(self):
        meal_item = MealItemFactory.create()
        data = {'mealName': 'Jollof Rice', 'description': 'tomato sautee rice', 'mealType': 'protein', 'image': 'a new image link'}
        response = self.client().put(self.make_url('/meal-items/{}/'.format(meal_item.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['mealItem']['name'], data['mealName'])
        self.assertEqual(payload['mealItem']['description'], data['description'])
        self.assertEqual(payload['mealItem']['mealType'], data['mealType'])
        self.assertEqual(payload['mealItem']['image'], data['image'])

        '''Test invalid update request'''
        # User arbitrary value of 100 as the meal item ID
        response = self.client().put(self.make_url('/meal-items/100/'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert400(response)

    def test_delete_meal_item_endpoint(self):
        meal_item = MealItemFactory.create()

        response = self.client().delete(self.make_url('/meal-items/{}/'.format(meal_item.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
      
        self.assert200(response)
        self.assertEqual(payload['status'], "success")
