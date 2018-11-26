from app.repositories.base_repo import BaseRepo
from app.models.vendor_rating import VendorRating


class VendorRatingRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, VendorRating)

	def new_vendor_rating(self, vendor_id, user_id, rating, channel, comment=''):
		vendor_rating = VendorRating(vendor_id=vendor_id, user_id=user_id, rating=rating, channel=channel, comment=comment)
		vendor_rating.save()
		return vendor_rating

	def new_rating(self, vendor_id, user_id, rating, rating_type, type_id, engagement_id, channel, comment=''):
		vendor_rating = VendorRating(
			vendor_id=vendor_id, user_id=user_id,
			rating=rating, channel=channel, comment=comment,
			rating_type=rating_type, type_id=type_id,
			engagement_id=engagement_id
		)
		vendor_rating.save()
		return vendor_rating
