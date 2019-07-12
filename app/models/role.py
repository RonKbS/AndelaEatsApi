from .base_model import BaseModel, db
from . import constants

class Role(BaseModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(constants.MAXLEN), nullable=False, unique=True)
    help = db.Column(db.Text(), nullable=True)

    permissions = db.relationship('Permission', lazy=False)
