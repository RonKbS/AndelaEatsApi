import pytz
from sqlalchemy import desc, asc
from app.models import VendorRating, Location

class BaseRepo:
	
	def __init__(self, _model):
		self._model = _model
		
	def fetch_all(self):
		"""Return all the data in the model."""
		return self._model.query.paginate(error_out=False)
	
	
	def get(self, *args):
		"""Return data by the Id."""
		return self._model.query.get(*args)
	
	def update(self, model_instance, **kwargs):
		""" Update Model """
		for key, val in kwargs.items():
			setattr(model_instance, key, val)
		model_instance.save()
		return model_instance
	
	
	def count(self):
		"""Return the count of all the data in the model."""
		return self._model.query.count()
	
	
	def get_first_item(self):
		"""Return the first data in the model."""
		return self._model.query.first()
	
	
	def order_by(self, *args):
		"""Query and order the data of the model."""
		return self._model.query.order_by(*args)
	
	
	def filter_all(self, **kwargs):
		"""Query and filter the data of the model."""
		return self._model.query.filter(**kwargs).paginate(error_out=False)
	
	
	def filter_by(self, **kwargs):
		"""Query and filter the data of the model."""
		#return self._model.query.filter_by(is_deleted=False).paginate(**kwargs, error_out=False)
		return self._model.query.filter_by(**kwargs).paginate(error_out=False)

	def filter_by_desc(self, *args, **kwargs):
		"""Query and filter the data of the model in descending order"""
		return self._model.query.filter_by(**kwargs).order_by(desc(*args)) \
			.paginate(error_out=False)

	def filter_by_asc(self, *args, **kwargs):
		"""Query and filter the data of the model in ascending order"""
		return self._model.query.filter_by(**kwargs).order_by(asc(*args)) \
			.paginate(error_out=False)

	def get_unpaginated(self, **kwargs):
		"""Query and filter the data of the model."""
		return self._model.query.filter_by(**kwargs).all()

	def get_unpaginated_asc(self, *args, **kwargs):
		"""Query and filter the data of the model in ascending order."""
		return self._model.query.filter_by(**kwargs).order_by(asc(*args)) \
			.all()

	def get_unpaginated_desc(self, *args, **kwargs):
		"""Query and filter the data of the model in ascending order."""
		return self._model.query.filter_by(**kwargs).order_by(desc(*args)) \
			.all()
	
	def find_first(self, **kwargs):
		"""Query and filter the data of a model, returning the first result."""
		return self._model.query.filter_by(**kwargs).first()
	
	
	def filter_and_count(self, **kwargs):
		"""Query, filter and counts all the data of a model."""
		return self._model.query.filter_by(**kwargs).count()
	
	
	def filter_and_order(self, *args, **kwargs):
		"""Query, filter and orders all the data of a model."""
		return self._model.query.filter_by(**kwargs).order_by(*args)
	
	
	def paginate(self, **kwargs):
		"""Query and paginate the data of a model, returning the first result."""
		return self._model.query.paginate(**kwargs)
	
	
	def filter(self, *args):
		"""Query and filter the data of the model."""
		return self._model.query.filter(*args).paginate(error_out=False)

	def get_rating(self, user_id, rating_type, type_id):

		rating = VendorRating.query.filter_by(user_id=user_id, rating_type=rating_type, type_id=type_id).first()

		return rating.rating if rating else None

	def exists(self, **kwargs):

		if self._model.query.filter_by(**kwargs).first():
			return True

		return False

	@staticmethod
	def get_location_time_zone(location_id):
		"""
		Get the time zone of a particular location

		:param location_id: string representing location id
		:return: timezone object
		:raises: AttributeError, pytz.exceptions.UnknownTimeZoneError
		"""
		location = Location.query.filter_by(id=location_id).first()

		try:
			return pytz.timezone('Africa/' + location.name)
		except AttributeError:
			return AttributeError
		except pytz.exceptions.UnknownTimeZoneError:
			return pytz.exceptions.UnknownTimeZoneError

