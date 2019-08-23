"""A controller module for vendor ratings
"""
from datetime import datetime
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

    def list_ratings(self, date):
        """retrieves a list of all ratings"""
        query_kwargs = self.get_params_dict()
        date = datetime.strptime(date, '%Y-%m-%d')

        ratings = self.vendor_rating_repo.filter_by(service_date=date, **query_kwargs)

        if ratings.items:
            result = []
            vendor_name = self.vendor_repo.get(ratings.items[0].vendor_id).name

            for rating in ratings.items:
                if not rating.main_meal_id:
                    continue

                meal_name = self.meal_repo.get(rating.main_meal_id).name

                if meal_name not in [item.get('mainMeal') for item in result]:
                    meal_rating = {'mainMeal': meal_name,
                                   'overallRating': self.vendor_rating_repo.meal_average(rating.main_meal_id, date),
                                   'items': [rtng.serialize() for rtng in ratings.items if rtng.main_meal_id == rating.main_meal_id]
                                   }
                    result.append(meal_rating)

            return self.handle_response('OK', payload={'date': date, 'vendor': vendor_name, 'result': result})
        return self.handle_response('No ratings for this date', status_code=404)

    def get_vendor_rating(self, rating_id):
        """retrieves the details of a specific rating, giving the rating id"""
        rating = self.vendor_rating_repo.get(rating_id)
        if rating:
            rtng = rating.serialize()

            return self.handle_response('OK', payload={'rating': rtng})
        else:
            return self.handle_response('Bad Request', status_code=400)

    def create_vendor_rating(self):
        '''Adds a vendor rating during a specific engagement'''
        (comment, rating, service_date, channel, engagement_id) = self.request_params(
            'comment', 'rating', 'serviceDate', 'channel', 'engagementId'
        )
        main_meal_id = None
        user_id = Auth.user('id')
        vendor_id = self.vendor_engagement_repo.get(engagement_id).vendor_id

        if self.vendor_repo.get(vendor_id):

            service_date = datetime.strptime(service_date, '%Y-%m-%d')

            rating = self.vendor_rating_repo.new_rating(vendor_id, user_id, rating, service_date, RatingType.engagement,
                        engagement_id, engagement_id, main_meal_id, channel, comment)
            self.vendor_repo.update_vendor_average_rating(vendor_id)
            rtng = rating.serialize()

            return self.handle_response('Rating created', payload={'rating': rtng}, status_code=201)

        return self.handle_response('Invalid vendor_id provided', status_code=400)

    def create_order_rating(self):
        """Adds a order or meal rating during a specific engagement """

        (order_id, main_meal_id, engagement_id, comment, rating, service_date, channel) = self.request_params('orderId', 'mainMealId', 'engagementId', 'comment', 'rating', 'serviceDate', 'channel')
        if not(1 <= rating <= 5):
            return self.handle_response('Rating must be between 1 and 5, inclusive.', status_code=400)

        user_id = Auth.user('id')
        if not self.meal_repo.get(main_meal_id):
            return self.handle_response('Meal item with this id not found', status_code=400)
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

        else:
            if (datetime.now() - datetime.strptime(service_date, '%Y-%m-%d')).days < 1:
                return self.handle_response('You can only rate meals of past days.', status_code=400)
            rating_type = RatingType.meal
            type_id = main_meal_id
            user_meal_rating = self.vendor_rating_repo.get_unpaginated(user_id=user_id, type_id=type_id, rating_type='meal')
            if user_meal_rating:
                return self.handle_response('You have already rated this meal', status_code=400)

        rating = self.vendor_rating_repo.new_rating(
                    vendor_id, user_id, rating, datetime.strptime(service_date, '%Y-%m-%d'), rating_type, type_id, engagement_id, main_meal_id, channel, comment
                )

        self.vendor_repo.update_vendor_average_rating(vendor_id)
        if rating.id and rating_type == RatingType.order:
            updates = {'has_rated': True}
            self.order_repo.update(order, **updates)

        rating_obj = rating.serialize()
        return self.handle_response('Rating successful', payload={'rating': rating_obj}, status_code=201)

    def update_vendor_rating(self, rating_id):
        """edits an existing rating"""

        rtng = self.vendor_rating_repo.get(rating_id)
        comment = self.get_json()['comment']
        if rtng:
            if Auth.user('id') == rtng.user_id: #You cannot update someone else's rating

                updates = {}
                if comment:
                    updates['comment'] = comment
                self.vendor_rating_repo.update(rtng, **updates)
                return self.handle_response('OK', payload={'rating': rtng.serialize()})
            return self.handle_response('You are not allowed to update a rating that is not yours', status_code=403)
        return self.handle_response('Invalid or incorrect rating_id provided', status_code=404)
