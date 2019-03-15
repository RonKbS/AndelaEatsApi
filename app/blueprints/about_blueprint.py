"""
Module to deal with the about page
"""
from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers.about_controller import AboutController


about_blueprint = Blueprint('about', __name__, url_prefix='{}/about'.format(BaseBlueprint.base_url_prefix))
about_controller = AboutController(request)


@about_blueprint.route('/view', methods=['GET'])
def get_about_page():
    return about_controller.get_about_page()


@about_blueprint.route('/create_or_update', methods=['POST', 'PATCH'])
def create_about_page():
    return about_controller.create_or_modify_about_page()

