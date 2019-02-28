from tests.base_test_case import BaseTestCase

from app.models import Vendor


class TestHardDelete(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_hard_delete_on_vendor_model(self):
        vendor = Vendor(
            name='Your name',
            address='Your Address',
            tel='12345678',
            contact_person='Contact Person',
        )

        vendor.save()
        vendor_id = vendor.id

        vendor.delete()

        self.assertEquals(Vendor.query.get(vendor_id), None)


