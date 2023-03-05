
from flask import request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.moderator import moderator
from app import db

from app.classes.user_orders import\
    User_Orders,\
    User_Orders_Schema
from app.classes.feedback import\
    Feedback_Feedback,\
    Feedback_Feedback_Schema
from app.classes.message import\
    Message_Chat
from app.classes.service import \
    Service_Issue,\
    Service_Ticket,\
    Service_Tickets_Comments,\
    Service_Tickets_Comments_Schema,\
    Service_Ticket_Schema
from app.classes.auth import Auth_User
from app.wallet_btc.wallet_btc_moderator import finalize_order_dispute_btc
from app.wallet_bch.wallet_bch_moderator import finalize_order_dispute_bch
from app.wallet_xmr.wallet_xmr_moderator import finalize_order_dispute_xmr


@moderator.route('/create/ticket/comment', methods=['POST'])
@login_required
def create_comment_to_ticket():
    """
    Creates a ticket for the user when they have an issue and leaves a first comment
    :return:
    """
    now = datetime.utcnow()

    user = db.session\
        .query(Auth_User) \
        .filter(Auth_User.id == current_user.id)\
        .first()
    if user.admin > 5:
        adminrole = 1
    else:
        adminrole = 0

    # get the body of text for message
    textbody = request.json["textbody"]
    # get the txt id
    ticket_uuid = request.json["ticketid"]

    # get main ticket so we can update read status
    get_main_ticket = db.session\
        .query(Service_Ticket)\
        .filter(Service_Ticket.uuid == ticket_uuid)\
        .first()

    # set status of ticket to read
    get_main_ticket.status = 2

    db.session.add(get_main_ticket)

    # create a comment
    user_ticket_comment = Service_Tickets_Comments(
        author=user.display_name,
        uuid=ticket_uuid,
        author_uuid=user.uuid,
        timestamp=now,
        admin=adminrole,
        text_body=textbody,
    )

    db.session.add(user_ticket_comment)
    db.session.commit()

    return jsonify({"ticket": user_ticket_comment.uuid})




@moderator.route('/ticket/<string:ticketuuid>', methods=['GET'])
@login_required
def get_ticket_mod(ticketuuid):
    """
    Gets the specific ticket info
    :return:
    """

    get_ticket = str(ticketuuid)
    

    user_tickets = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.uuid == get_ticket) \
        .order_by(Service_Ticket.timestamp.desc())\
        .first()
   
    comments_schema = Service_Ticket_Schema()
    return jsonify(comments_schema.dump(user_tickets))


@moderator.route('/ticket/messages/<string:ticketuuid>', methods=['GET'])
@login_required
def ticket_issue_messages(ticketuuid):

    """
    Gets the specific ticket info
    :return:
    """
    get_ticket = str(ticketuuid)

    user_tickets = db.session \
        .query(Service_Tickets_Comments) \
        .filter(Service_Tickets_Comments.uuid == get_ticket) \
        .order_by(Service_Tickets_Comments.timestamp.desc())\
        .all()

    comments_schema = Service_Tickets_Comments_Schema(many=True)
    return jsonify(comments_schema.dump(user_tickets))


@moderator.route('/ticket/close/<string:uuid>', methods=['PUT'])
@login_required
def ticket_mark_closed(uuid):
    """
    Mark a ticket as closed
    :return:
    """

    user_ticket = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.uuid == uuid) \
        .first()
    user_ticket.status = 0
    
    db.session.add(user_ticket)
    db.session.commit()
        
    return jsonify({"status": "success"})




@moderator.route('/dispute/settle/<string:uuid>', methods=['POST'])
@login_required
def mark_dispute_finished(uuid):
    """
    FInalizes an order with percent to each customer
    :return:
    """
    if request.method == 'POST':
   
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.moderator_uuid == current_user.uuid) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})
       
        if "percenttovendor" in request.json:
            percent_to_vendor_json = request.json["percenttovendor"]
            percent_to_vendor = int(percent_to_vendor_json)
        else:
            return jsonify({"status": "error"})
        if "percenttocustomer" in request.json:
            percent_to_customer_json = request.json["percenttocustomer"]
            percent_to_customer = int(percent_to_customer_json)
       
        else:
            return jsonify({"status": "error"})
        if get_order:
            if get_order.digital_currency == 1:
                finalize_order_dispute_btc(order_uuid=get_order.uuid,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            if get_order.digital_currency == 2:
                finalize_order_dispute_bch(order_uuid=get_order.uuid,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            if get_order.digital_currency == 3:
                finalize_order_dispute_xmr(order_uuid=get_order.uuid,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            get_order.overall_status = 10

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})


@moderator.route('/dispute/canceldispute/open/<string:uuid>', methods=['GET'])
@login_required
def mark_dispute_cancelled_still_open(uuid):
    """
    Brings an order to open status
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.moderator_uuid == current_user.uuid) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.overall_status = 3

        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})


@moderator.route('/dispute/canceldispute/closed/<string:uuid>', methods=['GET'])
@login_required
def mark_dispute_cancelled_still_closed(uuid):
    """
    Brings an order to closed status
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.moderator_uuid == current_user.uuid) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.overall_status = 10

        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})


@moderator.route('/dispute/extend/<string:uuid>', methods=['GET'])
@login_required
def extend_dispute_time(uuid):
    """
    Extends order for more time.  Will need to add into crons file
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.moderator_uuid == current_user.uuid) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.extended_timer = 1
    
        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})

@moderator.route('/postdisputemsg/<string:uuid>', methods=['POST'])
@login_required
def add_message_after_dispute(uuid):
    """
    Gets the order for the moderator
    :return:
    """
    if request.method == 'POST':
        if current_user.admin_role >= 2:
            # get the generic user order model
            get_order = db.session \
                .query(User_Orders) \
                .filter(User_Orders.moderator_uuid == current_user.uuid) \
                .filter(User_Orders.uuid == uuid) \
                .first()
            if "textbody" in request.json:
                msg_json = request.json["textbody"]
                msg = str(msg_json)
                get_order.msg = msg

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})


@moderator.route('/orderinfo/<string:uuid>', methods=['GET'])
@login_required
def get_order_model(uuid):
    """
    Gets the order for the moderator
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            # get the generic user order model
            get_order = db.session \
                .query(User_Orders) \
                .filter(User_Orders.uuid == uuid) \
                .first()
            # return its json data
            item_schema = User_Orders_Schema()
            return jsonify(item_schema.dump(get_order))


@moderator.route('/customer/ratings/<string:uuid>', methods=['GET'])
@login_required
def get_customer_ratings(uuid):
    """
    Gets the customer ratings.
     2= customer 
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            # get customer ratings
            get_user_ratings = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.customer_uuid == uuid)\
                .filter(Feedback_Feedback.type_of_feedback == 2)\
                .order_by(Feedback_Feedback.timestamp.desc())\
                .limit(20)
            # return jsonify schema
            feedback_schema = Feedback_Feedback_Schema(many=True)
            return jsonify(feedback_schema.dump(get_user_ratings))


@moderator.route('/vendor/ratings/<string:uuid>', methods=['GET'])
@login_required
def get_vendor_ratings(uuid):
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            # get vendor ratings
            get_user_ratings = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.vendor_uuid == uuid)\
                .filter(Feedback_Feedback.type_of_feedback == 1)\
                .order_by(Feedback_Feedback.timestamp.desc())\
                .limit(20)
            # return jsonify scheme
            feedback_schema = Feedback_Feedback_Schema(many=True)
            return jsonify(feedback_schema.dump(get_user_ratings))





##TICKETS
@moderator.route('/tickets/stats', methods=['GET'])
@login_required
def ticket_stats():
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if not current_user.admin_role == 10:
            return jsonify({"status": "unauthorized"})
        else:
            user_tickets_count = db.session \
                .query(Service_Ticket) \
                .order_by(Service_Ticket.timestamp.desc())\
                .count()
            user_tickets_open = db.session \
                .query(Service_Ticket) \
                .filter(Service_Ticket.status == 1)\
                .order_by(Service_Ticket.timestamp.desc())\
                .count()
            user_tickets_completed = db.session \
                .query(Service_Ticket) \
                .filter(Service_Ticket.status == 2)\
                .order_by(Service_Ticket.timestamp.desc())\
                .count()

            return jsonify({
                            "count": user_tickets_count,
                            "open": user_tickets_open,
                            "completed": user_tickets_completed,
                            })

@moderator.route('/dispute/stats', methods=['GET'])
@login_required
def disputes_stats():
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role != 10:
            return jsonify({"status": "unauthorized"})
        else:
            user_disputes_count = db.session \
                .query(User_Orders) \
                .filter(User_Orders.overall_status == 8)\
                .count()
           

            return jsonify({
                "count": user_disputes_count,
            
            })

@moderator.route('/getalltickets', methods=['GET'])
@login_required
def get_all_tickets():
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if not current_user.admin_role == 10:
            return jsonify({"status": "unauthorized"})
        else:
            user_tickets = db.session \
                .query(Service_Ticket) \
                .order_by(Service_Ticket.timestamp.desc())\
                .all()
          
            comments_schema = Service_Ticket_Schema(many=True)
            return jsonify(comments_schema.dump(user_tickets))


@moderator.route('/takeonmod/<string:uuid>', methods=['GET'])
@login_required
def become_mod_of_order(uuid):
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role <= 2:
            return jsonify({"status": "unauthorized"})
        else:
            # get the order from the uuid
            get_order = db.session \
                .query(User_Orders) \
                .filter(User_Orders.uuid == uuid) \
                .filter(User_Orders.moderator_uuid == None)\
                .first()
            # set current moderator as mod
            get_order.moderator_uuid = current_user.uuid
            get_order.moderator_user_name = current_user.display_name
            # add to db
            db.session.add(get_order)
            # get the message post that is currently none for mod uuid
            get_message_post = db.session\
                .query(Message_Chat)\
                .filter(Message_Chat.order_uuid == get_order.uuid)\
                .first()
            # set post mod id as current id
            get_message_post.mod_uuid = current_user.uuid
           
            # add to db
            db.session.add(get_message_post)
            # commit to db
            db.session.commit()

            return jsonify({"status": "success"})


@moderator.route('/disputes/available', methods=['GET'])
@login_required
def get_disputes_main_page_need_mod():
    """
    This gets currently open disputes that appears on the moderator home page
    :return:
    """
    if request.method == 'GET':
        # see if current user is a mod

        if current_user.admin_role >= 2:
            # query the disputes
            get_disputes = db.session \
                .query(User_Orders) \
                .filter(User_Orders.overall_status == 8) \
                .filter(User_Orders.moderator_uuid == None)\
                .all()
            disputes_schema = User_Orders_Schema(many=True)
            return jsonify(disputes_schema.dump(get_disputes))
        else:
            return jsonify({"status": "error"})


@moderator.route('/disputes/modded', methods=['GET'])
@login_required
def get_disputes_main_page_has_mod():
    """
    This gets currently open disputes that appears on the moderator home page
    :return:
    """
    if request.method == 'GET':
        # see if current user is a mod
        if current_user.admin_role >= 2:
            # query the disputes
            get_disputes = db.session \
                .query(User_Orders) \
                .filter(User_Orders.overall_status == 8) \
                .filter(User_Orders.moderator_uuid != None)\
                .all()
            disputes_schema = User_Orders_Schema(many=True)
            return jsonify(disputes_schema.dump(get_disputes))
        else:
            return jsonify({"status": "error"})
