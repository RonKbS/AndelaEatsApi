import factory
from app.utils import db
from datetime import date, datetime, timedelta
from factories.vendor_factory import VendorFactory
from app.models.vendor_engagement import VendorEngagement
#
# vendor = VendorFactory()
class VendorEngagementFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = VendorEngagement
		sqlalchemy_session = db.session

	vendor = factory.SubFactory(VendorFactory)
	
	id = factory.Sequence(lambda n: n)
	vendor_id = factory.SelfAttribute('vendor.id')
	start_date = date.today() #factory.Faker('date')
	end_date = datetime.now() + timedelta(weeks=+1) # factory.Faker('date')
	status = 1
	termination_reason = factory.Faker('paragraph')
	# cohort_position = fake_cohort_position
		
			