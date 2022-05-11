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
    Vendor_Notification, \
    Vendor_ExactAddress
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema
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

    # create vendor stats
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
    # create vendor exact address
    new_address = Vendor_ExactAddress(
                        uuid=current_user.uuid,
                        city='',
                        country=current_user.country,
                        state_or_provence='',
                        zip_code='',
                    )
    db.session.add(new_address)
    db.session.add(stats)
    db.session.add(current_user)
    db.session.commit()

    return jsonify({'user': {'user_id': current_user.uuid,
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
            .filter_by(type_of_feedback=1)\
            .order_by(Feedback_Feedback.timestamp.desc())\
            .limit(25)
        vendor_schema = Feedback_Feedback_Schema(many=True)
        return jsonify(vendor_schema.dump(vendor_feedback))


@vendor.route('/all-feedback/<string:vendor_uuid>', methods=['GET'])
def vendor_vendor_feedback_count(vendor_uuid):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_feedback = Feedback_Feedback.query\
            .filter_by(vendor_uuid=vendor_uuid)\
            .count()
        if vendor_feedback == 0:
            return jsonify({"total_feedback": 0,
                            'feedback_one': 0,
                            'feedback_two': 0,
                            'feedback_three': 0,
                            'feedback_four': 0,
                            'feedback_five': 0,
                            'feedback_six': 0,
                            'feedback_seven': 0,
                            'feedback_eight': 0,
                            'feedback_nine': 0,
                            'feedback_ten': 0,
                            })

        if vendor_feedback > 0:
            vendor_feedback_one = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=1)\
                .count()
            vendor_feedback_one_percent = (
                (int(vendor_feedback_one) / int(vendor_feedback))*100)

            vendor_feedback_two = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=2)\
                .count()
            vendor_feedback_two_percent = (
                (int(vendor_feedback_two) / int(vendor_feedback))*100)

            vendor_feedback_three = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=3)\
                .count()
            vendor_feedback_three_percent = (
                (int(vendor_feedback_three) / int(vendor_feedback))*100)

            vendor_feedback_four = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=4)\
                .count()
            vendor_feedback_four_percent = (
                (int(vendor_feedback_four) / int(vendor_feedback))*100)

            vendor_feedback_five = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=5)\
                .count()
            vendor_feedback_five_percent = (
                (int(vendor_feedback_five) / int(vendor_feedback))*100)

            vendor_feedback_six = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=6)\
                .count()
            vendor_feedback_six_percent = (
                (int(vendor_feedback_six) / int(vendor_feedback))*100)

            vendor_feedback_seven = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=7)\
                .count()
            vendor_feedback_seven_percent = (
                (int(vendor_feedback_seven) / int(vendor_feedback))*100)

            vendor_feedback_eight = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=8)\
                .count()
            vendor_feedback_eight_percent = (
                (int(vendor_feedback_eight) / int(vendor_feedback))*100)

            vendor_feedback_nine = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=9)\
                .count()
            vendor_feedback_nine_percent = (
                (int(vendor_feedback_nine) / int(vendor_feedback))*100)

            vendor_feedback_ten = Feedback_Feedback.query\
                .filter_by(vendor_uuid=vendor_uuid)\
                .filter_by(vendor_rating=10)\
                .count()
            vendor_feedback_ten_percent = (
                (int(vendor_feedback_ten) / int(vendor_feedback))*100)

        return jsonify({"total_feedback": vendor_feedback,
                        'feedback_one': vendor_feedback_one_percent,
                        'feedback_two': vendor_feedback_two_percent,
                        'feedback_three': vendor_feedback_three_percent,
                        'feedback_four': vendor_feedback_four_percent,
                        'feedback_five': vendor_feedback_five_percent,
                        'feedback_six': vendor_feedback_six_percent,
                        'feedback_seven': vendor_feedback_seven_percent,
                        'feedback_eight': vendor_feedback_eight_percent,
                        'feedback_nine': vendor_feedback_nine_percent,
                        'feedback_ten': vendor_feedback_ten_percent,
                        })


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
    vendor = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == vendor_id)\
        .first()

    vendor_name = vendor.username
    vendor_stats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(Profile_StatisticsVendor.vendor_uuid == vendor.uuid)\
        .first()

    vendor_rating = vendor_stats.avg_item_rating
    vendor_total_sales = vendor_stats.total_sales
    vendor_uuid = vendor_stats.vendor_uuid
    return jsonify({
        "vendorname": vendor_name,
        "vendoruuid": vendor_uuid,
        "vendorrating": vendor_rating,
        "vendortotalsales": vendor_total_sales,
    })


@vendor.route('/get/defaultaddress', methods=['GET'])
@login_required
def vendor_get_address():


    if request.method == 'GET':
        vendor_address = db.session\
            .query(Vendor_ExactAddress)\
            .filter(Vendor_ExactAddress.uuid == current_user.uuid)\
            .first()
        if vendor_address:
            city = vendor_address.city
            stateorprovence = vendor_address.state_or_provence
            zipcode = vendor_address.zip_code
        
            return jsonify({
                "city": city,
                "stateorprovence": stateorprovence,
                "zipcode": zipcode,
            })
        else:
            return jsonify({"status": 'error'}), 409

            


@vendor.route('/update/defaultaddress', methods=['PUT'])
@login_required
def vendor_update_address():
    """
    Returns all info about a user
    :return:
    """
    if request.method == 'PUT':
        if current_user.admin_role >= 1:
            vendor_address = Vendor_ExactAddress.query\
                .filter(Vendor_ExactAddress.uuid == current_user.uuid)\
                .first()
         
            if vendor_address:
     
                if "city" in request.json:
                    city = request.json["city"]
                else:
                    city = None
                if "stateorprovence" in request.json:
                    state_or_provence = request.json["stateorprovence"]
                else:
                    state_or_provence = None
                if "zip" in request.json:
                    zipcode = request.json["zip"]
                else:
                    zipcode = None        
                vendor_address.country = current_user.country
                vendor_address.city = city
                vendor_address.state_or_provence = state_or_provence
                vendor_address.zip_code = zipcode
                db.session.add(vendor_address)
                db.session.commit()
                return jsonify({"status": 'success'})
            else:
                return jsonify({"status": 'error'}), 409
        else:
            return jsonify({"status": 'error'}), 409


@vendor.route('/itemsforsale/<string:vendor_uuid>', methods=['GET'])
def vendor_profile_itemsforsale(vendor_uuid):
    """
    Grabs feedback of the vendor
    :return:
    """
    if request.method == 'GET':
        vendor_itemsforsale = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.vendor_uuid == vendor_uuid)\
            .limit(25)
        for f in vendor_itemsforsale:
            print(f.id)
        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(vendor_itemsforsale))
