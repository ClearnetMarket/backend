from flask import jsonify
from flask_login import current_user
from app.customerservice import customerservice
from app import db
from sqlalchemy import or_
from app.common.decorators import login_required

# models
from app.classes.service import \
    Service_Issue

from app.classes.user_orders import User_Orders
# End Models


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
        .filter(Service_Issue.status == 0).order_by(Service_Issue.timestamp.desc())\
        .count()
    return jsonify({
        "serviceissues": service_issues,
    })