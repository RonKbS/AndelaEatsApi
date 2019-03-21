from app.repositories.base_repo import BaseRepo
from app.models.user import User


class UserRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, User)

    def new_user(self, *args):
        """
        function for creating a new user

        :parameter
            args: a list containing the following positional values
                  [slack_id, first_name, last_name, email, user_role_id, photo]

        """
        slack_id, first_name, last_name, email, user_role_id, *image_url = args

        image_url = image_url[0] if image_url else None

        user = User(slack_id=slack_id, first_name=first_name, last_name=last_name, email=email,
                    user_role_id=user_role_id, image_url=image_url)
        user.save()
        return user
