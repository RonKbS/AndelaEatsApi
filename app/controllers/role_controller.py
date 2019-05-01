
from app.controllers.base_controller import BaseController
from app.repositories.role_repo import RoleRepo
from app.repositories.user_role_repo import UserRoleRepo
from app.repositories.permission_repo import PermissionRepo
from app.services.andela import AndelaService
from app.utils.auth import Auth


class RoleController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.role_repo = RoleRepo()
		self.user_role_repo = UserRoleRepo()
		self.permission_repo = PermissionRepo()
		self.andela_service = AndelaService()

	''' ROLES '''

	def list_roles(self):
		roles = self.role_repo.filter_by(is_deleted=False)
		role_list = [role.serialize() for role in roles.items]
		return self.handle_response('OK', payload={'roles': role_list, 'meta': self.pagination_meta(roles)})

	def get_role(self, role_id):
		role = self.role_repo.get(role_id)
		if role:
			return self.handle_response('OK', payload={'role': role.serialize()})
		return self.handle_response('Invalid or Missing role_id', status_code=400)

	def create_role(self):
		name, help_ = self.request_params('name', 'help')
		role1 = self.role_repo.find_first(name=name)
		if not role1:
			role = self.role_repo.new_role(name=name, help_=help_)
			return self.handle_response('OK', payload={'role': role.serialize()}, status_code=201)
		return self.handle_response('Role with this name already exists', status_code=400)

	def update_role(self, role_id):
		name, help_ = self.request_params('name', 'help')
		role = self.role_repo.get(role_id)
		if role:
			updates = {}
			if name:
				role1 = self.role_repo.find_first(name=name)
				if role1:
					return self.handle_response('Role with this name already exists', status_code=400)
				updates['name'] = name
			if help_:
				updates['help'] = help_

			self.role_repo.update(role, **updates)
			return self.handle_response('OK', payload={'role': role.serialize()})
		return self.handle_response('Invalid or incorrect role_id provided', status_code=400)

	def delete_role(self, role_id):
		role = self.role_repo.get(role_id)
		if role:
			updates = {}
			updates['is_deleted'] = True
			self.role_repo.update(role, **updates)
			return self.handle_response('role deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect role_id provided', status_code=404)

	''' USER ROLES '''

	def get_user_roles(self, user_id):
		user_roles = self.user_role_repo.get_unpaginated(user_id=user_id)
		if user_roles:
			role_list = [role.serialize() for role in user_roles]
			return self.handle_response('OK', payload={'user_role': role_list})
		return self.handle_response('There are no roles for this user', status_code=404)

	def create_user_role(self):
		location = Auth.get_location()
		role_id, email_address = self.request_params('roleId', 'email')
		user = self.andela_service.get_user_by_email_or_id(email_address)
		if user is None:
			return self.handle_response('This user record does not exist', status_code=400)
		user_id = user['id']
		user_role = self.user_role_repo.get_unpaginated(role_id=role_id, user_id=user_id, is_deleted=False)
		if not user_role:
			role = self.role_repo.get(role_id)
			if role:
				user_role = self.user_role_repo.new_user_role(
					role_id=role_id, user_id=user_id,
					location_id=location, email=email_address)
				return self.handle_response('OK', payload={'user_role': user_role.serialize()}, status_code=201)
			return self.handle_response('This role does not exist', status_code=400)
		return self.handle_response('This User has this Role already', status_code=400)

	def delete_user_role(self, user_role_id):
		user_role = self.user_role_repo.get(user_role_id)
		if user_role:
			updates = {}
			updates['is_deleted'] = True
			self.user_role_repo.update(user_role, **updates)
			return self.handle_response('user_role deleted for user', payload={"status": "success"})
		return self.handle_response(
			'Invalid or incorrect user_role_id provided', status_code=404
		)

	def disable_user_role(self):
		user_id, role_id = self.request_params('userId', 'roleId')
		user_role = self.user_role_repo.get_unpaginated(user_id=user_id, role_id=role_id)[0]
		if user_role:
			updates = {}
			updates['is_active'] = False
			self.user_role_repo.update(user_role, **updates)
			return self.handle_response('user_role disabled for user', payload={"status": "success"})
		return self.handle_response(
			'Invalid or incorrect user_role_id provided', status_code=404
		)

	''' PERMISSIONS '''

	def get_role_permissions(self, role_id):
		permissions = self.permission_repo.get_unpaginated(**{'role_id': role_id})
		perm_list = [permission.serialize() for permission in permissions]
		return self.handle_response('OK', payload={'role_id': role_id, 'role_permissions': perm_list})

	def get_single_permission(self, role_id, permission_id):
		permission = self.permission_repo.filter_by(role_id=role_id, id=permission_id)
		permissions = [permission.serialize() for permission in permission.items]
		return self.handle_response('OK', payload={'permission': permissions})

	def get_all_permissions(self):
		permissions = self.permission_repo.get_unpaginated()
		perm_list = [permission.serialize() for permission in permissions]
		return self.handle_response('OK', payload={'permissions': perm_list})

	def create_role_permission(self):
		role_id, name, keyword = self.request_params(
			'role_id', 'name', 'keyword'
		)
		permission = self.permission_repo.get_unpaginated(
			name=name, is_deleted=False)
		if not permission:
			role = self.role_repo.get(role_id)
			if role:
				permission = self.permission_repo.new_permission(
					role_id=role_id, name=name, keyword=keyword
				)
				return self.handle_response('OK', payload={
					'permission': permission.serialize()
				}, status_code=201)
			return self.handle_response(
				'This role does not exist', status_code=400
			)
		return self.handle_response(
			'This permission already exists', status_code=400
		)

	def update_permission(self, permission_id):
		role_id, name, keyword = self.request_params('role_id', 'name', 'keyword')
		permission = self.permission_repo.get(permission_id)
		if permission:
			updates = {}
			if name:
				permission1 = self.permission_repo.find_first(name=name)
				if permission1:
					return self.handle_response('Permission with this name already exists', status_code=400)
				updates['name'] = name
			if role_id:
				updates['role_id'] = role_id
			if keyword:
				updates['keyword'] = keyword

			self.role_repo.update(permission, **updates)
			return self.handle_response('OK', payload={'permission': permission.serialize()})
		return self.handle_response('Invalid or incorrect permission id provided', status_code=400)

	def delete_role_permission(self, permission_id):
		permission = self.permission_repo.get(permission_id)
		if permission:
			updates = {}
			updates['is_deleted'] = True
			self.role_repo.update(permission, **updates)
			return self.handle_response('permission deleted', payload={"status": "success"})
		return self.handle_response(
			'Invalid or incorrect permission id provided', status_code=404
		)
