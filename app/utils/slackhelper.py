from slack import WebClient

from config import get_env


class SlackHelper:

    def __init__(self):
        self.token = get_env('SLACK_TOKEN')
        self.client = WebClient(self.token)

    def post_message(self, message, channel, attachments=None, as_user=True):
        """
        Post a message to a public channel, private channel,
        or direct message/IM channel.

        https://api.slack.com/methods/chat.postMessage
        """
        return self.client.chat_postMessage(
            channel=channel,
            text=message,
            attachments=attachments,
            as_user=as_user
        )

    def update_message(self, message, channel, ts, attachments=None):
        """
        Update a message in a channel.

        https://api.slack.com/methods/chat.update
        """
        return self.client.chat_update(
            channel=channel,
            ts=ts,
            text=message,
            attachments=attachments
        )

    def user_info(self, user):
        """
        Get information about a member of a workspace.

        https://api.slack.com/methods/users.info
        """
        return self.client.users_info(
            user=user
        )

    def dialog(self, dialog, trigger_id):
        """Open a dialog with a user by exchanging a trigger_id.

        https://api.slack.com/methods/dialog.open
        """
        return self.client.dialog_open(
            dialog=dialog,
            trigger_id=trigger_id
        )

    def find_by_email(self, email):
        """
        Retrieve a single user by looking them up by their email address.

        https://api.slack.com/methods/users.lookupByEmail
        """
        return self.client.users_lookupByEmail(
            email=email
        )
