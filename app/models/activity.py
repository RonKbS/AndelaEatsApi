"""module of activity model class"""
from .base_model import BaseModel, db
from app.utils.enums import Channels, ActionType
from . import constants

class Activity(BaseModel):
    """Activity Model class"""
    __tablename__ = 'activities'

    module_name = db.Column(db.String(constants.MAXLEN))
    ip_address = db.Column(db.String(constants.MAXLEN))
    user_id = db.Column(db.String(constants.MAXLEN))
    action_type = db.Column(db.Enum(ActionType))
    action_details = db.Column(db.String(2000))
    channel = db.Column(db.Enum(Channels))
