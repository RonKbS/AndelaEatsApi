from app.repositories.permission_repo import PermissionRepo
from app.repositories.role_repo import RoleRepo
from app.repositories.user_role_repo import UserRoleRepo
from datetime import datetime
from app.utils import db
from app.models.permission import Permission
from app.models.role import Role
from app.models.user_role import UserRole
from sqlalchemy.exc import SQLAlchemyError


role_data = [{'id': '1', 'name': 'Administrator'}, {'id': '2', 'name': 'user'}]

user_role_data = [{'role_id': '1', 'user_id': 'eno.bassey@andela.com'},
            {'role_id': '1', 'user_id': 'ebuka.umeh@andela.com'},
            {'role_id': '1', 'user_id': 'nnamso.edemenang@gmail.com'},
            {'role_id': '1', 'user_id': 'victor.adukwu@andela.com'},
            {'role_id': '1', 'user_id': 'chibueze.ayogu@andela.com'},
            {'role_id': '1', 'user_id': 'kayode.adeola@andela.com'},
            {'role_id': '1', 'user_id': 'joseph.cobhams@andela.com'},
            {'role_id': '1', 'user_id': 'abdulfatai.aka@andela.com'}]

permission_data = [{'name': 'delete_menu', 'role_id': '1', 'keyword': 'delete'},
            {'name': 'create_menu', 'role_id': '1', 'keyword': 'create'},
            {'name': 'update_menu', 'role_id': '1', 'keyword': 'update'},
            {'name': 'read_menu', 'role_id': '1', 'keyword': 'read'},
            {'name': 'delete_meal_item', 'role_id': '1', 'keyword': 'delete'},
            {'name': 'create_meal_item', 'role_id': '1', 'keyword': 'create'},
            {'name': 'update_meal_item', 'role_id': '1', 'keyword': 'update'},
            {'name': 'read_meal_item', 'role_id': '1', 'keyword': 'read'},
            {'name': 'delete_vendor', 'role_id': '1', 'keyword': 'delete'},
            {'name': 'create_vendor', 'role_id': '1', 'keyword': 'create'},
            {'name': 'update_vendor', 'role_id': '1', 'keyword': 'update'},
            {'name': 'read_vendor', 'role_id': '1', 'keyword': 'read'},
            {'name': 'delete_vendor_engagement', 'role_id': '1', 'keyword': 'delete'},
            {'name': 'create_vendor_engagement', 'role_id': '1', 'keyword': 'create'},
            {'name': 'update_vendor_engagement', 'role_id': '1', 'keyword': 'update'},
            {'name': 'read_vendor_engagement', 'role_id': '1', 'keyword': 'read'}]

models = [Role, UserRole, Permission]

model_data = [role_data, user_role_data, permission_data]


def map_model_data():
    """it maps models and model_data"""
    model_data_map = []
    for index in range(0, len(models)):
        model_data_map.append({"model": models[index], 'data': model_data[index]})
    return model_data_map


def seed_db():
    errors = []
    mapped_model_data = map_model_data()
    for model_data in mapped_model_data:
        try:
            db.session.bulk_insert_mappings(
                model_data['model'], model_data['data'])
            db.session.commit()
        except SQLAlchemyError as error:
            errors.append({model_data['model'].__tablename__: error})
            db.session.rollback()
