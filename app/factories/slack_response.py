from app.utils import daterange


def _error_page() -> dict:
    """
    Slack error page.

    Returns:
        Slack error response page.
    """
    return {'text': 'Oops - Something is not right.'}



class SlackResponsePage:
    """Concrete slack response page for the factory."""

    _locations = []

    def slack_response(self, **kwargs) -> dict:
        pass

    def build_page(self, **kwargs) -> dict:
        """
        Builds slack response page as a dictionary.

        Args:
            **kwargs (): data used to build the slack response page.

        Returns:
            dict: Slack response page as a dictionary.
        """
        return self.slack_response(**kwargs)


class Landing(SlackResponsePage):
    """Landing page factory."""

    def slack_response(self, **kwargs) -> dict:
        """
        Build the slack response for the landing page.

        Args:
            **kwargs (): locations must be supplied among the kwargs.

        Returns:
            slack response landing page as a dict.
        """

        self._locations = kwargs.get('locations', None)
        if not self._locations:
            raise ValueError('No centers have been setup.')
        locations = kwargs['locations']

        return {
            'text': f'Welcome To Andela Eats',
            'attachments': [{
                'text': '',
                'callback_id': 'center_selector',
                'color': '#3AA3E3',
                'attachment_type': 'default',
                'actions': [
                    {'name': 'location',
                     'text': f'{location.name}',
                     'type': 'button',
                     'value': location.id} for location in locations.items]}]}


class CenterSelection(SlackResponsePage):
    """Center selection page factory"""

    def slack_response(self, **kwargs) -> dict:
        """
        Builds the response page display by slack bot to all user to select
        a center.

        Args:
            kwargs ():

        Returns:
            Slack response page as a dict.
        """
        location = kwargs.get('location', None)
        menu_start_end_on = kwargs.get('menu_period', None)

        if not location or not menu_start_end_on:
            raise ValueError('Location and menu start and end date required.')

        start_on = menu_start_end_on[0]
        end_on = menu_start_end_on[1]

        date_buttons = [{
            'name': 'selected_date', 'type': 'button',
            'text': '{}, {}'.format(day.strftime('%a'),
                                    day.strftime('%b %-d')),
            'value': '{}_{}'.format(day.strftime('%Y-%m-%d'),
                                    location.id)
        } for day in daterange(start_on, end_on)]

        request_buttons = [
            {
                "text": "",
                "callback_id": "day_selector",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": date_buttons
            }
        ]

        return {
            'text': f'Select Date',
            'attachments': request_buttons
        }


class DaySelection(SlackResponsePage):
    """
    Day selection slack page factory.
    """

    def slack_response(self, **kwargs) -> dict:
        """
        Builds the response page display by slack bot to all user to select
        a day.

        Args:
            kwargs (dict): Data required for building response page.
            Data required to be included is:
                    - 'day_meal_sessions'
                    - 'payload_action_value'.

        Returns:
            Slack response page as a dict.
        """
        day_meal_sessions = ['lunch', 'breakfast']
        payload_action_value = kwargs.get('payload', None)
        if not payload_action_value:
            return _error_page()

        period_buttons = [{
            'name': 'meal_period',
            'type': 'button',
            'text': f'{meal_session.capitalize()}',
            'value': f'{meal_session}_{payload_action_value}'}
            for meal_session in day_meal_sessions]

        request_buttons = [
            {
                "text": "",
                "callback_id": "period_selector",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": period_buttons
            }
        ]

        return {
            'text': f'Select Meal Period',
            'attachments': request_buttons
        }


class PeriodSelection(SlackResponsePage):
    """
    Period selection slack response page builder.
    """

    def slack_response(self, **kwargs) -> dict:
        """
        Builds the response page display by slack bot to all user to select
        a period.

        Args:
            kwargs (dict): Data required for building response page.
            Data required to be included is:
                    - 'day_meal_sessions'
                    - 'payload_action_value'.

        Returns:
            Slack response page as a dict.
        """
        payload = kwargs.get('payload', None)
        if not payload:
            return _error_page()

        period = payload['actions'][0]['value'].split('_')[0]
        date = payload['actions'][0]['value'].split('_')[1]
        location_id = payload['actions'][0]['value'].split('_')[2]
        actions = {
            "attachments": [
                {
                    "text": 'What do you want to do?',
                    "callback_id": "action_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "main meal",
                            "text": "View Menu List",
                            "type": "button",
                            "value": f'{period}_{date}_menu_{location_id}'
                        },
                        {
                            "name": "main meal",
                            "text": "Place order",
                            "type": "button",
                            "value": f'{period}_{date}_order_{location_id}'
                        }
                    ]
                }
            ]
        }

        return actions


class ActionSelection(SlackResponsePage):
    """
    Action selection slack response builder.
    """

    def slack_response(self, **kwargs) -> dict:
        """
        Builds the response page display by slack bot to all user to select
        a period.

        Args:
            kwargs (dict): Data required for building response page.
            Data required to be included is:
                    - 'day_meal_sessions'
                    - 'payload_action_value'.

        Returns:
            Slack response page as a dict.
        """
        pass


class SlackResponseFactory:
    """Factory that creates slack response pages."""

    @staticmethod
    def create_response(slack_response_page: str) -> SlackResponsePage:
        """Creates the response page"""
        if slack_response_page:
            page_split = slack_response_page.split('_')
            target_class = ''.join([part.capitalize() for part in page_split])
            if target_class in globals():
                return globals()[target_class]()
            raise ValueError('Slack response page is not valid.')
        raise ValueError('Slack response page to create is required.')
