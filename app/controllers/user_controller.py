from app.controllers.base_controller import BaseController
from app.repositories import UserRoleRepo, RoleRepo, UserRepo
from app.models import Role, User
from app.services.andela import AndelaService
from app.utils.auth import Auth
from app.utils.id_generator import PushID


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
        self.user_repo = UserRepo()

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

        user_roles = self.user_role_repo.filter_by(role_id=admin_role_id, is_active=True).items

        admin_users_list = []
        for user_role in user_roles:
            admin_user_profile = {}
            andela_user_profile = self.andela_service.get_user_by_email_or_id(user_role.user_id) or \
                                  self.andela_service.get_user_by_email_or_id(user_role.email)

            if andela_user_profile:
                associated_roles = [user_role.role_id for user_role in
                                    self.user_role_repo.filter_by(user_id=user_role.user_id).items]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [{'role_id': role.id, 'role_name': role.name} for role in role_objects]
                admin_user_profile['email'] = andela_user_profile['email']
                admin_user_profile['name'] = andela_user_profile['name']
                admin_user_profile['id'] = andela_user_profile['id']
                admin_user_profile['roles'] = roles

                admin_users_list.append(admin_user_profile)

        return self.handle_response(
            'OK',
            payload={'adminUsers': admin_users_list}
        )

    def list_all_users(self):

        params = self.get_params_dict()
        pg = int(params.get('page', 1))
        pp = int(params.get('per_page', 10))

        users = self.user_repo.paginate(error_out=False, page=pg, per_page=pp)
        if users.items:
            user_list = [user.serialize() for user in users.items]
            for user in user_list:
                associated_roles = [user_role.role_id for user_role in
                                    self.user_role_repo.filter_by(user_id=user['userId']).items]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [{'id': role.id, 'name': role.name} for role in role_objects]
                user['userRoles'] = roles
            return self.handle_response('OK', payload={'users': user_list, 'meta': self.pagination_meta(users)})
        return self.handle_response('No users found', status_code=404)

    def delete_user(self, id):
        user = self.user_repo.get(id)
        if user:
            if user.is_deleted:
                return self.handle_response('User has already been deleted', status_code=400)

            updates = {}
            updates['is_deleted'] = True

            self.user_repo.update(user, **updates)

            return self.handle_response('User deleted', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect id provided', status_code=404)

    def create_user(self):
        push_id = PushID()
        next_id = push_id.next_id()

        user_info = self.request_params('firstName', 'lastName', 'imageUrl', 'slackId', 'userId', 'userTypeId')

        first_name, last_name, image_url, slack_id, user_id, role_id = user_info

        role = self.role_repo.find_first(id=role_id)

        if not role:
            return self.handle_response(
                f"Role with userTypeId(roleId) {role_id} does not exist",
                status_code=400
            )

        if self.user_repo.exists(slack_id=slack_id):
            return self.handle_response(
                f"User with slackId '{slack_id}' already exists",
                status_code=400
            )

        if self.user_repo.exists(user_id=user_id) and user_id is not None:
            return self.handle_response(
                f"User with userId '{user_id}' already exists",
                status_code=400
            )

        slack_id = slack_id if slack_id else next_id
        user_id = user_id if user_id else slack_id

        user_type = self.user_role_repo.find_first(user_id=user_id) or \
                    self.user_role_repo.new_user_role(
                        role_id=role_id, user_id=user_id, location_id=Auth.get_location(),email=None)

        user = self.user_repo.new_user(*user_info, user_id=user_id, slack_id=slack_id, user_type=user_type).serialize()

        user.__setitem__('userType', role.to_dict(only=['id', 'name', 'help', "timestamps"]))
        user.pop('userTypeId')

        return self.handle_response('OK', payload={'user': user}, status_code=201)

    def list_user(self, slack_id):

        user = self.user_repo.find_first(slack_id=slack_id)

        if user:
            return self.handle_response('OK', payload={'user': user.serialize()}, status_code=200)

        return self.handle_response('User not found', status_code=404)

    def update_user(self, user_id):
        user = self.user_repo.get(user_id)

        if not user:
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'User not found'}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'User already deleted'}, status_code=400
            )

        user_info = self.request_params_dict('slackId', 'firstName', 'lastName', 'userId', 'imageUrl')

        slack_id = user_info.get('slack_id')
        user_id_sent = user_info.get('user_id')

        if slack_id and self.user_repo.check_exists_else_where(User, 'slack_id', slack_id, 'id', user_id):
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'Cannot update to the slack id of another existing user'},
                status_code=403
            )

        if user_id_sent and self.user_repo.check_exists_else_where(User, 'user_id', user_id_sent, 'id', user_id):
            return self.handle_response(
                msg="FAIL",
                payload={'user': 'Cannot update to the user id of another existing user'},
                status_code=403
            )

        user = self.user_repo.update(user, **user_info)

        return self.handle_response('OK', payload={'user': user.serialize()}, status_code=200)
