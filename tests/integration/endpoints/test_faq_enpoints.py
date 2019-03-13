from tests.base_test_case import BaseTestCase
from factories.faq_factory import FaqFactory
from factories.role_factory import RoleFactory
from factories.user_role_factory import UserRoleFactory


class TestFaqEndpoints(BaseTestCase):
    '''Test class for faq endpoints'''

    def setUp(self):
        self.BaseSetUp()

    def test_get_faq_succeeds(self):

        new_faq = FaqFactory.create()

        response = self.client().get(self.make_url("/faqs/"), query_string={'id': str(new_faq.id)}, headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['faqs'][0]['id'], new_faq.id)

    def test_create_faq_succeeds(self):

        new_role = RoleFactory.create(name='Administrator')

        new_user_role = UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        faq = FaqFactory.build()

        faq_data = dict(category=faq.category, question=faq.question, answer=faq.answer)

        response = self.client().post(self.make_url("/faqs/"), headers=self.headers(),
                                      data=self.encode_to_json_string(faq_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['faq']['question'], faq.question)
        self.assertEqual(response_json['payload']['faq']['answer'], faq.answer)

    def test_update_faq_succeeds(self):
        new_role = RoleFactory.create(name='Administrator')

        new_user_role = UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        faq = FaqFactory()
        update_faq_info = FaqFactory.build()

        faq_data = dict(question=update_faq_info.question, answer=update_faq_info.answer)

        response = self.client().patch(self.make_url(f"/faqs/{faq.id}"), headers=self.headers(),
                                      data=self.encode_to_json_string(faq_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['faq']['question'], update_faq_info.question)
        self.assertEqual(response_json['payload']['faq']['answer'], update_faq_info.answer)

