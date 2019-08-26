from app.utils.handled_exceptions import BaseModelValidationError
from tests.base_test_case import BaseTestCase
from tests.base_test_utils import BaseTestUtils
from factories import (
    MenuTemplateItemFactory,
    MenuTemplateWeekDayFactory, LocationFactory, MealItemFactory)


class TestMenuTemplateItem(BaseTestCase, BaseTestUtils):

    def setUp(self):
        self.BaseSetUp()
        self.meal_items = MealItemFactory.create_batch(5)
        [item.save() for item in self.meal_items]

    def tearDown(self):
        self.BaseTearDown()

    def test_create_menu_template_item_with_no_permission_fails(self):
        day = MenuTemplateWeekDayFactory()
        
        day.save()
        data = {
            "mainMealId": 1,
            "allowedSide": 1,
            "allowedProtein": 1,
            "dayId": day.id
        }
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['msg'],
                         'Access Error - No Role Granted')

    def test_create_menu_template_item_with_permission_succeeds(self):
        self.create_admin()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            json=data)
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'mainMealId')
        self.assertJSONKeysPresent(response_json['payload'], 'dayId')

    def test_create_menu_template_item_with_no_data_fails(self):
        self.create_admin()
        data = {}
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'], 'Bad Request - Request Must be JSON Formatted')

    def test_create_menu_template_item_with_missing_fields_fails(self):
        self.create_admin()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "allowedSide": 1,
            "allowedProtein": 1,
            "dayId": day.id
        }
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'], 'Bad Request - mainMealId is required')

    def test_create_menu_template_item_invalid_side_and_protein_item_ids_fails(self):
        self.create_admin()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [123],
            "sideItems": [233],
            "dayId": day.id
        }

        response_ = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONKeysPresent(response_json, 'msg')
        self.assertEqual(response_json['msg'],
                         "Bad Request - sideItems contains invalid id(s) for meal_item table ")

    def test_create_same_exact_menu_template_item_fails(self):
        self.create_admin()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }

        response_ = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response = self.client().post(
            self.make_url("/menu_template_items/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONKeysPresent(response_json['payload'], 'message')
        self.assertEqual(response_json['payload']['message'],
                         'Menu Template Item already exists')

    def test_get_menu_template_items_succeeds(self):
        self.create_admin()
        template = MenuTemplateItemFactory.create(
            main_meal_id=1,
            allowed_side=1,
            allowed_protein=1,
            day_id=1,
        )
        template.save()
        # template_id in url refers to menu template and not that created above
        response = self.client().get(
            self.make_url("/menu_template_items?day_id=1"),
            headers=self.headers()
        )
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['MenuTemplateItems'][0]['id'], 1)

    def test_get_menu_template_items_with_no_permission_fails(self):
        template = MenuTemplateItemFactory.create(
            main_meal_id=1,
            allowed_side=1,
            allowed_protein=1,
            day_id=1,
        )
        response = self.client().get(
            self.make_url(f"/menu_template_items?day_id=1"),
            headers=self.headers()
        )
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['msg'],
                         'Access Error - No Role Granted')

    def test_get_for_non_existant_menu_template_items_returns_empty_list(self):
        self.create_admin()
        template = MenuTemplateItemFactory.create(
            main_meal_id=1,
            allowed_side=1,
            allowed_protein=1,
            day_id=1,
        )
        template.save()
        response = self.client().get(
            self.make_url("/menu_template_items?day_id=4"),
            headers=self.headers()
        )
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['MenuTemplateItems'], [])
        
    def test_delete_menu_template_item_succeeds(self):
        self.create_admin()
        item = MenuTemplateItemFactory.create()
        item.save()
        response = self.client().delete(
            self.make_url(f"/menu_template_items/{item.id}"), headers=self.headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'],
                         f'menu_template_item deleted {item.id}')

    def test_delete_menu_template_item_that_doesnot_exist_fails(self):
        self.create_admin()
        response = self.client().delete(
            self.make_url(f"/menu_template_items/100"), headers=self.headers())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['msg'],
                         'MenuTemplateItem with id 100 not found')

    def test_delete_menu_template_item_with_no_permissions_fails(self):
        item = MenuTemplateItemFactory.create()
        item.save()
        response = self.client().delete(
            self.make_url(f"/menu_template_items/{item.id}"), headers=self.headers())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'],
                         'Access Error - No Role Granted')

    def test_get_deleted_menu_template_item_fails(self):
        self.create_admin()
        item = MenuTemplateItemFactory.create(is_deleted=True)
        item.save()
        response = self.client().get(
            self.make_url(f"/menu_template_items/{item.id}"), headers=self.headers())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['msg'], 'MenuTemplateItem with id {} not found'.format(item.id))

    def test_get_menu_template_item_succeeds(self):
        self.create_admin()
        item = MenuTemplateItemFactory.create()
        item.save()
        response = self.client().get(
            self.make_url(f"/menu_template_items/{item.id}"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(
            response_json['payload'], 'MenuTemplateItem')
        self.assertJSONKeysPresent(
            response_json['payload']['MenuTemplateItem'], 'mainMealId')
        self.assertJSONKeysPresent(
            response_json['payload']['MenuTemplateItem'], 'allowedProtein')
        self.assertJSONKeysPresent(
            response_json['payload']['MenuTemplateItem'], 'mainMealId')
        self.assertJSONKeysPresent(
            response_json['payload']['MenuTemplateItem'], 'allowedSide')

    def test_get_menu_template_with_no_permission_fails(self):
        item = MenuTemplateItemFactory.create()
        item.save()
        response = self.client().get(
            self.make_url(f"/menu_template_items/{item.id}"), headers=self.headers())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'],
                         'Access Error - No Role Granted')

    def test_get_non_existing_menu_template_fails(self):
        self.create_admin()
        response = self.client().get(
            self.make_url(f"/menu_template_items/123"), headers=self.headers())
            
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['msg'], 'MenuTemplateItem with id 123 not found')

    def test_update_template_item_no_parameters(self):
        self.create_admin()
        template_item = MenuTemplateItemFactory.create()
        template_item.save()

        response = self.client().put(
            self.make_url(f"/menu_template_items/{template_item.id}"),
                                     data=self.encode_to_json_string({}), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['msg']

        self.assert400(response)
        self.assertEqual(payload, 'Bad Request - Request Must be JSON Formatted')

    def test_update_template_item_endpoint_right_permission(self):
        self.create_admin()
        template_item = MenuTemplateItemFactory.create()
        
        meal_item = MealItemFactory.create()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }

        response = self.client().put(
            self.make_url(f"/menu_template_items/{template_item.id}"),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        data.pop("proteinItems")
        response_2 = self.client().patch(self.make_url(f"/menu_template_items/{template_item.id}"),
                                data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        payload_2 = self.decode_from_json_string(response_2.data.decode('utf-8'))['payload']

        self.assert200(response)
        self.assertEqual(payload['menuTemplateItem']['mainMealId'], data['mainMealId'])
        self.assertEqual(payload['menuTemplateItem']['allowedSide'], data['allowedSide'])
        self.assertEqual(payload['menuTemplateItem']['allowedProtein'], data['allowedProtein'])
        self.assert200(response_2)
        self.assertEqual(payload_2['menuTemplateItem']['mainMealId'], data['mainMealId'])
        self.assertEqual(payload_2['menuTemplateItem']['allowedSide'], data['allowedSide'])
        self.assertEqual(payload_2['menuTemplateItem']['allowedProtein'], data['allowedProtein'])

    def test_update_template_item_endpoint_wrong_permission(self):

        template_item = MenuTemplateItemFactory.create()

        meal_item = MealItemFactory.create()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }
        response = self.client().put(self.make_url(f"/menu_template_items/{template_item.id}"),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Role Granted')

    def test_update_template_item_endpoint_to_existing_allowed_protein_side(self):
        self.create_admin()
        items = MenuTemplateItemFactory.create_batch(5)
        [item.save() for item in items]

        template_item = MenuTemplateItemFactory.create(allowed_protein=items[0].allowed_protein)
        
        # meal_item = MealItemFactory.create(id=self.meal_items[0].id)
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": items[0].main_meal_id,
            "allowedSide": items[0].allowed_side,
            "allowedProtein": items[0].allowed_protein,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": items[0].day_id
        }

        response = self.client().put(self.make_url(f"/menu_template_items/{template_item.id}"),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assert400(response)
        self.assertEqual(response_json['payload']['message'], 'Menu Template Item already exists')

    def test_update_template_item_endpoint_invalid_id(self):
        self.create_admin()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }
        response = self.client().put(self.make_url(f"/menu_template_items/{5678}"), data=self.encode_to_json_string(data),
                                     headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], "MenuTemplateItem with id 5678 not found")

    def test_update_deleted_template_item(self):
        self.create_admin()

        template_item = MenuTemplateItemFactory.create(is_deleted=True)
        
        meal_item = MealItemFactory.create()
        day = MenuTemplateWeekDayFactory()
        day.save()
        data = {
            "mainMealId": self.meal_items[0].id,
            "allowedSide": 1,
            "allowedProtein": 1,
            "proteinItems": [i.id for i in self.meal_items],
            "sideItems": [i.id for i in self.meal_items],
            "dayId": day.id
        }

        response = self.client().put(self.make_url(f"/menu_template_items/{template_item.id}"),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'MenuTemplateItem with id 1 not found')