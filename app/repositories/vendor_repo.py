from app.repositories.base_repo import BaseRepo
from app.models.vendor import Vendor


class VendorRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Vendor)
	
	def new_vendor(self, name, address, tel, is_active, contact_person, location_id):
		vendor = Vendor(name=name, address=address, tel=tel, is_active=is_active, contact_person=contact_person, location_id=location_id)
		vendor.save()
		return vendor