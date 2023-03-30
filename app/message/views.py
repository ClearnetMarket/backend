
from datetime import datetime
from flask import jsonify, request
from flask_login import current_user, login_required
from app.message import message
from app import db
from sqlalchemy import or_
from app.classes.auth import Auth_User
from app.classes.user_orders import User_Orders
from app.classes.message import \
    Message_Chat, \
    Message_Chat_Schema, \
    Message_Post
from app.common.notification import create_notification
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
        "success": 'success',
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

    if current_user.admin_role >= 5:
        get_msg_post = db.session \
            .query(Message_Chat) \
            .filter(Message_Chat.post_id == post_id) \
            .first()
    else:
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
        return jsonify({"error": "Error: Unauthorized"})
    
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

    if get_msg_post is None:
        return jsonify({"error": "Error:  Error finding chat message"}),200
    get_msg_post_comments = db.session \
        .query(Message_Chat) \
        .filter(Message_Chat.post_id == get_msg_post.post_id) \
        .order_by(Message_Chat.timestamp.desc()) \
        .all()

    comments_schema = Message_Chat_Schema(many=True)
    return jsonify(comments_schema.dump(get_msg_post_comments))


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

    get_comments = db.session\
        .query(Message_Chat)\
        .filter(or_(Message_Chat.user_one_uuid == get_post.user_one_uuid,
                    Message_Chat.user_two_uuid == get_post.user_two_uuid,
                    Message_Chat.mod_uuid == get_post.mod_uuid,
                    ))\
        .first()
    get_user_one = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == get_post.user_one_uuid)\
        .first()
    get_user_two = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == get_post.user_two_uuid)\
        .first()

    get_mod = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == get_post.mod_uuid)\
        .first()
    if get_mod is not None:
        the_mod_uuid = get_mod.uuid
        the_mod_username = get_mod.display_name

        if get_user_one.uuid == current_user.uuid:
            whocommented = 1
        elif get_user_two.uuid == current_user.uuid:
            whocommented = 2
        elif get_mod.uuid == current_user.uuid:
            whocommented = 3
        else:
            whocommented = 0
    else:
        the_mod_uuid = None
        the_mod_username = None

        if get_user_one.uuid == current_user.uuid:
            whocommented = 1
        elif get_user_two.uuid == current_user.uuid:
            whocommented = 2
        else:
            whocommented = 0

    if current_user.admin_role < 2:
        adminrole = 0
    else:
        adminrole = 1

    # if user isn't an admin
    create_new_comment = Message_Chat(
        timestamp=now,
        order_uuid=get_comments.order_uuid,
        item_uuid=get_comments.item_uuid,
        user_one=get_user_one.display_name,
        user_one_uuid=get_user_one.uuid,
        user_two=get_user_two.display_name,
        user_two_uuid=get_user_two.uuid,
        mod_name=the_mod_username,
        mod_uuid=the_mod_uuid,
        body=get_body,
        admin=adminrole,
        post_id=get_post.id,
        read=1,
        who_commented=whocommented,
    )

    create_notification(username=get_user_one.display_name,
             user_uuid=get_user_one.uuid,
             msg="You have a new comment on a message."
             )

    create_notification(username=get_user_one.display_name,
                 user_uuid=get_user_one.uuid,
                 msg="You have a new comment on a message."
                 )

    # commit to db

    db.session.add(get_post)
    db.session.add(create_new_comment)
    db.session.commit()

    return jsonify({"success": "Success"})


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
    if get_post is not None:
        return jsonify({"error": "Error:  Couldnt find post"})

    generic_message = "A dispute has been issued for this item."
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.uuid == order_uuid) \
        .first()

    # create a new post
    get_post = Message_Post(timestamp=now,
                            user_one_uuid=get_order.vendor_uuid,
                            user_two_uuid=get_order.customer_uuid,
                            mod_uuid = None
                            )
    db.session.add(get_post)
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
        post_id=get_post.id,
        admin=0,
        read=1,
        who_commented=0
    )

    create_notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="A dispute has been issued on an order."
                 )
    create_notification(username=get_order.customer_user_name,
                 user_uuid=get_order.customer_uuid,
                 msg="A dispute has been issued on an order."
                 )
    # update order to reflect post id and timer
    get_order.dispute_post_id = get_post.id

    # adding the timer so when a user doesn't drag it out
    get_order.disputed_timer = now

    # commit to database
    db.session.add(get_order)
    db.session.add(create_new_message)
    db.session.commit()
    return jsonify({"success": "Success"})


@message.route('/create/item', methods=['POST'])
@login_required
def message_create():
    """
    Creates a New Message.  No previous message should exist.
    """
    now = datetime.utcnow()
  
    get_body = request.json["body"]

    if "item_uuid" in request.json:
        item_uuid = request.json["item_uuid"]
    else:
        item_uuid = None

    # see if it is an order question or an item
    if "order_uuid" in request.json:
        order_uuid = request.json["order_uuid"]
    else:
        order_uuid = None

    # get the market item
    get_market_item = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.uuid == item_uuid) \
        .first()

    get_post = db.session \
        .query(Message_Chat) \
        .filter(Message_Chat.user_one_uuid == get_market_item.vendor_uuid) \
        .filter(Message_Chat.user_two_uuid == current_user.uuid) \
        .filter(Message_Chat.item_uuid == get_market_item.uuid) \
        .first()

    if get_post:
        post_id_of_msg = get_post.post_id
        get_post.read = 1
        db.session.add(get_post)
    else:

        # create a new post
        create_post = Message_Post(timestamp=now,
                                   user_one_uuid=get_market_item.vendor_uuid,
                                   user_two_uuid=current_user.uuid,
                                   mod_uuid=None
                                  )
        db.session.add(create_post)
        db.session.flush()
        post_id_of_msg = create_post.id

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
        post_id=post_id_of_msg,
        admin=0,
        read=1,
        who_commented=2
    )

    create_notification(username=get_market_item.vendor_display_name,
                         user_uuid=get_market_item.vendor_uuid,
                         msg="You have a new message from a customer."
                         )


    db.session.add(create_new_message)
    db.session.commit()
        
    return jsonify({"success": "Success"})