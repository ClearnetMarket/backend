from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user


from app.orders import orders
from app import db

# models
from app.classes.user_orders import User_Orders, User_Orders_Schema
from app.classes.feedback import Feedback_Feedback, Feedback_Feedback_Schema


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
def get_order(uuid):
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':

        get_order = db.session \
            .query(User_Orders) \
            .filter(User_Orders.customer_id == current_user.id) \
            .order_by(User_Orders.uuid == uuid) \
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
            .order_by(User_Orders.uuid == uuid) \
            .first()
        if get_order:
            # vendor rating
            vendor_rating = request.json["vendorrating"]
            if 1 <= int(vendor_rating) <= 5:
                vendorrating = int(vendor_rating)
            # item rating
            item_rating = request.json["itemrating"]
            if 1 <= int(item_rating) <= 5:
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

            get_order.user_feedback = 1
            db.session.add(get_order)
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
            .order_by(User_Orders.uuid == uuid) \
            .first()
        if get_order:
            get_feedback = Feedback_Feedback.query.filter(
                Feedback_Feedback.order_uuid==uuid).first()
            print("hereeee")
            return jsonify({
                "item_rating": get_feedback.item_rating,
                "vendor_rating": get_feedback.vendor_rating,
                "review": get_feedback.review,
            })
        else:
            return jsonify({"status": "error"})

            
