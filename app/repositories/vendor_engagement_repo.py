from app.repositories.base_repo import BaseRepo
from app.models.vendor_engagement import VendorEngagement
from datetime import datetime
from sqlalchemy import or_, and_

class VendorEngagementRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, VendorEngagement)
	
	def new_vendor_engagement(self, vendor_id, start_date, location_id, end_date=None, status=1, termination_reason=None):
		try:
			vendor_engagement = VendorEngagement(
				vendor_id=vendor_id, start_date=start_date, location_id=location_id, end_date=end_date,
				status=status, termination_reason=termination_reason
			)
			vendor_engagement.save()
			return vendor_engagement
		except Exception as e:
			raise Exception(e)

	def get_engagement_by_date(self):
		return VendorEngagement.query.filter(
			VendorEngagement.start_date >= datetime.now().date(),
			VendorEngagement.is_deleted.is_(False)).paginate(error_out=False)

	def get_existing_engagement(self, start_date):
		return VendorEngagement.query.filter(
			VendorEngagement.end_date >= start_date,
			VendorEngagement.is_deleted.is_(False)
		).count()
