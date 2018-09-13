from app.repositories.base_repo import BaseRepo
from app.models.vendor_rating import VendorRating


class VendorRatingRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, VendorRating)

	def new_vendor_rating(self, vendor_id, user_id, vendor_engagement_id, rating, comment=''):
		vendor_rating = VendorRating(vendor_id=vendor_id, user_id=user_id, vendor_engagement_id=vendor_engagement_id, rating=rating, comment=comment)
		vendor_rating.save()
		return vendor_rating
