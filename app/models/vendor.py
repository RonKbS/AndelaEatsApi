from .base_model import BaseModel, db


class Vendor(BaseModel):
    __tablename__ = 'vendors'

    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(240), nullable=False)
    tel = db.Column(db.String(20), nullable=False)
    contact_person = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    average_rating = db.Column(db.Float, default=0.0, nullable=True)
    location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'), default=1)
    location = db.relationship('Location', lazy=False)
    engagements = db.relationship('VendorEngagement', lazy=True)
    ratings = db.relationship('VendorRating', lazy=True)
