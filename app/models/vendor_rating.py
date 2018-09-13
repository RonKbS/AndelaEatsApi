from .base_model import BaseModel, db


class VendorRating(BaseModel):
    __tablename__='vendor_ratings'

    vendor_id = db.Column(db.Integer(), db.ForeignKey('vendors.id'))
    user_id = db.Column(db.String(100))
    vendor_engagement_id = db.Column(db.Integer(), db.ForeignKey('vendor_engagements.id'))
    # order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'))
    order_id = db.Column(db.Integer())
    comment = db.Column(db.String(1000), nullable=True)
    rating = db.Column(db.Float())
