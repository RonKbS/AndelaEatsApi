import factory
from app.utils import db
from random import randint
from app.models.order import Order
from app.utils.enums import Channels
from datetime import date, timedelta
from tests.base_test_case import BaseTestCase


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Order
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    channel = Channels.web
    date_booked_for = date.today() + timedelta(days=1)
    date_booked = date.today()
    user_id = '-LG__88sozO1OGrqda2z'
