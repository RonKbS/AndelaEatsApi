from app.controllers.base_controller import BaseController
from app.repositories.location_repo import LocationRepo

class LocationController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.location_repo = LocationRepo()
	
	def list_locations(self):
		locations = self.location_repo.fetch_all()
		location_list = [location.serialize() for location in locations.items]
		return self.handle_response('OK', payload={'locations': location_list, 'meta': self.pagination_meta(locations)})
	
	def get_location(self, location_id):
		location = self.location_repo.get(location_id)
		if location:
			return self.handle_response('OK', payload={'location': location.serialize()})
		return self.handle_response('Invalid or Missing location_id')
	
	def create_location(self):
		name, = self.request_params('name')
		location = self.location_repo.new_location(name=name)
		return self.handle_response('OK', payload={'location':location.serialize()})
	
	def update_location(self, location_id):
		pass
	
	def delete_location(self, delete_location):
		pass