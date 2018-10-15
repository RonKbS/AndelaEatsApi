import factory
from app.utils import db
from random import randint
from app.models.order import Order
from app.utils.enums import Channels
from datetime import date


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Order
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    channel = Channels.web
    date_booked_for = date.today()
    user_id = "a valid user"
