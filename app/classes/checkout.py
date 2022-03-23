from app import db, ma


class Checkout_CheckoutShoppingCart(db.Model):
    __tablename__ = 'checkout_shopping_cart'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    customer = db.Column(db.VARCHAR(40))
    customer_id = db.Column(db.INTEGER)
    vendor = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    vendor_uuid = db.Column(db.VARCHAR(50))
    currency = db.Column(db.INTEGER)
    title_of_item = db.Column(db.VARCHAR(500))
    price_of_item = db.Column(db.DECIMAL(20, 2))
    image_of_item = db.Column(db.VARCHAR(100))
    quantity_of_item = db.Column(db.INTEGER)
    return_policy = db.Column(db.TEXT)
    savedforlater = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    vendorsupply = db.Column(db.INTEGER)
    shipping_info_0 = db.Column(db.VARCHAR(350))
    shipping_day_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.VARCHAR(350))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.VARCHAR(350))
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_3 = db.Column(db.INTEGER)
    shipping_free = db.Column(db.INTEGER)
    shipping_two = db.Column(db.INTEGER)
    shipping_three = db.Column(db.INTEGER)
    return_allowed = db.Column(db.INTEGER)

    digital_currency_1 = db.Column(db.INTEGER)
    digital_currency_2 = db.Column(db.INTEGER)
    digital_currency_3 = db.Column(db.INTEGER)

    selected_currency = db.Column(db.INTEGER)
    selected_shipping = db.Column(db.INTEGER)
    selected_shipping_description = db.Column(db.VARCHAR(350))

    final_shipping_price_btc = db.Column(db.DECIMAL(20, 8))
    final_price_btc = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_bch = db.Column(db.DECIMAL(20, 8))
    final_price_bch = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_xmr = db.Column(db.DECIMAL(20, 12))
    final_price_xmr = db.Column(db.DECIMAL(20, 12))





class Checkout_ShoppingCartTotal(db.Model):
    __tablename__ = 'checkout_shopping_cart_total'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    customer_id = db.Column(db.INTEGER)

    # btc
    # how many of item
    btc_sum_of_item = db.Column(db.INTEGER)
    # bitcoin market price at time of transaction
    btc_price = db.Column(db.DECIMAL(20, 8))
    # total shipping price in btc
    btc_shipping_price = db.Column(db.DECIMAL(20, 8))
    # total cost in btc
    btc_total_price = db.Column(db.DECIMAL(20, 8))

    # bch
    # how many of item
    bch_sum_of_item = db.Column(db.INTEGER)
    # bch market price at time of transaction
    bch_price = db.Column(db.DECIMAL(20, 8))
    # total shipping price in bch
    bch_shipping_price = db.Column(db.DECIMAL(20, 8))
    # total cost in bch
    bch_total_price = db.Column(db.DECIMAL(20, 8))

    # xmr
    # how many of item
    xmr_sum_of_item = db.Column(db.INTEGER)
    # monero market price at time of transaction
    xmr_price = db.Column(db.DECIMAL(20, 12))
    # total shipping price in xmr
    xmr_shipping_price = db.Column(db.DECIMAL(20, 12))
    # total cost in xmr
    xmr_total_price = db.Column(db.DECIMAL(20, 12))









class Checkout_ShoppingCartTotal_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_ShoppingCartTotal
        
    # btc
    btc_sum_of_item = ma.auto_field()
    btc_price = ma.auto_field()
    btc_shipping_price = ma.auto_field()
    btc_total_price = ma.auto_field()
    # bch
    bch_sum_of_item = ma.auto_field()
    bch_price = ma.auto_field()
    bch_shipping_price = ma.auto_field()
    bch_total_price = ma.auto_field()
    # xmr
    xmr_sum_of_item = ma.auto_field()
    xmr_price = ma.auto_field()
    xmr_shipping_price = ma.auto_field()
    xmr_total_price = ma.auto_field()


class Checkout_CheckoutShoppingCart_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_CheckoutShoppingCart

    customer = ma.auto_field()

    vendor = ma.auto_field()

    currency = ma.auto_field()
    title_of_item = ma.auto_field()
    price_of_item = ma.auto_field()
    image_of_item = ma.auto_field()
    quantity_of_item = ma.auto_field()
    return_policy = ma.auto_field()
    savedforlater = ma.auto_field()
    item_id = ma.auto_field()
    vendorsupply = ma.auto_field()
    shipping_info_0 = ma.auto_field()

    shipping_day_0 = ma.auto_field()
    shipping_info_2 = ma.auto_field()
    shipping_price_2 = ma.auto_field()
    shipping_day_2 = ma.auto_field()
    shipping_info_3 = ma.auto_field()
    shipping_price_3 = ma.auto_field()
    shipping_day_3 = ma.auto_field()
    shipping_free = ma.auto_field()
    shipping_two = ma.auto_field()
    shipping_three = ma.auto_field()
    digital_currency_1 = ma.auto_field()
    digital_currency_2 = ma.auto_field()
    digital_currency_3 = ma.auto_field()
    selected_currency = ma.auto_field()
    selected_shipping = ma.auto_field()
    selected_shipping_description = ma.auto_field()

    final_shipping_price_btc = ma.auto_field()
    final_price_btc = ma.auto_field()

    final_shipping_price_bch = ma.auto_field()
    final_price_bch = ma.auto_field()

    final_shipping_price_xmr = ma.auto_field()
    final_price_xmr = ma.auto_field()
