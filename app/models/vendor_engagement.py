from .base_model import BaseModel, db

class VendorEngagement(BaseModel):
    __tablename__ = 'vendor_engagements'
    
    vendor_id = db.Column(db.Integer(), db.ForeignKey('vendors.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer(), nullable=False, default=1)
    termination_reason = db.Column(db.Text(), nullable=True)
    vendor = db.relationship('Vendor', lazy=False)
    
    # meal_items = db.relationship('MealItem', backref='vendor_engagements', lazy=True)
    # menus = db.relationship('Menu', backref='vendor_engagements', lazy=True)
    # vendor_ratings = db.relationship('VendorRating', backref='vendor_engagements', lazy=True)