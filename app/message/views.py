from flask import session, jsonify
from app.message import message
from app import db
from datetime import datetime

from app.classes.auth import Auth_User
from app.classes.message import Message_Notifications
from app.classes.message import \
    Message_Post, \
    Message_PostUser, \
    Message_Comment
from app.notification import notification

from app.common.decorators import login_required


@message.route('/notification-count', methods=['GET'])
def message_notitification_count():
    """
    Gets the notification count for new users
    :return:
    """
    user_id = session.get("user_id")
    gnotifications = Message_Notifications.query\
        .filter(Message_Notifications.user_id == user_id,
                Message_Notifications.read == 0)\
        .count()

    return jsonify({
        "messagescount": gnotifications,
    })
