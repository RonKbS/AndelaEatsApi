from app.controllers.base_controller import BaseController
from app.repositories import UserRoleRepo, RoleRepo
from app.models import Role
from app.services.andela import AndelaService


class UserController(BaseController):
    '''
    User Controller.
    '''

    def __init__(self, request):
        '''
        Constructor.

        Parameters:
        -----------
            request 
        '''

        BaseController.__init__(self, request)
        self.user_role_repo = UserRoleRepo()
        self.role_repo = RoleRepo()
        self.andela_service = AndelaService()

    def list_admin_users(self, admin_role_id: int = 1) -> list:
        '''
        List admin users.

        Parameters:
        -----------
        admin_role_id {int}
            Admin role ID (default: {1}).

        Returns:
        --------
        list
            List of admin users' profiles.
        '''

        user_roles = self.user_role_repo.filter_by(
            role_id=admin_role_id,
            is_active=True
        ).items

        admin_users_list = []
        for user_role in user_roles:
            admin_user_profile = {}
            andela_user_profile = self.andela_service.get_user_by_email_or_id(
                user_role.user_id
            )
            associated_roles = [user_role.role_id for user_role in self.user_role_repo.filter_by(user_id=user_role.user_id).items]
            role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
            roles = [{'id': role.id, 'name': role.name} for role in role_objects]
            admin_user_profile['Email'] = andela_user_profile['email']
            admin_user_profile['Name'] = andela_user_profile['name']
            admin_user_profile['Id'] = andela_user_profile['id']
            admin_user_profile['Roles'] = roles

            admin_users_list.append(admin_user_profile)

        return self.handle_response(
            'OK',
            payload={'AdminUsers': admin_users_list}
        )
