from flask import request
from sqlalchemy import event


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

from .listener_helpers import add_activity

tables = [Vendor]


def after_insert_listener(mapper, connection, target):
    add_activity(target)


def after_update_listener(mapper, connection, target):
    add_activity(target, listener_type="update")


def after_delete_listener(mapper, connection, target):
    add_activity(target, listener_type="delete")


# Add after_insert, after_update, after_delete listeners to models
for table in tables:
   event.listen(table, 'after_insert', after_insert_listener)
   event.listen(table, 'after_update', after_update_listener)
   event.listen(table, 'after_delete', after_delete_listener)



