from flask import jsonify, request
from flask_login import current_user
from app.customerservice import customerservice
from app import db
from sqlalchemy import or_
from app.common.decorators import login_required
from datetime import datetime
# models
from app.classes.service import \
    Service_Issue,\
    Service_Ticket,\
    Service_Tickets_Comments,\
    Service_Tickets_Comments_Schema,\
    Service_Ticket_Schema
from app.classes.auth import Auth_User
from app.classes.user_orders import User_Orders
# End Models


@customerservice.route('/markasread/<string:ticketuuid>', methods=['PUT'])
@login_required
def ticket_mark_as_read(ticketuuid):
    """
    Marks a ticket as read.  Changes status
    :return:
    """

    user_tickets = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.author_uuid == current_user.uuid) \
        .filter(Service_Ticket.uuid == ticketuuid) \
        .order_by(Service_Ticket.timestamp.desc())\
        .first()
        
    if user_tickets.status == 0:
        user_tickets.status = 0
    else:
        user_tickets.status = 1

    db.session.add(user_tickets)
    db.session.commit()
    
    return jsonify({"status": "success"})




@customerservice.route('/tickets', methods=['GET'])
@login_required
def user_get_tickets():
    """
    Gets the issues for the sidebar so they can click and view previous issues
    :return:
    """

    user_tickets = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.author_uuid == current_user.uuid) \
        .order_by(Service_Ticket.timestamp.desc())\
        .all()

    comments_schema = Service_Ticket_Schema(many=True)
    return jsonify(comments_schema.dump(user_tickets))



@customerservice.route('/tickets/count', methods=['GET'])
@login_required
def user_get_ticket_count():
    """
    Gets the issues for the sidebar so they can click and view previous issues
    :return:
    """

    user_tickets = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.author_uuid == current_user.uuid) \
        .filter(Service_Ticket.status == 1) \
        .count()

    return jsonify({"tickets": user_tickets})
    

@customerservice.route('/ticket', methods=['POST'])
@login_required
def ticket_issue():
    """
    Gets the specific ticket info
    :return:
    """
 
    get_ticket = request.json['ticketid']
    print(get_ticket)
    user = db.session\
        .query(Auth_User) \
        .filter(Auth_User.id == current_user.id)\
        .first()
        
    user_tickets = db.session \
        .query(Service_Ticket) \
        .filter(Service_Ticket.uuid == get_ticket) \
        .filter(Service_Ticket.author_uuid == user.uuid) \
        .order_by(Service_Ticket.timestamp.desc())\
        .first()
    print(user_tickets.author_uuid)
    comments_schema = Service_Ticket_Schema()
    return jsonify(comments_schema.dump(user_tickets))
    
@customerservice.route('/ticket/messages', methods=['POST'])
@login_required
def ticket_issue_messages():
    """
    Gets the specific ticket info
    :return:
    """

    get_ticket = request.json['ticketid']


    user_tickets = db.session \
        .query(Service_Tickets_Comments) \
        .filter(Service_Tickets_Comments.uuid == get_ticket) \
        .order_by(Service_Tickets_Comments.timestamp.desc())\
        .all()

    comments_schema = Service_Tickets_Comments_Schema(many=True)
    return jsonify(comments_schema.dump(user_tickets))

@customerservice.route('/create/ticket', methods=['POST'])
@login_required
def user_create_ticket():
    """
    Creates a ticket for the first time. when they have an issue and leaves a first comment
    :return:
    """
    now = datetime.utcnow()
    
    user = db.session\
        .query(Auth_User) \
        .filter(Auth_User.id == current_user.id)\
        .first()

    # get the body of text for message
    textbody = request.json["textbody"]
    subject = request.json["subject"]

    # create a new ticket
    user_ticket = Service_Ticket(
        author=user.display_name,
        author_uuid=user.uuid,
        timestamp=now,
        admin=0,
        status=1,
        subject=subject
   
    )
    db.session.add(user_ticket)
    db.session.flush()
    
    # create a comment
    user_ticket_comment = Service_Tickets_Comments(
        author=user.display_name,
        uuid=user_ticket.uuid,
        author_uuid=user.uuid,
        timestamp=now,
        admin=0,
        text_body=textbody,
    ) 

    db.session.add(user_ticket_comment)
    db.session.commit()
        
    return jsonify({"ticket": user_ticket.uuid})
    
    
@customerservice.route('/create/ticket/comment', methods=['POST'])
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
    get_main_ticket.status = 3
    
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



    
    
    
    
    
    
    
    
    
@customerservice.route('/vendor-topbar-get-issues-count', methods=['GET'])
@login_required
def vendor_topbar_get_issues_count():
    """
    Gets the count of vendor order issues.  Notification bar at top
    :return:
    """
    user_id = current_user.id
    myorderscount = db.session\
        .query(User_Orders)\
        .filter(User_Orders.customer_id == user_id.id)\
        .filter(or_(User_Orders.disputed_order == 1, User_Orders.request_return == 2))\
        .count()
    return jsonify({
        "vendorissues": myorderscount,
    })


@customerservice.route('/customer-topbar-get-issues-count', methods=['GET'])
@login_required
def customer_topbar_get_issues_count():
    """
    Gets the count of customer issues.  Notification bar at top
    :return:
    """
    user_id = current_user.id
    service_issues = db.session \
        .query(Service_Issue) \
        .filter(Service_Issue.author_id == user_id) \
        .filter(Service_Issue.status == 0)\
        .order_by(Service_Issue.timestamp.desc())\
        .count()
    return jsonify({
        "serviceissues": service_issues,
    })
    
    
    