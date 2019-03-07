"""
Module to deal with Activity logs
"""

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers.activity_controller import ActivityController
from app.utils.security import Security

activity_blueprint = Blueprint('activity', __name__, url_prefix='{}/activities'.format(BaseBlueprint.base_url_prefix))
activity_controller = ActivityController(request)


@activity_blueprint.route('/range', methods=['GET'])
@Security.url_validator(['date_range|required:range'])
def list_activities_date_range():
    return activity_controller.list_by_date_range()


@activity_blueprint.route('/action_range', methods=['GET'])
@Security.url_validator(['action_type|required:enum_options', 'date_range|required:range'])
def list_activities_action_type_date_range():
    return activity_controller.list_by_action_type_and_date_range()
