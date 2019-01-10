from app.repositories.base_repo import BaseRepo
from app.models.activity import Activity


class ActivityRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, Activity)

	def new_activity(self, module_name, ip_address, user_id, action_type, action_details,
					 channel):
		activity = Activity(
			module_name=module_name, ip_address=ip_address, user_id=user_id, action_type=action_type,
			action_details=action_details, channel=channel
		)
		activity.save()
		return activity

	def get_range_action_paginated_options(self, action_type, start_date, end_date):
		return Activity.query.filter(
			Activity.action_type == action_type,
			Activity.created_at >= start_date, Activity.created_add <= end_date
		).order_by(Activity.created_at.desc()).paginate(error_out=False)

	def get_range_paginated_options(self, start_date, end_date):
		return Activity.query.filter(
			Activity.created_at >= start_date, Activity.created_add <= end_date
		).order_by(Activity.created_at.desc()).paginate(error_out=False)
