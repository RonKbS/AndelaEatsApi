import factory

from app.models.meal_item import MealItem
from app.models.menu_template import MenuTemplateItem
from app.utils import db
from app.utils.enums import WeekDays
from factories.menu_template_factory import MenuTemplateWeekDayFactory, MenuTemplateFactory
from factories.meal_item_factory import MealItemFactory
from factories.location_factory import LocationFactory


class MenuTemplateItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MenuTemplateItem
        sqlalchemy_session = db.session

    day_id = factory.fuzzy.FuzzyChoice(WeekDays)
    main_meal_id = factory.SelfAttribute('meal_items.id', default=MealItem)
    allowed_side = 1
    allowed_protein = 1
    day = factory.SubFactory(MenuTemplateWeekDayFactory)
    main_meal = factory.SubFactory(MealItemFactory)
