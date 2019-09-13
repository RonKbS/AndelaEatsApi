from flask import jsonify, make_response, request
from flask.views import MethodView

from andelaeats.constants.success import messages
from andelaeats.database import db


class BaseMixin:
    model = None
    schema = None


class ModelListCreateMixin(BaseMixin):
    def get(self):
        records = self.model.query.all()
        schema = self.schema(many=True)
        return make_response(
            jsonify({self.model.plural_name(): schema.dump(records)}), 200
        )

    def post(self):
        request_data = request.get_json()
        schema = self.schema()
        record = schema.load(request_data, session=db.session)
        record.save()
        return make_response(
            jsonify({self.model.__name__.lower(): schema.dump(record)}), 201
        )


class RetrieveDeleteMixin(BaseMixin):
    def get(self, uuid):
        record = self.model.get_or_404(uuid)
        schema = self.schema()
        return make_response(
            jsonify({self.model.__name__.lower(): schema.dump(record)}), 200
        )

    def delete(self, uuid):
        record = self.model.get_or_404(uuid)
        record.delete()
        return make_response(
            jsonify(
                {
                    "msg": "OK",
                    "payload": messages["deleted"].format(self.model.__name__),
                }
            )
        )


class ModelUpdateMixin(BaseMixin):
    def put(self, uuid):
        record = self.model.get_or_404(uuid)
        request_data = request.get_json()
        schema = self.schema()
        record = schema.load(request_data, instance=record, session=db.session)
        return make_response(
            jsonify({self.model.__name__.lower(): schema.dump(record)}), 200
        )

    def patch(self, uuid):
        record = self.model.get_or_404(uuid)
        request_data = request.get_json()
        schema = self.schema()
        record = schema.load(
            request_data, instance=record, partial=True, session=db.session
        )
        return make_response(
            jsonify({self.model.__name__.lower(): schema.dump(record)}), 200
        )
