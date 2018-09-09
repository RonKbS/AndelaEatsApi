from .base_model import BaseModel, db

class Order(BaseModel):
	__tablename__ = 'orders'
	
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date_booked_for = db.Column(db.Date, nullable=False)
	status = db.Column(db.SmallInteger(), default=0)
# 	meal_item_orders = db.relationship('MealItem', secondary='meal_item_order')
#
#
# # many to many relationship between meal item and order
# meal_item_order = db.Table(
# 	'meal_item_orders',
# 	db.Column(
# 		'order_id',
# 		db.String,
# 		db.ForeignKey('orders.id'),
# 		nullable=False),
# 	db.Column(
# 		'meal_item_id',
# 		db.String,
# 		db.ForeignKey('meal_items.id'),
# 		nullable=False))
#