from app import db, ma


class Checkout_CheckoutShoppingCart(db.Model):
    __tablename__ = 'checkout_shopping_cart'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    item_id = db.Column(db.INTEGER)
    item_uuid = db.Column(db.VARCHAR(50))
    customer_user_name = db.Column(db.VARCHAR(140))
    customer_id = db.Column(db.INTEGER)
    customer_uuid = db.Column(db.VARCHAR(50))
    vendor_user_name = db.Column(db.VARCHAR(140))
    vendor_id = db.Column(db.INTEGER)
    vendor_uuid = db.Column(db.VARCHAR(50))
    currency = db.Column(db.INTEGER)
    title_of_item = db.Column(db.VARCHAR(500))
    price_of_item = db.Column(db.DECIMAL(20, 2))
    image_of_item = db.Column(db.VARCHAR(500))
    # how many items in your cart you wanna buy
    quantity_of_item = db.Column(db.INTEGER)

    # how many items vendor has
    vendor_supply = db.Column(db.INTEGER)
    saved_for_later = db.Column(db.INTEGER)

    shipping_info_0 = db.Column(db.VARCHAR(350))
    shipping_day_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.VARCHAR(350))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.VARCHAR(350))
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_3 = db.Column(db.INTEGER)
    shipping_free = db.Column(db.BOOLEAN)
    shipping_two = db.Column(db.BOOLEAN)
    shipping_three = db.Column(db.BOOLEAN)

    digital_currency_1 = db.Column(db.BOOLEAN)
    digital_currency_2 = db.Column(db.BOOLEAN)
    digital_currency_3 = db.Column(db.BOOLEAN)

    selected_digital_currency = db.Column(db.INTEGER)
    selected_shipping = db.Column(db.INTEGER)
    selected_shipping_description = db.Column(db.VARCHAR(350))

    final_shipping_price_btc = db.Column(db.DECIMAL(20, 8))
    final_price_btc = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_bch = db.Column(db.DECIMAL(20, 8))
    final_price_bch = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_xmr = db.Column(db.DECIMAL(20, 12))
    final_price_xmr = db.Column(db.DECIMAL(20, 12))


class Checkout_ShoppingCart_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_CheckoutShoppingCart

        fields = ('id', 'customer_user_name', 'vendor_user_name', 'customer_uuid', 'vendor_uuid',
                  'title_of_item', 'price_of_item', 'image_of_item', 'quantity_of_item',
                  'digital_currency_1', 'digital_currency_2', 'digital_currency_3',
                  'shipping_free', 'shipping_two', 'shipping_three',
                  'shipping_info_0', 'shipping_info_2', 'shipping_info_3',
                  'shipping_day_0', 'shipping_day_2', 'shipping_day_3',
                  'shipping_price_3', 'shipping_price_3', 'shipping_price_3',
                  'selected_digital_currency', 'selected_shipping', 'vendor_supply'
                  )


cart_schema = Checkout_ShoppingCart_Schema()
carts_schema = Checkout_ShoppingCart_Schema(many=True)


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


class Checkout_CheckoutShoppingCartTotal_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout_ShoppingCartTotal


cart_total_schema = Checkout_CheckoutShoppingCartTotal_Schema()
carts_total_schema = Checkout_CheckoutShoppingCartTotal_Schema(many=True)
