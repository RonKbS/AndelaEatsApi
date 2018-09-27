from app.controllers.base_controller import BaseController
from app.repositories.role_repo import RoleRepo
from app.repositories.user_role_repo import UserRoleRepo
from app.repositories.permission_repo import PermissionRepo

class RoleController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.role_repo = RoleRepo()
		self.user_role_repo = UserRoleRepo()
		self.permission_repo = PermissionRepo()
	
	''' ROLES '''
	def list_roles(self):
		roles = self.role_repo.fetch_all()
		role_list = [role.serialize() for role in roles.items]
		return self.handle_response('OK', payload={'roles': role_list, 'meta': self.pagination_meta(roles)})
	
	def get_role(self, role_id):
		role = self.role_repo.get(role_id)
		if role:
			return self.handle_response('OK', payload={'role': role.serialize()})
		return self.handle_response('Invalid or Missing role_id')
	
	def create_role(self):
		name, help = self.request_params('name', 'help')
		return self.handle_response('OK')
		role = self.role_repo.new_role(name=name, help=help)
		if role:
			return self.handle_response('OK', payload={'role': role.serialize()})
		return self.handle_response('Application Error')
	
	def update_role(self, role_id):
		pass
	
	def delete_role(self, delete_role):
		pass
	
	''' USER ROLES '''
	def get_user_role(self, user_id):
		user_role = self.user_role_repo.get(user_id)
		if user_role:
			return self.handle_response('OK', payload={'user_role': user_role.serialize()})
		return self.handle_response('Invalid or Missing user_id')
		
	def create_user_role(self):
		role_id, user_id = self.request_params('role_id', 'user_id')
		user_role = self.user_role_repo.new_user_role(role_id=role_id, user_id=user_id)
		if user_role:
			return self.handle_response('OK', payload={'user_role': user_role.serialize()})
		return self.handle_response('Application Error')
	
	def delete_user_role(self, user_id):
		pass
	
	''' PERMISSIONS '''
	def get_role_permissions(self, role_id):
		permissions = self.permission_repo.filter_by(**{'role_id':role_id})
		perm_list = [permission.serialize() for permission in permissions.items]
		return self.handle_response('OK', payload={'role_id':role_id, 'role_permissions': perm_list, 'meta': self.pagination_meta(permissions)})
	
	def create_role_permission(self):
		role_id, name, keyword = self.request_params('role_id', 'name', 'keyword')
		permission = self.permission_repo.new_permission(role_id=role_id, name=name, keyword=keyword)
		if permission:
			return self.handle_response('OK', payload={'permission': permission.serialize()})
		return self.handle_response('Application Error')
	
	def delete_role_permission(self, permission_id):
		pass
		
		
		