from flask import jsonify, request
from flask_login import current_user, login_required
from app.notification import notification
from app import db
from datetime import datetime
from app.classes.auth import Auth_User
from app.classes.notifications import  Message_Notifications

@notification.route('/new/messages', methods=['GET'])
@login_required
def message_new():
    """
    Gets new messages
    :return:
    """
    gnotifications = db.session \
        .query(Message_Notifications) \
        .filter(Message_Notifications.user_uuid == current_user.uuid,
                Message_Notifications.read == 0) \
        .count()

    return jsonify({
        "count": gnotifications,
    })


@notification.route('/new/messages/markasread', methods=['PUT'])
@login_required
def message_new_markasread():
    """
    Marks all notifications as read
    :return:
    """
    gnotifications = db.session \
        .query(Message_Notifications) \
        .filter(Message_Notifications.user_uuid == current_user.uuid,
                Message_Notifications.read == 0) \
        .all()
    for notification in gnotifications:
        notification.read = 1
        db.session.add(notification)
    db.session.commit()
  
    return jsonify({
        "status": "success",
    })



@notification.route('/updated/order', methods=['GET'])
@login_required
def order_updated():
    """
    Gets orders that have a different status
    :return:
    """

    pass