from .base_model import BaseModel, db
from datetime import datetime


class MealService(BaseModel):
    __tablename__ = 'meal_services'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    session_id = db.Column(db.Integer(), db.ForeignKey('meal_sessions.id'), nullable=False)
