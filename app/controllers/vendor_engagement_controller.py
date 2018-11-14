'''A controller module for vendor-related
'''
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.vendor_repo import VendorRepo
from app.repositories.vendor_engagement_repo import VendorEngagementRepo

class VendorEngagementController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.vendor_engagement_repo = VendorEngagementRepo()
		self.vendor_repo = VendorRepo()

	def list_vendor_engagements(self):
		engagements = self.vendor_engagement_repo.fetch_all()

		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)

		return self.handle_response(
			'OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)}
		)

	def upcoming_vendor_engagements(self):
		engagements = self.vendor_engagement_repo.get_engagement_by_date()

		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)

		return self.handle_response(
			'OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)}
		)

	def get_vendor_engagement(self, engagement_id):
		engagement = self.vendor_engagement_repo.get(engagement_id)
		if engagement:
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()

			return self.handle_response('OK', payload={'engagement': e})
		else:
			return self.handle_response('Bad Request', status_code=400)

	def create_vendor_engagement(self):
		vendor_id, start_date, end_date, status = self.request_params('vendorId', 'startDate', 'endDate', 'status')

		if self.vendor_repo.get(vendor_id):

			start_date = datetime.strptime(start_date, '%Y-%m-%d')
			end_date = datetime.strptime(end_date, '%Y-%m-%d')
			engagement = self.vendor_engagement_repo.new_vendor_engagement(vendor_id, start_date, end_date, status)
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()

			return self.handle_response('OK', payload={'engagement': e})

		return self.handle_response('Invalid vendor_id provided', status_code=400)

	def update_vendor_engagement(self, engagement_id):
		vendor_id, start_date, end_date, status,\
			termination_reason = self.request_params('vendorId', 'startDate', 'endDate', 'status', 'terminationReason')
		engagement = self.vendor_engagement_repo.get(engagement_id)

		if start_date:
			start_date = datetime.strptime(start_date, '%Y-%m-%d')

		if end_date:
			end_date = datetime.strptime(end_date, '%Y-%m-%d')

		if engagement:
			updates = {'vendor_id': vendor_id}
			if start_date:
				updates['start_date'] = start_date
			if end_date:
				updates['end_date'] = end_date
			if status is not None:
				updates['status'] = status
			if termination_reason:
				updates['termination_reason'] = termination_reason

			self.vendor_engagement_repo.update(engagement, **updates)
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()
			return self.handle_response('OK', payload={'engagement': e})

		return self.handle_response('Invalid or incorrect engagement_id provided', status_code=400)

	def delete_engagement(self, engagement_id):
		engagement = self.vendor_engagement_repo.get(engagement_id)
		if engagement:
			if engagement.is_deleted:
				return self.handle_response('This engagement has already been deleted', status_code=400)

			if any(not dependent.is_deleted for dependent in engagement.menus):
				return self.handle_response(
					'This engagement cannot be deleted because it has a child object', status_code=400
				)
			updates = {}
			updates['is_deleted'] = True

			self.vendor_engagement_repo.update(engagement, **updates)
			return self.handle_response('Engagement deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect engagement_id provided', status_code=400)
