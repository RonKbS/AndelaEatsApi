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
                  [slack_id, first_name, last_name, email, user_id, photo]

        """
        slack_id, first_name, last_name, user_id, image_url = args

        user = User(slack_id=slack_id, first_name=first_name, last_name=last_name,
                    image_url=image_url, user_id=user_id)
        user.save()
        return user
