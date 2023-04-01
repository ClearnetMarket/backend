from flask import jsonify
from flask_login import current_user, login_required
from app.notification import notification
from app import db
from app.classes.notifications import Notification_Notifications, Notification_Notifications_Schema


@notification.route('/notifications/new/count', methods=['GET'])
@login_required
def notification_notification_count():
    """
    Gets new messages
    :return:
    """
    gnotifications = db.session \
        .query(Notification_Notifications) \
        .filter(Notification_Notifications.user_uuid == current_user.uuid) \
        .filter(Notification_Notifications.read == 1)\
        .count()

    return jsonify({
        "success": "success",
        "count": gnotifications,
    })

@notification.route('/notifications', methods=['GET'])
@login_required
def notification_notification_new():
    """
    Gets new messages
    :return:
    """
    gnotifications = db.session \
        .query(Notification_Notifications) \
        .filter(Notification_Notifications.user_uuid == current_user.uuid) \
        .order_by(Notification_Notifications.timestamp.desc())\
        .limit(10)
    msg_schema = Notification_Notifications_Schema(many=True)
    return jsonify(msg_schema.dump(gnotifications))


@notification.route('/new/notification/markasread', methods=['PUT'])
@login_required
def notification_notification_markasread():
    """
    Marks all notifications as read
    :return:
    """
    gnotifications = db.session \
        .query(Notification_Notifications) \
        .filter(Notification_Notifications.user_uuid == current_user.uuid) \
        .filter(Notification_Notifications.read == 1) \
        .all()
    for note in gnotifications:
        note.read = 0
        db.session.add(note)
    db.session.commit()
  
    return jsonify({
        "success": "marked messages as read",
    })


