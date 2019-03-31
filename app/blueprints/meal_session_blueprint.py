"""
Module to deal with meal sessions
"""
from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers.meal_session_controller import MealSessionController
from app.utils.security import Security
from app.utils.auth import Auth


meal_session_blueprint = Blueprint('meal_session', __name__, url_prefix='{}/meals'.format(BaseBlueprint.base_url_prefix))
meal_session_controller = MealSessionController(request)


@meal_session_blueprint.route('/session', methods=['POST'])
@Auth.has_role('admin')
@Security.validator([
    'name|required:enum_MealSessionNames',
    'date|required:date',
    'startTime|required:time',
    'endTime|required:time',
    'locationId|int']
)
@swag_from('documentation/create_meal_session.yml')
def create():
    return meal_session_controller.create_session()


<<<<<<< HEAD
@meal_session_blueprint.route('/session/<int:meal_session_id>', methods=['PUT'])
@Auth.has_role('admin')
@Security.validator([
    'name|required:enum_MealSessionNames',
    'date|required:date',
    'startTime|required:time',
    'endTime|required:time',
    'locationId|int']
)


@swag_from('documentation/update_meal_session.yml')
def update(meal_session_id):
    return meal_session_controller.update_session(meal_session_id)


@meal_session_blueprint.route('/session', methods=['GET'])
=======
@meal_session_blueprint.route('/session/', methods=['GET'])
>>>>>>> add tests
@Auth.has_role('admin')
@swag_from('documentation/get_meal_sessions.yml')
def list_sessions():
    return meal_session_controller.list_meal_sessions()

