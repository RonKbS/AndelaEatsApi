'''module of order model class'''
from .base_model import BaseModel, db
from app.utils.enums import Channels, OrderStatus, MealPeriods


class Order(BaseModel):
	'''Order Model class'''
	__tablename__ = 'orders'

	user_id = db.Column(db.String(100))
	date_booked_for = db.Column(db.Date, nullable=False)
	date_booked = db.Column(db.Date)
	channel = db.Column(db.Enum(Channels))
	meal_period = db.Column(db.Enum(MealPeriods))
	order_status = db.Column(db.Enum(OrderStatus))
	menu_id = db.Column(db.Integer(), db.ForeignKey('menus.id'))
	meal_item_orders = db.relationship('MealItem', secondary='meal_item_orders', lazy=False, backref=db.backref('orders', lazy=True))

# many to many relationship between meal item and order
meal_item_orders = db.Table(
    'meal_item_orders',
    db.Column('order_id', db.SmallInteger, db.ForeignKey('orders.id'), nullable=False),
    db.Column('meal_item_id', db.SmallInteger, db.ForeignKey('meal_items.id'), nullable=False))
