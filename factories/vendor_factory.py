import factory
from faker import Faker
from app.utils import db
from random import randint
from app.models.vendor import Vendor


fake = Faker()
fake_name = fake.name()
fake_address = fake.address()
fake_tel = ''.join([str(randint(1, n)) for n in range(1, 12)])
fake_contact = fake.name()

class VendorFactory(factory.alchemy.SQLAlchemyModelFactory):
	
	
	class Meta:
		model = Vendor
		sqlalchemy_session = db.session
		
	id = factory.Sequence(lambda n: n)
	name = fake_name
	address = fake_address
	tel = fake_tel
	contact_person = fake_contact