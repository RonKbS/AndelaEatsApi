import factory
from app.utils import db
from app.models.order import Order
from app.utils.enums import Channels
from datetime import date, timedelta
from factories.menu_factory import MenuFactory
from factories.location_factory import LocationFactory


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Order
        sqlalchemy_session = db.session

    channel = Channels.web
    date_booked_for = date.today() + timedelta(days=1)
    date_booked = date.today()
    user_id = '-LG__88sozO1OGrqda2z'
    menu = factory.SubFactory(MenuFactory)
    menu_id = factory.SelfAttribute('menu.id')
    location = factory.SubFactory(LocationFactory)