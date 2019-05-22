from sqlalchemy import desc, asc
from app.models import VendorRating
from flask_sqlalchemy import Pagination
from functools import wraps
from app.utils.handled_exceptions import BaseModelValidationError


def filter_deleted(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not kwargs:
            kwargs = dict(is_deleted=False)
        kwargs.update(is_deleted=False) if not kwargs.get('is_deleted') else None

        return func(*args, **kwargs)

    return decorated


class BaseRepo:

    DEFAULT_PAGINATION_PAGE_NUMBER = 1
    DEFAULT_PAGINATION_PER_PAGE_NUMBER = 20

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

    def paginate(self, page=None, per_page=None, error_out=False):

        try:
            page = BaseRepo._positive_int('page', page) if page else BaseRepo.DEFAULT_PAGINATION_PAGE_NUMBER
            per_page = BaseRepo._positive_int('per_page', per_page) if per_page else \
                BaseRepo.DEFAULT_PAGINATION_PER_PAGE_NUMBER
        except ValueError as err:
            raise BaseModelValidationError(str(err))

        offset = (page - 1) * per_page

        all_items = self._model.query.filter_by(is_deleted=False)
        items = all_items.limit(per_page).offset(offset).all()

        return Pagination(self, page, per_page, all_items.count(), items)


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

    @filter_deleted
    def filter_by(self, **kwargs):
        """Query and filter the data of the model."""
        #return self._model.query.filter_by(is_deleted=False).paginate(**kwargs, error_out=False)
        return self._model.query.filter_by(**kwargs).paginate(error_out=False)

    @filter_deleted
    def filter_by_desc(self, *args, **kwargs):
        """Query and filter the data of the model in descending order"""
        return self._model.query.filter_by(**kwargs).order_by(desc(*args)) \
            .paginate(error_out=False)

    @filter_deleted
    def filter_by_asc(self, *args, **kwargs):
        """Query and filter the data of the model in ascending order"""
        return self._model.query.filter_by(**kwargs).order_by(asc(*args)) \
            .paginate(error_out=False)

    @filter_deleted
    def get_unpaginated(self, **kwargs):
        """Query and filter the data of the model."""
        return self._model.query.filter_by(**kwargs).all()

    @filter_deleted
    def get_unpaginated_asc(self, *args, **kwargs):
        """Query and filter the data of the model in ascending order."""
        return self._model.query.filter_by(**kwargs).order_by(asc(*args)) \
            .all()

    @filter_deleted
    def get_unpaginated_desc(self, *args, **kwargs):
        """Query and filter the data of the model in ascending order."""
        return self._model.query.filter_by(**kwargs).order_by(desc(*args)) \
            .all()

    @filter_deleted
    def find_first(self, **kwargs):
        """Query and filter the data of a model, returning the first result."""
        return self._model.query.filter_by(**kwargs).first()

    @filter_deleted
    def filter_and_count(self, **kwargs):
        """Query, filter and counts all the data of a model."""
        return self._model.query.filter_by(**kwargs).count()

    @filter_deleted
    def filter_and_order(self, *args, **kwargs):
        """Query, filter and orders all the data of a model."""
        return self._model.query.filter_by(**kwargs).order_by(*args)

    def filter(self, *args):
        """Query and filter the data of the model."""
        return self._model.query.filter(*args).paginate(error_out=False)

    def exists(self, **kwargs):

        if self._model.query.filter_by(**kwargs).first():
            return True

        return False

    def get_rating(self, user_id, rating_type, type_id):

        rating = VendorRating.query.filter_by(user_id=user_id, rating_type=rating_type, type_id=type_id).first()

        return rating.rating if rating else None

    @staticmethod
    def check_exists_else_where(model_class, first_attribute, first_compare_value, second_attribute, second_compare_value):
        """
        Checks whether a value already exists somewhere else other than specified.
        A typical example would be
        User.filter(User.slack_id == 'slack_id', User.id != '01')

        :param model_class:The model class for example User
        :param first_attribute: The attribute to perform first search on
        :param first_compare_value: The value to compare with first attribute
        :param second_attribute: The attribute to exclude in the filter once the first comparison passes
        :param second_compare_value: The value to compare with second attribute
        :return list: A list of all the items found
        :return string: A string specifying what went wrong.
        """
        try:
            return model_class.query.filter(
                getattr(model_class, first_attribute) == first_compare_value,
                getattr(model_class, second_attribute) != second_compare_value
            ).all()
        except Exception as e:
            return "An error occurred during the check: Details {}".format(str(e))

    @staticmethod
    def _positive_int(key, value):

        try:
            value = int(value)
        except ValueError:
            raise ValueError(f'{key} must be a positive integer')
        else:
            if value < 0:
                raise ValueError(f'{key} must be a non-negative value')
        return value

