from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.bot_controller import BotController

url_prefix = '{}/bot'.format(BaseBlueprint.base_url_prefix)
bot_blueprint = Blueprint('bot', __name__, url_prefix=url_prefix)
bot_controller = BotController(request)


@bot_blueprint.route('/', methods=['GET'])
def bot():
	return bot_controller.bot()


@bot_blueprint.route('/interactions/', methods=['GET'])
# @swag_from('documentation/get_all_meal_items.yml')
def interactions():
	return bot_controller.interactions()
