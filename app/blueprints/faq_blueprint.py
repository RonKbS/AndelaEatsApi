'''A module of FAQ blueprint'''
from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Auth
from app.controllers.faq_controller import FaqController
from app.utils.security import Security
from app.models import Faq
from flasgger import swag_from


faq_blueprint = Blueprint('faq', __name__, url_prefix='{}/faqs'.format(BaseBlueprint.base_url_prefix))

faq_controller = FaqController(request)


@faq_blueprint.route('/', methods=['GET'])
@Security.validate_query_params(Faq)
@swag_from('documentation/get_faqs.yml')
def list_faqs():

    kwargs = faq_controller.get_params_dict()

    return faq_controller.list_faqs(**kwargs)


@faq_blueprint.route('/', methods=['POST'])
@Auth.has_role('Administrator')
@Security.validator(['category|required:enum_FaqCategoryType', 'question|required', 'answer|required'])
@swag_from('documentation/create_faq.yml')
def create_faq():

    return faq_controller.create_faq()


@faq_blueprint.route('/<int:faq_id>', methods=['PUT', 'PATCH'])
@Auth.has_role('Administrator')
@Security.validator(['category|optional:enum_FaqCategoryType', 'question|optional', 'answer|optional'])
@swag_from('documentation/update_faq.yml')
def update_faq(faq_id):

    return faq_controller.update_faq(faq_id)

