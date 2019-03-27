"""
Module to deal with the about page
"""
from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Auth
from app.controllers.about_controller import AboutController
from app.utils.security import Security


about_blueprint = Blueprint('about', __name__, url_prefix='{}/about'.format(BaseBlueprint.base_url_prefix))
about_controller = AboutController(request)


@about_blueprint.route('/view', methods=['GET'])
@swag_from('documentation/get_about_page.yml')
def get_about_page():
    return about_controller.get_about_page()


@about_blueprint.route('/create_or_update', methods=['POST', 'PATCH'])
@Auth.has_role('admin')
@Security.validator(['data|required'])
@swag_from('documentation/create_about.yml')
def create_about_page():
    return about_controller.create_or_modify_about_page()

