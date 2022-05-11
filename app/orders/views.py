from datetime import datetime
from decimal import Decimal
from operator import or_
from webbrowser import get
from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.orders import orders
from app import db

# models
from app.classes.user_orders import User_Orders, User_Orders_Schema
from app.classes.feedback import Feedback_Feedback
from app.classes.vendor import Vendor_Notification

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
        if user_orders_count:
            return jsonify({"count": user_orders_count})
        else:
            return jsonify({"status": "error"}), 409


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
    Post  feedback
    feedback given by customer
    :return:
    """
    if request.method == 'POST':
        now = datetime.utcnow()
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        # get feedback (might not be any)
        get_feedback = db.session\
            .query(Feedback_Feedback)\
            .filter(Feedback_Feedback.author_uuid == current_user.uuid)\
            .first()
        # if order exists else 409
        if get_order:
            # get the request json
            if request.json["rating"]:
                vendor_rating = request.json["rating"]
            else:
                return jsonify({"status": "error"}), 409
            # set feedback to nearest integer
            if 0 <= Decimal(vendor_rating) <= 10:
                vendorrating = int(vendor_rating)
            # if there is no feedback already create it
            if get_feedback is None:
                create_new_feedback = Feedback_Feedback(
                    timestamp=now,
                    order_uuid=get_order.uuid,
                    item_uuid=get_order.item_uuid,
                    customer_name=get_order.customer_user_name,
                    customer_uuid=get_order.customer_uuid,
                    vendor_name=get_order.vendor_user_name,
                    vendor_uuid=get_order.vendor_uuid,
                    vendor_comment=None,
                    type_of_feedback=1,
                    author_uuid=current_user.uuid,
                    item_rating=None,
                    vendor_rating=vendorrating,
                    customer_rating=None,
                    review=None
                )
                db.session.add(create_new_feedback)
                db.session.flush()
                get_feedback = create_new_feedback
            else:
                # feedback exists just add the review
                get_feedback.vendor_rating = vendorrating
                db.session.add(get_feedback)
            # if both conditions are met set it as review added
            # this ensure proper review is added not just hhalf
            if get_feedback.review is not None and get_feedback.vendor_rating is not None:
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
    Post  feedback written review
    feedback given by customer
    :return:
    """
    if request.method == 'POST':
        now = datetime.utcnow()
        # get the order by current customer
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        # get feedback (might not be any)
        get_feedback = db.session\
            .query(Feedback_Feedback)\
            .filter(Feedback_Feedback.author_uuid == current_user.uuid)\
            .first()
        # if order exists else 409
        if get_order:
            if request.json["review"]:
                review_by_user = request.json["review"]
            else:
                return jsonify({"status": "error"}), 409
            # if no feedback exists
            # Note... vendor rating is none
            if get_feedback is None:
                create_new_feedback = Feedback_Feedback(
                    timestamp=now,
                    order_uuid=get_order.uuid,
                    item_uuid=get_order.item_uuid,
                    customer_name=get_order.customer_user_name,
                    customer_uuid=get_order.customer_uuid,
                    vendor_name=get_order.vendor_user_name,
                    vendor_uuid=get_order.vendor_uuid,
                    vendor_comment=None,
                    type_of_feedback=1,
                    author_uuid=current_user.uuid,
                    item_rating=None,
                    vendor_rating=None,
                    customer_rating=None,
                    review=review_by_user
                )
                db.session.add(create_new_feedback)
                db.session.flush()
            else:
                # feedback exists just add the review
                get_feedback.review = review_by_user
                db.session.add(get_feedback)
            # if both conditions are met set it as review added
            # this ensure proper review is added not just hhalf
            if get_feedback.review is not None and get_feedback.vendor_rating is not None:
                get_order.vendor_feedback = 1
                db.session.add(get_order)
            db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 409



@orders.route('/feedback/vendor/<string:order_uuid>', methods=['POST'])
@login_required
def order_feedback_vendor(order_uuid):
    """
    Leaves a review.

    Review is given from vendor
    :return:
    """
    if request.method == 'POST':
        now = datetime.utcnow()
       
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.vendor_id == current_user.id) \
            .filter(User_Orders.uuid == order_uuid) \
            .first()
        if get_order:
          
            # vendor rating
            customer_rating = request.json["customerrating"]
            if 0 <= Decimal(customer_rating) <= 10:
                customer_rating = int(customer_rating)

            review_by_vendor = request.json["review"]
            # create a new feedback
            create_new_feedback = Feedback_Feedback(
                timestamp=now,
                order_uuid=get_order.uuid,
                item_uuid=get_order.item_uuid,
                customer_name=get_order.customer_user_name,
                customer_uuid=get_order.customer_uuid,
                vendor_name=get_order.vendor_user_name,
                vendor_uuid=get_order.vendor_uuid,
                vendor_comment=None,
                type_of_feedback=2,
                author_uuid=current_user.uuid,
                item_rating=None,
                vendor_rating=None,
                customer_rating=customer_rating,
                review=review_by_vendor
            )
            # change order to show it got feedback
            get_order.vendor_feedback = 1
            db.session.add(get_order)
            # create a new notification for vendor
            new_notification = Vendor_Notification(
                dateadded=now,
                user_id=get_order.vendor_id,
                new_feedback=1,
                new_disputes=0,
                new_orders=0,
                new_returns=0,
            )
            db.session.add(new_notification)
            db.session.add(create_new_feedback)
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
        print(uuid)
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        print(get_order.id)
        if get_order:
            get_feedback = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.order_uuid==uuid)\
                .first()

            return jsonify({
                "item_rating": get_feedback.item_rating,
                "vendor_rating": get_feedback.vendor_rating,
                "review": get_feedback.review,
            })
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
                print("going to finalize")
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
