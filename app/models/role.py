from .base_model import BaseModel, db

class Role(BaseModel):
	__tablename__ = 'roles'
	
	name = db.Column(db.String(100), nullable=False)
	help = db.Column(db.Text(), nullable=True)
	
	permissions = db.relationship('Permission', lazy=False)
	