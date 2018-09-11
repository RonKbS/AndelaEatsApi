from .base_model import BaseModel, db

class UserRole(BaseModel):
	__tablename__ = 'user_roles'
	

	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
	user_id = db.Column(db.String)
	