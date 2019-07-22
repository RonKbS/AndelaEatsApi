from app.utils.handled_exceptions import BaseModelValidationError
from tests.base_test_case import BaseTestCase
from tests.base_test_utils import BaseTestUtils
from factories import LocationFactory, MenuTemplateFactory


class TestMenuTemplate(BaseTestCase, BaseTestUtils):
    def setUp(self):
        self.BaseSetUp()

    def tearUp(self):
        self.BaseTearDown()

    def test_create_menu_template_with_no_permission_fails(self):
        data = {
            "templateName": "Name of the template",
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
            "templateName": "Name of the template",
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
            "templateName": "Name of the template",
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
            "templateName": template.name,
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
        data = {
            "templateName": "Update the name of template",
        }
        response = self.client().put(
            self.make_url(f"/menu_templates/{template.id}"), headers=self.headers(),
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
            "templateName": "Update the name of template",
        }
        response = self.client().put(
            self.make_url(f"/menu_templates/13192498"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        self.assertEqual(response.status_code, 404)
    
    def test_update_menu_template_succeeds(self):
        self.create_admin()
        template = MenuTemplateFactory.create(name="Name of the template")        
        data = {
            "templateName": "Update the name of template",
        }
        response = self.client().put(
            self.make_url(f"/menu_templates/{template.id}"), headers=self.headers(),
            data=self.encode_to_json_string(data))
        response_json = self.decode_from_json_string(
            response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertJSONKeysPresent(response_json['payload'], 'name')
        self.assertEqual(response_json['payload']['name'], "Update the name of template")
        self.assertJSONKeysPresent(response_json['payload'], 'locationId')
