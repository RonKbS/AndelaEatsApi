from app.controllers.base_controller import BaseController
from app.repositories.user_role_repo import UserRoleRepo
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
        admin_user_profile = {}
        for user_role in user_roles:
            andela_user_profile = self.andela_service.get_user_by_email_or_id(
                user_role.user_id
            )
            admin_user_profile['Email'] = andela_user_profile['email']
            admin_user_profile['Name'] = andela_user_profile['name']
            admin_user_profile['Id'] = andela_user_profile['id']

            admin_users_list.append(admin_user_profile)

        return self.handle_response(
            'OK',
            payload={'AdminUsers': admin_users_list}
        )
