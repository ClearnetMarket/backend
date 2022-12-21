
from decimal import Decimal
from operator import or_

from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.orders import orders
from app import db

# models
from app.classes.user_orders import User_Orders, User_Orders_Schema
from app.classes.feedback import Feedback_Feedback
from app.wallet_btc.wallet_btc_work import finalize_order_btc
from app.wallet_bch.wallet_bch_work import finalize_order_bch
from app.wallet_xmr.wallet_xmr_work import finalize_order_xmr


@orders.route('/<string:uuid>', methods=['GET'])
@login_required
def get_order_model(uuid):
    """
    Gets the order for the customer
    :return:
    """
    if request.method == 'GET':
        # get order
        # user must be customer or vendor

        get_order = db.session \
            .query(User_Orders) \
            .filter(or_(User_Orders.customer_id == current_user.id,
                        User_Orders.vendor_id == current_user.id)) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        # if order exists
        if get_order:
            # return schema
            item_schema = User_Orders_Schema()
            return jsonify(item_schema.dump(get_order))
        else:
            return jsonify({"status": "error"}), 409


@orders.route('', methods=['GET'])
@login_required
def get_user_orders():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':

        user_orders = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .order_by(User_Orders.created.desc()) \
            .limit(10)

        item_schema = User_Orders_Schema(many=True)
        return jsonify(item_schema.dump(user_orders))


@orders.route('/count', methods=['GET'])
@login_required
def get_user_orders_count():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':

        user_orders_count = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .count()

        if user_orders_count is not None:
            return jsonify({"count": user_orders_count})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/vendor/<string:uuid>', methods=['GET'])
@login_required
def get_order_vendor(uuid):
    """
    Gets the order for the vendor
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.vendor_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order:
            item_schema = User_Orders_Schema()
            return jsonify(item_schema.dump(get_order))
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/feedback/score/<string:uuid>', methods=['POST'])
@login_required
def order_feedback_score(uuid):
    """
    CUSTOMER
    Post  feedback     given by customer
    # type of feedback = 1
    :return:
    """
    if request.method == 'POST':

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
        # if order exists else 409
        if get_order:
            # get the request json
            try:
                if request.json["vendorrating"]:
                    vendor_rating = request.json["vendorrating"]
                else:
                    return jsonify({"status": "error"}), 409
            except Exception as e:
                print(str(e))
                return jsonify({"status": "error"}), 409
            try:
                if request.json["itemrating"]:
                    item_rating = request.json["itemrating"]
                else:
                    return jsonify({"status": "error"}), 409
            except Exception as e:
                print(str(e))
                return jsonify({"status": "error"}), 409

            # set feedback to nearest integer
            if 0 <= Decimal(vendor_rating) <= 10:
                vendorrating = int(vendor_rating)
            else:
                vendorrating = 0
            # set feedback to nearest integer
            if 0 <= Decimal(item_rating) <= 10:
                itemrating = int(vendor_rating)
            else:
                itemrating = 0

            # feedback exists just add the review
            get_order.type_of_feedback = vendor_rating
            get_order.author_uuid = current_user.uuid
            db.session.add(get_order)

            get_feedback.vendor_rating = vendorrating
            get_feedback.item_rating = itemrating
            db.session.add(get_feedback)

            # if both conditions are met set it as review added
            # this ensures proper review is added not just hhalf
            if get_feedback.review_of_vendor is not None\
                and get_feedback.vendor_rating is not None:
                get_order.vendor_feedback = 1
                db.session.add(get_order)

            db.session.commit()

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


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
    if request.method == 'POST':

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
        # if order exists else 409
        if get_order:
            if request.json["review"]:
                review_by_user = request.json["review"]
            else:
                return jsonify({"status": "error"}), 409
            # if no feedback exists
            # Note... vendor rating is none

            # feedback exists just add the review
            get_order.review_of_vendor = review_by_user
            get_order.author_uuid = current_user.uuid
            db.session.add(get_order)

            # update feedback
            get_feedback.review_of_vendor = review_by_user
            db.session.add(get_feedback)

            # if both conditions are met set it as review added
            # this ensures proper review is added not just hhalf
            if get_feedback.review_of_vendor is not None\
                and get_feedback.vendor_rating is not None:
                get_order.vendor_feedback = 1
                db.session.add(get_order)
            db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/vendor/feedback/score/<string:uuid>', methods=['POST'])
@login_required
def order_vendor_feedback_score(uuid):
    """
    VENDOR
    Post feedback     given by vendor
        # type of feedback = 2
    :return:
    """

    if request.method == 'POST':

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
        # if order exists else 409
        if get_order:
            # get the request json
            if request.json["rating"]:
                customer_rating = request.json["rating"]
            else:
                return jsonify({"status": "error"}), 409

            # set feedback to nearest integer
            if 0 <= Decimal(customer_rating) <= 10:
                customerrating = int(customer_rating)
            else:
                customerrating = 1

            # modify order
            get_order.author_uuid = current_user.uuid
            get_order.customer_rating = customerrating
            db.session.add(get_order)

            # add the review
            get_feedback.customer_rating = customerrating
            db.session.add(get_feedback)

            # if both conditions are met set it as review added
            # this ensures proper review is added not just half

            if get_feedback.review_of_customer is not None\
                and get_feedback.customer_rating is not None:
                get_order.user_feedback = 1
                db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/vendor/feedback/review/<string:uuid>', methods=['POST'])
@login_required
def order_vendor_feedback_review(uuid):
    """
    VENDOR
    Post  feedback written review
    feedback given by vendor

    # type of feedback = 2
    :return:
    """
    if request.method == 'POST':

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

        # if order exists else 409
        if get_order:
            if request.json["review"]:
                review_by_user = request.json["review"]
            else:
                return jsonify({"status": "error"}), 409
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
                if get_feedback.review_of_customeris is not None\
                    and get_feedback.customer_rating is not None:
                    get_order.user_feedback = 1
                    db.session.add(get_order)

            db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/feedback/get/<string:uuid>', methods=['GET'])
@login_required
def get_order_feedback(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()

        if get_order:
            get_feedback = db.session \
                .query(Feedback_Feedback) \
                .filter(Feedback_Feedback.order_uuid == uuid) \
                .first()
            if get_feedback:
                return jsonify({
                    "item_rating": get_feedback.item_rating,
                    "vendor_rating": get_feedback.vendor_rating,
                    "review": get_feedback.review_of_vendor,
                })
            else:
                return jsonify({"order_feedback": 'None'})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/mark/disputed/<string:uuid>', methods=['GET'])
@login_required
def mark_order_disputed(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order:
            get_order.overall_status = 8
            db.session.add(get_order)
            db.session.commit()
            return jsonify({"status": "error"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/mark/delivered/<string:uuid>', methods=['GET'])
@login_required
def mark_order_delivered(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """

    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()

        if get_order:
            get_order.overall_status = 4

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/mark/finalized/<string:uuid>', methods=['GET'])
@login_required
def mark_order_finalized(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """

    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()

        if get_order:
            if get_order.digital_currency == 1:
                finalize_order_btc(get_order.uuid)
            if get_order.digital_currency == 2:
                finalize_order_bch(get_order.uuid)
            if get_order.digital_currency == 3:
                finalize_order_xmr(get_order.uuid)

            get_order.overall_status = 10

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409


@orders.route('/request/cancel/<string:uuid>', methods=['GET'])
@login_required
def mark_order_request_cancel(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """

    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()

        if get_order:

            get_order.overall_status = 6

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409
