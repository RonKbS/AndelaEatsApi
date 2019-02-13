'''Module of integration tests for bot endpoints'''

from tests.base_test_case import BaseTestCase
from factories import LocationFactory


class TestBotEndpoints(BaseTestCase):
    '''Test class for bot endpoints'''

    def setUp(self):
        self.BaseSetUp()

    def test_get_bot_endpoint(self):
        new_location = LocationFactory.create()

        response = self.client().get(self.make_url('/bot/'))
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['attachments'][0]['actions'][0]['text'], new_location.name)

