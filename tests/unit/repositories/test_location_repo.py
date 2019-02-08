from tests.base_test_case import BaseTestCase
from app.models.location import Location
from factories.location_factory import LocationFactory
from app.repositories.location_repo import LocationRepo


class TestMenuRepo(BaseTestCase):

  def setUp(self):
    self.BaseSetUp()
    self.repo = LocationRepo()

  def test_new_location_method_returns_new_location_object(self):
    location = LocationFactory.build()

    new_location = self.repo.new_location( location.name, location.zone)

    self.assertIsInstance(new_location, Location)
    self.assertEqual(new_location.name, location.name)
    self.assertEqual(new_location.zone, location.zone)
     
