from datetime import datetime
from decimal import Decimal
from flask import request, jsonify
from flask_login import login_required, current_user


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


@orders.route('/<string:uuid>', methods=['GET'])
@login_required
def get_order_model(uuid):
    """
    Gets the order for the customer
    :return:
    """
    if request.method == 'GET':
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        
        item_schema = User_Orders_Schema()
        return jsonify(item_schema.dump(get_order))


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

        item_schema = User_Orders_Schema()
        return jsonify(item_schema.dump(get_order))


@orders.route('/feedback/<string:uuid>', methods=['POST'])
@login_required
def order_feedback(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'POST':
        now = datetime.utcnow()
        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order:
            # vendor rating
            vendor_rating = request.json["vendorrating"]
            if 0 <= Decimal(vendor_rating) <= 10:
                vendorrating = int(vendor_rating)
            # item rating
            item_rating = request.json["itemrating"]
            if 0 <= Decimal(item_rating) <= 10:
                itemrating = int(item_rating)
            review_by_user = request.json["review"]

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
                item_rating=itemrating,
                vendor_rating=vendorrating,
                customer_rating=None,
                review=review_by_user
            )

            get_order.vendor_feedback = 1
            db.session.add(get_order)
            db.session.add(create_new_feedback)
            db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})


@orders.route('/feedback/vendor/<string:order_uuid>', methods=['POST'])
@login_required
def order_feedback_vendor(order_uuid):
    """
    Used on index.  Grabs today's featured items
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
            return jsonify({"status": "error"})


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
            get_feedback = Feedback_Feedback.query\
                .filter(Feedback_Feedback.order_uuid==uuid)\
                .first()

            return jsonify({
                "item_rating": get_feedback.item_rating,
                "vendor_rating": get_feedback.vendor_rating,
                "review": get_feedback.review,
            })
        else:
            return jsonify({"status": "error"})


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
            if get_order.digital_currency == 1:
                finalize_order_btc(get_order.uuid)
            if get_order.digital_currency == 2:
                finalize_order_bch(get_order.uuid)
            if get_order.digital_currency == 3:
                finalize_order_xmr(get_order.uuid)
            
            get_order.overall_status = 4
            
            db.session.add(get_order)
            db.session.commit()
            
            return jsonify({"status": "success"})
