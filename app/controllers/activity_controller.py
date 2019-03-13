from app.controllers.base_controller import BaseController
from app.repositories.activity_repo import ActivityRepo
from app.utils.enums import ActionType, Channels


class ActivityController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.activity_repo = ActivityRepo()

    def list_by_date_range(self):
        date_ranges = self.get_params('date_range')[0].split(":")

        activities = self.activity_repo.get_range_paginated_options(
            start_date=date_ranges[0], end_date=date_ranges[1]
        )

        return self.handle_response(
            'OK',
            payload={
                'activities': self.return_transformed_enum_items(('actionType', 'channel'), activities.items)
            }
        )

    def list_by_action_type_and_date_range(self):

        query_params = self.get_params_dict()

        date_ranges = query_params.get('date_range').split(":")
        action_type = query_params.get('action_type')

        activities = self.activity_repo.get_range_action_paginated_options(
            action_type=action_type, start_date=date_ranges[0], end_date=date_ranges[1]
        )

        return self.handle_response(
            'OK',
            payload={
                'activities': self.return_transformed_enum_items(('actionType', 'channel'), activities.items)
            }
        )
