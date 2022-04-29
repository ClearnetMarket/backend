
from flask import request, jsonify
from flask_login import login_required, current_user

from app.moderator import moderator
from app import db

from app.classes.user_orders import User_Orders, User_Orders_Schema
from app.classes.feedback import Feedback_Feedback, Feedback_Feedback_Schema

from app.wallet_btc.wallet_btc_moderator import finalize_order_dispute_btc
from app.wallet_bch.wallet_bch_moderator import finalize_order_dispute_bch
from app.wallet_xmr.wallet_xmr_moderator import finalize_order_dispute_xmr


@moderator.route('/disputes/available', methods=['GET'])
@login_required
def get_disputes_main_page_need_mod():
    """
    This gets currently open disputes that appears on the moderator home page
    :return:
    """
    if request.method == 'GET':
        # see if current user is a mod
     
        if current_user.admin_role >= 2:
        # query the disputes
            get_disputes = db.session \
                .query(User_Orders) \
                .filter(User_Orders.overall_status == 8) \
                .filter(User_Orders.moderator_uuid == None)\
                .all()
            disputes_schema = User_Orders_Schema(many=True)
            return jsonify(disputes_schema.dump(get_disputes))
        else:
            return jsonify({"status": "error"})


@moderator.route('/disputes/modded', methods=['GET'])
@login_required
def get_disputes_main_page_has_mod():
    """
    This gets currently open disputes that appears on the moderator home page
    :return:
    """
    if request.method == 'GET':
        # see if current user is a mod
        if current_user.admin_role >= 2:
            # query the disputes
            get_disputes = db.session \
                .query(User_Orders) \
                .filter(User_Orders.overall_status == 8) \
                .filter(User_Orders.moderator_uuid != None)\
                .all()
            disputes_schema = User_Orders_Schema(many=True)
            return jsonify(disputes_schema.dump(get_disputes))
        else:
            return jsonify({"status": "error"})


@moderator.route('/dispute/settle/<string:uuid>', methods=['GET'])
@login_required
def mark_dispute_finished(uuid):
    """
    FInalizes an order with percent to each customer
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        percent_to_vendor_json = request.json["percenttovendor"]
        percent_to_vendor = int(percent_to_vendor_json)
        percent_to_customer_json = request.json["percenttocustomer"]
        percent_to_customer = int(percent_to_customer_json)

        if get_order:
            if get_order.digital_currency == 1:
                finalize_order_dispute_btc(order_uuid=get_order,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            if get_order.digital_currency == 2:
                finalize_order_dispute_bch(order_uuid=get_order,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            if get_order.digital_currency == 3:
                finalize_order_dispute_xmr(order_uuid=get_order,
                                           percent_to_customer=percent_to_customer,
                                           percent_to_vendor=percent_to_vendor)
            get_order.overall_status = 10

            db.session.add(get_order)
            db.session.commit()

            return jsonify({"status": "success"})


@moderator.route('/dispute/canceldispute/open/<string:uuid>', methods=['GET'])
@login_required
def mark_dispute_cancelled_still_open(uuid):
    """
    Brings an order to open status
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.overall_status = 3

        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})


@moderator.route('/dispute/canceldispute/closed/<string:uuid>', methods=['GET'])
@login_required
def mark_dispute_cancelled_still_closed(uuid):
    """
    Brings an order to closed status
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.overall_status = 10

        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})


@moderator.route('/dispute/extend/<string:uuid>', methods=['GET'])
@login_required
def extend_dispute_time(uuid):
    """
    Extends order for more time
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .filter(User_Orders.uuid == uuid) \
            .first()
        if get_order.moderator_uuid != current_user.uuid:
            return jsonify({"status": "error"})

        get_order.extended_timer = 1

        db.session.add(get_order)
        db.session.commit()

        return jsonify({"status": "success"})


@moderator.route('/orderinfo/<string:uuid>', methods=['GET'])
@login_required
def get_order_model(uuid):
    """
    Gets the order for the moderator
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            get_order = db.session \
                .query(User_Orders) \
                .filter(User_Orders.uuid == uuid) \
                .first()

            item_schema = User_Orders_Schema()
            return jsonify(item_schema.dump(get_order))


@moderator.route('/customer/ratings/<string:uuid>', methods=['GET'])
@login_required
def get_customer_ratings(uuid):
    """
    Gets the customer ratings.
     2= customer 
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            get_user_ratings = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.customer_uuid == uuid)\
                .filter(Feedback_Feedback.type_of_feedback == 2)\
                .order_by(Feedback_Feedback.timestamp.desc())\
                .limit(20)

            feedback_schema = Feedback_Feedback_Schema()
            return jsonify(feedback_schema.dump(get_user_ratings))


@moderator.route('/vendor/ratings/<string:uuid>', methods=['GET'])
@login_required
def get_vendor_ratings(uuid):
    """
    Gets the vendor ratings
    1 = vendor
    :return:
    """
    if request.method == 'GET':
        if current_user.admin_role >= 2:
            get_user_ratings = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.vendor_uuid == uuid)\
                .filter(Feedback_Feedback.type_of_feedback == 1)\
                .order_by(Feedback_Feedback.timestamp.desc())\
                .limit(20)

            feedback_schema = Feedback_Feedback_Schema()
            return jsonify(feedback_schema.dump(get_user_ratings))
