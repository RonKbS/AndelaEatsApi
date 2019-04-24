from flask import request
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

from .listener_helpers import attach_listen_type

tables_logged_after_every_insert = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, Order]
tables_logged_after_every_update = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, Order]
tables_logged_after_every_delete = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, VendorRating, Order]
generate_id_tables = (User,)

# attach all listeners to each admin table
attach_listen_type(tables_logged_after_every_insert, 'after_insert')
attach_listen_type(tables_logged_after_every_update, 'after_update')
attach_listen_type(tables_logged_after_every_delete, 'after_delete')


def model_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    if not target.slack_id:
        target.slack_id = push_id.next_id()

for table in generate_id_tables:
    event.listen(table, 'before_insert', model_id_generator)
