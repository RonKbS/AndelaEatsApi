import factory
import factory.fuzzy
from app.utils import db
from datetime import date, datetime, timedelta
from app.models.menu import Menu
from factories.meal_item_factory import MealItemFactory
from factories.vendor_engagement_factory import VendorEngagementFactory


class MenuFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Menu
		sqlalchemy_session = db.session

	id = factory.Sequence(lambda n: n)
	
	meal_period = 'lunch'
	allowed_side = 1
	allowed_protein = 1
	side_items = factory.Faker('word')
	protein_items = factory.Faker('word')
	main_meal_id = factory.SelfAttribute('main_meal.id')
	vendor_engagement_id = factory.SelfAttribute('vendor_engagement.id')
	is_deleted = False
	main_meal = factory.SubFactory(MealItemFactory)
	vendor_engagement = factory.SubFactory(VendorEngagementFactory)

	date = datetime.now().date()
