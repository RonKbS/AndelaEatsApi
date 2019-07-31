import factory
import factory.fuzzy
from app.utils import db
from datetime import datetime
from app.models.menu import Menu
from factories.meal_item_factory import MealItemFactory
from factories.vendor_engagement_factory import VendorEngagementFactory
from factories.location_factory import LocationFactory


class MenuFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Menu
        sqlalchemy_session = db.session

    meal_period = 'lunch'
    allowed_side = 1
    allowed_protein = 1
    side_items = factory.Faker('word')
    protein_items = factory.Faker('word')
    main_meal_id = factory.SelfAttribute('main_meal.id')
    is_deleted = False
    main_meal = factory.SubFactory(MealItemFactory)
    vendor_engagement = factory.SubFactory(VendorEngagementFactory)
    location = factory.SubFactory(LocationFactory)
    date = datetime.now().date()