
from datetime import datetime
from flask import request,  jsonify
from flask_login import current_user
from app.classes.item import Item_MarketItem
from app.vendororders import vendororders
from app import db
from sqlalchemy import or_
from app.common.decorators import login_required
from app.classes.user_orders import User_Orders, User_Orders_Schema, User_Orders_Tracking
from app.classes.feedback import Feedback_Feedback
from app.wallet_bch.wallet_bch_work import bch_refund_rejected_user
from app.wallet_btc.wallet_btc_work import btc_refund_rejected_user
from app.wallet_xmr.wallet_xmr_work import xmr_refund_rejected_user
from app.vendor.item_management.check_online import put_online_allowed
from app.classes.vendor import Vendor_Notification

@vendororders.route('/count', methods=['GET'])
@login_required
def vendor_orders_count():

    if request.method == 'GET':
        vendor_orders_new = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=1) \
            .count()
        vendor_orders_accepted = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=2) \
            .count()
        vendor_orders_shipped = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=3) \
            .count()
        vendor_orders_delivered = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=4) \
            .count()
        vendor_orders_finalized = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=10) \
            .count()
        vendor_orders_request_cancel = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=6) \
            .count()
        vendor_orders_cancelled = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=7) \
            .count()
        vendor_orders_dispute = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=8) \
            .count()
        return jsonify({
            'vendor_orders_new': vendor_orders_new,
            'vendor_orders_accepted': vendor_orders_accepted,
            'vendor_orders_shipped': vendor_orders_shipped,
            'vendor_orders_finalized': vendor_orders_finalized,
            'vendor_orders_delivered': vendor_orders_delivered,
            'vendor_orders_request_cancel': vendor_orders_request_cancel,
            'vendor_orders_cancelled': vendor_orders_cancelled,
            'vendor_orders_dispute': vendor_orders_dispute,
        })


@vendororders.route('/new', methods=['GET'])
@login_required
def vendor_orders_waiting_on_accepted():

    if request.method == 'GET':
       
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=1) \
            .all()

        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/new/accept/<string:orderuuid>', methods=['PUT'])
@login_required
def vendor_orders_new_accept(orderuuid):

    if request.method == 'PUT':
    
        vendor_order = db.session\
            .query(User_Orders) \
            .filter_by(uuid=orderuuid) \
            .filter_by(vendor_id=current_user.id)\
            .first()

        vendor_order.overall_status = 2
        db.session.add(vendor_order)
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/new/reject/<string:orderuuid>', methods=['POST'])
@login_required
def vendor_orders_reject(orderuuid):

    if request.method == 'POST':
        vendor_order = db.session\
            .query(User_Orders) \
            .filter_by(uuid=orderuuid) \
            .filter_by(vendor_uuid=current_user.uuid)\
            .first()
        db.session.delete(vendor_order)

        # return order amount from escrow back to user
        if vendor_order.digital_currency == 1:
            btc_refund_rejected_user(
                amount=vendor_order.price_total_btc,
                user_id=vendor_order.customer_id,
                order_uuid=vendor_order.uuid
                 )
        if vendor_order.digital_currency == 2:
            bch_refund_rejected_user(
                amount=vendor_order.price_total_bch,
                user_id=vendor_order.customer_id,
                  order_uuid=vendor_order.uuid
                  )
        if vendor_order.digital_currency == 3:
            xmr_refund_rejected_user(
                amount=vendor_order.price_total_xmr,
                user_id=vendor_order.customer_id,
                order_uuid=vendor_order.uuid
                 )
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/waiting', methods=['GET'])
@login_required
def vendor_orders_waiting_on_shipment():

    if request.method == 'GET':
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=2) \
            .all()

        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/waiting/markasshipped/<string:orderuuid>', methods=['PUT'])
@login_required
def vendor_orders_mark_as_shipped(orderuuid):

    if request.method == 'PUT':
        vendor_order = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(uuid=orderuuid) \
            .first()
        vendor_order.overall_status=3
        vendor_order.date_shipped = datetime.utcnow()
        
        db.session.add(vendor_order)
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/shipped', methods=['GET'])
@login_required
def vendor_orders_shipped():

    if request.method == 'GET':
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter(or_(User_Orders.overall_status==3, User_Orders.overall_status==4))\
            .all()
        
        user_order_info = User_Orders_Schema(many=True)
        return jsonify(user_order_info.dump(vendor_orders))


@vendororders.route('/finalized', methods=['GET'])
@login_required
def vendor_orders_finalized():

    if request.method == 'GET':
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=10) \
            .all()

        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/requestcancel', methods=['GET'])
@login_required
def vendor_orders_waiting_on_cancel():

    if request.method == 'GET':
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=6) \
            .all()
        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/disputed', methods=['GET'])
@login_required
def vendor_orders_disputed():

    if request.method == 'GET':
        vendor_orders = db.session\
            .query(User_Orders) \
            .filter(User_Orders.vendor_id==current_user.id) \
            .filter_by(overall_status=8) \
            .all()
        for f in vendor_orders:
            print(f.id)
        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/tracking/add', methods=['POST'])
@login_required
def vendor_orders_add_tracking():

    if request.method == 'POST':
        now = datetime.utcnow()
        order_uuid = request.json["order_uuid"]
        carrier_name = request.json["carrier_name"]
        tracking_number = request.json["tracking_number"]
      
        see_if_order_exists = db.session\
            .query(User_Orders)\
            .filter_by(uuid=order_uuid)\
            .filter_by(vendor_id=current_user.id)\
            .first()
        see_if_tracking_exists = db.session\
            .query(User_Orders_Tracking)\
            .filter(User_Orders_Tracking.order_uuid == order_uuid, User_Orders_Tracking.vendor_uuid == current_user.uuid)\
            .first()
        if see_if_order_exists:
            if see_if_tracking_exists is None:
                add_new_tracking = User_Orders_Tracking(
                    created=now,
                    order_uuid=order_uuid,
                    carrier=carrier_name,
                    tracking_number=tracking_number,
                    vendor_uuid=see_if_order_exists.vendor_uuid
                )
                db.session.add(add_new_tracking)
                db.session.commit()
            else:
                see_if_tracking_exists.tracking_number = tracking_number
                see_if_tracking_exists.carrier = carrier_name
                db.session.add(see_if_tracking_exists)
                db.session.commit()

            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'success'})


@vendororders.route('/tracking/get/<string:order_uuid>', methods=['GET'])
@login_required
def vendor_orders_get_tracking(order_uuid):

    if request.method == 'GET':
        tracking_data = db.session\
            .query(User_Orders_Tracking) \
            .filter_by(vendor_uuid=current_user.uuid) \
            .filter_by(order_uuid=order_uuid) \
            .first()

        if tracking_data:

            return jsonify({
                'tracking_number': tracking_data.tracking_number,
                'carrier_name': tracking_data.carrier,
            })
        else:
            return jsonify({'tracking': None})


@vendororders.route('/feedback/add/vendor/<string:order_uuid>', methods=['POST'])
@login_required
def vendor_orders_add_vendor_feedback(order_uuid):
    """
      this function adds feedback for customer
    - vendor gives a review for the customer
    """
    if request.method == 'POST':
        
        see_if_feedback_exists = db.session\
                                     .query(User_Orders)\
                                     .filter(vendor_feedback=1)\
                                     .filter(uuid=order_uuid)\
                                     .filter(customer_uuid=current_user.uuid)\
                                     .first() is not None
      
        get_item_rating = request.json["item_rating"]
        get_vendor_rating_for_customer = request.json["vendor_rating"]
        if see_if_feedback_exists:
            # get the feedback based on order uuid
            get_feedback = db.session\
            .query(Feedback_Feedback)\
            .filter(Feedback_Feedback.order_uuid == order_uuid)\
            .first()
            
            # set feedback based on form data from requests
            get_feedback.customer_rating = get_vendor_rating_for_customer
            get_feedback.item_rating = get_item_rating
            
            db.session.add(get_feedback)
            db.session.commit()

        return jsonify({'status': 'success'})


@vendororders.route('/online/<string:uuid>', methods=['GET'])
@login_required
def vendor_orders_put_online(uuid):
    """
    This function puts items online in the itemsforsale page
    """
    if request.method == 'GET':
        get_item = db.session\
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.vendor_uuid == current_user.uuid) \
            .filter(Item_MarketItem.uuid == uuid) \
            .first()
        check_if_allowed = put_online_allowed(item=get_item)
        if check_if_allowed is True:
            
            get_item.online = 1

            db.session.add(get_item)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': check_if_allowed})


@vendororders.route('/offline/<string:uuid>', methods=['GET'])
@login_required
def vendor_orders_put_offline(uuid):
    """
    This function puts items offline in the itemsforsale page
    """
    if request.method == 'GET':
       
        get_item = db.session\
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.vendor_uuid == current_user.uuid) \
            .filter(Item_MarketItem.uuid == uuid) \
            .first()

        get_item.online = 0
     
        
        db.session.add(get_item)
        db.session.commit()

        return jsonify({'status': 'success'})


@vendororders.route('/notification/dispute/<string:uuid>', methods=['POST'])
@login_required
def vendor_notification_dispute(uuid):
    """
    This function puts items offline in the itemsforsale page
    """         
   
    if request.method == 'POST':
        now = datetime.utcnow()
        get_order = db.session\
            .query(User_Orders)\
            .filter(User_Orders.uuid==uuid)\
            .first()
        if get_order.vendor_uuid == current_user.uuid or get_order.customer_uuid == current_user.uuid:
          
            
            print("HGEREWER")
            create_new_notification = Vendor_Notification(
                dateadded=now,
                user_id=get_order.vendor_id,
                new_feedback=0,
                new_disputes=1,
                new_orders=0,
                new_returns=0,
            )
            db.session.add(create_new_notification)
            db.session.commit()
            return jsonify({'status': 'successfully created notification'})
        