from app.repositories.base_repo import BaseRepo
from app.models.vendor_engagement import VendorEngagement


class VendorEngagementRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, VendorEngagement)
	
	def new_vendor_engagement(self, vendor_id, start_date, end_date=None, status=1, termination_reason=None):
		vendor_engagement = VendorEngagement(vendor_id=vendor_id, start_date=start_date, end_date=end_date, status=status, termination_reason=termination_reason)
		vendor_engagement.save()
		return vendor_engagement