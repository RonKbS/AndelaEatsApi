from sqlalchemy import event
from app.utils.id_generator import PushID


from .location import Location
from .vendor import Vendor
from .vendor_engagement import VendorEngagement
from .role import Role
from .permission import Permission
from .user_role import UserRole
from .vendor_rating import VendorRating
from .menu import Menu
from .meal_item import MealItem
from .order import Order
from .activity import Activity
from .faq import Faq
from .about import About
from .user import User
from .meal_session import MealSession
from .meal_service import MealService
from .menu_template import MenuTemplate, MenuTemplateItem

__all__ = (
    'Location', 'Vendor', 'VendorEngagement', 'Role', 'Permission',
    'UserRole', 'VendorRating', 'Menu', 'MealItem', 'Order', 'Activity',
    'Faq', 'About', 'User', 'MealSession', 'MealService', 'MenuTemplateItem',
    'MenuTemplate'
)

from .listener_helpers import attach_listen_type

tables_logged_after_every_insert = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, Order,
                                    MealSession, MenuTemplate, MenuTemplateItem]
tables_logged_after_every_update = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, Order,
                                    MealSession, MenuTemplate, MenuTemplateItem]
tables_logged_after_every_delete = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, VendorRating, Order,
                                    MealSession, MenuTemplate, MenuTemplateItem]
generate_id_tables = (User,)

# attach all listeners to each admin table
attach_listen_type(tables_logged_after_every_insert, 'after_insert')
attach_listen_type(tables_logged_after_every_update, 'after_update')
attach_listen_type(tables_logged_after_every_delete, 'after_delete')


def model_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    next_id = push_id.next_id()

    target.slack_id = target.slack_id if target.slack_id else next_id

    target.user_id = target.user_id if target.user_id else target.slack_id


for table in generate_id_tables:
    event.listen(table, 'before_insert', model_id_generator)
