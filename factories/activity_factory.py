import factory, datetime
from app.utils import db
from app.models.activity import Activity
from app.utils.enums import Channels, ActionType



class ActivityFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Activity
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    channel = Channels.web
    module_name = 'orders'
    ip_address = 'localhost'
    action_type = ActionType.create
    action_details = "Creation of a new item"
    user_id = '-L5J538y77WvOnzJ1FPG'
    created_at = datetime.datetime.now()

