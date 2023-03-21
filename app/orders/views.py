
from decimal import Decimal
from operator import or_
from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import  timedelta
from app.orders import orders
from app import db
from app.common.notification import create_notification
# models
from app.classes.user_orders import User_Orders, User_Orders_Schema
from app.classes.feedback import Feedback_Feedback
from app.classes.profile import Profile_StatisticsVendor
from app.wallet_btc.wallet_btc_work import finalize_order_btc
from app.wallet_bch.wallet_bch_work import finalize_order_bch
from app.wallet_xmr.wallet_xmr_work import finalize_order_xmr


@orders.route('', methods=['GET'])
@login_required
def get_user_orders():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    user_orders = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .order_by(User_Orders.created.desc()) \
        .limit(10)

    item_schema = User_Orders_Schema(many=True)
    return jsonify(item_schema.dump(user_orders))

@orders.route('/<string:uuid>', methods=['GET'])
@login_required
def get_order_model(uuid):
    """
    Gets the order for the customer
    :return:
    """
    # get order
    # user must be customer or vendor

    get_order = db.session \
        .query(User_Orders) \
        .filter(or_(User_Orders.customer_id == current_user.id,
                    User_Orders.vendor_id == current_user.id)) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    # if order exists
    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200
        # return schema
    item_schema = User_Orders_Schema()
    return jsonify(item_schema.dump(get_order))


@orders.route('/autofinalize/<string:uuid>', methods=['GET'])
@login_required
def get_order_autofinalize_time(uuid):
    """
    Gets the order for the customer
    :return:
    """
    # get order
    # user must be customer or vendor

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    # if order exists
    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200
    # return schema
    whenbought = get_order.created
    twentydaysfromorder = (whenbought + timedelta(days=20))

    return jsonify({
        "success": "success",
        "status":twentydaysfromorder})


@orders.route('/count', methods=['GET'])
@login_required
def get_user_orders_count():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    user_orders_count = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .count()

    if user_orders_count is None:
        return jsonify({"error": "Error: Order not found"}), 200
    return jsonify({"count": user_orders_count})


@orders.route('/vendor/<string:uuid>', methods=['GET'])
@login_required
def get_order_vendor(uuid):
    """
    Gets the order for the vendor
    :return:
    """

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.vendor_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    if get_order is None:
         return jsonify({"error": "Error: Order not found"}), 200
    item_schema = User_Orders_Schema()
    return jsonify(item_schema.dump(get_order))


@orders.route('/feedback/score/<string:uuid>', methods=['POST'])
@login_required
def order_feedback_score(uuid):
    """
    CUSTOMER
    Post  feedback  given by customer
    # type of feedback = 1
    :return:
    """

    # get the request json
    try:
        if request.json["vendorrating"]:
            vendor_rating = request.json["vendorrating"]
        else:
            return jsonify({"error": "Error"}), 200
    except Exception:
        return jsonify({"error": "Error"}), 200


    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    # get feedback (might not be any)
    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.author_uuid == current_user.uuid) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()

    # if order exists else
    if get_order is None:
        return jsonify({"error": "Error"}), 200

    # set feedback to nearest integer
    if 0 <= Decimal(vendor_rating) <= 10:
        vendorrating = int(vendor_rating)
    else:
        vendorrating = 0
    # set feedback to nearest integer

    # feedback exists just add the review
    get_order.type_of_feedback = vendor_rating
    get_order.author_uuid = current_user.uuid
    get_order.vendor_feedback = 1
    get_feedback.vendor_rating = vendorrating
    db.session.add(get_order)

    db.session.add(get_feedback)
    db.session.flush()

    db.session.commit()

    return jsonify({"success": "success"})


@orders.route('/feedback/review/<string:uuid>', methods=['POST'])
@login_required
def order_feedback_review(uuid):
    """
    CUSTOMER
    Post feedback written review
    feedback given by customer
    # type of feedback = 1
    :return:
    """
    if request.json["review"]:
        review_by_user = request.json["review"]
    else:
        return jsonify({"error": "Error"}), 200

    # get the order by current customer
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    # get feedback (might not be any)
    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.author_uuid == current_user.uuid) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()
    # if order exists else
    get_stats_vendor = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(Profile_StatisticsVendor.vendor_uuid == current_user.uuid)\
        .first()
    if get_order is None:
        return jsonify({"error": "Error:  Order not found"}), 200

    # Add stats
    vendor_current_review_count = get_stats_vendor.total_reviews
    vendor_new_amount = vendor_current_review_count + 1
    get_stats_vendor.total_reviews = vendor_new_amount
    db.session.add()

    # feedback exists just add the review
    get_order.review_of_vendor = review_by_user
    get_order.author_uuid = current_user.uuid

    get_order.vendor_feedback = 1
    db.session.add(get_order)

    # update feedback
    get_feedback.review_of_vendor = review_by_user
    db.session.add(get_feedback)

    db.session.commit()

    return jsonify({"success": "success"})


@orders.route('/vendor/feedback/score/<string:uuid>', methods=['POST'])
@login_required
def order_vendor_feedback_score(uuid):
    """
    VENDOR
    Post feedback  given by vendor
    # type of feedback = 2
    :return:
    """

    # get the request json
    if request.json["rating"]:
        customer_rating = request.json["rating"]
    else:
        return jsonify({"error": "error getting rating"}), 200

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.vendor_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    # get feedback (might not be any)
    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.author_uuid == current_user.uuid) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()

    # if order exists else
    get_stats_buyer = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(Profile_StatisticsVendor.user_uuid == current_user.uuid)\
        .first()

    # if order exists
    if get_order is None:
        return jsonify({"error": "Error"}), 200
        # set feedback to nearest integer
    if 0 <= Decimal(customer_rating) <= 10:
        customerrating = int(customer_rating)
    else:
        customerrating = 1

    # Add stats
    buyer_current_review_count = get_stats_buyer.total_reviews
    vendor_new_amount = buyer_current_review_count + 1
    get_stats_buyer.total_reviews = vendor_new_amount
    db.session.add()

    # modify order
    get_order.author_uuid = current_user.uuid
    get_order.customer_rating = customerrating
    db.session.add(get_order)

    # add the review
    get_feedback.customer_rating = customerrating
    db.session.add(get_feedback)

    # if both conditions are met set it as review added
    # this ensures proper review is added not just half


    create_notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="Your have a new feedback."
                 )

    if get_feedback.review_of_customer is not None\
        and get_feedback.customer_rating is not None:
        get_order.user_feedback = 1
        db.session.add(get_order)
    db.session.commit()

    return jsonify({"success": "success"})



@orders.route('/vendor/feedback/review/<string:uuid>', methods=['POST'])
@login_required
def order_vendor_feedback_review(uuid):
    """
    VENDOR
    Post feedback written review
    feedback given by vendor

    # type of feedback = 2
    :return:
    """

    try:
        if request:
            review_by_user = request.json["review"]
        else:
            return jsonify({"error": "Error"}), 200
    except:
        return jsonify({"error": "Error"}), 200

    # get the order by current customer
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.vendor_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()

    # get feedback (might not be any)
    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.author_uuid == current_user.uuid) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()

    # if order exists else
    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200

    # if no feedback exists
    # Note... vendor rating is none

    get_order.author_uuid = current_user.uuid
    get_order.review_of_customer = review_by_user

    db.session.add(get_order)

    # feedback exists just add the review
    get_feedback.review_of_customer = review_by_user
    db.session.add(get_feedback)

    # if both conditions are met set it as review added
    # this ensures proper review is added not just hhalf

    if get_feedback:
        if get_feedback.review_of_customer is not None\
            and get_feedback.customer_rating is not None:
            get_order.user_feedback = 1
            db.session.add(get_order)

    db.session.commit()

    return jsonify({"success": "success"})


@orders.route('/feedback/get/<string:uuid>', methods=['GET'])
@login_required
def get_order_feedback(uuid):
    """
    Get feedback of item from customer perspective on an order
    :return:
    """


    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()

    if get_order is None:
        return jsonify({"error": "Error: Order not Found"}), 200

    if get_feedback is None:
        return jsonify({"error": 'Error: Feedback not found'})

    return jsonify({
        "success": 'success',
        "item_rating": get_feedback.item_rating,
        "vendor_rating": get_feedback.vendor_rating,
        "review": get_feedback.review_of_vendor,
    })


@orders.route('/feedback/get/vendor/<string:uuid>', methods=['GET'])
@login_required
def get_order_feedback_vendor(uuid):
    """
    Get feedback of item from customer perspective on an order
    :return:
    """

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.uuid == uuid) \
        .first()

    get_feedback = db.session \
        .query(Feedback_Feedback) \
        .filter(Feedback_Feedback.author_uuid == current_user.uuid) \
        .filter(Feedback_Feedback.order_uuid == uuid) \
        .first()
    if get_order is None:
        return jsonify({"error": "Error: Order not Found"}), 200

    if get_feedback is None:
        return jsonify({"error": 'Error: Feedback not found'})

    if get_feedback.customer_rating == None:
        rated = 'None'
    else:
        rated = 'success'

    return jsonify({
        "success": rated,
        "customer_rating": get_feedback.customer_rating,
        "review": get_feedback.review_of_customer,
    })


@orders.route('/mark/disputed/<string:uuid>', methods=['GET'])
@login_required
def mark_order_disputed(uuid):
    """

    :return:
    """

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200

    get_order.overall_status = 8

    create_notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="You have a new dispute on an order."
                 )

    db.session.add(get_order)
    db.session.commit()
    return jsonify({"success": "Success: Order marked as disputed"})


@orders.route('/mark/delivered/<string:uuid>', methods=['GET'])
@login_required
def mark_order_delivered(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()
    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200

    create_notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="Your order has been marked as delivered."
                 )

    get_order.overall_status = 4

    db.session.add(get_order)
    db.session.commit()

    return jsonify({"success": "Success: Order marked as delivered"})



@orders.route('/mark/finalized/<string:uuid>', methods=['GET'])
@login_required
def mark_order_finalized(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()

    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200

    if get_order.digital_currency == 1:
        finalize_order_btc(get_order.uuid)
    if get_order.digital_currency == 2:
        finalize_order_bch(get_order.uuid)
    if get_order.digital_currency == 3:
        finalize_order_xmr(get_order.uuid)

    get_order.overall_status = 10

    notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="Your order has been marked as finalized."
                 )

    db.session.add(get_order)
    db.session.commit()

    return jsonify({"success": "Success: Order marked as finalized"})


@orders.route('/request/cancel/<string:uuid>', methods=['GET'])
@login_required
def mark_order_request_cancel(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """

    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_id == current_user.id) \
        .filter(User_Orders.uuid == uuid) \
        .first()

    if get_order is None:
        return jsonify({"error": "Error: Order not found"}), 200

    get_order.overall_status = 6

    notification(username=get_order.vendor_user_name,
                 user_uuid=get_order.vendor_uuid,
                 msg="A customer has requested to cancel an order."
                 )

    db.session.add(get_order)
    db.session.commit()

    return jsonify({"success": "Success: Order marked as cancelled"})
