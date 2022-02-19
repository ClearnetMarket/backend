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
    shipping_day_least_0 = db.Column(db.INTEGER)
    shipping_day_most_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.VARCHAR(350))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_2 = db.Column(db.INTEGER)
    shipping_day_most_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.VARCHAR(350))
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_3 = db.Column(db.INTEGER)
    shipping_day_most_3 = db.Column(db.INTEGER)
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

    final_shipping_price_xmr = db.Column(db.DECIMAL(20, 8))
    final_price_xmr = db.Column(db.DECIMAL(20, 8))


class Checkout_CheckoutShoppingCart_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_CheckoutShoppingCart
    id = ma.auto_field()
    customer = ma.auto_field()
    customer_id = ma.auto_field()
    vendor = ma.auto_field()
    vendor_id = ma.auto_field()
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
    shipping_day_least_0 = ma.auto_field()
    shipping_day_most_0 = ma.auto_field()
    shipping_info_2 = ma.auto_field()
    shipping_price_2 = ma.auto_field()
    shipping_day_least_2 = ma.auto_field()
    shipping_day_most_2 = ma.auto_field()
    shipping_info_3 = ma.auto_field()
    shipping_price_3 = ma.auto_field()
    shipping_day_least_3 = ma.auto_field()
    shipping_day_most_3 = ma.auto_field()
    shipping_free = ma.auto_field()
    shipping_two = ma.auto_field()
    shipping_three = ma.auto_field()
    return_allowed = ma.auto_field()
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


class Checkout_ShoppingCartTotal(db.Model):
    __tablename__ = 'checkout_shopping_cart_total'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    customer = db.Column(db.INTEGER)
    # btc
    btc_sumofitem = db.Column(db.INTEGER)
    btcprice = db.Column(db.DECIMAL(20, 8))
    shippingbtcprice = db.Column(db.DECIMAL(20, 8))
    totalbtcprice = db.Column(db.DECIMAL(20, 8))
    # bch
    btc_cash_sumofitem = db.Column(db.INTEGER)
    btc_cash_price = db.Column(db.DECIMAL(20, 8))
    shipping_btc_cashprice = db.Column(db.DECIMAL(20, 8))
    total_btc_cash_price = db.Column(db.DECIMAL(20, 8))
    # xmr
    xmr_sumofitem = db.Column(db.INTEGER)
    xmrprice = db.Column(db.DECIMAL(20, 12))
    shippingxmrprice = db.Column(db.DECIMAL(20, 12))
    totalxmrprice = db.Column(db.DECIMAL(20, 12))
    # affiliate stuff
    percent_off_order = db.Column(db.DECIMAL(6, 2))
    btc_cash_off = db.Column(db.DECIMAL(20, 8))
    btc_off = db.Column(db.DECIMAL(20, 8))
    xmr_off = db.Column(db.DECIMAL(20, 12))


class Checkout_ShoppingCartTotal_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_ShoppingCartTotal

    id = ma.auto_field()
    customer = ma.auto_field()
    # btc
    btc_sumofitem = ma.auto_field()
    btcprice = ma.auto_field()
    shippingbtcprice = ma.auto_field()
    totalbtcprice = ma.auto_field()
    # bch
    btc_cash_sumofitem = ma.auto_field()
    btc_cash_price = ma.auto_field()
    shipping_btc_cashprice = ma.auto_field()
    total_btc_cash_price = ma.auto_field()
    # xmr
    xmr_sumofitem = ma.auto_field()
    xmrprice = ma.auto_field()
    shippingxmrprice = ma.auto_field()
    totalxmrprice = ma.auto_field()
    # affiliate stuff
    percent_off_order = ma.auto_field()
    btc_cash_off = ma.auto_field()
    btc_off = ma.auto_field()
    xmr_off = ma.auto_field()
