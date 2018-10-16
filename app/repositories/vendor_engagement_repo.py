from app.repositories.base_repo import BaseRepo
from app.models.vendor_engagement import VendorEngagement
from datetime import datetime

class VendorEngagementRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, VendorEngagement)
	
	def new_vendor_engagement(self, vendor_id, start_date, end_date=None, status=1, termination_reason=None):
		vendor_engagement = VendorEngagement(vendor_id=vendor_id, start_date=start_date, end_date=end_date, status=status, termination_reason=termination_reason)
		vendor_engagement.save()
		return vendor_engagement

	def get_engagement_by_date(self):
		return VendorEngagement.query.filter(VendorEngagement.start_date >= datetime.now().date()).paginate(error_out=False)