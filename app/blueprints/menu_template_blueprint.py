"""
Module to deal with the menu templates
"""

from flasgger import swag_from

from app.blueprints.base_blueprint import (Auth, BaseBlueprint, Blueprint,
                                           request)
from app.controllers.menu_template_controller import MenuTemplateController
from app.utils.security import Security

url_prefix = '{}/menu_template'.format(BaseBlueprint.base_url_prefix)

menu_template_blueprint = Blueprint(
    'menu_template', __name__, url_prefix=url_prefix)
menu_template_controller = MenuTemplateController(request)


@menu_template_blueprint.route('/', methods=['POST'])
@Auth.has_role('admin')
@Security.validator(['name|required', 'mealPeriod|string:required:enum_MealPeriods', 'description|required'])
@swag_from('documentation/create_menu_template.yml')
def create_menu_template():
    return menu_template_controller.create()


@menu_template_blueprint.route('/<int:id>', methods=['PATCH','PUT'])
@Auth.has_role('admin')
@Security.validator(['name|string', 'description|string','mealPeriod|string:enum_MealPeriods'])
def update_menu_template(id):
    return menu_template_controller.update(id)


