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

	'''' VENDOR '''
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
		name, tel, address, contact_person = self.request_params('name', 'tel', 'address', 'contactPerson')
		vendor = self.vendor_repo.new_vendor(name, address, tel, contact_person).serialize()
		return self.handle_response('OK', payload={'vendor': vendor})

	def update_vendor(self, vendor_id):
		name, tel, address, contact_person = self.request_params('name', 'tel', 'address', 'contactPerson')
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
		vendor = self.vendor_repo.get(vendor_id)
		if vendor:
			if vendor.is_deleted:
				return self.handle_response('Vendor has already been deleted', status_code=400)

			if any( not dependent.is_deleted for dependent in(vendor.engagements or vendor.ratings)):
				return self.handle_response('Vendor cannot be deleted because it has a child object', status_code=400)
			updates = {}
			updates['is_deleted'] = True

			self.vendor_repo.update(vendor, **updates)
			return self.handle_response('Vendor deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect vendor_id provided', status_code=400)


	''' VENDOR ENGAGEMENT '''
	def list_vendor_engagements(self):
		engagements = self.vendor_engagement_repo.fetch_all()

		engagements_list = []
		for e in engagements.items:
			engagement = e.serialize()
			engagement['vendor'] = e.vendor.serialize()
			engagements_list.append(engagement)

		return self.handle_response('OK', payload={'engagements': engagements_list, 'meta': self.pagination_meta(engagements)})

	def upcoming_vendor_engagements(self):
		engagements = self.vendor_engagement_repo.get_engagement_by_date()

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
		vendor_id, start_date, end_date = self.request_params('vendorId', 'startDate', 'endDate')

		if self.vendor_repo.get(vendor_id):

			start_date = datetime.strptime(start_date, '%Y-%m-%d')
			end_date = datetime.strptime(end_date, '%Y-%m-%d')
			engagement = self.vendor_engagement_repo.new_vendor_engagement(vendor_id, start_date, end_date)
			e = engagement.serialize()
			e['vendor'] = engagement.vendor.serialize()

			return self.handle_response('OK', payload={'engagement': e})

		return self.handle_response('Invalid vendor_id provided', status_code=400)

	def update_vendor_engagement(self, engagement_id):
		vendor_id, start_date, end_date, status, termination_reason = self.request_params('vendorId', 'startDate', 'endDate', 'status', 'terminationReason')
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
				return self.handle_response('This engagement cannot be deleted because it has a child object', status_code=400)
			updates = {}
			updates['is_deleted'] = True

			self.vendor_engagement_repo.update(engagement, **updates)
			return self.handle_response('Engagement deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect engagement_id provided', status_code=400)


	''' VENDOR RATING '''
	def list_ratings(self, vendor_id):
		'''retrieves a list of ratings for a specific vendor'''

		ratings = self.vendor_rating_repo.filter_by(vendor_id=vendor_id)

		if ratings:
			ratings_list = [rating.serialize() for rating in ratings.items]
			return self.handle_response('OK', payload={'ratings': ratings_list, 'meta': self.pagination_meta(ratings)})

		return self.handle_response('Expected vendor in request')

	def get_vendor_rating(self, rating_id):
		'''retrieves the details of a specific rating, giving the rating id'''
		rating = self.vendor_rating_repo.get(rating_id)
		if rating:
			rtng = rating.serialize()

			return self.handle_response('OK', payload={'rating': rtng})
		else:
			return self.handle_response('Bad Request', status_code=400)

	def create_vendor_rating(self):
		'''Adds a vendor rating during a specific engagement'''
		(vendor_id, comment, rating, channel) = self.request_params('vendor_id', 'comment', 'rating', 'channel')
		user_id = Auth.user('id')

		if self.vendor_repo.get(vendor_id):

			rating = self.vendor_rating_repo.new_vendor_rating(vendor_id, user_id, rating, channel, comment)
			rtng = rating.serialize()

			return self.handle_response('Rating created', payload={'rating': rtng}, status_code=201)

		return self.handle_response('Invalid vendor_id provided', status_code=400)

	def update_vendor_rating(self, rating_id):
		'''edits an existing rating'''

		rtng = self.vendor_rating_repo.get(rating_id)
		comment = self.get_json()['comment']

		if Auth.user('id') == rtng.user_id: #You cannot update someone else's rating
			if rtng:
				updates = {}
				if comment:
					updates['comment'] = comment
				self.vendor_rating_repo.update(rtng, **updates)
				return self.handle_response('OK', payload={'rating': rtng.serialize()})
			return self.handle_response('Invalid or incorrect rating_id provided', status_code=400)
		return self.handle_response('You are not allowed to update a rating that is not yours', status_code=403)
