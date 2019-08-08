'''module of order model class'''
from .base_model import BaseModel, db
from app.utils.enums import Channels, OrderStatus, MealPeriods
from . import constants


class Order(BaseModel):
    '''Order Model class'''
    __tablename__ = 'orders'

    user_id = db.Column(db.String(constants.MAXLEN))
    date_booked_for = db.Column(db.Date, nullable=False)
    date_booked = db.Column(db.Date)
    channel = db.Column(db.Enum(Channels))
    meal_period = db.Column(db.Enum(MealPeriods))
    order_status = db.Column(db.Enum(OrderStatus))
    has_rated = db.Column(db.Boolean, default=False)
    menu = db.relationship('Menu', lazy=False)
    menu_id = db.Column(db.Integer(), db.ForeignKey('menus.id'))
    meal_item_orders = db.relationship('MealItem', secondary='meal_item_orders', lazy=False,
                                       backref=db.backref('orders', lazy=True))
    location_id = db.Column(
        db.Integer(), db.ForeignKey('locations.id'), default=1)
    location = db.relationship('Location', lazy=False)


# many to many relationship between meal item and order
meal_item_orders = db.Table(
    'meal_item_orders',
    db.Column('order_id', db.SmallInteger,
              db.ForeignKey('orders.id'), nullable=False),
    db.Column('meal_item_id', db.SmallInteger, db.ForeignKey('meal_items.id'), nullable=False))
