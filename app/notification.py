from app import db
from app.classes.notifications import Notification_Notifications
from datetime import datetime

def create_notification(username, user_uuid, msg):

    now = datetime.utcnow()

    addnotice = Notification_Notifications(
        username=username,
        user_uuid=user_uuid,
        timestamp=now,
        message=msg,
        read=1
    )
    db.session.add(addnotice)
