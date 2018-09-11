from .base_model import BaseModel, db

class Permission(BaseModel):
	__tablename__ = 'permissions'
	
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
	name = db.Column(db.String(100), nullable=False)
	keyword = db.Column(db.String(100), nullable=False)
	