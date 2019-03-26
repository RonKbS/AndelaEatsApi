from app.repositories.base_repo import BaseRepo
from app.models import Vendor, VendorRating


class VendorRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Vendor)
	
	def new_vendor(self, name, address, tel, is_active, contact_person, location_id):
		vendor = Vendor(name=name, address=address, tel=tel, is_active=is_active, contact_person=contact_person, location_id=location_id)
		vendor.save()
		return vendor

	def update_vendor_average_rating(self, vendor_id):
		vendor_ratings = VendorRating.query.filter_by(vendor_id=vendor_id).all()
		vendor = self.get(vendor_id)
		rating_values = [rating.rating for rating in vendor_ratings]
		rating_sum = sum(rating_values)
		average = round(rating_sum / len(rating_values), 1)
		self.update(vendor, average_rating=average)
		return average
