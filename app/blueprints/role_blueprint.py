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
def get_role(role_id):
	return role_controller.get_role(role_id)


@role_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
def create_role():
	return role_controller.create_role()


@role_blueprint.route('/<int:role_id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('create_roles')
def update_role(role_id):
	return role_controller.update_role(role_id)


@role_blueprint.route('/<int:role_id>', methods=['DELETE'])
@Auth.has_permission('delete_roles')
def delete_role(role_id):
	return role_controller.delete_role(role_id)

''' USER ROLES '''


@role_blueprint.route('/user/<user_id>', methods=['GET'])
@Auth.has_permission('view_user_roles')
def get_user_role(user_id):
	return role_controller.get_user_roles(user_id)


@role_blueprint.route('/user', methods=['POST'])
@Security.validator(['role_id|required:int', 'user_id|required'])
@Auth.has_permission('create_user_roles')
def create_user_role():
	return role_controller.create_user_role()


@role_blueprint.route('/user/<int:user_role_id>', methods=['DELETE'])
@Auth.has_permission('delete_user_roles')
def delete_user_role(user_role_id):
	return role_controller.delete_user_role(user_role_id)

''' ROLE PERMISSIONS '''


@role_blueprint.route('/permissions/<int:role_id>', methods=['GET'])
@Auth.has_permission('view_permissions')
@swag_from('documentation/get_all_permissions.yml')
def get_role_permissions(role_id):
	return role_controller.get_role_permissions(role_id)


@role_blueprint.route('/permissions', methods=['GET'])
@Auth.has_permission('view_permissions')
def get_all_permissions():
	return role_controller.get_all_permissions()


@role_blueprint.route('/permissions', methods=['POST'])
@Security.validator(['role_id|required:int', 'name|required', 'keyword|required'])
@Auth.has_permission('create_permissions')
def create_role_permission():
	return role_controller.create_role_permission()


@role_blueprint.route('/permissions/<int:permission_id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('create_permissions')
def update_permission(permission_id):
	return role_controller.update_permission(permission_id)


@role_blueprint.route('/permissions/<int:permission_id>', methods=['DELETE'])
@Auth.has_permission('delete_permissions')
def delete_role_permission(permission_id):
	return role_controller.delete_role_permission(permission_id)
