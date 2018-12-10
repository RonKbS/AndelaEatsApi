from app.repositories.base_repo import BaseRepo
from app.models.location import Location

class LocationRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Location)
	
	def new_location(self, name, zone):
		location = Location(name=name, zone=zone)
		location.save()
		return location