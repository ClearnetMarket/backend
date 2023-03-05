from flask import jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import or_
from app.classes.user_orders import User_Orders
from app.message import message
from app import db
from datetime import datetime
from sqlalchemy import or_
from app.classes.auth import Auth_User
from app.classes.message import \
    Message_Chat, \
    Message_Chat_Schema, \
    Message_Post
from app.classes.notifications import Message_Notifications
from app.classes.item import Item_MarketItem


@message.route('/markasread/<int:post_id>', methods=['PUT'])
@login_required
def message_markasread(post_id):
    """
    Counts the number of messages a user has
    :return:
    """

    get_msg_post = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid)) \
        .filter(Message_Chat.post_id == post_id) \
        .filter(Message_Chat.read == 1) \
        .first()

    if get_msg_post:

        get_msg_post.read = 0

        db.session.add(get_msg_post)
        db.session.commit()

    return jsonify({
        "status": 'success',
    })



@message.route('/count', methods=['GET'])
@login_required
def message_count():
    """
    Counts the number of messages a user has
    :return:
    """

    get_count = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid)) \
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
    get_msgs_side = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid)) \
        .distinct(Message_Chat.post_id) \
        .order_by(Message_Chat.post_id.desc()) \
        .all()

    msg_schema = Message_Chat_Schema(many=True)

    return jsonify(msg_schema.dump(get_msgs_side))


@message.route('/main/post/<int:post_id>', methods=['GET'])
@login_required
def message_msg(post_id):
    """
    Returns the main first question asked  the vendor or party.
    :return:
    """
    get_msg_post = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid)) \
        .filter(Message_Chat.post_id == post_id) \
        .first()

    msg_schema = Message_Chat_Schema()
    return jsonify(msg_schema.dump(get_msg_post))


@message.route('/main/comment/<int:post_id>', methods=['GET'])
@login_required
def message_msg_comments(post_id):
    """
    Returns the comments of the main post by the post id
    :return:
    """
    get_msg_post = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid,
                    Message_Chat.mod_uuid == current_user.uuid,

                    )
                ) \
        .filter(Message_Chat.post_id == post_id) \
        .first()
    if get_msg_post is None:
        return jsonify({"status": "unauthorized"})
    else:
        get_msg_post_comments = db.session \
            .query(Message_Chat) \
            .filter(Message_Chat.post_id == post_id) \
            .order_by(Message_Chat.timestamp.desc()) \
            .all()

        comments_schema = Message_Chat_Schema(many=True)
        return jsonify(comments_schema.dump(get_msg_post_comments))


@message.route('/main/comment/orderuuid/<string:order_uuid>', methods=['GET'])
@login_required
def message_msg_comments_orderuuid(order_uuid):
    """
    Returns the comments of the main post by order id
    :return:
    """

    get_msg_post = db.session \
        .query(Message_Chat) \
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid,
                    Message_Chat.mod_uuid == current_user.uuid,
                    )
                ) \
        .filter(Message_Chat.order_uuid == order_uuid) \
        .first()

    if get_msg_post is not None:
        get_msg_post_comments = db.session \
            .query(Message_Chat) \
            .filter(Message_Chat.post_id == get_msg_post.post_id) \
            .order_by(Message_Chat.timestamp.desc()) \
            .all()

        comments_schema =Message_Chat_Schema(many=True)
        return jsonify(comments_schema.dump(get_msg_post_comments))


@message.route('/create/item', methods=['POST'])
@login_required
def message_create():
    """
    Creates a New Message.  No previous message can exist.
    :return:
    """
    now = datetime.utcnow()
  
    # json request variables
    get_user_two_uuid = request.json["user_two_uuid"]
    get_body = request.json["body"]
    if get_user_two_uuid == current_user.uuid:
        return jsonify({"error": "Cannot message yourself"}), 200

    if "item_uuid" in request.json:
        item_uuid = request.json["item_uuid"]
    else:
        item_uuid = None

    # see if it is an order question or an item
    if "order_uuid" in request.json:
        order_uuid = request.json["order_uuid"]
    else:
        order_uuid = None
        # check to see if mod is greater than 
        # 1
    # get the market item
    get_market_item = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.uuid == item_uuid) \
        .first()

    get_user_two_name = db.session \
        .query(Auth_User) \
        .filter(Auth_User.uuid == get_user_two_uuid) \
        .first()

    get_user_two_name_display = get_user_two_name.display_name

    # see if a post exists between two users
    # if it does create a comment .
    get_post = db.session \
        .query(Message_Chat) \
        .filter(Message_Chat.user_one_uuid == get_market_item.vendor_uuid) \
        .filter(Message_Chat.user_two_uuid == current_user.uuid) \
        .filter(Message_Chat.item_uuid == get_market_item.uuid) \
        .first()

    if get_post is None:
        # user one is always the vendor
        if get_market_item.vendor_uuid == get_user_two_uuid:

            newpost = Message_Post(timestamp=now)
            db.session.add(newpost)
            db.session.flush()

            create_new_message = Message_Chat(
                timestamp=now,
                order_uuid=order_uuid,
                item_uuid=item_uuid,
                user_one=get_market_item.vendor_display_name,
                user_one_uuid=get_market_item.vendor_uuid,
                user_two=current_user.display_name,
                user_two_uuid=current_user.uuid,
                mod_name=None,
                mod_uuid=None,
                body=get_body,
                post_id=newpost.id,
                admin=0,
                read=1
            )
            create_new_notification = Message_Notifications(
                type_of_notification=1,
                username=get_market_item.vendor_display_name,
                user_uuid=get_market_item.vendor_uuid,
                timestamp=now,
                read=1,
            )

        else:
            create_new_message = Message_Chat(
                timestamp=now,
                order_uuid=order_uuid,
                item_uuid=item_uuid,
                user_one=get_market_item.vendor_display_name,
                user_one_uuid=get_market_item.vendor_uuid,
                user_two=get_user_two_name_display,
                user_two_uuid=get_user_two_uuid,
                mod_name=None,
                mod_uuid=None,
                body=get_body,
                post_id=None,
                admin=0,
                read=1
            )
            create_new_notification = Message_Notifications(
                type_of_notification=1,
                username=get_user_two_name_display,
                user_uuid=get_user_two_uuid,
                timestamp=now,
                read=1,
            )
        
        # create new notification
        
        db.session.add(create_new_notification)
        db.session.add(create_new_message)
        db.session.commit()

    else:

        create_new_message = Message_Chat(
            timestamp=now,
            order_uuid=order_uuid,
            item_uuid=item_uuid,
            user_one=get_market_item.vendor_display_name,
            user_one_uuid=get_market_item.vendor_uuid,
            user_two=current_user.display_name,
            user_two_uuid=current_user.uuid,
            mod_name=None,
            mod_uuid=None,
            body=get_body,
            post_id=get_post.post_id,
            admin=0,
            read=1
        )
        create_new_notification = Message_Notifications(
            type_of_notification=1,
            username=get_market_item.vendor_display_name,
            user_uuid=get_market_item.vendor_uuid,
            timestamp=now,
            read=1,
        )
        
        # set main post to unread
        get_post.read = 1

        db.session.add(get_post)
        db.session.add(create_new_notification)
        db.session.add(create_new_message)
        db.session.commit()
        
    return jsonify({"status": "Success"})


@message.route('/create/comment/<int:post_id>', methods=['POST'])
@login_required
def message_comment(post_id):
    """
    Creates a New comment on an existing post
    :return:
    """
    now = datetime.utcnow()

    # get json data from request
    get_body = request.json["textbody"]

    # ensure post id is an int
    post_id = int(post_id)

    # get ori post
    get_post = db.session \
        .query(Message_Post) \
        .filter(Message_Post.id == post_id) \
        .first()
    get_other_comment = db.session\
        .query(Message_Chat)\
        .filter(or_(Message_Chat.user_one_uuid == current_user.uuid,
                    Message_Chat.user_two_uuid == current_user.uuid,
                    ))\
        .first()
    # see if one of the two users is in the convo or else cant talk in it
    if get_other_comment.user_one_uuid == current_user.uuid \
            or get_other_comment.user_two_uuid == current_user.uuid \
            or get_other_comment.mod_uuid == current_user.uuid:

        if get_other_comment.user_one_uuid == current_user.uuid:
            get_comment_user_one_name = current_user.uuid
            get_comment_user_one_uuid = current_user.display_name
            get_comment_user_two_name = None
            get_comment_user_two_uuid = None
        else:
            get_comment_user_one_name = None
            get_comment_user_one_uuid = None
            get_comment_user_two_name = current_user.uuid
            get_comment_user_two_uuid = current_user.display_name

        if current_user.admin_role < 2:
            
            # if user isnt an admin
            create_new_comment = Message_Chat(
                timestamp=now,
                order_uuid=get_other_comment.order_uuid,
                item_uuid=get_other_comment.item_uuid,
                user_one=get_comment_user_one_name,
                user_one_uuid=get_comment_user_one_uuid,
                user_two=get_comment_user_two_name,
                user_two_uuid=get_comment_user_two_uuid,
                mod_name=None,
                mod_uuid=None,
                body=get_body,
                admin=0,
                post_id=get_post.id,
                read=1
            )
        else:
            # user is an admin
            create_new_comment = Message_Chat(
                timestamp=now,
                order_uuid=get_other_comment.order_uuid,
                item_uuid=get_other_comment.item_uuid,
                user_one=None,
                user_one_uuid=None,
                user_two=None,
                user_two_uuid=None,
                mod_name=current_user.display_name,
                mod_uuid=current_user.uuid,
                body=get_body,
                admin=1,
                post_id=get_post.id,
                read=1
            )


        create_new_notification_vendor = Message_Notifications(
            type_of_notification=1,
            username=get_comment_user_one_name,
            user_uuid=get_comment_user_one_uuid,
            timestamp=now,
            read=1,
        )
        create_new_notification_customer = Message_Notifications(
            type_of_notification=1,
            username=get_comment_user_two_name,
            user_uuid=get_comment_user_two_uuid,
            timestamp=now,
            read=1,
        )
        # commit to db
        db.session.add(create_new_notification_vendor)
        db.session.add(create_new_notification_customer)
        db.session.add(get_post)
        db.session.add(create_new_comment)
        db.session.commit()

        return jsonify({"status": "Success"})

    # if its not users or mod return an error
    else:
        return jsonify({"status": "error"})


@message.route('/create/dispute/<string:order_uuid>', methods=['POST'])
@login_required
def create_new_post_dispute(order_uuid):
    """
    This function is called when a dispute is issued.  Its only created
    after the button is placed in orders page.  
    It creates a generic message and  fills the post field.

    """
    now = datetime.utcnow()

    # see if a post already exists
    get_post = db.session \
        .query(Message_Chat) \
        .filter(Message_Chat.order_uuid == order_uuid) \
        .first()

    # if no post exists
    if get_post is None:

        generic_message = "A dispute has been issued."
        
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.uuid == order_uuid) \
            .first()

        # create a new post
        newpost = Message_Post(timestamp=now)
        db.session.add(newpost)

        # pre commit to database
        db.session.flush()

        # create a new main message thats generic
        create_new_message = Message_Chat(
            timestamp=now,
            order_uuid=order_uuid,
            item_uuid=get_order.item_uuid,
            user_one=get_order.vendor_user_name,
            user_one_uuid=get_order.vendor_uuid,
            user_two=get_order.customer_user_name,
            user_two_uuid=get_order.customer_uuid,
            mod_name=None,
            mod_uuid=None,
            body=generic_message,
            post_id=newpost.id,
            admin=0,
            read=1
        )

        create_new_notification_vendor = Message_Notifications(
            type_of_notification=1,
            username=get_order.vendor_user_name,
            user_uuid=get_order.vendor_uuid,
            timestamp=now,
            read=1,
        )
        create_new_notification_customer = Message_Notifications(
            type_of_notification=1,
            username=get_order.customer_user_name,
            user_uuid=get_order.customer_uuid,
            timestamp=now,
            read=1,
        )
        
        # update order to reflect post id and timer
        get_order.dispute_post_id = newpost.id

        # adding the timer so when a user doesnt drag it out
        get_order.disputed_timer = now

        # commit to database
        db.session.add(create_new_notification_customer)
        db.session.add(create_new_notification_vendor)
        db.session.add(get_order)
        db.session.add(create_new_message)
        db.session.commit()
        return jsonify({"status": "Success"})
    else:
        return jsonify({"status": "error"})
