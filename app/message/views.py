from flask import jsonify, request
from flask_login import current_user, login_required
from app.message import message
from app import db
from datetime import datetime
from sqlalchemy import or_
from app.classes.auth import Auth_User
from app.classes.message import Message_Chat,\
    Message_Comment, \
    Message_Comment_Schema, \
    Message_Chat_Schema, \
    Message_Post,\
    Message_Notifications
from app.classes.item import Item_MarketItem
from app.notification import notification


@message.route('/notification-count', methods=['GET'])
def message_notitification_count():
    """
    Gets the notification count for new users
    :return:
    """
    user_id = current_user.id
    gnotifications = Message_Notifications.query\
        .filter(Message_Notifications.user_id == user_id,
                Message_Notifications.read == 0)\
        .count()

    return jsonify({
        "messagescount": gnotifications,
    })


@message.route('/count', methods=['GET'])
@login_required
def message_count():
    """
    Counts the number of messages a user has
    :return:
    """
    get_count = Message_Chat.query\
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid, Message_Chat.user_two_uuid == current_user.uuid))\
        .count()

    return jsonify({
        "get_count": get_count,
    })


@message.route('/msgs/all', methods=['GET'])
@login_required
def message_msg_sidebar():
    """
    Returns User Msgs list on the side...aka who you had conversations with
    :return:
    """
    get_msgs_side = Message_Chat.query\
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,Message_Chat.user_two_uuid == current_user.uuid))\
        .distinct(Message_Chat.post_id)\
        .all()
    msg_schema = Message_Chat_Schema(many=True)
 
    return jsonify(msg_schema.dump(get_msgs_side))


@message.route('/main/post/<int:post_id>', methods=['GET'])
@login_required
def message_msg(post_id):
    """
    Returns the main first question asked to the vendor or party.
    :return:
    """
    get_msg_post = Message_Chat.query\
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,Message_Chat.user_two_uuid == current_user.uuid))\
        .filter(Message_Chat.post_id == post_id)\
        .first()
   
    msg_schema = Message_Chat_Schema()
    return jsonify(msg_schema.dump(get_msg_post))


@message.route('/main/comment/<int:post_id>', methods=['GET'])
@login_required
def message_msg_comments(post_id):
    """
    Returns the comments of the main post
    :return:
    """
    get_msg_post = Message_Chat.query\
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid, Message_Chat.user_two_uuid == current_user.uuid))\
        .filter(Message_Chat.post_id == post_id)\
        .first()
    if get_msg_post is not None:
        get_msg_post_comments = Message_Comment.query\
            .filter(Message_Comment.post_id == post_id)\
            .order_by(Message_Comment.timestamp.desc())\
            .all()
        comments_schema = Message_Comment_Schema(many=True)
        return jsonify(comments_schema.dump(get_msg_post_comments))


@message.route('/create/item', methods=['POST'])
@login_required
def message_create():
    """
    Creates a New Message
    :return:
    """
    now = datetime.utcnow()
    
    get_item_uuid = request.json["item_uuid"]
    get_user_two_uuid = request.json["user_two_uuid"]
    get_body = request.json["textbody"]

    get_market_item = Item_MarketItem.query\
        .filter(Item_MarketItem.uuid == get_item_uuid)\
        .first()

    get_user_two_name = Auth_User.query\
        .filter(Auth_User.uuid == get_user_two_uuid)\
        .first()
    get_user_two_name_display = get_user_two_name.display_name

    # see if a post exists between two users
    # if it does create a comment ..
    get_post = Message_Chat.query\
        .filter(Message_Chat.user_one_uuid == get_market_item.vendor_uuid)\
        .filter(Message_Chat.user_two_uuid == current_user.uuid)\
        .filter(Message_Chat.item_uuid == get_market_item.uuid)\
        .first() 
    
    if get_post is None:
        # user one is always the vendor
        if get_market_item.vendor_uuid == get_user_two_uuid:

            newpost = Message_Post(timestamp=now)
            db.session.add(newpost)
            db.session.flush()

            create_new_message = Message_Chat(
                timestamp=now,
                order_uuid=None,
                item_uuid=get_item_uuid,
                user_one=get_market_item.vendor_display_name,
                user_one_uuid=get_market_item.vendor_uuid,
                user_two=current_user.display_name,
                user_two_uuid=current_user.uuid,
                mod_name=None,
                mod_uuid=None,
                body=get_body,
                post_id=newpost.id,
                admin=0,
                read=0
            )
        else:
            create_new_message = Message_Chat(
                timestamp=now,
                order_uuid=None,
                item_uuid=get_item_uuid,
                user_one=get_market_item.vendor_display_name,
                user_one_uuid=get_market_item.vendor_uuid,
                user_two=get_user_two_name_display,
                user_two_uuid=get_user_two_uuid,
                mod_name=None,
                mod_uuid=None,
                body=get_body,
                post_id=newpost.id,
                admin=0,
                read=0
            )

        db.session.add(create_new_message)
        db.session.commit()

    else:
        create_new_comment = Message_Comment(
            body=get_body,
            timestamp=now,
            user_one_uuid=current_user.uuid,
            user_one=current_user.display_name,
            post_id=get_post.post_id,
            mod_name=None,
            mod_uuid=None,
        )

        db.session.add(create_new_comment)
        db.session.commit()
    return jsonify({"status": "Success"})


@message.route('/create/comment/<int:post_id>', methods=['POST'])
@login_required
def message_comment(post_id):
    """
    Creates a New Message
    :return:
    """
    now = datetime.utcnow()
    get_body = request.json["textbody"]

    get_post = Message_Chat.query.filter(Message_Chat.post_id == post_id).first()
    if get_post.user_one_uuid == current_user.uuid or get_post.user_two_uuid == current_user.uuid:
        get_user_name = Auth_User.query\
            .filter(Auth_User.uuid == current_user.uuid)\
            .first()

        create_new_comment = Message_Comment(
            body=get_body,
            timestamp=now,
            user_one_uuid=get_user_name.uuid,
            user_one=get_user_name.display_name,
            post_id=post_id,
            mod_name=None,
            mod_uuid=None,
        )

        get_post.read = 1
        db.session.add(get_post)

        db.session.add(create_new_comment)
        db.session.commit()

        return jsonify({"status": "Success"})
