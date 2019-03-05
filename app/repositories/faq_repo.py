from app.repositories.base_repo import BaseRepo
from app.models.faq import Faq


class FaqRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Faq)

    @staticmethod
    def new_faq(category, question, answer):

        faq = Faq(category=category, question=question, answer=answer)
        faq.save()

        return faq
