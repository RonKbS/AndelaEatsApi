from .base_model import BaseModel, db

class Vendor(BaseModel):
	__tablename__ = 'vendors'
	
	name = db.Column(db.String(120), nullable=False)
	address = db.Column(db.String(240), nullable=False)
	tel = db.Column(db.String(20), nullable=False)
	contact_person = db.Column(db.String(120), nullable=False)
	engagements = db.relationship('VendorEngagement', lazy=True)
 
	# ratings = db.relationship('VendorRating', backref='vendors', lazy=True)