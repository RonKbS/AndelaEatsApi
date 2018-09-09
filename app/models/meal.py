from .base_model import BaseModel, db


class MealItem(BaseModel):
    __tablename__ = 'meal_items'
    vendor_engagement_id= db.Column(db.String(), db.ForeignKey('vendor_engagements.id'))
    meal_type_id = db.Column(db.String(), db.ForeignKey('meal_types.id'))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(1000))


class MealType(BaseModel):
    __tablename__ = 'meal_types'
    name = db.Column(db.String(120), nullable=False)
    meal_items = db.relationship('MealItem', backref='meal_types', lazy=True)


class MealPeriod(BaseModel):
    __tablename__ = 'meal_periods'
    name = db.Column(db.String(120), nullable=False, unique=True)
    menus = db.relationship('Menu', backref='MealPeriod', lazy=True)