from tests.base_test_case import BaseTestCase
from factories.faq_factory import FaqFactory


class TestFaqEndpoints(BaseTestCase):
    '''Test class for faq endpoints'''

    def setUp(self):
        self.BaseSetUp()

    def test_get_faq_succeeds(self):

        new_faq = FaqFactory.create()

        response = self.client().get(self.make_url("/faqs/"), query_string={'id': str(new_faq.id)}, headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))


        print('response', response_json)
        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['FAQs'][0]['id'], new_faq.id)