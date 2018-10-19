from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request
from app.controllers.order_controller import OrderController
from app.utils.auth import Auth

url_prefix = '{}/orders'.format(BaseBlueprint.base_url_prefix)
order_blueprint = Blueprint('order', __name__, url_prefix=url_prefix)
order_controller = OrderController(request)

@order_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_orders')
def list_order():
    return order_controller.list_orders()

@order_blueprint.route('/<int:order_id>/', methods=['GET'])
def get_order(order_id):
    return order_controller.get_order(order_id)

@order_blueprint.route('/', methods=['POST'])
@Security.validator(['dateBookedFor|required:string', 'channel|string', 'mealItems|required:list'])
def create_order():
    return order_controller.create_order()

@order_blueprint.route('/<int:order_id>/', methods=['PATCH', 'PUT'])
@Security.validator(['userId|required:string', 'dateBookedFor|required:date', 'channel|string', 'mealItems|required:list'])
def update_order(order_id):
    return order_controller.update_order(order_id)

@order_blueprint.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    return order_controller.delete_order(order_id)
