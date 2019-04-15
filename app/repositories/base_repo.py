from sqlalchemy import desc, asc


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

    def exists(self, **kwargs):

        if self._model.query.filter_by(**kwargs).first():
            return True

        return False

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
