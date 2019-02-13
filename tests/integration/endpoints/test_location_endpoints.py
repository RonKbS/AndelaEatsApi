'''Module of integration tests for bot endpoints'''

from tests.base_test_case import BaseTestCase
from factories import LocationFactory


class TestLocationEndpoints(BaseTestCase):
    '''Test class for bot endpoints'''

    def setUp(self):
        self.BaseSetUp()

    def test_get_location_succeeds(self):

        new_location = LocationFactory.create()

        response = self.client().get(self.make_url('/locations/'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['locations'][0]['name'], new_location.name)

    def test_get_specific_location_succeeds(self):

        new_location = LocationFactory.create()

        response = self.client().get(self.make_url(f'/locations/{new_location.id}'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['location']['name'], new_location.name)

    def test_create_location_succeeds(self):
        location = LocationFactory.build()

        location_data = {'name': location.name, 'zone': location.zone}

        response = self.client().post(self.make_url('/locations/'), data=self.encode_to_json_string(location_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['location']['name'], location.name)

    def test_update_existing_location_succeeds(self):
        new_location = LocationFactory.create()

        update_location_data = {'name': new_location.name, 'zone': 'central'}

        response = self.client().patch(self.make_url(f'/locations/{new_location.id}'), data=self.encode_to_json_string(update_location_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['location']['name'], update_location_data['name'])
        self.assertEqual(response_json['payload']['location']['zone'], new_location.zone)

    def test_update_non_existing_location_with_fails(self):
        update_location_data = {'name': 'test name', 'zone': 'central'}

        response = self.client().patch(self.make_url(f'/locations/100'),
                                       data=self.encode_to_json_string(update_location_data),
                                       headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], 'Location Not Found')

    def test_delete_existing_location_succeeds(self):
        new_location = LocationFactory.create()

        response = self.client().delete(self.make_url(f'/locations/{new_location.id}'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'Location deleted successfully')

    def test_delete_non_existing_location_fails(self):

        response = self.client().delete(self.make_url(f'/locations/100'), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], 'Location Not Found')




