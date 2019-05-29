'''A controller module for vendor-related
'''
import pdb
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.vendor_repo import VendorRepo
from app.utils.auth import Auth
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.models import VendorEngagement

class VendorEngagementController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.vendor_engagement_repo = VendorEngagementRepo()
		self.vendor_repo = VendorRepo()

	def list_vendor_engagements(self):
		location = Auth.get_location()

		engagements = self.vendor_engagement_repo.filter_by_desc(
			self.vendor_engagement_repo._model.start_date,
			is_deleted=False, location_id=location
		)

		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)

		return self.handle_response(
			'OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)}
		)

	def list_vendor_engagements_by_vendor(self, vendor_id):

		vendor = self.vendor_repo.get(vendor_id)
		if vendor.is_deleted is True:
			return self.handle_response('Invalid Vendor', status_code=400)

		if vendor.is_active is False:
			return self.handle_response('Vendor is disabled', status_code=400)

		engagements = self.vendor_engagement_repo.filter_by(vendor_id=vendor_id)

		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)

		return self.handle_response(
			'OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)}
		)

	def upcoming_vendor_engagements(self):
		location = Auth.get_location()
		engagements = self.vendor_engagement_repo.get_engagement_by_date()

		engagements_list = []
		for e in engagements.items:
			if e.location_id == location:
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
		vendor = self.vendor_repo.get(vendor_id)
		start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
		existing_engagement = self.vendor_engagement_repo.get_existing_engagement(start_date=start_date)
		if existing_engagement > 0:
			return self.handle_response('An engagement already exists for this period. Kindly disable engagement first.', status_code=400)
		if vendor:
			engagement = self.vendor_engagement_repo.new_vendor_engagement(vendor_id, start_date, vendor.location_id, end_date, status)
			print(engagement.id)
			e = engagement.serialize()

			e['vendor'] = engagement.vendor.serialize()
			return self.handle_response('OK', payload={'engagement': e}, status_code=201)

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

	def immediate_past_engagement(self, location_id):
		past_dates = self.vendor_engagement_repo.get_past_engagement_dates(location_id)
		if past_dates:
			latest_date = max(past_dates)

			immediate_past_engagment = VendorEngagement.query.filter_by(end_date=latest_date).first()
			e = immediate_past_engagment.serialize()

			engmnt = {k: v for k, v in e.items() if k in ['startDate', 'endDate', 'vendor']}
			vendor_id = e['vendorId']
			vendor = self.vendor_repo.get(vendor_id).serialize()
			vendor_info = {k: v for k, v in vendor.items() if k in ['id', 'name', 'tel', 'contactPerson']}
			engmnt['vendor'] = vendor_info

			return self.handle_response('OK', payload={'engagement': engmnt})
		else:
			return self.handle_response('No past engagement for this location', status_code=404)

