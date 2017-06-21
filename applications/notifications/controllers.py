from datetime import datetime

from applications.notifications.models import *
import applications.notifications.dal as db
from graphspace.exceptions import ErrorCodes, BadRequest
from graphspace.database import *

from django.conf import settings


# Function to add notification to database
def add_owner_notification(message, type, resource, resource_id, owner_email=None, is_read=False, is_email_sent=False):
    sess = Database().session()
    notify = db.add_owner_notification(sess, message=message, type=type, owner_email=owner_email,
                                       resource=resource, resource_id=resource_id, is_read=is_read, is_email_sent=is_email_sent)
    # Apply changes to DB as the Middleware is not called
    sess.commit()
    return notify


def search_owner_notifications(request, owner_email=None, is_read=None, limit=20, offset=0):
    sort_attr = db.OwnerNotification.created_at
    orber_by = db.desc(sort_attr)

    total, notifications = db.find_owner_notifications(request.db_session,
                                                       owner_email=owner_email,
                                                       is_read=is_read,
                                                       limit=limit,
                                                       offset=offset,
                                                       order_by=orber_by)

    return total, notifications
