import json

from flask import url_for

from andelaeats.constants.errors import serialization_errors
from andelaeats.constants.success import messages


class ViewTestsMeta(type):
    def __new__(cls, name, bases, attrs):
        model_name = attrs["model"].__name__.lower()

        attrs[
            "test_get_all_" + attrs["model"].plural_name() + "_succeeds"
        ] = cls.get_all_generator()

        attrs["test_get_one_" + model_name + "_succeeds"] = cls.get_one_generator()

        attrs["test_delete_" + model_name + "_succeeds"] = cls.delete_generator()

        attrs["test_create_" + model_name + "_succeeds"] = cls.create_generator()

        for method in ["put", "patch"]:
            attrs[f"test_{method}_{model_name}_succeeds"] = cls.update_generator(
                method=method
            )

        for method in ["put", "patch"]:
            attrs[
                f"test_{method}_non_existing_{model_name}_fails"
            ] = cls.not_found_generator(method=method, data=json.dumps({}))

        for method in ["get", "delete"]:
            attrs[
                f"test_{method}_non_existing_{model_name}_fails"
            ] = cls.not_found_generator(method=method)

        for method in ["put", "post", "patch"]:
            attrs[
                f"test_{method}_{model_name}_with_invalid_json_fails"
            ] = cls.invalid_json_generator(method=method, data={})
        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def get_all_generator(cls):
        def fn(self, app, client):
            fixture = self.factory()
            fixture.save()
            with app.app_context():
                response = client.get(url_for(self.url))
            assert response.status_code == 200
            assert response.json[self.model.plural_name()][0] == self.schema().dump(
                fixture
            )

        return fn

    @classmethod
    def get_one_generator(cls):
        def fn(self, app, client):
            fixture = self.factory()
            fixture.save()
            vars()[self.model.__name__.lower()] = fixture
            with app.app_context():
                response = client.get(f"{url_for(self.url)}{fixture.uuid}")
            assert response.status_code == 200
            assert response.json[self.model.__name__.lower()] == self.schema().dump(
                fixture
            )

        return fn

    @classmethod
    def not_found_generator(cls, method, **kwargs):
        def fn(self, app, client):
            record_id = 100
            with app.app_context():
                response = getattr(client, method)(
                    f"{url_for(self.url)}{record_id}", **kwargs
                )
            assert response.status_code == 404
            assert (
                response.json["msg"]
                == f"{self.model.__name__} with id {record_id} not found"
            )

        return fn

    @classmethod
    def invalid_json_generator(cls, method, **kwargs):
        def fn(self, app, client):
            record_id = 100
            with app.app_context():
                response = getattr(client, method)(
                    f"{url_for(self.url)}{record_id}", **kwargs
                )
            assert response.status_code == 400
            assert response.json["msg"] == serialization_errors["INVALID_JSON"]

        return fn

    @classmethod
    def delete_generator(cls):
        def fn(self, app, client):
            fixture = self.factory()
            fixture.save()
            with app.app_context():
                response = client.delete(f"{url_for(self.url)}{fixture.uuid}")
            assert response.status_code == 200
            assert response.json["payload"] == messages["deleted"].format(
                self.model.__name__
            )

        return fn

    @classmethod
    def create_generator(cls):
        def fn(self, app, client):
            fixture = self.factory.build()
            fixture_dump = self.schema(exclude=("created_at", "uuid")).dump(fixture)
            with app.app_context():
                response = client.post(
                    f"{url_for(self.url)}", data=json.dumps(fixture_dump)
                )
            assert response.status_code == 201
            response.json[self.model.__name__.lower()].pop("uuid")
            response.json[self.model.__name__.lower()].pop("created_at")
            assert response.json[self.model.__name__.lower()] == fixture_dump

        return fn

    @classmethod
    def update_generator(cls, method):
        def fn(self, app, client):
            fixture = self.factory()
            fixture.save()
            update = self.factory.build()
            with app.app_context():
                response = getattr(client, method)(
                    f"{url_for(self.url)}{fixture.uuid}",
                    data=self.schema(exclude=("created_at", "uuid")).dumps(update),
                )
            assert response.status_code == 200
            assert response.json[self.model.__name__.lower()] == self.schema().dump(
                fixture
            )

        return fn
