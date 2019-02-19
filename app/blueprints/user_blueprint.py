from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Auth
from app.controllers.user_controller import UserController
from flasgger import swag_from

user_blueprint = Blueprint('user', __name__, url_prefix='{}/users'.format(BaseBlueprint.base_url_prefix))
user_controller = UserController(request)


@user_blueprint.route('/admin', methods=['GET'])
@Auth.has_permission('create_user_roles')
@swag_from('documentation/get_all_admin_users.yml')
def list_users():
    return user_controller.list_admin_users()