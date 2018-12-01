from .base_model import BaseModel, db
from app.utils.enums import MealPeriods


class Menu(BaseModel):
    __tablename__ = 'menus'

    date = db.Column(db.Date(), nullable=False)
    meal_period = db.Column(db.Enum(MealPeriods), nullable=False)
    main_meal_id = db.Column(db.Integer(), db.ForeignKey('meal_items.id'), nullable=False)
    allowed_side = db.Column(db.Integer(), default=1)
    allowed_protein = db.Column(db.Integer(), default=1)
    side_items = db.Column(db.String(), nullable=False)
    protein_items = db.Column(db.String(), nullable=False)
    vendor_engagement_id = db.Column(db.Integer(), db.ForeignKey('vendor_engagements.id'))
    location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'), default=1)
    location = db.relationship('Location', lazy=False)
    main_meal = db.relationship('MealItem', lazy=False)
    vendor_engagement = db.relationship('VendorEngagement', lazy=False)
