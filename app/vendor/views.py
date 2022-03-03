from flask import request, session, jsonify
from flask_login import current_user
from app.vendor import vendor
from app import db
from app.common.decorators import login_required
from sqlalchemy.sql import or_
# models
from app.classes.profile import \
    Profile_StatisticsVendor,\
    Profile_StatisticsVendor_Schema
from app.classes.achievements import\
    Achievements_UserAchievements,\
    Achievements_UserAchievements_Schema,\
    Achievements_WhichAch,\
    Achievements_WhichAch_Schema
from app.classes.userdata import \
    UserData_Feedback,\
    UserData_Feedback_Schema
from app.classes.vendor import \
    Vendor_Orders,\
    Vendor_Notification


# end models
@vendor.route('/become-vendor', methods=['POST'])
@login_required
def vendor_signup():
    """
    Signs up user to become a vendor
    :return:
    """
    if request.method == 'GET':
        current_user.admin = 1
        current_user.admin_role = 1
        db.session.add(current_user)
        db.session.commit()
        return jsonify({
            "status": 'success',
        })



@vendor.route('/vendor-stats/<string:vendor_id>', methods=['GET'])
def vendor_vendor_stats(vendor_id):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_stats = Profile_StatisticsVendor \
            .filter_by(vendorid=vendor_id) \
            .first()
        vendor_schema = Profile_StatisticsVendor_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_stats))


@vendor.route('/vendor-feedback/<string:vendor_id>', methods=['GET'])
def vendor_vendor_feedback(vendor_id):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_feedback = UserData_Feedback.query\
            .filter_by(vendorid=vendor_id)\
            .order_by(UserData_Feedback.timestamp.desc())\
            .limit(25)
        vendor_schema = UserData_Feedback_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_feedback))


@vendor.route('/vendor-achievements/<string:vendor_id>', methods=['GET'])
def vendor_vendor_achievements(vendor_id):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_get_achs = Achievements_UserAchievements.query \
            .filter(Achievements_UserAchievements.user_id==vendor_id) \
            .first()
        vendor_schema = Achievements_UserAchievements_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_get_achs))


@vendor.route('/vendor-feedback/<string:vendor_id>', methods=['GET'])
def vendor_vendor_main_achievement(vendor_id):
    """
    Grabs main achievement of vendor
    :return:
    """
    if request.method == 'GET':
        vendorach = Achievements_WhichAch.query\
            .filter_by(user_id=vendor_id)\
            .first()
        vendor_schema = Achievements_WhichAch_Schema(many=True)
        return jsonify(vendor_schema.dump(vendorach))


@vendor.route('/all-feedback/', methods=['GET'])
@login_required
def vendor_vendor_feedback_count(vendor_id):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_feedback = UserData_Feedback.query\
            .filter_by(vendorid=vendor_id)\
            .order_by(UserData_Feedback.timestamp.desc())\
            .limit(25)
        vendor_schema = UserData_Feedback_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_feedback))


@vendor.route('/new-orders-count', methods=['GET'])
@login_required
def vendor_topbar_get_orders_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    new_orders = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_orders != 0)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({
        "count": new_orders,
    })

@vendor.route('/new-disputes-count', methods=['GET'])
@login_required
def vendor_topbar_get_disputes_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
   
    new_disputes = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_disputes != 0)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({
        "count": new_disputes,
    })


@vendor.route('/new-feedback-count', methods=['GET'])
@login_required
def vendor_topbar_get_feedback_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """

    new_feedback = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_feedback != 0)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({
        "count": new_feedback,
    })


@vendor.route('/new-feedback-count', methods=['GET'])
@login_required
def vendor_topbar_get_returns_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """

    new_returns = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_returns != 0)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({
        "count": new_returns,
    })


