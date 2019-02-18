from app.utils import db
from app.models import Location, Role, UserRole, Permission
from sqlalchemy.exc import SQLAlchemyError
from .seed_data import location_data, role_data, user_role_data, permission_data
from collections import OrderedDict
from termcolor import colored


SEED_OPTIONS = ('location', 'role', 'user_role', 'permission')

model_mapper = OrderedDict({
    'location': {'model': Location, 'data': location_data},
    'role': {'model': Role, 'data': role_data},
    'user_role': {'model': UserRole, 'data': user_role_data},
    'permission': {'model': Permission, 'data': permission_data}
})


def bulk_insert(model, data):
    try:
        db.session.bulk_insert_mappings(model, data)
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(colored(error, 'red'))


def seed_db(table_name):

    if not table_name:
        for _, model in model_mapper.items():
            bulk_insert(**model)
        return

    return bulk_insert(**model_mapper.get(table_name))
