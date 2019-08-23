import factory

from app.models.menu_template import MenuTemplate, MenuTemplateWeekDay
from app.utils import db
from app.utils.enums import MealPeriods, WeekDays
from factories.location_factory import LocationFactory


class MenuTemplateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MenuTemplate
        sqlalchemy_session = db.session
    name = factory.Faker('word')
    meal_period = 'lunch'
    description = factory.Faker('word')
    location_id = factory.SelfAttribute('location.id')
    location = factory.SubFactory(LocationFactory)


class MenuTemplateWeekDayFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MenuTemplateWeekDay
        sqlalchemy_session = db.session

    day = factory.fuzzy.FuzzyChoice(WeekDays)

    template_id = factory.SelfAttribute('menu_template.id')

    menu_template = factory.SubFactory(MenuTemplateFactory)
