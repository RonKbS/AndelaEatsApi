from factories import role_factory
from factories.role_factory import RoleFactory
from factories.user_role_factory import UserRoleFactory


class BaseTestUtils():
    user_id = None

    def __init__(self, user_id=None):
        self.user_id = user_id

    def create_admin(self):
        role = RoleFactory.create(name='admin')
        user_id = self.user_id()
        UserRoleFactory.create(user_id=user_id, role=role)
        return role
