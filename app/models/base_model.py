from app.utils import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.utils import to_camel_case


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session().rollback()
            raise error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        s = {to_camel_case(column.name): getattr(self, column.name) for column in self.__table__.columns if column.name not in ['created_at', 'updated_at', 'start_time', 'stop_time']}
        if 'start_time' in self.__table__.columns:
                s[to_camel_case('start_time')] = str(self.start_time)
        if 'stop_time' in self.__table__.columns:
                s[to_camel_case('stop_time')] = str(self.stop_time)
        s['timestamps'] = {'created_at': datetime.strftime(self.created_at, '%Y-%m-%d'), 'updated_at': self.updated_at}

        return s

    def to_dict(self, only=None, exclude=()):

        dict_obj = {}

        mapper = {
            'only':
                lambda obj, name, only: dict_obj.__setitem__(name, getattr(obj, name)) if name in only else False,
            'exclude':
                lambda obj, name, exclude: dict_obj.__setitem__(name, getattr(obj, name))
                if name not in exclude else False
        }

        if only:
            filter_func = mapper.get('only')
            predicate = only
        else:
            filter_func = mapper.get('exclude')
            predicate = exclude

        def _to_dict(obj, predicate):
            for column in obj.__table__.columns:
                filter_func(obj, column.name, predicate)

            return dict_obj

        return _to_dict(self, predicate)

    @classmethod
    def get_columns(cls):
        fields = {}

        for column in cls.__table__.columns:
                fields.__setitem__(column.name, column.type)

        return fields
