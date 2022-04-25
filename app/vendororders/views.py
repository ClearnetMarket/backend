
from datetime import date, datetime
from flask import request,  jsonify
from flask_login import current_user
from app.vendororders import vendororders
from app import db
from app.common.decorators import login_required
from app.classes.user_orders import User_Orders, User_Orders_Schema, User_Orders_Tracking
from app.classes.feedback import Feedback_Feedback, Feedback_Feedback_Schema


@vendororders.route('/count', methods=['GET'])
@login_required
def vendor_orders_count():

    if request.method == 'GET':
        vendor_orders_new = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=1) \
            .count()
        vendor_orders_accepted = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=2) \
            .count()
        vendor_orders_shipped = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=3) \
            .count()
        vendor_orders_finalized = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=4) \
            .count()
        vendor_orders_finalized_early = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=5) \
            .count()
        vendor_orders_request_cancel = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=6) \
            .count()
        vendor_orders_cancelled = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=7) \
            .count()
        vendor_orders_dispute = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=8) \
            .count()
        return jsonify({
            'vendor_orders_new': vendor_orders_new,
            'vendor_orders_accepted': vendor_orders_accepted,
            'vendor_orders_shipped': vendor_orders_shipped,
            'vendor_orders_finalized': vendor_orders_finalized,
            'vendor_orders_finalized_early': vendor_orders_finalized_early,
            'vendor_orders_request_cancel': vendor_orders_request_cancel,
            'vendor_orders_cancelled': vendor_orders_cancelled,
            'vendor_orders_dispute': vendor_orders_dispute,
        })



@vendororders.route('/new', methods=['GET'])
@login_required
def vendor_orders_waiting_on_accepted():

    if request.method == 'GET':
       
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=1) \
            .all()

        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/new/accept/<string:orderuuid>', methods=['PUT'])
@login_required
def vendor_orders_new_accept(orderuuid):

    if request.method == 'PUT':
        print(orderuuid)
        vendor_order = User_Orders.query \
            .filter_by(uuid=orderuuid) \
            .filter_by(vendor_id=current_user.id)\
            .first()

        vendor_order.overall_status = 2
        db.session.add(vendor_order)
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/new/reject/<string:orderuuid>', methods=['DELETE'])
@login_required
def vendor_orders_reject(orderuuid):

    if request.method == 'GET':
        vendor_order = User_Orders.query \
            .filter_by(uuid=orderuuid) \
            .filter_by(vendor_id=current_user.id)\
            .first()
        db.session.delete(vendor_order)
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/waiting', methods=['GET'])
@login_required
def vendor_orders_waiting_on_shipment():

    if request.method == 'GET':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=2) \
            .all()

        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))



@vendororders.route('/waiting/markasshipped/<string:orderuuid>', methods=['PUT'])
@login_required
def vendor_orders_mark_as_shipped(orderuuid):

    if request.method == 'PUT':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(uuid=orderuuid) \
            .first()
        vendor_orders.overall_status=3
        db.session.add(vendor_orders)
        db.session.commit()
        return jsonify({'status': 'success'})


@vendororders.route('/shipped', methods=['GET'])
@login_required
def vendor_orders_shipped():

    if request.method == 'GET':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=3) \
            .all()
        
        user_order_info = User_Orders_Schema(many=True)
        return jsonify(user_order_info.dump(vendor_orders))




@vendororders.route('/finalized', methods=['GET'])
@login_required
def vendor_orders_finalized():

    if request.method == 'GET':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=4) \
            .all()
        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))


@vendororders.route('/requestcancel', methods=['GET'])
@login_required
def vendor_orders_waiting_on_cancel():

    if request.method == 'GET':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=6) \
            .all()
        vendor_orders_schema = User_Orders_Schema(many=True)
        return jsonify(vendor_orders_schema.dump(vendor_orders))



@vendororders.route('/disputed', methods=['GET'])
@login_required
def vendor_orders_disputed():

    if request.method == 'GET':
        vendor_orders = User_Orders.query \
            .filter_by(vendor_id=current_user.id) \
            .filter_by(overall_status=8) \
            .all()
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
      
        see_if_order_exists = User_Orders.query\
        .filter_by(uuid=order_uuid)\
        .filter_by(vendor_id=current_user.id)\
        .first()
        if see_if_order_exists:
            add_new_tracking = User_Orders_Tracking(
                created=now,
                order_uuid=order_uuid,
                carrier=carrier_name,
                tracking_number=tracking_number,
                vendor_uuid=see_if_order_exists.vendor_uuid
            )
            db.session.add(add_new_tracking)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'success'})


@vendororders.route('/tracking/get/<string:order_uuid>', methods=['GET'])
@login_required
def vendor_orders_get_tracking(order_uuid):

    if request.method == 'GET':
        tracking_data = User_Orders_Tracking.query \
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
    if request.method == 'POST':
        now = datetime.utcnow()
        see_if_feedback_exists = User_Orders.query\
            .filter(vendor_feedback=1)\
            .filter(uuid=order_uuid)\
            .filter(customer_uuid=current_user.uuid)\
            .first() is not None
      
        get_item_rating = request.json["item_rating"]
        get_vendor_rating = request.json["vendor_rating"]
        if see_if_feedback_exists:
            get_order = User_Orders.query.filter(uuid=order_uuid).first()
            add_new_feedback_for_vendor = Feedback_Feedback(
                timestamp=now,
                order_uuid=get_order.uuid,
                item_uuid=get_order.item_uuid,
                customer_name=get_order.customer_user_name,
                customer_uuid=get_order.customer_uuid,
                vendor_name=get_order.vendor_user_name,
                vendor_uuid=get_order.vendor_uuid,
                vendor_comment=None,
                type_of_feedback=1,
                item_rating=get_item_rating,
                vendor_rating=get_vendor_rating,
                customer_rating=None,
                author_uuid=current_user.uuid,
            )
        db.session.add(add_new_feedback_for_vendor)
        db.session.commit()
        return jsonify({'status': 'success'})
