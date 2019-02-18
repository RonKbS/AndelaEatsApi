from app.utils import db
from app.models import Location, Role, UserRole, Permission
from sqlalchemy.exc import SQLAlchemyError
from .seed_data import location_data, role_data, user_role_data, permission_data
from collections import OrderedDict
from termcolor import colored
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


SEED_OPTIONS = ('location', 'role', 'user_role', 'permission')

model_mapper = OrderedDict({
    'location': {'model': Location, 'data': location_data},
    'role': {'model': Role, 'data': role_data},
    'user_role': {'model': UserRole, 'data': user_role_data},
    'permission': {'model': Permission, 'data': permission_data}
})


def check_start_insert_condition(start_insert, table_name, name):

    if not start_insert:
        start_insert = True if table_name == name else False

    return start_insert


def truncate_db(table_name=None):

    stop_truncate = False

    for table in reversed(model_mapper):

        if not stop_truncate:
            try:
                query = 'TRUNCATE table {} CASCADE'.format(model_mapper.get(table).get('model').__tablename__)
                db.engine.execute(text(query))

            except OperationalError:
                query = 'DELETE FROM {}'.format(model_mapper.get(table).get('model').__tablename__)
                db.engine.execute(text(query))

        stop_truncate = check_start_insert_condition(stop_truncate, table_name, table)





def bulk_insert(model, data):
    try:
        db.session.bulk_insert_mappings(model, data)
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(colored(error, 'red'))


def seed_db(table_name):

    start_insert = False if table_name else True

    truncate_db(table_name)

    for name, model in model_mapper.items():

        start_insert = check_start_insert_condition(start_insert, table_name, name)

        if start_insert:
            bulk_insert(**model)
