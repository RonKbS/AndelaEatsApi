from .base_model import BaseModel, db


class VendorRating(BaseModel):
    __tablename__='vendor_ratings'
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    vendor_id = db.Column(db.String(), db.ForeignKey('vendors.id'))
    user_id = db.Column(db.String(100))
    vendor_engagement_id = db.Column(db.String(), db.ForeignKey('vendor_engagements.id'))
    order_id = db.Column(db.String(), db.ForeignKey('orders.id'))
    comment = db.Column(db.String(1000), nullable=True)
    rating = db.Column(db.Integer)