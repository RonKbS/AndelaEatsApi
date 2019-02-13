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
		return self.handle_response('Invalid or Missing location_id', status_code=400)
	
	def create_location(self):
		name, zone = self.request_params('name', 'zone')
		location = self.location_repo.new_location(name=name, zone=zone)
		return self.handle_response('OK', payload={'location': location.serialize()}, status_code=201)
	
	def update_location(self, location_id):
		name, zone = self.request_params('name', 'zone')
		location = self.location_repo.get(location_id)

		if location:
			location = self.location_repo.update(location, **dict(name=name, zone=zone))
			return self.handle_response('OK', payload={'location': location.serialize()}, status_code=201)

		return self.handle_response('Location Not Found', status_code=404)
	
	def delete_location(self, location_id):
		location = self.location_repo.get(location_id)

		if location and not location.is_deleted:
			location = self.location_repo.update(location, **dict(is_deleted=True))
			return self.handle_response('Location deleted successfully', payload={'location': location.serialize()}, status_code=200)

		return self.handle_response('Location Not Found', status_code=404)