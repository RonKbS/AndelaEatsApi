'''A controller module for vendor-related
'''
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.vendor_repo import VendorRepo
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.repositories.vendor_rating_repo import VendorRatingRepo
from app.utils.auth import Auth


class VendorController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.vendor_repo = VendorRepo()
		self.vendor_engagement_repo = VendorEngagementRepo()
		self.vendor_rating_repo = VendorRatingRepo()

	def list_vendors(self):
		location = Auth.get_location()
		vendors = self.vendor_repo.filter_by(is_deleted=False, is_active=True, location_id=location)
		vendors_list = [vendor.serialize() for vendor in vendors.items]
		return self.handle_response('OK', payload={'vendors': vendors_list, 'meta': self.pagination_meta(vendors)})

	def list_deleted_vendors(self):
		location = Auth.get_location()
		vendors = self.vendor_repo.filter_by(is_deleted=True, location_id=location)
		vendors_list = [vendor.serialize() for vendor in vendors.items]
		return self.handle_response('OK', payload={'vendors': vendors_list, 'meta': self.pagination_meta(vendors)})

	def list_suspended_vendors(self):
		location = Auth.get_location()
		vendors = self.vendor_repo.filter_by(is_deleted=False, is_active=False, location_id=location)
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
		location = Auth.get_location()
		name, tel, address, is_active, contact_person = self.request_params(
			'name', 'tel', 'address', 'isActive', 'contactPerson')

		vendor = self.vendor_repo.new_vendor(name, address, tel, is_active, contact_person, location).serialize()
		return self.handle_response('OK', payload={'vendor': vendor}, status_code=201)

	def update_vendor(self, vendor_id):
		name, tel, address, is_active, contact_person = self.request_params(
			'name', 'tel', 'address', 'isActive', 'contactPerson')
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			updates = {}
			if name:
				updates['name'] = name
			if tel:
				updates['tel'] = tel
			if address:
				updates['address'] = address
			if is_active:
				updates['is_active'] = is_active
			if contact_person:
				updates['contact_person'] = contact_person

			self.vendor_repo.update(vendor, **updates)
			return self.handle_response('OK', payload={'vendor': vendor.serialize()})

		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)

	def suspend_vendor(self, vendor_id):
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			updates = {}
			updates['is_active'] = 0
			self.vendor_repo.update(vendor, **updates)
			return self.handle_response('OK', payload={'vendor': vendor.serialize()})
		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)
	
	def un_suspend_vendor(self, vendor_id):
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			updates = {}
			updates['is_active'] = 1
			self.vendor_repo.update(vendor, **updates)
			return self.handle_response('OK', payload={'vendor': vendor.serialize()})
		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)

	def delete_vendor(self, vendor_id):
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			if vendor.is_deleted:
				return self.handle_response('Vendor has already been deleted', status_code=400)

			if any(not dependent.is_deleted for dependent in(vendor.engagements or vendor.ratings)):
				return self.handle_response('Vendor cannot be deleted because it has a child object', status_code=400)
			updates = {}
			updates['is_deleted'] = True

			self.vendor_repo.update(vendor, **updates)

			engagements = self.vendor_engagement_repo.filter_by(vendor_id=vendor_id)
			for e in engagements.items:
				updates_engagement = {}
				updates_engagement['is_deleted'] = True

				self.vendor_engagement_repo.update(e, **updates_engagement)
			return self.handle_response('Vendor deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)
