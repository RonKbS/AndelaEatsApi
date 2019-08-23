from .base_model import BaseModel, db
from . import constants

class Location(BaseModel):
    __tablename__ = 'locations'

    name = db.Column(db.String(constants.MAXLEN), nullable=False)
    zone = db.Column(db.String(10), nullable=True)
    engagements = db.relationship('VendorEngagement', lazy=True)
    vendors = db.relationship('Vendor', lazy=True)
    user_roles = db.relationship('UserRole', lazy=True)
