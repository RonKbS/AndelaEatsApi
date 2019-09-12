"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template
from flask_marshmallow import Marshmallow

from andelaeats import commands, location, meal, order, rating, user, vendor
from andelaeats.extensions import (  # noqa
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    migrate,
)
from andelaeats.utils.auth import Auth
from andelaeats.utils.error_handlers import handle_exception
from andelaeats.utils.handled_errors import BaseModelValidationError
from andelaeats.utils.validators import json_validator


def create_app(config_object="andelaeats.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_before_register(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    # bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)
    # login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)

    ma = Marshmallow(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(location.views.blueprint)
    app.register_blueprint(rating.views.blueprint)
    app.register_blueprint(meal.views.blueprint)
    app.register_blueprint(vendor.views.blueprint)
    app.register_blueprint(order.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(BaseModelValidationError, handle_exception)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_before_register(app):
    app.before_request(Auth.check_token)
    app.before_request(Auth.check_location_header)
    app.before_request(json_validator)
