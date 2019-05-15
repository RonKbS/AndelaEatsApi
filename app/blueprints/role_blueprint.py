from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.role_controller import RoleController
from flasgger import swag_from

url_prefix = '{}/roles'.format(BaseBlueprint.base_url_prefix)
role_blueprint = Blueprint('role', __name__, url_prefix=url_prefix)
role_controller = RoleController(request)

''' ROLES '''


@role_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_roles')
@swag_from('documentation/get_all_roles.yml')
def list_roles():
	return role_controller.list_roles()


@role_blueprint.route('/<int:role_id>', methods=['GET'])
@Auth.has_permission('view_roles')
@swag_from('documentation/get_role_by_id.yml')
def get_role(role_id):
	return role_controller.get_role(role_id)


@role_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
@swag_from('documentation/create_role.yml')
def create_role():
	return role_controller.create_role()


@role_blueprint.route('/<int:role_id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('create_roles')
@swag_from('documentation/update_role.yml')
def update_role(role_id):
	return role_controller.update_role(role_id)


@role_blueprint.route('/<int:role_id>', methods=['DELETE'])
@Auth.has_permission('delete_roles')
@swag_from('documentation/delete_role.yml')
def delete_role(role_id):
	return role_controller.delete_role(role_id)

''' USER ROLES '''

@role_blueprint.route('/user/<user_id>', methods=['GET'])
@Auth.has_permission('view_user_roles')
@swag_from('documentation/view_user_roles.yml')
def get_user_role(user_id):
	return role_controller.get_user_roles(user_id)


@role_blueprint.route('/user', methods=['POST'])
@Security.validator(['roleId|required:int', 'email|required:email'])
@Auth.has_permission('create_user_roles')
@swag_from('documentation/create_user_role.yml')
def create_user_role():
	return role_controller.create_user_role()


@role_blueprint.route('/user/delete/<int:user_role_id>', methods=['DELETE'])
@Auth.has_permission('delete_user_roles')
@swag_from('documentation/delete_user_roles.yml')
def delete_user_role(user_role_id):
	return role_controller.delete_user_role(user_role_id)


@role_blueprint.route('/user/disable/', methods=['POST'])
@Security.validator(['roleId|required:int', 'userId|required'])
@Auth.has_permission('delete_user_roles')
@swag_from('documentation/disable_user_roles.yml')
def disable_user_role():
	return role_controller.disable_user_role()

''' ROLE PERMISSIONS '''


@role_blueprint.route('/<int:role_id>/permissions', methods=['GET'])
@Auth.has_permission('view_permissions')
@swag_from('documentation/get_all_permissions_by_role_id.yml')
def get_role_permissions(role_id):
	return role_controller.get_role_permissions(role_id)


@role_blueprint.route('/<int:role_id>/permissions/<int:permission_id>', methods=['GET'])
@Auth.has_permission('view_permissions')
@swag_from('documentation/get_permission_by_role_id_permission_id.yml')
def get_single_permission(role_id, permission_id):
	return role_controller.get_single_permission(role_id, permission_id)


@role_blueprint.route('/permissions', methods=['GET'])
@Auth.has_permission('view_permissions')
@swag_from('documentation/get_all_permissions.yml')
def get_all_permissions():
	return role_controller.get_all_permissions()


@role_blueprint.route('/permissions', methods=['POST'])
@Security.validator(['role_id|required:int', 'name|required', 'keyword|required'])
@Auth.has_permission('create_permissions')
@swag_from('documentation/create_permissions.yml')
def create_role_permission():
	return role_controller.create_role_permission()


@role_blueprint.route('/permissions/<int:permission_id>', methods=['PUT', 'PATCH'])
@Security.validator(['role_id|required:int', 'name|required', 'keyword|required'])
@Auth.has_permission('create_permissions')
@swag_from('documentation/update_permissions.yml')
def update_permission(permission_id):
	return role_controller.update_permission(permission_id)


@role_blueprint.route('/permissions/<int:permission_id>', methods=['DELETE'])
@Auth.has_permission('delete_permissions')
@swag_from('documentation/delete_permissions.yml')
def delete_role_permission(permission_id):
	return role_controller.delete_role_permission(permission_id)
