
from flask import request, jsonify
from flask_login import login_required, current_user

from app.moderator import moderator
from app import db

from app.classes.user_orders import User_Orders
from app.wallet_btc.wallet_btc_moderator import finalize_order_dispute_btc
from app.wallet_bch.wallet_bch_moderator import finalize_order_dispute_bch
from app.wallet_xmr.wallet_xmr_moderator import finalize_order_dispute_xmr


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
            get_order.overall_status = 4

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

        get_order.overall_status = 4

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
