from tests.base_test_case import BaseTestCase

from factories import RoleFactory, UserRoleFactory, PermissionFactory

def create_user_role(keyword):
    role = RoleFactory.create()
    user_id = BaseTestCase.user_id()
    PermissionFactory.create(keyword=keyword, role_id=role.id)
    return UserRoleFactory.create(user_id=user_id, role_id=role.id), user_id