from .base_model import BaseModel, db
from app.utils.enums import MealTypes

class MealItem(BaseModel):
    __tablename__ = 'meal_items'

    meal_type = db.Column(db.Enum(MealTypes))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
