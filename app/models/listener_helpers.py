"""Helpers for event listeners"""
from sqlalchemy import event
from datetime import datetime as dt

from app.utils.auth import request
from app.utils import auth
from .activity import Activity, db


def add_activity(target, listener_type="insert"):
    """Log any update or change by an admin user"""
    try:
        user_id = auth.Auth.user('UserInfo').get('id')
        ip_address = request.remote_addr
    except Exception as e:
        user_id = 'unknown'
        ip_address = 'unknown'

    model_name = target.__class__.__name__

    target_as_dict = target.to_dict()
    target_as_dict["created_at"] = target_as_dict["created_at"].strftime('%Y-%m-%dT%H:%M:%S.%f')
    target_as_dict["updated_at"] = target_as_dict["updated_at"].strftime('%Y-%m-%dT%H:%M:%S.%f')

    action_detail = dict()
    action_detail["Previous State"] = get_changes(target)

    listener_types = {
        "insert": "create",
        "update": "update",
        "delete": "delete"
    }

    action_type = listener_types.get(listener_type, "")

    channel = target.channel if hasattr(target, 'channel') else None

    channel = 'slack' if channel is 'slack' else 'web'

    if listener_type is "insert":
        action_detail["Current State"] = target_as_dict
        del action_detail["Previous State"]
        action_details = stringify_action_detail(user_id, model_name, action_detail, "created")

    if listener_type is "update" and not target_as_dict.get('is_deleted'):
        action_detail["Current State"] = target_as_dict
        action_details = stringify_action_detail(user_id, model_name, action_detail, "updated")

    if listener_type is "update" and target_as_dict.get('is_deleted'):
        action_detail["Soft deleted Entity"] = target_as_dict
        action_details = stringify_action_detail(user_id, model_name, action_detail, "soft deleted")

    if listener_type is "delete":
        action_detail["Deleted Entity"] = target_as_dict
        del action_detail["Previous State"]
        action_detail["Current State"] = {}
        action_details = stringify_action_detail(user_id, model_name, action_detail, "hard deleted")

    @event.listens_for(db.session, "after_flush", once=True)
    def receive_after_flush(session, context):

        session.add(Activity(
                module_name=model_name,
                ip_address=ip_address,
                user_id=user_id,
                action_type=action_type,
                action_details=action_details,
                channel=channel
            ))


def get_changes(target):
    """Return only changes that have been made on an entry"""
    state = db.inspect(target)
    changes = {}

    for attr in state.attrs:
        hist = state.get_history(attr.key, True)
        if not hist.has_changes():
            continue

        # hist.deleted holds old value
        # hist.added holds new value
        changes[attr.key] = hist.deleted

    # Extract first value in the list of changed items
    for key, value in changes.items():
        if isinstance(value, list) and len(value) > 0:
            changes[key] = value[0]

    return changes


def stringify_action_detail(user_id, model_name, action_detail, action_type):
    """Convert action detail into a more readable format"""
    return "{" + user_id + "} " + action_type + " {" + model_name + "}" + " on " + "{" + \
        dt.today().strftime('%A') + "}" + " " + dt.today().strftime('%Y-%m-%d') + \
        "\n" + "Body: " + str(action_detail)

