import factory
from app.utils import db
from app.models.about import About


class AboutFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = About
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
