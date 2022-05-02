from app import db, ma
from uuid import uuid4


def get_uuid_item():
    return uuid4().hex


class User_Orders(db.Model):
    __tablename__ = 'user_orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.TIMESTAMP())
    uuid = db.Column(db.String(32), default=get_uuid_item)
    title_of_item = db.Column(db.VARCHAR(500))
    item_uuid = db.Column(db.VARCHAR(50))
    node = db.Column(db.VARCHAR(50))
    image_one = db.Column(db.VARCHAR(1000))
    quantity = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)

    vendor_user_name = db.Column(db.VARCHAR(40))
    vendor_uuid = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    customer_user_name = db.Column(db.VARCHAR(40))
    customer_uuid = db.Column(db.VARCHAR(40))
    customer_id = db.Column(db.INTEGER)
    moderator_uuid = db.Column(db.VARCHAR(40))

    overall_status = db.Column(db.INTEGER)
    disputed_timer = db.Column(db.TIMESTAMP())
    date_shipped = db.Column(db.TIMESTAMP())
    completed_time = db.Column(db.TIMESTAMP())
    released = db.Column(db.INTEGER)
    extended_timer = db.Column(db.INTEGER)
    private_note = db.Column(db.TEXT)
    escrow = db.Column(db.VARCHAR(500))

    request_cancel = db.Column(db.INTEGER)
    reason_cancel = db.Column(db.INTEGER)

    vendor_feedback = db.Column(db.INTEGER)
    user_feedback = db.Column(db.INTEGER)

    digital_currency = db.Column(db.INTEGER)
    shipping_price_btc = db.Column(db.DECIMAL(20, 8))
    shipping_price_bch = db.Column(db.DECIMAL(20, 8))
    shipping_price_xmr = db.Column(db.DECIMAL(20, 12))
    shipping_description = db.Column(db.VARCHAR(500))
    fee_btc = db.Column(db.DECIMAL(20, 8))
    fee_bch = db.Column(db.DECIMAL(20, 8))
    fee_xmr = db.Column(db.DECIMAL(20, 8))

    price_per_item_btc = db.Column(db.DECIMAL(20, 8))
    price_per_item_bch = db.Column(db.DECIMAL(20, 8))
    price_per_item_xmr = db.Column(db.DECIMAL(20, 12))

    price_total_btc = db.Column(db.DECIMAL(20, 8))
    price_total_bch = db.Column(db.DECIMAL(20, 8))
    price_total_xmr = db.Column(db.DECIMAL(20, 12))
    
    address_name = db.Column(db.VARCHAR(1000))
    address = db.Column(db.VARCHAR(1000))
    apt = db.Column(db.VARCHAR(1000))
    city = db.Column(db.VARCHAR(1000))
    country = db.Column(db.VARCHAR(1000))
    state_or_provence = db.Column(db.VARCHAR(1000))
    zip_code = db.Column(db.VARCHAR(200))
    msg = db.Column(db.VARCHAR(2500))
    dispute_post_id = db.Column(db.INTEGER)


class User_Orders_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_Orders
        fields = ('uuid', 'created', 'quantity', 'title_of_item', 'item_uuid', 'image_one',
                  'currency', 'vendor_user_name', 'customer_user_name',
                  'customer_uuid', 'vendor_uuid', 'overall_status', 'date_shipped',
                  'completed', 'completed_time', 'released',
                  'shipping_price_btc', 'shipping_price_bch', 'shipping_price_xmr',
                  'shipping_description', 'vendor_feedback', 'user_feedback', 'digital_currency',
                  'fee_btc', 'fee_bch', 'fee_xmr', 'price_total_btc', 'price_total_bch', 'price_total_xmr',
                  'price_per_item_btc', 'price_per_item_bch', 'price_per_item_xmr',
                  'address_name', 'address', 'apt', 'country',
                  'city', 'state_or_provence', 'zip_code', 'msg', 'moderator_uuid', 'dispute_post_id'
                  )


class User_Orders_Tracking(db.Model):
    __tablename__ = 'user_orders_tracking'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.TIMESTAMP())
    order_uuid = db.Column(db.String(32))
    carrier = db.Column(db.VARCHAR(500))
    tracking_number = db.Column(db.VARCHAR(1000))
    vendor_uuid = db.Column(db.VARCHAR(40))
