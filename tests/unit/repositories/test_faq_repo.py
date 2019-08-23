from tests.base_test_case import BaseTestCase
from app.models.faq import Faq
from factories.faq_factory import FaqFactory
from app.repositories.faq_repo import FaqRepo


class TestFaqRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = FaqRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_faq_method_returns_new_faq_object(self):
        faq = FaqFactory.build()

        new_faq = self.repo.new_faq(faq.category, faq.question, faq.answer)

        self.assertIsInstance(new_faq, Faq)
        self.assertEqual(new_faq.category, faq.category)
        self.assertEqual(new_faq.question, faq.question)
        self.assertEqual(new_faq.answer, faq.answer)
