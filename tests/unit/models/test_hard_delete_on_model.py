from tests.base_test_case import BaseTestCase

from app.models import Vendor, Activity
from factories.location_factory import LocationFactory


class TestHardDelete(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_hard_delete_on_vendor_model(self):
        vendor = Vendor(
            name='Your name',
            address='Your Address',
            tel='12345678',
            contact_person='Contact Person',
            location=LocationFactory(),
        )

        vendor.save()
        vendor_id = vendor.id

        vendor.delete()

        self.assertEquals(Vendor.query.get(vendor_id), None)

    def test_creating_vendor_gets_logged(self):
        vendor = Vendor(
            name='Your name',
            address='Your Address',
            tel='12345678',
            contact_person='Contact Person',
            location=LocationFactory(),
        )
        vendor.save()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("created" in activity[0])

    def test_updating_vendor_gets_logged(self):
        vendor = Vendor(
            name='Your name',
            address='Your Address',
            tel='12345678',
            contact_person='Contact Person',
            location=LocationFactory(),
        )
        vendor.save()

        vendor = Vendor.query.get(1)
        vendor.name = "New Name"
        vendor.save()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("updated" in activity[1])

    def test_hard_deleting_vendor_gets_logged(self):
        vendor = Vendor(
            name='Your name',
            address='Your Address',
            tel='12345678',
            contact_person='Contact Person',
            location=LocationFactory(),
        )
        vendor.save()

        vendor = Vendor.query.get(1)
        vendor.delete()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("hard deleted" in activity[-1])

