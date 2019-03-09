from flasgger import swag_from


from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers import ReportsController

reports_blueprint = Blueprint('reports', __name__, url_prefix='{}/reports'.format(BaseBlueprint.base_url_prefix))


reports_controller = ReportsController(request)


@reports_blueprint.route('/', methods=['GET'])
@swag_from('documentation/get_report.yml')
def dashboard_summary():
    return reports_controller.dashboard_summary()
