from .base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = 'users'

    slack_id = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String, nullable=True)
