import json

import pytest

from andelaeats.constants.success import messages
from andelaeats.location.models import Location
from andelaeats.location.schema import LocationSchema

from ...factories import LocationFactory
from ..generator import ViewTestsMeta

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestLocationsEndpoints(metaclass=ViewTestsMeta):
    url = "location.locations"
    schema = LocationSchema
    factory = LocationFactory
    model = Location

    def test_create_location_with_existing_name_fails(self, client, location):
        location = LocationFactory.build(name=location.name)
        location_data = json.dumps(
            {"name": location.name, "timezone": location.timezone}
        )
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400
        assert (
            response.json["error"]["name"][0]
            == f"Location with name '{location.name}' already exists"
        )

    def test_create_location_with_missing_fields_fails(self, client):
        location = LocationFactory.build()
        location_data = json.dumps({"name": location.name})
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400

    def test_create_location_with_invalid_json_fails(self, client):
        location = LocationFactory.build()
        location_data = {"name": location.name}
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400

    def test_create_location_with_no_fields_fails(self, client):
        location = LocationFactory.build()
        location_data = json.dumps({})
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400

    def test_update_location_with_missing_fields_fails(self, client, location):
        new_location = LocationFactory.build()
        update = json.dumps({"name": new_location.name})
        response = client.put(f"{api_version}/locations/{location.uuid}", data=update)
        assert response.status_code == 400
        assert response.json["error"] == {
            "timezone": ["Missing data for required field."]
        }

    def test_update_non_existing_location_with_fails(self, client):
        new_location = LocationFactory.build()
        location_id = 100
        update = json.dumps({"name": new_location.name})
        response = client.put(f"{api_version}/locations/{location_id}", data=update)
        assert response.status_code == 404
        assert response.json["msg"] == f"Location with id {location_id} not found"

    def test_patch_existing_location_succeeds(self, client, location):
        new_location = LocationFactory.build()

        update = json.dumps({"name": new_location.name})

        response = client.patch(f"{api_version}/locations/{location.uuid}", data=update)
        assert response.status_code == 200
        assert response.json["location"]["name"] == new_location.name
