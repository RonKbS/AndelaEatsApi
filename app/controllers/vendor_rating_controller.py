'''A controller module for vendor ratings
'''

from app.controllers.base_controller import BaseController
from app.repositories import VendorRatingRepo, VendorRepo, VendorEngagementRepo, OrderRepo, MenuRepo, MealItemRepo
from app.utils.auth import Auth
from app.utils.enums import RatingType


class VendorRatingController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.vendor_rating_repo = VendorRatingRepo()
		self.vendor_repo = VendorRepo()
		self.vendor_engagement_repo = VendorEngagementRepo()
		self.menu_repo = MenuRepo()
		self.meal_repo = MealItemRepo()
		self.order_repo = OrderRepo()

	def list_ratings(self, vendor_id):
		'''retrieves a list of ratings for a specific vendor'''

		ratings = self.vendor_rating_repo.get_unpaginated(vendor_id=vendor_id)

		if ratings:
			ratings_list = [rating.serialize() for rating in ratings]
			return self.handle_response('OK', payload={'ratings': ratings_list})

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
		(vendor_id, comment, rating, channel, engagement_id) = self.request_params(
			'vendorId', 'comment', 'rating', 'channel', 'engagementId'
		)
		user_id = Auth.user('id')

		if self.vendor_repo.get(vendor_id):

			rating = self.vendor_rating_repo.new_rating(vendor_id, user_id, rating, RatingType.engagement,
						0, engagement_id, channel, comment)
			rtng = rating.serialize()

			return self.handle_response('Rating created', payload={'rating': rtng}, status_code=201)

		return self.handle_response('Invalid vendor_id provided', status_code=400)

	def create_order_rating(self):
		"""Adds a order or meal rating during a specific engagement """

		(order_id, main_meal_id, engagement_id, comment, rating, channel) = self.request_params('orderId', 'mainMealId', 'engagementId', 'comment', 'rating', 'channel')
		if not(order_id or main_meal_id):
			return self.handle_response('Please indicate what you are rating', status_code=400)
		user_id = Auth.user('id')
		engagement = self.vendor_engagement_repo.get(engagement_id)
		if not engagement:
				return self.handle_response('Engagement with this id is not found', status_code=400)
		vendor_id = engagement.vendor_id
		if order_id:
			rating_type = RatingType.order
			type_id = order_id
			order = self.order_repo.get(order_id)
			if not order:
				return self.handle_response('Order with this id is not found', status_code=400)
			if order.has_rated:
				return self.handle_response('This order has been rated', status_code=400)
			menu = self.menu_repo.get(order.menu_id)
			meal_id = menu.main_meal_id
					
		if main_meal_id:
			if not self.meal_repo.get(main_meal_id):
				return self.handle_response('Meal item with this id not found', status_code=400)
			rating_type = RatingType.meal
			type_id = main_meal_id
			user_meal_rating = self.vendor_rating_repo.get_unpaginated(user_id=user_id, type_id=type_id, rating_type='meal')
			if user_meal_rating:
				return self.handle_response('You have already rated this meal', status_code=400)

		rating = self.vendor_rating_repo.new_rating(
					vendor_id, user_id, rating, rating_type, type_id, engagement_id, channel, comment, type_id
				)
		if rating_type == RatingType.order:
			updates = {}
			updates['has_rated'] = True
			updated_order = self.order_repo.update(order, **updates).serialize()

		rating_obj = rating.serialize()
		return self.handle_response('Rating successful', payload={'rating': rating_obj}, status_code=201)

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
