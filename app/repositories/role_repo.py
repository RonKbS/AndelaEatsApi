from app.repositories.base_repo import BaseRepo
from app.models.role import Role

class RoleRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Role)
		
	def new_role(self, name, help=None):
		role = Role(name=name, help=help)
		role.save()
		return role