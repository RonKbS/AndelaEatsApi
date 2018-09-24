'''Module for VendorRating Model class'''
from .base_model import BaseModel, db

class VendorRating(BaseModel):
	__tablename__='vendor_ratings'

	vendor_id = db.Column(db.Integer(), db.ForeignKey('vendors.id'))
	user_id = db.Column(db.String(100))
	comment = db.Column(db.String(1000), nullable=True)
	rating = db.Column(db.Float())
	channel = db.Column(db.String(100))
	vendor = db.relationship('Vendor', lazy=False)
