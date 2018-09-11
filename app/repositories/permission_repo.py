from app.repositories.base_repo import BaseRepo
from app.models.permission import Permission

class PermissionRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Permission)
	
	def new_permission(self, role_id, name, keyword):
		perm = Permission(role_id=role_id, name=name, keyword=keyword)
		perm.save()
		return perm