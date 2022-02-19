from app import db, ma
from uuid import uuid4


def get_uuid_item():
    return uuid4().hex


class Vendor_Orders(db.Model):
    __tablename__ = 'vendor_orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    uuid = db.Column(db.String(32), default=get_uuid_item)

    type = db.Column(db.INTEGER)
    vendor = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    customer = db.Column(db.VARCHAR(40))
    customer_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    incart = db.Column(db.INTEGER)
    new_order = db.Column(db.INTEGER)
    accepted_order = db.Column(db.INTEGER)
    waiting_order = db.Column(db.INTEGER)
    disputed_order = db.Column(db.INTEGER)
    disputedtimer = db.Column(db.TIMESTAMP())
    modid = db.Column(db.INTEGER)
    delivered_order = db.Column(db.INTEGER)
    title = db.Column(db.VARCHAR(500))
    age = db.Column(db.TIMESTAMP())
    returncancelage = db.Column(db.TIMESTAMP())
    return_by = db.Column(db.TIMESTAMP())
    private_note = db.Column(db.TEXT)
    escrow = db.Column(db.VARCHAR(500))
    item_id = db.Column(db.INTEGER)
    string_auction_id = db.Column(db.VARCHAR(50))
    string_node_id = db.Column(db.VARCHAR(50))
    image_one = db.Column(db.VARCHAR(100))
    quantity = db.Column(db.INTEGER)
    request_cancel = db.Column(db.INTEGER)
    reason_cancel = db.Column(db.INTEGER)
    cancelled = db.Column(db.INTEGER)
    request_return = db.Column(db.INTEGER)
    shipping_price = db.Column(db.DECIMAL(20, 8))
    shipdescription = db.Column(db.VARCHAR(500))
    overallreason = db.Column(db.TEXT)
    return_id = db.Column(db.INTEGER)
    return_quantity = db.Column(db.INTEGER)
    return_amount = db.Column(db.DECIMAL(20, 8))
    feedback = db.Column(db.INTEGER)
    userfeedback = db.Column(db.INTEGER)
    completed = db.Column(db.INTEGER)
    perbtc = db.Column(db.DECIMAL(20, 2))
    completed_time = db.Column(db.TIMESTAMP())
    return_allowed = db.Column(db.INTEGER)
    buyorsell = db.Column(db.INTEGER)
    released = db.Column(db.INTEGER)
    digital_currency = db.Column(db.INTEGER)
    fee = db.Column(db.DECIMAL(20, 8))
    price = db.Column(db.DECIMAL(20, 8))
    price_peritem_btc = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_btc = db.Column(db.DECIMAL(20, 8))
    price_peritem_bch = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_bch = db.Column(db.DECIMAL(20, 8))
    price_peritem_xmr = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_xmr = db.Column(db.DECIMAL(20, 8))
    # affiliate stuff
    affiliate_discount_percent = db.Column(db.DECIMAL(4, 2))
    affiliate_code = db.Column(db.VARCHAR(20))
    affiliate_profit = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc_cash = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_xmr = db.Column(db.DECIMAL(20, 12))

class Vendor_Orders_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Orders

    uuid = ma.auto_field()

    type = ma.auto_field()
    vendor = ma.auto_field()
    vendor_id = ma.auto_field()
    customer = ma.auto_field()
    customer_id = ma.auto_field()
    currency = ma.auto_field()
    incart = ma.auto_field()
    new_order = ma.auto_field()
    accepted_order = ma.auto_field()
    waiting_order = ma.auto_field()
    disputed_order = ma.auto_field()
    disputedtimer = ma.auto_field()
    modid = ma.auto_field()
    delivered_order = ma.auto_field()
    title = ma.auto_field()
    age = ma.auto_field()
    returncancelage = ma.auto_field()
    return_by = ma.auto_field()
    private_note = ma.auto_field()
    escrow = ma.auto_field()
    item_id = ma.auto_field()
    string_auction_id = ma.auto_field()
    string_node_id = ma.auto_field()
    image_one = ma.auto_field()
    quantity = ma.auto_field()
    request_cancel = ma.auto_field()
    reason_cancel = ma.auto_field()
    cancelled = ma.auto_field()
    request_return = ma.auto_field()
    shipping_price = ma.auto_field()
    shipdescription = ma.auto_field()
    overallreason = ma.auto_field()
    return_id = ma.auto_field()
    return_quantity = ma.auto_field()
    return_amount = ma.auto_field()
    feedback = ma.auto_field()
    userfeedback = ma.auto_field()
    completed = ma.auto_field()
    perbtc = ma.auto_field()
    completed_time = ma.auto_field()
    return_allowed = ma.auto_field()
    buyorsell = ma.auto_field()
    released = ma.auto_field()
    digital_currency = ma.auto_field()
    fee = ma.auto_field()
    price = ma.auto_field()
    price_peritem_btc = ma.auto_field()
    price_beforediscount_btc = ma.auto_field()
    price_peritem_bch = ma.auto_field()
    price_beforediscount_bch = ma.auto_field()
    price_peritem_xmr = ma.auto_field()
    price_beforediscount_xmr = ma.auto_field()


class Vendor_NotShipping(db.Model):
    __tablename__ = 'vendor_not_shipping_country'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    code = db.Column(db.INTEGER)
    name = db.Column(db.VARCHAR(40))

class Vendor_NotShipping_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_NotShipping
    id = ma.auto_field()
    code = ma.auto_field()
    name = ma.auto_field()


class Vendor_VendorVerification(db.Model):
    __tablename__ = 'vendor_verification_level'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.INTEGER)
    vendor_level = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    amount = db.Column(db.DECIMAL(20, 8))

class Vendor_VendorVerification_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_VendorVerification
    id = ma.auto_field()
    vendor_id = ma.auto_field()
    vendor_level = ma.auto_field()
    timestamp = ma.auto_field()
    amount = ma.auto_field()

class Vendor_Duration(db.Model):
    __tablename__ = 'vendor_duration_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    time = db.Column(db.VARCHAR(140))
    displaytime = db.Column(db.VARCHAR(140))

class Vendor_Duration_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Duration
    id = ma.auto_field()
    time = ma.auto_field()
    displaytime = ma.auto_field()


class Vendor_EbaySearchItem(db.Model):
    __tablename__ = 'vendor_ebay_item'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,  primary_key=True,autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    itemebayid = db.Column(db.BIGINT)
    itemtitle = db.Column(db.VARCHAR(500))
    itemprice = db.Column(db.DECIMAL(20, 4))
    itemquantity = db.Column(db.INTEGER)
    item_condition = db.Column(db.INTEGER)
    itemcategory = db.Column(db.VARCHAR(300))
    status = db.Column(db.INTEGER)
    errortext = db.Column(db.TEXT)


class Vendor_EbaySearchItem_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_EbaySearchItem
