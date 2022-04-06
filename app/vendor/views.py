from flask import request,  jsonify
from flask_login import current_user
from app.vendor import vendor
from app import db
import datetime
from app.common.decorators import login_required
# models
from app.classes.profile import \
    Profile_StatisticsVendor,\
    Profile_StatisticsVendor_Schema

from app.classes.feedback import \
    Feedback_Feedback,\
    Feedback_Feedback_Schema
from app.classes.vendor import \
    Vendor_Notification
from app.classes.auth import Auth_User
from app.classes.profile import Profile_StatisticsVendor

# end models


@vendor.route('/becomevendor', methods=['POST'])
@login_required
def vendor_signup():
    """
    Signs up user to become a vendor
    :return:
    """

    now = datetime.datetime.utcnow()
    current_user.admin = 1
    current_user.admin_role = 1
   
    stats = Profile_StatisticsVendor(
        username=current_user.username,
        vendorid=current_user.id,
        totalsales=0,
        totaltrades=0,
        totalreviews=0,
        startedselling=now,
        vendorrating=5,
        avgitemrating=0,
        diffpartners=0,
        disputecount=0,
        beenflagged=0,
        totalbtcspent=0,
        totalbtcrecieved=0,
        totalbtccashspent=0,
        totalbtccashrecieved=0,
        totalxmrspent=0,
        totalxmrrecieved=0,
        totalusdmade=0,
        vendor_uuid=current_user.uuid
    )
 
    db.session.add(stats)
   
    db.session.add(current_user)
    db.session.commit()

    return jsonify({ 'user': {'user_id': current_user.uuid,
                              'user_name': current_user.username,
                              'user_email': current_user.email,
                              'profile_image': current_user.profileimage,
                              'country': current_user.country,
                              'currency': current_user.currency,
                              'user_admin': 0,
                              'token': current_user.api_key
                              }})


@vendor.route('/vendor-stats/<string:vendor_id>', methods=['GET'])
def vendor_vendor_stats(vendor_id):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_stats = Profile_StatisticsVendor.query \
            .filter_by(vendorid=vendor_id) \
            .first()
        vendor_schema = Profile_StatisticsVendor_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_stats))


@vendor.route('/vendor-feedback/<string:vendor_uuid>', methods=['GET'])
def vendor_vendor_feedback(vendor_uuid):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_feedback = Feedback_Feedback.query\
            .filter_by(vendor_uuid=vendor_uuid)\
            .order_by(Feedback_Feedback.timestamp.desc())\
            .limit(25)
        vendor_schema = Feedback_Feedback_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_feedback))


@vendor.route('/all-feedback/', methods=['GET'])
@login_required
def vendor_vendor_feedback_count(vendor_id):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_feedback = Feedback_Feedback.query\
            .filter_by(vendorid=vendor_id)\
            .order_by(Feedback_Feedback.timestamp.desc())\
            .limit(25)
        vendor_schema = Feedback_Feedback_Schema(many=True)
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
    return jsonify({"count": new_orders})

@vendor.route('/new-orders-count/markasread', methods=['DELETE'])
@login_required
def vendor_topbar_get_orders_markasread():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    new_orders = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_orders == 1)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .all()
    for f in new_orders:
        db.session.delete(f)
    db.session.commit()
    return jsonify({"status": 'success'})

@vendor.route('/new-disputes-count', methods=['GET'])
@login_required
def vendor_topbar_get_disputes_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """

    new_disputes = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_disputes == 1)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({"count": new_disputes})


@vendor.route('/new-disputes-count/markasread', methods=['DELETE'])
@login_required
def vendor_topbar_get_disputes_markasread():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    new_disputes = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_disputes == 1)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .all()
    for f in new_disputes:
        db.session.delete(f)
    db.session.commit()
    return jsonify({"status": 'success'})

@vendor.route('/new-feedback-count', methods=['GET'])
@login_required
def vendor_topbar_get_feedback_count():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """

    new_feedback = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_feedback == 1)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .count()
    return jsonify({"count": new_feedback})


@vendor.route('/new-feedback-count/markasread', methods=['DELETE'])
@login_required
def vendor_topbar_get_feedback_markasread():
    """
    Gets the count for any new orders.  Used on topbar for vendors
    :return:
    """
    new_feedback = db.session\
        .query(Vendor_Notification)\
        .filter(Vendor_Notification.new_feedback == 1)\
        .filter(Vendor_Notification.user_id == current_user.id)\
        .all()
    for f in new_feedback:
        db.session.delete(f)
    db.session.commit()
    return jsonify({"status": 'success'})

@vendor.route('/vendoriteminfo/<string:vendor_id>', methods=['GET'])
def vendor_topbar_get_vendor_info(vendor_id):
    """
    Gets the vendor name, ratings count and sales count
    :return:
    """

    vendor = Auth_User.query.filter(Auth_User.uuid == vendor_id).first()

    vendor_name = vendor.username
    vendor_stats = Profile_StatisticsVendor.query\
        .filter(Profile_StatisticsVendor.vendorid == vendor.id)\
        .first()
    vendor_rating = vendor_stats.avgitemrating
    vendor_total_sales = vendor_stats.totalsales
    vendor_uuid = vendor_stats.vendor_uuid
    return jsonify({
        "vendorname": vendor_name,
        "vendoruuid": vendor_uuid,
        "vendorrating": vendor_rating,
        "vendortotalsales": vendor_total_sales,
    })

