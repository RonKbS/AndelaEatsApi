import base64
from tests.base_test_case import BaseTestCase
from factories.about_factory import AboutFactory

class TestAboutEndpoint(BaseTestCase):
    """Test class for About endpoints"""

    def setUp(self):
        self.BaseSetUp()
        self.html_data = dict(data="<html><head <meta charset=\"UTF-8\"></head></html>")
        self.html_data_update = dict(data="<html><head <meta charset=\"UTF-8\"></head><body></body></html>")

    def test_create_about_details_succeeds(self):

        response = self.client().post(
            self.make_url("/about/"), headers=self.headers(),
            data=self.encode_to_json_string(self.html_data)
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['data']["details"], self.html_data["data"])

    def test_patch_about_details_succeeds(self):
        AboutFactory.create(
            details=base64.b64encode(self.html_data['data'].encode('utf-8'))
        )

        response = self.client().patch(
            self.make_url("/about/"), headers=self.headers(),
            data=self.encode_to_json_string(self.html_data_update)
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['data']["details"], self.html_data_update["data"])

    def test_get_about_details_succeeds_for_existing_about_page(self):
        AboutFactory.create(
            details=base64.b64encode(self.html_data['data'].encode('utf-8'))
        )

        response = self.client().get(
            self.make_url("/about/"), headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['data']["details"], self.html_data["data"])

    def test_get_about_details_succeeds_for_non_existing_about_page(self):

        response = self.client().get(
            self.make_url("/about/"), headers=self.headers()
        )

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['data'], {})
