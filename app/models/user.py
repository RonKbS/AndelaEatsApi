from .base_model import BaseModel, db

class User(BaseModel):
	__tablename__ = 'users'
	
	email = db.Column(db.String(120), nullable=False, unique=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	image = db.Column(db.String(1000))
	# user_orders = db.relationship('Order', backref='users', lazy=True)
	vendor_ratings = db.relationship('VendorRating', backref='users', lazy=True)