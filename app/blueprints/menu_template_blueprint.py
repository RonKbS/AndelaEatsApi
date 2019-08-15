"""
Module to deal with the menu templates
"""

from flasgger import swag_from

from app.blueprints.base_blueprint import (Auth, BaseBlueprint, Blueprint,
                                           request)
from app.controllers.menu_template_controller import MenuTemplateController
from app.models.menu_template import MenuTemplate
from app.utils.security import Security

url_prefix = '{}/menu_template'.format(BaseBlueprint.base_url_prefix)

menu_template_blueprint = Blueprint(
    'menu_template', __name__, url_prefix=url_prefix)
menu_template_controller = MenuTemplateController(request)


@menu_template_blueprint.route('/', methods=['POST', 'GET'])
@Auth.has_role('admin')
@Security.validator(['name|required', 'mealPeriod|required:enum_MealPeriods', 'description|required'])
@swag_from('documentation/menu_template.yml')
def create_menu_template():
    return menu_template_controller.create() if request.method == 'POST' else menu_template_controller.get_all()


@menu_template_blueprint.route('/<int:id>', methods=['PATCH', 'PUT'])
@Auth.has_role('admin')
@Security.validator(['name|string', 'description|string', 'mealPeriod|enum_MealPeriods'])
@swag_from('documentation/menu_template.yml')
def update_menu_template(id):
    return menu_template_controller.update(id)


@menu_template_blueprint.route('/<string:id>', methods=['GET'])
@Auth.has_role('admin')
@swag_from('documentation/get_menu_template.yml')
def get_menu_template(id):
    return menu_template_controller.get(id)