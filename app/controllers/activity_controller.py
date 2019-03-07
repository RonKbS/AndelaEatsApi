from app.controllers.base_controller import BaseController
from app.repositories.activity_repo import ActivityRepo
from app.utils.enums import ActionType, Channels


class ActivityController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.activity_repo = ActivityRepo()

    def list_by_date_range(self):
        dates = self.request.args['date_range'].split(":")

        start_date, end_date = dates[0], dates[1]

        activities = self.activity_repo.get_range_paginated_options(
            start_date=start_date, end_date=end_date
        )

        return self.handle_response(
            'OK',
            payload={
                'activities': self.return_transformed_enum_items(('actionType', 'channel'), activities.items)
            }
        )

    def list_by_action_type_and_date_range(self,):
        action_type = self.request.args['action_type']
        dates = self.request.args['date_range'].split(":")
        start_date, end_date = dates[0], dates[1]

        import pdb;pdb.set_trace()

        activities = self.activity_repo.get_range_action_paginated_options(
            action_type=action_type, start_date=start_date, end_date=end_date
        )

        return self.handle_response(
            'OK',
            payload={
                'activities': self.return_transformed_enum_items(('actionType', 'channel'), activities.items)
            }
        )
