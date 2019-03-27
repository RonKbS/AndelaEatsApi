from .base_model import BaseModel, db
from app.utils.enums import MealSessionNames


class MealSession(BaseModel):

    __tablename__ = 'meal_sessions'

    name = db.Column(db.Enum(MealSessionNames))
    start_time = db.Column(db.Time(), nullable=False)
    stop_time = db.Column(db.Time(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'))
