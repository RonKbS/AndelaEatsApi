from .base_model import BaseModel, db


class VendorEngagement(BaseModel):
	__tablename__ = 'vendor_engagements'
	
	vendor_id = db.Column(db.Integer(), db.ForeignKey('vendors.id'))
	location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'), default=1)
	start_date = db.Column(db.Date, nullable=False)
	end_date = db.Column(db.Date, nullable=True)
	status = db.Column(db.Integer(), nullable=False, default=1)
	termination_reason = db.Column(db.Text(), nullable=True)
	vendor = db.relationship('Vendor', lazy=False)
	location = db.relationship('Location', lazy=False)
	menus = db.relationship('Menu', backref='vendor_engagements', lazy=True)
