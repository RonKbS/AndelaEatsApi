from .base_model import BaseModel, db

class UserRole(BaseModel):
	__tablename__ = 'user_roles'
	

	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
	location_id = db.Column(db.Integer(), db.ForeignKey('locations.id'), default=1)
	location = db.relationship('Location', lazy=False)
	user_id = db.Column(db.String)
	email = db.Column(db.String)
	is_active = db.Column(db.Boolean, default=True, nullable=True)
	