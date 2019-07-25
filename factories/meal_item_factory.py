import factory
from app.utils import db
from app.utils.enums import MealTypes
from app.models.meal_item import MealItem
from factories.location_factory import LocationFactory


class MealItemFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = MealItem
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    meal_type = MealTypes.side
    name = factory.Faker('name')
    location = factory.SubFactory(LocationFactory)
    image = 'https://www.pexels.com/photo/burrito-chicken-delicious-dinner-461198/'
