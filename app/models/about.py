"""
Model to store the about page
"""
from .base_model import BaseModel, db


class About(BaseModel):
    """About Model class"""
    __tablename__ = 'abouts'

    details = db.Column(db.LargeBinary())
