from .base_model import BaseModel, db

from app.utils.enums import FaqCategoryType


class Faq(BaseModel):

    __tablename__ = 'faqs'

    category = db.Column(db.Enum(FaqCategoryType), nullable=False, default='user_faq')
    question = db.Column(db.String(2000), nullable=False)
    answer = db.Column(db.String(2000), nullable=False)
