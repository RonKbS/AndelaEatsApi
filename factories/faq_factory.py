import factory
from app.utils import db
from app.models.faq import Faq
from app.utils.enums import FaqCategoryType


class FaqFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Faq
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    category = FaqCategoryType.user_faq
    question = factory.Faker('sentence', nb_words=8)
    answer = factory.Faker('sentence', nb_words=20)
