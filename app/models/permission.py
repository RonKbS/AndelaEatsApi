from .base_model import BaseModel, db
from . import constants

class Permission(BaseModel):
    __tablename__ = 'permissions'

    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    role = db.relationship('Role', lazy=False)
    name = db.Column(db.String(constants.MAXLEN), nullable=False)
    keyword = db.Column(db.String(constants.MAXLEN), nullable=False)
