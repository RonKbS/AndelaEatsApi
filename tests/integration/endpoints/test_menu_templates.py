from factories import (LocationFactory, MenuTemplateFactory,
                       VendorEngagementFactory, MenuTemplateItemFactory, PermissionFactory)
from tests.base_test_case import BaseTestCase
from tests.base_test_utils import BaseTestUtils


class TestMenuTemplate(BaseTestCase, BaseTestUtils):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_menu_template_with_no_permission_fails(self):
        data = {
            "name": "Name of the template",
            "mealPeriod": "lunch"
        }
        response = self.client().post(
            self.make_url("/menu_template/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['msg'],
                         'Access Error - No Role Granted')

    def test_create_menu_template_with_permission_succeeds(self):
        self.create_admin()
        LocationFactory.create(id=1).save()
        data = {
            "name": "Name of the template",
            "mealPeriod": "lunch",
            "description": "somehting"
        }
        response = self.client().post(
            self.make_url("/menu_template/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')

    def test_create_menu_template_with_no_data_fails(self):
        self.create_admin()
        data = {}
        response = self.client().post(
            self.make_url("/menu_template/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'], 'Bad Request - Request Must be JSON Formatted')

    def test_create_menu_template_with_missing_fields_fails(self):
        self.create_admin()
        LocationFactory()
        data = {
            "name": "Name of the template",
            "mealPeriod": "lunch",
        }
        response = self.client().post(
            self.make_url("/menu_template/"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'], 'Bad Request - description is required')

    def test_create_menu_template_with_same_name_in_a_center_fails(self):
        self.create_admin()
        template = MenuTemplateFactory.create()
        template.save()
        data = {
            "name": template.name,
            "mealPeriod": "lunch",
            "description": "sumon"
        }
        response = self.client().post(
            self.make_url("/menu_template/"), headers=self.headers(template.location_id),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONKeysPresent(response_json['payload'], 'message')
        self.assertEqual(response_json['payload']['message'],
                         'Meal Template with name  exists in your center')

    def test_update_menu_template_with_permission_succeeds(self):
        self.create_admin()
        template = MenuTemplateFactory.create(name="Name of the template")
        template.save()
        data = {
            "name": "Update the name of template",
            "description": "sumon"
        }
        response = self.client().put(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')

    def test_update_menu_template_non_existing_template_fails(self):
        self.create_admin()
        data = {
            "name": "Update the name of template",
        }
        response = self.client().put(
            self.make_url(f"/menu_template/13192498"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        self.assertEqual(response.status_code, 404)

    def test_update_one_field_of_a_menu_template_succeeds(self):
        self.create_admin()
        template = MenuTemplateFactory.create(name="Name of the template")
        template.save()
        data = {
            "name": "Update the name of template",
        }
        response = self.client().put(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertEqual(response_json['payload']
                         ['name'], "Update the name of template")
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')

    def test_update_menu_template_description(self):
        self.create_admin()
        template = MenuTemplateFactory.create(name="Name of the template")
        template.save()
        data = {
            "description": "updated"
        }
        response = self.client().put(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertEqual(response_json['payload']
                         ['description'], "updated")
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')

    def test_get_deleted_menu_template_fails(self):
        self.create_admin()
        template = MenuTemplateFactory.create(
            name="Name of the template", is_deleted=True)
        template.save()
        response = self.client().get(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json['msg'], 'MenuTemplate with id {} not found'.format(template.id))

    def test_get_menu_template_succeeds(self):
        self.create_admin()
        template = MenuTemplateFactory.create(
            name="Name of the template")
        template.save()
        response = self.client().get(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertJSONKeysPresent(response_json['payload'], 'weekdays')
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')

    def test_get_menu_template_with_no_permission_fails(self):
        template = MenuTemplateFactory.create(
            name="Name of the template")
        template.save()
        response = self.client().get(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['msg'],
                         'Access Error - No Role Granted')

    def test_get_non_existing_menu_template_fails(self):
        self.create_admin()
        response = self.client().get(
            self.make_url(f"/menu_template/123"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response_json['msg'], 'MenuTemplate with id 123 not found')

    def test_get_all_menu_template_succeeds(self):
        self.create_admin()
        templates = MenuTemplateFactory.build_batch(10)
        [template.save() for template in templates]
        response = self.client().get(
            self.make_url(f"/menu_template"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(
            len(response_json['payload']['MenuTemplates']), 10)
        self.assertJSONKeysPresent(response_json['payload'], 'meta')

    def test_get_all_menu_template_with_no_permissions_fails(self):
        templates = MenuTemplateFactory.build_batch(10)
        [template.save() for template in templates]
        response = self.client().get(
            self.make_url(f"/menu_template"), headers=self.headers())
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['msg'],
                         'Access Error - No Role Granted')

    def test_delete_menu_template_succeeds(self):
        self.create_admin()
        template = MenuTemplateFactory.create(
            name="Name of the template")
        template.save()
        response = self.client().delete(
            self.make_url(f"/menu_template/{template.id}"), headers=self.headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'],
                         f'menu_template deleted {template.id}')

    def test_delete_menu_template_fails_with_non_existing_template(self):
        self.create_admin()
        response = self.client().delete(
            self.make_url(f"/menu_template/100"), headers=self.headers())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['msg'],
                         'MenuTemplate with id 100 not found')

    def test_copy_menu_template_to_menus_with_permission_succeeds(self):
        role = self.create_admin()
        PermissionFactory.create(keyword='view_menu', role=role)
        item = MenuTemplateItemFactory.create()
        engagement = VendorEngagementFactory.create(
            start_date='2019-10-10', end_date='2019-10-30')
        engagement.save()
        item.save()
        data = {
            "vendorEngagementId": engagement.id,
            "startDate": "2019-10-10",
            "endDate": "2019-10-20",
            "menuTemplateId": item.day.template_id
        }
        response = self.client().post(
            self.make_url("/menu_template/copy"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response.json, 'msg')
        self.assertJSONKeyPresent(response.json, 'payload')
        self.assertJSONKeyPresent(response.json['payload'], 'message')

    def test_copy_menu_template_to_menus_with_permission_succeeds_and_duplicate_show_number_of_duplicates(self):
        role = self.create_admin()
        PermissionFactory.create(keyword='view_menu', role=role)
        item = MenuTemplateItemFactory.create()
        engagement = VendorEngagementFactory.create(
            start_date='2019-10-10', end_date='2019-10-30')
        engagement.save()
        item.save()
        data = {
            "vendorEngagementId": engagement.id,
            "startDate": "2019-10-10",
            "endDate": "2019-10-20",
            "menuTemplateId": item.day.template_id
        }
        self.client().post(
            self.make_url("/menu_template/copy"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response = self.client().post(
            self.make_url("/menu_template/copy"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response.json, 'msg')
        self.assertJSONKeyPresent(response.json, 'payload')
        self.assertJSONKeyPresent(response.json['payload'], 'message')

    def test_copy_menu_template_to_menus_invalid_date_range_fails(self):
        role = self.create_admin()
        PermissionFactory.create(keyword='view_menu', role=role)
        item = MenuTemplateItemFactory.create()
        engagement = VendorEngagementFactory.create()
        engagement.save()
        item.save()
        data = {
            "vendorEngagementId": engagement.id,
            "startDate": "2018-10-10",
            "endDate": "2018-10-20",
            "menuTemplateId": item.day.template_id
        }
        response = self.client().post(
            self.make_url("/menu_template/copy"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        self.assertEqual(response.status_code, 400)
        self.assertJSONKeyPresent(response.json, 'msg')
        self.assertJSONKeyPresent(response.json, 'payload')
        self.assertEqual(response.json['payload'], {
            'msg': f'Start and end date should be between {engagement.start_date} and {engagement.end_date}'},)
