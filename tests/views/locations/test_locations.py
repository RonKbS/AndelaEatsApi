import json

import pytest

from andelaeats.constants.success import messages
from andelaeats.location.models import City

from ...factories import LocationFactory

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestLocationsEndpoints:
    def test_get_all_cities(self, client, location):
        response = client.get(f"{api_version}/locations")
        assert response.status_code == 200
        assert response.json["locations"][0]["name"] == location.name

    def test_get_location_succeeds(self, client, location):
        response = client.get(f"{api_version}/locations")
        assert response.status_code == 200
        assert response.json["locations"][0]["name"] == location.name

    def test_get_specific_location_succeeds(self, client, location):
        response = client.get(f"{api_version}/locations/{location.id}")
        assert response.status_code == 200
        assert response.json["location"]["name"] == location.name

    def test_create_location_succeeds(self, client):
        location = LocationFactory.build()
        location_data = json.dumps(
            {"name": location.name, "timezone": location.timezone}
        )
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 201
        assert response.json["location"]["name"] == location.name

    def test_create_location_with_missing_fields_fails(self, client):
        location = LocationFactory.build()
        location_data = json.dumps({"name": location.name})
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400

    def test_create_location_with_no_fields_fails(self, client):
        location = LocationFactory.build()
        location_data = json.dumps({})
        response = client.post(f"{api_version}/locations/", data=location_data)
        assert response.status_code == 400

    def test_update_existing_location_succeeds(self, client, location):
        new_location = LocationFactory.build()

        update = json.dumps({"name": new_location.name})

        response = client.put(f"{api_version}/locations/{location.id}", data=update)
        assert response.status_code == 200
        assert response.json["location"]["name"] == new_location.name

    def test_update_non_existing_location_with_fails(self, client):
        new_location = LocationFactory.build()
        city_id = 100
        update = json.dumps({"name": new_location.name})
        response = client.put(f"{api_version}/locations/{city_id}", data=update)
        assert response.status_code == 404
        assert response.json["msg"] == f"City with id {city_id} not found"

    def test_delete_existing_location_succeeds(self, client, location):
        response = client.delete(f"{api_version}/locations/{location.id}")
        assert response.status_code == 200
        assert response.json["msg"] == "OK"
        assert response.json["payload"] == "Location successfully deleted"

    def test_delete_non_existing_location_fails(self, client):
        city_id = 100
        response = client.delete(f"{api_version}/locations/{city_id}")
        assert response.status_code == 404
        assert response.json["msg"] == f"City with id {city_id} not found"
