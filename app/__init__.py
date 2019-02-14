from flask_api import FlaskAPI
from flask_cors import CORS
from config import env, get_env
from app.utils import db #, timedelta
from app.blueprints.base_blueprint import BaseBlueprint
from app.utils.auth import Auth
from flasgger import Swagger
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.cron import Cron

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(env.app_env[config_name])
    app.config.from_pyfile('../config/env.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CORS
    CORS(app)

    # Blueprints
    blueprint = BaseBlueprint(app)
    blueprint.register()

    cron = Cron(app)
    scheduler = BackgroundScheduler()
    # in your case you could change seconds to hours
    scheduler.add_job(cron.run_24_hourly, trigger='interval', hours=24)
    scheduler.start()

    from . import models
    db.init_app(app)
    swg = Swagger(app)

    return app
