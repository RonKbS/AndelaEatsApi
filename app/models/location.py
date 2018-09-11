from .base_model import BaseModel, db

class Location(BaseModel):
	__tablename__ = 'locations'
	
	name = db.Column(db.String(100), nullable=False)
	