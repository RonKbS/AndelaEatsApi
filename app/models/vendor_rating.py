'''Module for VendorRating Model class'''
from app.utils.enums import RatingType
from .base_model import BaseModel, db
from . import constants


class VendorRating(BaseModel):
    __tablename__ = 'vendor_ratings'

    vendor_id = db.Column(db.Integer(), db.ForeignKey('vendors.id'))
    user_id = db.Column(db.String(constants.MAXLEN))
    comment = db.Column(db.String(1000), nullable=True)
    service_date = db.Column(db.Date())
    rating = db.Column(db.Float())
    channel = db.Column(db.String(constants.MAXLEN))
    rating_type = db.Column(db.Enum(RatingType))
    type_id = db.Column(db.Integer(), default=0)
    engagement_id = db.Column(
        db.Integer(), db.ForeignKey('vendor_engagements.id'))
    vendor = db.relationship('Vendor', lazy=False)
    engagement = db.relationship('VendorEngagement', lazy=False)
    main_meal_id = db.Column(db.Integer(), db.ForeignKey(
        'meal_items.id'), nullable=True)
