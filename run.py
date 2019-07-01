from app.utils import db
from config import get_env
from app import create_app
from flask import jsonify, make_response
from flask_script import Manager
from app.utils.auth import Auth
from app.utils.handled_exceptions import BaseModelValidationError
from app.utils.seeders.seed_database import seed_db, SEED_OPTIONS
from flask_migrate import Migrate, MigrateCommand
from werkzeug.exceptions import HTTPException
import traceback
import logging
import click
import bugsnag
import rollbar
from termcolor import colored

error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(name)s:%(message)s'))

error_logger.addHandler(file_handler)

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

# Migrations
manager.add_command('db', MigrateCommand)


@app.before_request
def check_token():
    return Auth.check_token()


@app.before_request
def check_location_header():
    return Auth.check_location_header()


@app.errorhandler(BaseModelValidationError)
def handle_base_model_validation_error(error):
    return make_response(
        jsonify({'msg': error.msg})
    ), error.status_code


@app.errorhandler(Exception)
def handle_exception(error):
    """Error handler called when a ValidationError is raised"""

    response = {
        'msg': 'An error occurred while processing your request. Please contact Admin.'}

    if isinstance(error, HTTPException):
        return make_response(
            jsonify({'msg': error.description})
        ), error.code

    traceback.print_exc()
    error_logger.exception(str(error))
    bugsnag.notify(error)

    if get_env('APP_ENV') in ['staging', 'production']:
        rollbar.report_exc_info()

    return make_response(jsonify(response)), 500


# Creates the db tables
@manager.command
def create_db():
    db.create_all()

# Drops the db tables


@manager.command
def drop_db():
    db.drop_all()


# seeds database
@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
@click.argument('table_name', required=False)
@click.option(
    '--table_name',
    help='The Resource name you want to seed.',
    type=click.Choice(SEED_OPTIONS)
)
@click.option('--testing', is_flag=True)
def seed_database(table_name=None, testing=False):
    seed_db(table_name, testing)

# generate test token
@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
def generate_test_token():
    from tests.base_test_case import BaseTestCase
    print(colored('TOKEN:', 'red'), colored(BaseTestCase.generate_token(), 'green'))


@manager.command
def show_routes():
    from termcolor import colored

    count = 0
    for rule in app.url_map.iter_rules():
        methods = [m for m in rule.methods if m in [
            'GET', 'POST', 'PUT', 'PATCH', 'DELETE']]
        line = 'Method: {method} | Route: {route} | Controller Endpoint: {endpoint}'.format(
            method=methods[0], route=rule, endpoint=rule.endpoint)

        if 'GET' in methods:
            print(colored(line, 'green'), end='\n\n')

        if 'POST' in methods:
            print(colored(line, 'yellow'), end='\n\n')

        if 'PUT' in methods or 'PATCH' in methods:
            print(colored(line, 'grey'), end='\n\n')

        if 'DELETE' in methods:
            print(colored(line, 'red'), end='\n\n')

        count += 1
    print(count, 'Routes Found')


if __name__ == '__main__':
    manager.run()
