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
@Security.validator(['templateName|required', 'mealPeriod|required', 'description|required'])
@swag_from('documentation/create_menu_template.yml')
def create_menu_template():
    return menu_template_controller.create()


@menu_template_blueprint.route('/<string:id>', methods=['PATCH','PUT'])
@Auth.has_role('admin')
@Security.validator(['templateName|string', 'locationId|int'])
def update_menu_template(id):
    return menu_template_controller.update(id)


