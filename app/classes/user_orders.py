from app import db, ma
from uuid import uuid4


def get_uuid_item():
    return uuid4().hex


class User_Orders(db.Model):
    __tablename__ = 'user_orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    uuid = db.Column(db.String(32), default=get_uuid_item)
    title_of_item = db.Column(db.VARCHAR(500))
    item_uuid = db.Column(db.VARCHAR(50))
    node = db.Column(db.VARCHAR(50))
    image_one = db.Column(db.VARCHAR(100))
    quantity = db.Column(db.INTEGER)
    vendor_user_name = db.Column(db.VARCHAR(40))
    vendor_uuid = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    customer_user_name = db.Column(db.VARCHAR(40))
    customer_uuid = db.Column(db.VARCHAR(40))
    customer_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    incart = db.Column(db.INTEGER)
    new_order = db.Column(db.INTEGER)
    accepted_order = db.Column(db.INTEGER)
    waiting_order = db.Column(db.INTEGER)
    disputed_order = db.Column(db.INTEGER)
    disputed_timer = db.Column(db.TIMESTAMP())
    moderator_uuid = db.Column(db.VARCHAR(40))
    delivered_order = db.Column(db.INTEGER)
    date_shipped = db.Column(db.TIMESTAMP())
    completed = db.Column(db.INTEGER)
    completed_time = db.Column(db.TIMESTAMP())
    released = db.Column(db.INTEGER)

    private_note = db.Column(db.TEXT)
    escrow = db.Column(db.VARCHAR(500))

    request_cancel = db.Column(db.INTEGER)
    reason_cancel = db.Column(db.INTEGER)
    cancelled = db.Column(db.INTEGER)

    shipping_price_btc = db.Column(db.DECIMAL(20, 8))
    shipping_price_bch = db.Column(db.DECIMAL(20, 8))
    shipping_price_xmr = db.Column(db.DECIMAL(20, 12))
    shipping_description = db.Column(db.VARCHAR(500))

    vendor_feedback = db.Column(db.INTEGER)
    user_feedback = db.Column(db.INTEGER)


    digital_currency = db.Column(db.INTEGER)
    fee_btc = db.Column(db.DECIMAL(20, 8))
    fee_bch = db.Column(db.DECIMAL(20, 8))
    fee_xmr = db.Column(db.DECIMAL(20, 8))
    price_total_btc = db.Column(db.DECIMAL(20, 8))
    price_total_bch = db.Column(db.DECIMAL(20, 8))
    price_total_xmr = db.Column(db.DECIMAL(20, 12))
    price_per_item_btc = db.Column(db.DECIMAL(20, 8))
    price_per_item_bch = db.Column(db.DECIMAL(20, 8))
    price_per_item_xmr = db.Column(db.DECIMAL(20, 12))



class User_Orders_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_Orders

