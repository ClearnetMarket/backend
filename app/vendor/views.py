from flask import request, session, jsonify

from app.vendor import vendor
from app import db
from app.common.decorators import login_required
from sqlalchemy.sql import func, or_
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
    Vendor_Orders

# end models


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

@vendor.route('/new-orders', methods=['GET'])
@login_required
def vendor_topbar_get_issues_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    user_id = session.get("user_id")

    neworders = db.session\
        .query(Vendor_Orders.new_order)\
        .filter(Vendor_Orders.vendor_id == user_id,
                Vendor_Orders.new_order == 1)\
        .count()
    return jsonify({
        "neworders": neworders,
    })

@vendor.route('/new-orders', methods=['GET'])
@login_required
def vendor_topbar_get_disputes_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    user_id = session.get("user_id")
    rdispute = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.completed == 0)\
        .filter(Vendor_Orders.vendor_id == user_id)\
        .filter(or_(
            Vendor_Orders.request_return != 0,
            Vendor_Orders.disputed_order == 1))\
        .count()
    return jsonify({
        "disputes": rdispute,
    })
