import factory
from app.utils import db
from random import randint
from app.utils.enums import MealTypes
from app.models.meal_item import MealItem

class MealItemFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = MealItem
        sqlalchemy_session = db.session
    
    id = factory.sequence(lambda n: n)
    meal_type = MealTypes.side
    name = factory.Faker('name')
    description = factory.Faker('sentence', nb_words=4)
    image = 'https://www.pexels.com/photo/burrito-chicken-delicious-dinner-461198/'

