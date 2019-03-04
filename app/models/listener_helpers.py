"""Helpers for event listeners"""
from sqlalchemy import event
from datetime import datetime as dt

from app.utils.auth import request
from app.utils import auth
from .activity import Activity, db


def add_activity(target, listener_type="insert"):
    """Log any update or change by an admin user

    : param1 target: instance of model
    : param2 listener_type: listener type attached to the model

    : return: None
    """
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
        """After flush event handler, fires just after flash but before a commit is made
        link: https://stackoverflow.com/questions/51376652/sqlalchemy-before-flush-event-handler-doesnt-see-change-of-foreign-key-when-ins

            : param1 session: The target Session(db.session in this case)
            : param2 context: Internal UOWTransaction object which handles the details of the flush.

            : return: None
        """
        session.add(Activity(
                module_name=model_name,
                ip_address=ip_address,
                user_id=user_id,
                action_type=action_type,
                action_details=action_details,
                channel=channel
            ))


def get_changes(target):
    """Return only changes that have been made on an entry

    : param1 target: instance of model

    : return: a dictionary containing changes made to the model
    """
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
    """Convert action detail into a more readable format

    : param1 user_id: Unique user identifier, got from the token
    : param2 model_name: the name of the model for which changes were made
    : param3 action_detail: the current or new state of the model instance
    : param4 action_type: the type of action that was performed ie. insert, update or delete

    : return: a string representation containing details of what happened
    """
    return "{" + user_id + "} " + action_type + " {" + model_name + "}" + " on " + "{" + \
        dt.today().strftime('%A') + "}" + " " + dt.today().strftime('%Y-%m-%d') + \
        "\n" + "Body: " + str(action_detail)


def after_insert_listener(mapper, connection, target):
    """Convert function that will be called when an insert event is encountered

    : param1 mapper: the Mapper which is the target of this event
    : param2 connection:  the Connection being used to emit INSERT statements for this instance.
                          This provides a handle into the current transaction on the target database
                          specific to this instance.
    : param3 target: the mapped instance being persisted

    : return: None
    """
    add_activity(target)


def after_update_listener(mapper, connection, target):
    """Convert function that will be called when an update event is encountered

    : param1 mapper: the Mapper which is the target of this event
    : param2 connection:  the Connection being used to emit update statements for this instance.
                          This provides a handle into the current transaction on the target database
                          specific to this instance.
    : param3 target: the mapped instance being persisted

    : return: None
    """
    add_activity(target, listener_type="update")


def after_delete_listener(mapper, connection, target):
    """Convert function that will be called when a delete event is encountered

    : param1 mapper: the Mapper which is the target of this event
    : param2 connection:  the Connection being used to emit delete statements for this instance.
                          This provides a handle into the current transaction on the target database
                          specific to this instance.
    : param3 target: the mapped instance being persisted

    : return: None
    """
    add_activity(target, listener_type="delete")


def attach_listen_type(tables, listen_type='after_insert'):
    """Convert function that attaches the event listeners to the tables

    : param1 tables: A list of tables to attach a particular listener
    : param2 listener_type: The type of event to attach

    : return: None
    """
    listen_type_mapper = {
        'after_insert': 'after_insert',
        'after_update': 'after_update',
        'after_delete': 'after_delete',
    }

    listen_function_mapper = {
        'after_insert': after_insert_listener,
        'after_update': after_update_listener,
        'after_delete': after_delete_listener,
    }

    for table in tables:
        event.listen(table,
                     listen_type_mapper.get(listen_type, 'after_insert'),
                     listen_function_mapper.get(listen_type, after_insert_listener)
                     )
