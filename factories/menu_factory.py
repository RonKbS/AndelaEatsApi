import factory
from app.utils import db
from datetime import date, datetime, timedelta
from app.models.menu import Menu


class MenuFactory(factory.alchemy.SQLAlchemyModelFactory):


  class Meta:
    model = Menu
    sqlalchemy_session = db.session

  id = factory.Sequence(lambda n: n)
  date = (datetime.now() + timedelta(weeks=+1)).date().strftime('%Y-%m-%d')
  meal_period = 'lunch'
  allowed_side = 1
  allowed_protein = 1