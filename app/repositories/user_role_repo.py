from app.repositories.base_repo import BaseRepo
from app.models.user_role import UserRole

class UserRoleRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, UserRole)
	
	def new_user_role(self, role_id, user_id, location_id, email):
		user_role = UserRole(role_id=role_id, user_id=user_id, location_id=location_id, email=email)
		user_role.save()
		return user_role