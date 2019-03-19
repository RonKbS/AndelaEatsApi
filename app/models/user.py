from .base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = 'users'

    slack_id = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    user_role_id = db.Column(db.Integer(), db.ForeignKey('user_roles.id'))
    image_url = db.Column(db.String, nullable=True)
