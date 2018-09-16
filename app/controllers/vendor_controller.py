from app.controllers.base_controller import BaseController
from app.repositories.vendor_repo import VendorRepo
from datetime import datetime
from app.repositories.vendor_engagement_repo import VendorEngagementRepo

class VendorController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.vendor_repo = VendorRepo()
		self.vendor_engagement_repo = VendorEngagementRepo()
		
	''' VENDOR'''
	def list_vendors(self):
		vendors = self.vendor_repo.fetch_all()
		vendors_list = [vendor.serialize() for vendor in vendors.items]
		return self.handle_response('OK', payload={'vendors': vendors_list, 'meta': self.pagination_meta(vendors)})
	
	def get_vendor(self, vendor_id):
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			vendor = vendor.serialize()
			return self.handle_response('OK', payload={'vendor': vendor})
		else:
			return self.handle_response('Bad Request - Invalid or Missing vendor_id', status_code=400)
	
	def create_vendor(self):
		name, tel, address, contact_person = self.request_params('name', 'tel', 'address', 'contact_person')
		vendor = self.vendor_repo.new_vendor(name, address, tel, contact_person).serialize()
		return self.handle_response('OK', payload={'vendor': vendor})
	
	def update_vendor(self, vendor_id):
		name, tel, address, contact_person = self.request_params('name', 'tel', 'address', 'contact_person')
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			updates = {}
			if name:
				updates['name'] = name
			if tel:
				updates['tel'] = tel
			if address:
				updates['address'] = address
			if contact_person:
				updates['contact_person'] = contact_person
				
			self.vendor_repo.update(vendor, **updates)
			return self.handle_response('OK', payload={'vendor': vendor.serialize()})
		
		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)
	
	def delete_vendor(self, vendor_id):
		pass
	
	''' VENDOR ENGAGEMENT'''
	def list_vendor_engagements(self):
		engagements = self.vendor_engagement_repo.fetch_all()
		
		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)
			
		return self.handle_response('OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)})
	
	def get_vendor_engagement(self, engagement_id):
		engagement = self.vendor_engagement_repo.get(engagement_id)
		if engagement:
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()
			
			return self.handle_response('OK', payload={'engagement': e})
		else:
			return self.handle_response('Bad Request', status_code=400)
	
	def create_vendor_engagement(self):
		vendor_id, start_date, end_date = self.request_params('vendor_id', 'start_date', 'end_date')
		
		if self.vendor_repo.get(vendor_id):
			
			start_date = datetime.strptime(start_date, '%Y-%m-%d')
			end_date = datetime.strptime(end_date, '%Y-%m-%d')
			engagement = self.vendor_engagement_repo.new_vendor_engagement(vendor_id, start_date, end_date)
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()
			
			return self.handle_response('OK', payload={'engagement': e})
		
		return self.handle_response('Invalid vendor_id provided', status_code=400)
		
	def update_vendor_engagement(self, engagement_id):
		vendor_id, start_date, end_date, status, termination_reason = self.request_params('vendor_id', 'start_date', 'end_date', 'status', 'termination_reason')
		engagement = self.vendor_engagement_repo.get(engagement_id)
		print(self.request_params('vendor_id', 'start_date', 'end_date', 'status', 'termination_reason'))
		
		if engagement:
			updates = {'vendor_id': vendor_id}
			if start_date:
				updates['start_date'] = start_date
			if end_date:
				updates['end_date'] = end_date
			if status is not None:
				updates['status'] = status
				print(status, updates)
			if termination_reason:
				updates['termination_reason'] = termination_reason
				
			self.vendor_engagement_repo.update(engagement, **updates)
			return self.handle_response('OK', payload={'vendor': engagement.serialize()})
		
		return self.handle_response('Invalid or incorrect engagement_id provided', status_code=400)
		
		pass
	
	def delete_vendor_engagement(self, vendor_id):
		pass
		
	''' VENDOR RATING'''
	