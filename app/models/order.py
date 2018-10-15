from .base_model import BaseModel, db
from app.utils.enums import Channels


class Order(BaseModel):
    __tablename__ = 'orders'

    user_id = db.Column(db.String(100))
    date_booked_for = db.Column(db.Date, nullable=False)
    channel = db.Column(db.Enum(Channels))
    status = db.Column(db.SmallInteger(), default=0)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    meal_item_orders = db.relationship('MealItem', secondary='meal_item_orders')


# many to many relationship between meal item and order
meal_item_orders = db.Table(
    'meal_item_orders',
    db.Column(
        'order_id',
        db.String,
        db.ForeignKey('orders.id'),
        nullable=False),
    db.Column(
        'meal_item_id',
        db.String,
        db.ForeignKey('meal_items.id'),
        nullable=False))
