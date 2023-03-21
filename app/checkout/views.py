from flask import jsonify, request
from flask_login import current_user, login_required
from app.checkout import checkout
from app import db
from app.common.notification import create_notification
from datetime import datetime
from decimal import Decimal

# models
from app.classes.checkout import \
    Checkout_CheckoutShoppingCart, \
    Checkout_ShoppingCartTotal, \
    carts_schema
from app.classes.auth import \
    Auth_User, \
    Auth_UserFees
from app.classes.item import \
    Item_MarketItem
from app.classes.service import \
    Service_ShippingSecret
from app.classes.user_orders import User_Orders
from app.classes.models import Query_Country
from app.classes.wallet_btc import Btc_Wallet
from app.classes.wallet_bch import Bch_Wallet
from app.classes.wallet_xmr import Xmr_Wallet
from app.classes.vendor import Vendor_Notification
from app.classes.userdata import UserData_DefaultAddress
from app.classes.feedback import Feedback_Feedback
from app.classes.profile import\
    Profile_StatisticsUser, \
    Profile_StatisticsVendor
# endmodels

from app.wallet_bch.wallet_bch_work import bch_send_coin_to_escrow
from app.wallet_btc.wallet_btc_work import btc_send_coin_to_escrow
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin_to_escrow
from app.common.functions import floating_decimals, \
    convert_local_to_bch, \
    convert_local_to_btc, \
    convert_local_to_xmr


def cart_calculate_total_price(user_id):
    """
    # Calculates cart total table
    First it gets the total cart, all cart items, and wallets of each user
    Then Loop through each cart item appending it to the list
        - appends total price of item
        - appends 

    """

    total_cart = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter(Checkout_ShoppingCartTotal.customer_id == user_id) \
        .first()
    shopping_cart = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .all()

    # Bitcoin
    btc_pricelist = []
    btc_shipping_pricelist = []
    btc_items_quan = []

    # Bitcoin cash
    bch_pricelist = []
    bch_shipping_pricelist = []
    bch_items_quan = []

    # Monero
    xmr_pricelist = []
    xmr_shipping_pricelist = []
    xmr_items_quan = []

    total_cart.btc_sum_of_item = 0
    total_cart.btc_price = 0
    total_cart.btc_shipping_price = 0
    total_cart.btc_total_price = 0
    total_cart.bch_sum_of_item = 0
    total_cart.bhc_price = 0
    total_cart.bch_shipping_price = 0
    total_cart.bch_total_price = 0
    total_cart.xmr_sum_of_item = 0
    total_cart.xmr_price = 0
    total_cart.xmr_shipping_price = 0
    total_cart.xmr_total_price = 0
    for cart in shopping_cart:

        if cart.selected_digital_currency == 1:
            btc_pricelist.append(cart.final_price_btc)
            btc_shipping_pricelist.append(cart.final_shipping_price_btc)
            btc_items_quan.append(int(cart.quantity_of_item))
        elif cart.selected_digital_currency == 2:
            bch_pricelist.append(cart.final_price_bch)
            bch_shipping_pricelist.append(cart.final_shipping_price_bch)
            bch_items_quan.append(int(cart.quantity_of_item))
        elif cart.selected_digital_currency == 3:
            xmr_pricelist.append(cart.final_price_xmr)
            xmr_shipping_pricelist.append(cart.final_shipping_price_xmr)
            xmr_items_quan.append(int(cart.quantity_of_item))
        else:
            return jsonify({'error': 'Error:  Incorrect Currency'})

    # get sum of prices in list 
    if len(btc_pricelist) > 0:
        btc_sum_of_item = sum(btc_items_quan)

        total_cart.btc_sum_of_item = btc_sum_of_item
        # get sum of prices in list
        btc_formatted_total_price = ("{0:.8f}".format(sum(btc_pricelist)))
        # get sum of shipping prices
        btc_formatted_total_shipping_price = ("{0:.8f}".format(sum(btc_shipping_pricelist)))
        total_cart.btc_price = btc_formatted_total_price
        total_cart.btc_shipping_price = btc_formatted_total_shipping_price
        # get total price
        btc_add_total = Decimal(btc_formatted_total_price) + Decimal(btc_formatted_total_shipping_price)
        total_cart.btc_total_price = btc_add_total

    if len(bch_pricelist) > 0:
        # get sum of prices in list
        bch_sum_of_item = sum(bch_items_quan)
        total_cart.bch_sum_of_item = bch_sum_of_item
        bch_formatted_total_price = ("{0:.8f}".format(sum(bch_pricelist)))
        # get sum of shipping prices
        bch_formatted_total_shipping_price = ("{0:.8f}".format(sum(bch_shipping_pricelist)))
        total_cart.bch_price = bch_formatted_total_price
        total_cart.bch_shipping_price = bch_formatted_total_shipping_price
        # get total price
        bch_add_total = Decimal(bch_formatted_total_price) + Decimal(bch_formatted_total_shipping_price)
        total_cart.bch_total_price = bch_add_total

    # get sum of prices in list
    if len(xmr_pricelist) > 0:
        xmr_sum_of_item = sum(xmr_items_quan)
        total_cart.xmr_sum_of_item = xmr_sum_of_item
        # get sum of prices in list
        xmr_formatted_total_price = ("{0:.12f}".format(sum(xmr_pricelist)))
        # get sum of shipping prices
        xmr_formatted_total_shipping_price = ("{0:.12f}".format(sum(xmr_shipping_pricelist)))
        total_cart.xmr_price = xmr_formatted_total_price
        total_cart.xmr_shipping_price = xmr_formatted_total_shipping_price
        # get total price
        xmr_add_total = Decimal(xmr_formatted_total_price) + Decimal(xmr_formatted_total_shipping_price)
        total_cart.xmr_total_price = xmr_add_total

    db.session.add(total_cart)
    db.session.flush()


def cart_calculate_item_shipping_and_price_cart(cartitemid):
    """
    # calculates shopping cart table
    Function takes cart if of item in shopping cart
    THen it determines the currency being used
    Converts the local price to cryptocurrency prices
    determines quantity and calculates price
    """

    cartitem = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartitemid) \
        .first()
    getitem = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.id == cartitem.item_id) \
        .first()

    cartitem_exists = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartitemid) \
        .first() is not None
    getitem_exists = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.id == cartitem.item_id) \
        .first() is not None

    if cartitem_exists is None or getitem_exists is None:
        return jsonify({"error": "Could not find items in the cart"}), 200
        # BITCOIN

    if cartitem.selected_digital_currency == 1:
        # SHIPPING
        # free shipping
        if cartitem.selected_shipping == 1:
            shipprice = 0
        elif cartitem.selected_shipping == 2:
            shipprice = Decimal(getitem.shipping_price_2)
        else:
            shipprice = Decimal(getitem.shipping_price_3)
        # convert it to btc cash
        btc_ship_price = Decimal(convert_local_to_btc(amount=shipprice, currency=getitem.currency))
        # get it formatted correctly
        btc_shipprice_formatted = (floating_decimals(btc_ship_price, 8))
        # times the shipping price times quantity
        btc_shippingtotal = Decimal(cartitem.quantity_of_item) * Decimal(btc_shipprice_formatted)
        # return shipping price
        btc_ship_price_final = (floating_decimals(btc_shippingtotal, 8))
        # set variable in database
        cartitem.final_shipping_price_btc = btc_ship_price_final

        # PRICING
        btc_itemprice = Decimal(getitem.price)
        btc_price_per_item = Decimal(convert_local_to_btc(amount=btc_itemprice, currency=getitem.currency))
        btc_price_formatted = (floating_decimals(btc_price_per_item, 8))
        btc_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(btc_price_formatted)
        btc_price_final = (floating_decimals(btc_pricing_multiply, 8))
        cartitem.final_price_btc = btc_price_final

    # BITCOIN CASH
    if cartitem.selected_digital_currency == 2:
        # SHIPPING
        # free shipping
        if cartitem.selected_shipping == 1:
            shipprice = 0
        elif cartitem.selected_shipping == 2:
            shipprice = Decimal(getitem.shipping_price_2)
        else:
            shipprice = Decimal(getitem.shipping_price_3)
        # convert it to btc cash
        bch_ship_price = Decimal(convert_local_to_bch(amount=shipprice, currency=getitem.currency))
        # get it formatted correctly
        bch_shipprice_formatted = (floating_decimals(bch_ship_price, 8))
        # times the shipping price times quantity
        bch_shippingtotal = Decimal(cartitem.quantity_of_item) * Decimal(bch_shipprice_formatted)
        # return shipping price
        bch_ship_price_final = (floating_decimals(bch_shippingtotal, 8))
        # set variable in database
        cartitem.final_shipping_price_bch = bch_ship_price_final

        # PRICING
        bch_itemprice = Decimal(getitem.price)
        bch_price_per_item = Decimal(convert_local_to_bch(amount=bch_itemprice, currency=getitem.currency))
        bch_price_formatted = (floating_decimals(bch_price_per_item, 8))
        bch_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(bch_price_formatted)
        bch_price_final = (floating_decimals(bch_pricing_multiply, 8))
        cartitem.final_price_bch = bch_price_final

    # Monero
    if cartitem.selected_digital_currency == 3:
        # free shipping
        if cartitem.selected_shipping == 1:
            shipprice = 0
        elif cartitem.selected_shipping == 2:
            shipprice = Decimal(getitem.shipping_price_2)
        else:
            shipprice = Decimal(getitem.shipping_price_3)
        # convert it to btc cash
        xmr_ship_price = Decimal(convert_local_to_xmr(amount=shipprice, currency=getitem.currency))
        # get it formatted correctly
        xmr_shipprice_formatted = (floating_decimals(xmr_ship_price, 12))
        # times the shipping price times quantity
        xmr_shippingtotal = Decimal(cartitem.quantity_of_item) * Decimal(xmr_shipprice_formatted)
        # return shipping price
        xmr_ship_price_final = (floating_decimals(xmr_shippingtotal, 12))
        # set variable in database
        cartitem.final_shipping_price_xmr = xmr_ship_price_final

        # PRICING
        xmr_itemprice = Decimal(getitem.price)
        xmr_price_per_item = Decimal(convert_local_to_xmr(amount=xmr_itemprice, currency=getitem.currency))
        xmr_price_formatted = (floating_decimals(xmr_price_per_item, 12))
        xmr_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(xmr_price_formatted)
        xmr_price_final = (floating_decimals(xmr_pricing_multiply, 12))
        cartitem.final_price_xmr = xmr_price_final

    db.session.add(cartitem)
    db.session.flush()


def cart_calculate_item_shipping_and_price_all(userid):
    """
    # calculates shopping cart table
    Function takes cart if of item in shopping cart
    THen it determines the currency being used
    Converts the local price to cryptocurrency prices
    determines quantity and calculates price
    """

    cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_id == userid) \
        .all()

    # BITCOIN
    for f in cart_items:

        getitem = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.id == f.item_id) \
            .first()
        if f.selected_digital_currency == 1:

            # SHIPPING
            # free shipping
            if f.selected_shipping == 1:
                shipprice = 0
            elif f.selected_shipping == 2:
                shipprice = Decimal(getitem.shipping_price_2)
            else:
                shipprice = Decimal(getitem.shipping_price_3)
            # convert it to btc cash
            btc_ship_price = Decimal(convert_local_to_btc(amount=shipprice, currency=getitem.currency))
            # get it formatted correctly
            btc_shipprice_formatted = (floating_decimals(btc_ship_price, 8))
            # times the shipping price times quantity
            btc_shippingtotal = Decimal(f.quantity_of_item) * Decimal(btc_shipprice_formatted)
            # return shipping price
            btc_ship_price_final = (floating_decimals(btc_shippingtotal, 8))
            # set variable in database
            f.final_shipping_price_btc = btc_ship_price_final

            # PRICING
            btc_itemprice = Decimal(getitem.price)
            btc_price_per_item = Decimal(convert_local_to_btc(amount=btc_itemprice, currency=getitem.currency))
            btc_price_formatted = (floating_decimals(btc_price_per_item, 8))
            btc_pricing_multiply = Decimal(f.quantity_of_item) * Decimal(btc_price_formatted)
            btc_price_final = (floating_decimals(btc_pricing_multiply, 8))
            f.final_price_btc = btc_price_final

        # BITCOIN CASH
        if f.selected_digital_currency == 2:

            # SHIPPING
            # free shipping
            if f.selected_shipping == 1:
                shipprice = 0
            elif f.selected_shipping == 2:
                shipprice = Decimal(getitem.shipping_price_2)
            else:
                shipprice = Decimal(getitem.shipping_price_3)
            # convert it to btc cash
            bch_ship_price = Decimal(convert_local_to_bch(amount=shipprice, currency=getitem.currency))
            # get it formatted correctly
            bch_shipprice_formatted = (floating_decimals(bch_ship_price, 8))
            # times the shipping price times quantity
            bch_shippingtotal = Decimal(f.quantity_of_item) * Decimal(bch_shipprice_formatted)
            # return shipping price
            bch_ship_price_final = (floating_decimals(bch_shippingtotal, 8))
            # set variable in database
            f.final_shipping_price_bch = bch_ship_price_final

            # PRICING
            bch_itemprice = Decimal(getitem.price)
            bch_price_per_item = Decimal(convert_local_to_bch(amount=bch_itemprice, currency=getitem.currency))
            bch_price_formatted = (floating_decimals(bch_price_per_item, 8))
            bch_pricing_multiply = Decimal(f.quantity_of_item) * Decimal(bch_price_formatted)
            bch_price_final = (floating_decimals(bch_pricing_multiply, 8))
            f.final_price_bch = bch_price_final

        # Monero
        if f.selected_digital_currency == 3:
            # free shipping
            if f.selected_shipping == 1:
                shipprice = 0
            elif f.selected_shipping == 2:
                shipprice = Decimal(getitem.shipping_price_2)
            else:
                shipprice = Decimal(getitem.shipping_price_3)
            # convert it to btc cash
            xmr_ship_price = Decimal(convert_local_to_xmr(amount=shipprice, currency=getitem.currency))
            # get it formatted correctly
            xmr_shipprice_formatted = floating_decimals(xmr_ship_price, 12)
            # times the shipping price times quantity
            xmr_shippingtotal = Decimal(f.quantity_of_item) * Decimal(xmr_shipprice_formatted)
            # return shipping price
            xmr_ship_price_final = floating_decimals(xmr_shippingtotal, 12)
            # set variable in database
            f.final_shipping_price_xmr = xmr_ship_price_final

            # PRICING
            xmr_itemprice = Decimal(getitem.price)
            xmr_price_per_item = Decimal(convert_local_to_xmr(amount=xmr_itemprice, currency=getitem.currency))
            xmr_price_formatted = floating_decimals(xmr_price_per_item, 12)
            xmr_pricing_multiply = Decimal(f.quantity_of_item) * Decimal(xmr_price_formatted)
            xmr_price_final = floating_decimals(xmr_pricing_multiply, 12)
            f.final_price_xmr = xmr_price_final

        db.session.add(f)

    db.session.flush()


def checkout_clear_shopping_cart(userid):
    """
    Puts totals of cart to zero
    Then deletes all items in the regular cat
    """
    # clear user shoppingcarttotal
    user = db.session \
        .query(Auth_User) \
        .filter_by(username=current_user.username) \
        .first()
    get_total_cart_for_user = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer_id=user.id) \
        .first()

    get_shopping_cart = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_id == userid) \
        .all()
    get_total_cart_for_user.btc_sum_of_item = 0
    get_total_cart_for_user.btc_price = 0
    get_total_cart_for_user.btc_shipping_price = 0
    get_total_cart_for_user.btc_total_price = 0
    get_total_cart_for_user.bch_sum_of_item = 0
    get_total_cart_for_user.bch_price = 0
    get_total_cart_for_user.bch_shipping_price = 0
    get_total_cart_for_user.bch_total_price = 0
    get_total_cart_for_user.xmr_sum_of_item = 0
    get_total_cart_for_user.xmr_price = 0
    get_total_cart_for_user.xmr_shipping_price = 0
    get_total_cart_for_user.xmr_total_price = 0
    db.session.add(get_total_cart_for_user)

    # delete items in cart
    for cart in get_shopping_cart:
        db.session.delete(cart)
    db.session.flush()


def checkout_delete_private_msg(userid):
    """
    Deletes the private message
    """
    user = db.session \
        .query(Auth_User) \
        .filter(Auth_User.id == userid) \
        .first()
    oldmsg = db.session \
        .query(Service_ShippingSecret) \
        .filter_by(user_id=user.id, orderid=0) \
        .first()
    db.session.delete(oldmsg)
    db.session.flush()


def checkoutput_item_offline(itemid):
    """
    If user bought last or only item. take vendors item offline
    """
    getitem = db.session \
        .query(Item_MarketItem) \
        .filter_by(uuid=itemid) \
        .first()

    # turn off if item is less than one
    if getitem.item_count == 0:
        getitem.online = 0
        db.session.add(getitem)

        # send notification to vendor saying its all sold out
        create_notification(username=getitem.vendor_name,
                     user_uuid=getitem.vendor_uuid,
                     msg="Your item has been sold out and is has been put offline."
                     )

# updates pricing and quanity of items in shopping cart
@checkout.route('/update/price', methods=['GET'])
@login_required
def checkout_update_cart_information():
    """
    updates pricing and quanity of items in shopping cart
    """
    # get user shopping cart
    get_cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_id == current_user.id) \
        .all()
    # set current amount to 0
    new_amount = 0
    # loop through cart
    for f in get_cart_items:
        # get the market item of the order
        get_market_item = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.id == f.item_id) \
            .first()
        # if order price doesnt equal market price set the price
        if f.price_of_item != get_market_item.price:
            new_amount += 1
            f.price_of_item = get_market_item.price

        db.session.add(f)

    if new_amount > 0:
        db.session.commit()
    return jsonify({'success': 'Got cat information'})


# updates pricing for the user
@checkout.route('/update/price', methods=['GET'])
@login_required
def checkout_update_payment_information():
    """
    Sends the Payments for the cryptocurrencies
    """
    cart_calculate_item_shipping_and_price_all(current_user.id)
    cart_calculate_total_price(current_user.id)
    db.session.commit()
    return jsonify({'success': 'Updated payment information'})


@checkout.route('/add/<string:itemuuid>', methods=['POST'])
@login_required
def cart_add_to_shopping_cart(itemuuid):
    """
    Adds item to shopping cart
    """

    get_item_for_sale = db.session \
        .query(Item_MarketItem) \
        .filter_by(uuid=itemuuid) \
        .first()
    if get_item_for_sale.vendor_uuid == current_user.uuid:
        return jsonify({'error': 'Error:  Can not buy your own item.'}), 200
    # see if in shopping cart

    see_if_item_in_cart = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.item_uuid == itemuuid) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid) \
        .first()

    if see_if_item_in_cart:
        return jsonify({'error': 'Error: Item is in cart already.'}), 200


    if get_item_for_sale.shipping_free is True:
        shipping_selected = 1
        shipinfodesc = f'Takes {get_item_for_sale.shipping_day_0} days for Free'
    elif get_item_for_sale.shipping_free is True:
        shipping_selected = 2
        shipinfodesc = f'Takes {get_item_for_sale.shipping_day_2} days for ' \
                       f'{get_item_for_sale.shipping_price_2}{get_item_for_sale.currency_symbol}'
    else:
        shipping_selected = 3
        shipinfodesc = f'Takes {get_item_for_sale.shipping_day_3} days for ' \
                       f'{get_item_for_sale.shipping_price_3}{get_item_for_sale.currency_symbol}'

    # add generic payment type
    if get_item_for_sale.digital_currency_1 is True:
        auto_currency = 1
    elif get_item_for_sale.digital_currency_2 is True:
        auto_currency = 2
    elif get_item_for_sale.digital_currency_3 is True:
        auto_currency = 3
    else:
        auto_currency = 5
    new_shopping_cart_item = Checkout_CheckoutShoppingCart(
        item_id=get_item_for_sale.id,
        item_uuid=get_item_for_sale.uuid,
        customer_user_name=current_user.username,
        customer_id=current_user.id,
        customer_uuid=current_user.uuid,
        vendor_user_name=get_item_for_sale.vendor_display_name,
        vendor_id=get_item_for_sale.vendor_id,
        vendor_uuid=get_item_for_sale.vendor_uuid,
        currency=get_item_for_sale.currency,
        title_of_item=get_item_for_sale.item_title,
        price_of_item=get_item_for_sale.price,
        image_of_item=get_item_for_sale.image_one_url_250,
        shipping_info_0=get_item_for_sale.shipping_info_0,
        shipping_day_0=get_item_for_sale.shipping_day_0,
        shipping_info_2=get_item_for_sale.shipping_info_2,
        shipping_price_2=get_item_for_sale.shipping_price_2,
        shipping_day_2=get_item_for_sale.shipping_day_2,
        shipping_info_3=get_item_for_sale.shipping_info_3,
        shipping_price_3=get_item_for_sale.shipping_price_3,
        shipping_day_3=get_item_for_sale.shipping_day_3,
        vendor_supply=get_item_for_sale.item_count,
        shipping_free=get_item_for_sale.shipping_free,
        shipping_two=get_item_for_sale.shipping_two,
        shipping_three=get_item_for_sale.shipping_three,
        digital_currency_1=get_item_for_sale.digital_currency_1,
        digital_currency_2=get_item_for_sale.digital_currency_2,
        digital_currency_3=get_item_for_sale.digital_currency_3,
        saved_for_later=0,
        quantity_of_item=1,
        selected_digital_currency=auto_currency,
        selected_shipping=shipping_selected,
        selected_shipping_description=shipinfodesc,
        final_shipping_price_btc=None,
        final_price_btc=None,
        final_shipping_price_bch=None,
        final_price_bch=None,
        final_shipping_price_xmr=None,
        final_price_xmr=None,
    )

    db.session.add(new_shopping_cart_item)
    db.session.flush()
    cart_calculate_item_shipping_and_price_cart(new_shopping_cart_item.id)
    cart_calculate_total_price(new_shopping_cart_item.customer_id)
    db.session.commit()
    return jsonify({'success': 'Added to cart'})



@checkout.route('/data/incart', methods=['GET'])
@login_required
def data_shopping_cart_in_cart():
    """
    Returns items in the shopping cart
    """

    cart = db.session \
               .query(Checkout_CheckoutShoppingCart) \
               .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                       Checkout_CheckoutShoppingCart.saved_for_later == 0) \
               .first() is not None
    if cart is None:
        return jsonify({"error": 'Error: Cart is empty'}), 200
    cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .all()

    return carts_schema.jsonify(cart_items)


@checkout.route('/data/incart/count', methods=['GET'])
@login_required
def data_shopping_cart_in_cart_count():
    """
    Returns items in the shopping cart
    """

    cart = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .first() is not None
    if cart is None:
        return jsonify({"error": 'Error: Cart is empty'}), 200
    cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .count()

    return jsonify(
        {"success": "Got cart count successfully",
         "cart_count": cart_items }
    ), 200


@checkout.route('/data/saved', methods=['GET'])
@login_required
def data_shopping_cart_in_saved():
    """
    Returns items in the shopping cart
    """

    cart = db.session \
               .query(Checkout_CheckoutShoppingCart) \
               .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                       Checkout_CheckoutShoppingCart.saved_for_later == 1) \
               .first() is not None
    if cart is None:
        return jsonify({"error": "Error: cart is empty"}), 200
    cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 1) \
        .all()
    return carts_schema.jsonify(cart_items)


@checkout.route('/data/total', methods=['GET'])
@login_required
def data_shopping_cart_total():
    """
    Returns total costs of items for first shopping cart page
    """
    total_in_cart = []
    total_shipping_cart = []
    total_items = []
    all_cart_items = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_id == current_user.id) \
        .filter(Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .all()
    for f in all_cart_items:
        total_in_cart.append(f.price_of_item * f.quantity_of_item)
        total_items.append(f.quantity_of_item)
        if f.selected_shipping is None:
            total_shipping_cart.append(0)
        if f.selected_shipping == 1:
            total_shipping_cart.append(0)
        if f.selected_shipping == 2:
            total_shipping_cart.append(f.shipping_price_2 * f.quantity_of_item)
        if f.selected_shipping == 3:
            total_shipping_cart.append(f.shipping_price_3 * f.quantity_of_item)

    total_items_in_cart = sum(total_items)
    total_price_of_items_with_quantity = sum(total_in_cart)
    total_shipping_price_of_items_with_quantity = sum(total_shipping_cart)

    total = (total_shipping_price_of_items_with_quantity + total_price_of_items_with_quantity)
    return jsonify({
        'success': 'Got shopping cart total',
        'total_items': total_items_in_cart,
        'total_shipping': total_shipping_price_of_items_with_quantity,
        'total_price_before_shipping': total_price_of_items_with_quantity,
        'total_price': total
    })


@checkout.route('/data/cart/total', methods=['GET'])
@login_required
def data_checkout_total():
    """
    Returns items in the shopping cart second page total
    """

    total_cart = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter(Checkout_ShoppingCartTotal.customer_id == current_user.id) \
        .first()

    return jsonify({
        'success': 'Got checkout cart total',
        'btc_sum_of_item': total_cart.btc_sum_of_item,
        'btc_price': total_cart.btc_price,
        'btc_shipping_price': total_cart.btc_shipping_price,
        'btc_total_price': total_cart.btc_total_price,

        'bch_sum_of_item': total_cart.bch_sum_of_item,
        'bch_price': total_cart.bch_price,
        'bch_shipping_price': total_cart.bch_shipping_price,
        'bch_total_price': total_cart.bch_total_price,

        'xmr_sum_of_item': total_cart.xmr_sum_of_item,
        'xmr_price': total_cart.xmr_price,
        'xmr_shipping_price': total_cart.xmr_shipping_price,
        'xmr_total_price': total_cart.xmr_total_price,
    })


@checkout.route('/changeshippingoption/<int:cartid>', methods=['PUT'])
@login_required
def cart_update_shipping_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
    Triggers function to update shipping 
    """

    cartitem = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()
    getitem = db.session \
        .query(Item_MarketItem) \
        .filter_by(id=cartitem.item_id) \
        .first()

    new_shipping = request.json["new_shipping_option"]
    new_shipping = int(new_shipping)
    if new_shipping == 1:
        if getitem.shipping_free is False:
            return jsonify({'error': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_0
    if new_shipping == 2:
        if getitem.shipping_two is False:
            return jsonify({'error': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_2
    if new_shipping == 3:
        if getitem.shipping_three is False:
            return jsonify({'error': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_3

    db.session.flush()
    cart_calculate_item_shipping_and_price_cart(cartitem.id)
    cart_calculate_total_price(cartitem.customer_id)
    db.session.commit()
    return jsonify({'success': 'Updating shipping option'})


@checkout.route('/currentquantity/<int:cartid>', methods=['GET'])
@login_required
def cart_current_quantity(cartid):
    """
    gets current quantity
    """
    the_cart_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()
    return jsonify({
        'success': 'Got cart quanitity',
        'amount': the_cart_item.quantity_of_item
    })


@checkout.route('/movecartitem/<int:cartid>', methods=['PUT'])
@login_required
def cart_move_cart_item(cartid):
    """
    Moves the item from saved to cart
    """
    the_cart_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()

    if the_cart_item.customer_id != current_user.id:
        return jsonify({'error': 'Error:  Couldnt find your cart'})
    the_cart_item.saved_for_later = 0
    db.session.add(the_cart_item)

    cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
    cart_calculate_total_price(the_cart_item.customer_id)

    db.session.commit()
    return jsonify({'success': 'Moved item Successfully'})


@checkout.route('/saveforlater/<int:cartid>', methods=['PUT'])
@login_required
def cart_save_for_later(cartid):
    """
    Save the item fopr later
    """
    cartitem = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()
    if cartitem.customer_id != current_user.id:
        return jsonify({'error': 'Error: Error finding your cart'})
    cartitem.saved_for_later = 1
    db.session.add(cartitem)
    db.session.commit()
    return jsonify({'success': 'Saved item for later'})


@checkout.route('/changepaymentoption/<int:cartid>', methods=['POST'])
@login_required
def cart_update_payment_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """
    the_cart_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()
    getitem = db.session \
        .query(Item_MarketItem) \
        .filter_by(id=the_cart_item.item_id) \
        .first()
    new_currency = request.json["new_currency"]
    new_currency = int(new_currency)

    if new_currency == 1:
        if getitem.digital_currency_1 is False:
            return jsonify({'error': 'Error:  Currency Error'})
        else:
            the_cart_item.selected_digital_currency = new_currency
    if new_currency == 2:

        if getitem.digital_currency_2 is False:
            return jsonify({'error': 'Error:  Currency Error'})
        else:
            the_cart_item.selected_digital_currency = new_currency
    if new_currency == 3:
        if getitem.digital_currency_3 is False:
            return jsonify({'error': 'Error:  Currency Error'})
        else:
            the_cart_item.selected_digital_currency = new_currency
    cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
    cart_calculate_total_price(the_cart_item.customer_id)

    db.session.add(the_cart_item)
    db.session.commit()
    return jsonify({'success': 'Updated payment option'})


@checkout.route('/updateamount/<int:cartid>', methods=['PUT'])
@login_required
def cart_update_quantity(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """
    the_cart_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()
    getitem = db.session \
        .query(Item_MarketItem) \
        .filter_by(id=the_cart_item.item_id) \
        .first()
    new_amount = request.json["new_amount"]
    if int(new_amount) > getitem.item_count:
        return jsonify({'error': 'Error.  Vendor Doesnt have that many items for sale'})
    if the_cart_item.customer_id != current_user.id:
        return jsonify({'error': 'error.  Not your shopping cart.'})
    the_cart_item.quantity_of_item = new_amount
    cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
    cart_calculate_total_price(the_cart_item.customer_id)
    db.session.add(the_cart_item)
    db.session.commit()
    return jsonify({'success': 'Updated quantity'})


@checkout.route('/delete/<int:cartid>', methods=['DELETE'])
@login_required
def cart_delete_item(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """
    the_cart_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.id == cartid) \
        .first()

    if the_cart_item.customer_id != current_user.id:
        return jsonify({'error': 'Error:  Could not find your cart'})

    db.session.delete(the_cart_item)
    db.session.commit()
    return jsonify({'success': 'Deleted item.'})


@checkout.route('/setamount/one', methods=['POST'])
@login_required
def cart_set_quantity_initial_amount():
    """
    When User enters shopping cart.  set amounts to 1
    """
    the_cart = db.session\
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid) \
        .all()
    for f in the_cart:
        f.quantity_of_item = 1
        db.session.add(f)
    db.session.commit()
    return jsonify({'success': 'Set Quantity'})


@checkout.route('/info/delete/<string:itemid>', methods=['POST'])
@login_required
def checkout_delete_secret_info(itemid):
    """
    Delete the message sent to the user
    # """
    user = db.session \
        .query(Auth_User) \
        .filter_by(username=current_user.username) \
        .first()
    get_cart = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer=user.id) \
        .first()
    the_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid) \
        .first()
    if the_item is None:
        return jsonify({'error': 'Error: Couldnt find item'})
    if get_cart.btc_price == 0 and get_cart.bch_price == 0:
        return jsonify({'error': 'Error. No Items in your shopping cart.'})

    # get the message
    msg = db.session \
        .query(Service_ShippingSecret) \
        .filter_by(user_id=user.id, orderid=0) \
        .first()
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'success': 'success'})


@checkout.route('/info/add/<string:itemid>', methods=['POST'])
@login_required
def checkout_add_secret_info(itemid):
    """
    Delete the message sent to the user
    """
    the_item = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid) \
        .first()
    if the_item:
        # get the message
        messagedata = request.json["privatemsg"]
        addmsg = Service_ShippingSecret(
            user_id=current_user.id,
            txtmsg=messagedata,
            timestamp=datetime.utcnow(),
            orderid=0
        )
        db.session.add(addmsg)
        db.session.commit()

        return jsonify({'success': 'Added information'})


def checkout_check_address():
    """
    This function checks if there is a proper address it either returns true or the issue
    """
    get_customer_shipping = db.session \
        .query(UserData_DefaultAddress) \
        .filter(UserData_DefaultAddress.uuid == Checkout_CheckoutShoppingCart.customer_uuid) \
        .first()

    if get_customer_shipping is None:
        return jsonify({'error': 'No Shipping Address provided for vendor'})
    # check if Address
    if len(get_customer_shipping.address) >=5:
        pass
    else:
        return jsonify({'error': 'Error. No Shipping Address provided for vendor.'})

    # check if country
    if get_customer_shipping.country != 0:
        pass
    else:
        return jsonify({'error': 'Error. No Shipping Address provided for vendor.'})

    # check if country
    if get_customer_shipping.country != 0:
        pass
    else:
        return jsonify({'error': 'Error. No Shipping Address provided for vendor.'})

    # check if country
    if len(get_customer_shipping.city) >= 5:
        pass
    else:
        return jsonify({'error': 'Error. City address needs to be specified.'})

    return True


    
@checkout.route('/payment', methods=['POST'])
@login_required
def finalize():
    """
    # PAYMENT STUFF once you click payment button
    """
    # check  if address

    see_if_address = checkout_check_address()

    if see_if_address is not True:
        return jsonify({'error': see_if_address}), 200
    print("1111")
    # make order
    create_order = checkout_make_order()
    if create_order is not True:
        return jsonify({'error': 'Error Creating Order'}), 200
    print("22222")
    # send coin painment
    check_payment = checkout_make_payment()
    if check_payment is not True:
        return jsonify({'error': 'Error with Payment. Not enough Funds.'}), 200
    print("3333")
    checkout_clear_shopping_cart(current_user.id)
    db.session.commit()

    return jsonify({'success': 'Finalized payment'}), 200


def checkout_make_order():
    """
    creates the orders for the shopping cart
    """
    # Total cart
    now = datetime.utcnow()

    cart = db.session \
        .query(Checkout_CheckoutShoppingCart) \
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.saved_for_later == 0) \
        .all()
    get_customer_shipping = db.session \
        .query(UserData_DefaultAddress) \
        .filter(UserData_DefaultAddress.uuid == Checkout_CheckoutShoppingCart.customer_uuid) \
        .first()
    for k in cart:
        sellerfee = db.session \
            .query(Auth_UserFees) \
            .filter(Auth_UserFees.user_id == k.vendor_id) \
            .first()
        physicalitemfee = sellerfee.vendorfee
        if k.selected_digital_currency == 1:
            dbfeetopercent = (floating_decimals((physicalitemfee / 100), 8))
            fee_btc = (floating_decimals(
                (dbfeetopercent * k.final_price_btc), 8))
            fee_xmr = 0
            fee_bch = 0
            price_total_xmr = 0
            price_total_bch = 0
            price_total_btc = k.final_price_btc
            price_per_item_btc = Decimal(k.final_price_btc) / Decimal(k.quantity_of_item)
            price_per_item_xmr = 0
            price_per_item_bch = 0
            shipping_price_xmr = 0
            shipping_price_bch = 0
            shipping_price_btc = k.final_shipping_price_btc

        elif k.selected_digital_currency == 2:
            dbfeetopercent = (floating_decimals((physicalitemfee / 100), 8))
            fee_bch = (floating_decimals(
                (dbfeetopercent * k.final_price_bch), 8))
            fee_btc = 0
            fee_xmr = 0
            price_total_btc = 0
            price_total_xmr = 0
            price_total_bch = k.final_price_bch
            price_per_item_btc = 0
            price_per_item_xmr = 0
            price_per_item_bch = Decimal(k.final_price_bch) / Decimal(k.quantity_of_item)
            shipping_price_btc = 0
            shipping_price_xmr = 0
            shipping_price_bch = k.final_shipping_price_bch

        elif k.selected_digital_currency == 3:
            dbfeetopercent = (floating_decimals((physicalitemfee / 100), 12))
            fee_xmr = (floating_decimals(
                (dbfeetopercent * k.final_price_xmr), 12))
            fee_btc = 0
            fee_bch = 0
            price_total_btc = 0
            price_total_bch = 0
            price_total_xmr = k.final_price_xmr
            price_per_item_btc = 0
            price_per_item_bch = 0
            price_per_item_xmr = Decimal(
                k.final_price_xmr) / Decimal(k.quantity_of_item)
            shipping_price_btc = 0
            shipping_price_bch = 0
            shipping_price_xmr = k.final_shipping_price_xmr
        else:
            return False

        get_customer_country = db.session \
            .query(Query_Country) \
            .filter(Query_Country.value == get_customer_shipping.country) \
            .first()
        user_country = get_customer_country.name

        order = User_Orders(
            title_of_item=k.title_of_item,
            created=now,
            item_uuid=k.item_uuid,
            image_one=k.image_of_item,
            quantity=k.quantity_of_item,
            vendor_user_name=k.vendor_user_name,
            vendor_uuid=k.vendor_uuid,
            vendor_id=k.vendor_id,
            customer_user_name=k.customer_user_name,
            customer_uuid=k.customer_uuid,
            customer_id=k.customer_id,
            currency=k.currency,
            overall_status=0,
            disputed_timer=None,
            moderator_uuid=None,
            date_shipped=None,
            completed_time=None,
            extended_timer=0,
            released=0,
            private_note=None,
            escrow=0,
            request_cancel=0,
            reason_cancel=None,
            shipping_price_btc=shipping_price_btc,
            shipping_price_bch=shipping_price_bch,
            shipping_price_xmr=shipping_price_xmr,
            shipping_description=k.selected_shipping_description,
            vendor_feedback=0,
            user_feedback=0,
            digital_currency=k.selected_digital_currency,
            fee_btc=fee_btc,
            fee_bch=fee_bch,
            fee_xmr=fee_xmr,
            price_total_btc=price_total_btc,
            price_total_bch=price_total_bch,
            price_total_xmr=price_total_xmr,
            price_per_item_btc=price_per_item_btc,
            price_per_item_bch=price_per_item_bch,
            price_per_item_xmr=price_per_item_xmr,
            address_name=get_customer_shipping.address_name,
            address=get_customer_shipping.address,
            apt=get_customer_shipping.apt,
            city=get_customer_shipping.city,
            country=user_country,
            state_or_provence=get_customer_shipping.state_or_provence,
            zip_code=get_customer_shipping.zip_code,
            msg=get_customer_shipping.msg
        )
        new_notice_vendor = Vendor_Notification(
            dateadded=now,
            user_id=k.vendor_id,
            new_feedback=0,
            new_disputes=0,
            new_orders=1,
            new_returns=0,
        )

        db.session.add(new_notice_vendor)
        db.session.add(order)
        
    db.session.flush()

    return True


def checkout_make_payment():
    """
    Sends the Payments for the cryptocurrencies
    """

    cart_total = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer_id=current_user.id) \
        .first()

    # add security here before proceeding
    userwallet_bch = db.session \
        .query(Bch_Wallet) \
        .filter_by(user_id=current_user.id) \
        .first()
    userwallet_btc = db.session \
        .query(Btc_Wallet) \
        .filter_by(user_id=current_user.id) \
        .first()
    userwallet_xmr = db.session \
        .query(Xmr_Wallet) \
        .filter_by(user_id=current_user.id) \
        .first()

    # See if customer has the coin
    current_cart_total_bch = Decimal(cart_total.bch_total_price)
    if current_cart_total_bch > 0:
        if Decimal(userwallet_bch.currentbalance) <= current_cart_total_bch:
            print("123213*********")
            return False

    current_cart_total_btc = Decimal(cart_total.btc_total_price)
    if current_cart_total_btc > 0:
        if Decimal(userwallet_btc.currentbalance) <= current_cart_total_btc:
            print("4444*********")
            return False

    current_cart_total_xmr = Decimal(cart_total.xmr_total_price)
    if current_cart_total_xmr > 0:
        if Decimal(userwallet_xmr.currentbalance) <= current_cart_total_xmr:
            print("22*********")
            return False

    # get the orders
    orders = db.session \
        .query(User_Orders) \
        .filter(User_Orders.customer_uuid == current_user.uuid) \
        .filter(User_Orders.overall_status == 0) \
        .all()


    # loop through ORDERS. send coin and doing transactions 1 by 1.
    # this does not loop through the shopping cart
    # modifies orders
    for order in orders:

        get_item = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.uuid == order.item_uuid) \
            .first()

        # update the order to notify vendor
        order.incart = 0
        order.vendor_user_name = get_item.vendor_name
        order.vendor_id = get_item.vendor_id
        order.vendor_uuid = get_item.vendor_uuid
        order.overall_status = 1
        # add total sold to item
        # calculate how many items are left
        newsold = int(get_item.total_sold) + int(order.quantity)

        newquantleft = int(get_item.item_count) - int(order.quantity)

        get_item.total_sold = newsold
        get_item.item_count = newquantleft

        # add a message for each order
        addmsg = Service_ShippingSecret(
            user_id=current_user.id,
            txtmsg=order.private_note,
            timestamp=datetime.utcnow(),
            orderid=order.id
        )

        # BUYER stats
        get_stats_buyer = db.session\
            .query(Profile_StatisticsUser)\
            .filter(Profile_StatisticsUser.user_uuid == current_user.uuid)\
            .first()


        # VENDOR Stats
        get_stats_vendor = db.session\
            .query(Profile_StatisticsVendor)\
            .filter(Profile_StatisticsVendor.vendor_uuid == Item_MarketItem.vendor_uuid)\
            .first()

        # add total items bought
        buyer_current_bought = get_stats_buyer.total_items_bought 
        buyer_new_bought = buyer_current_bought + order.quantity
        get_stats_buyer.total_items_bought = buyer_new_bought
        
        # add total partners
        buyer_current_bought = get_stats_buyer.diff_partners
        buyer_new_bought = buyer_current_bought + 1
        get_stats_buyer.diff_partners = buyer_new_bought
        
        # BTC
        if order.digital_currency == 1:
            price_of_item_order = floating_decimals((order.price_total_btc + order.shipping_price_btc), 8)
            if current_cart_total_btc > 0:
                btc_send_coin_to_escrow(
                    amount=price_of_item_order,
                    user_id=order.customer_id,
                    order_uuid=order.uuid
                )
                # Buyer add current coin
                # Total Spent
                buyer_current_coin = get_stats_buyer.total_btc_spent
                buyer_new_coin = buyer_current_coin + price_of_item_order
                get_stats_buyer.total_btc_spent = buyer_new_coin
                
                # Vendor add current coin
                vendor_current_coin = get_stats_vendor.total_btc_recieved
                vendor_new_coin = vendor_current_coin + price_of_item_order
                get_stats_vendor.total_btc_recieved = vendor_new_coin
            
        # BCH
        if order.digital_currency == 2:
            price_of_item_order = floating_decimals((order.price_total_bch + order.shipping_price_bch), 8)
            if current_cart_total_bch > 0:
                bch_send_coin_to_escrow(
                    amount=price_of_item_order,
                    user_id=order.customer_id,
                    order_uuid=order.uuid
                )
                # add current coin
                buyer_current_coin = get_stats_buyer.total_bch_spent
                buyer_new_coin = buyer_current_coin + price_of_item_order
                get_stats_buyer.total_bch_spent = buyer_new_coin
                
                # Vendor add current coin
                vendor_current_coin = get_stats_vendor.total_bch_recieved
                vendor_new_coin = vendor_current_coin + price_of_item_order
                get_stats_vendor.total_btc_recieved = vendor_new_coin
        # XMR
        if order.digital_currency == 3:
            price_of_item_order = floating_decimals((order.price_total_xmr + order.shipping_price_xmr), 12)
            if current_cart_total_xmr > 0:
                xmr_send_coin_to_escrow(
                    amount=price_of_item_order,
                    user_id=order.customer_id,
                    order_uuid=order.uuid
                )
                # add current coin
                buyer_current_coin = get_stats_buyer.total_xmr_spent
                buyer_new_coin = buyer_current_coin + price_of_item_order
                get_stats_buyer.total_xmr_spent = buyer_new_coin
                
                # Vendor add current coin
                vendor_current_coin = get_stats_vendor.total_xmr_recieved
                vendor_new_coin = vendor_current_coin + price_of_item_order
                get_stats_vendor.total_xmr_recieved = vendor_new_coin


        # create a review for vendor
        add_new_feedback_for_customer = Feedback_Feedback(
            timestamp=datetime.utcnow(),
            title_of_item=order.title_of_item,
            order_uuid=order.uuid,
            item_uuid=order.item_uuid,
            customer_name=order.customer_user_name,
            customer_uuid=order.customer_uuid,
            vendor_name=order.vendor_user_name,
            vendor_uuid=order.vendor_uuid,
            vendor_comment=None,
            type_of_feedback=1,
            item_rating=None,
            vendor_rating=None,
            customer_rating=None,
            review_of_customer=None,
            review_of_vendor=None,
            author_uuid=current_user.uuid,
        )
        # create a review for customer
        add_new_feedback_for_vendor = Feedback_Feedback(
            timestamp=datetime.utcnow(),
            order_uuid=order.uuid,
            item_uuid=order.item_uuid,
            customer_name=order.customer_user_name,
            customer_uuid=order.customer_uuid,
            vendor_name=order.vendor_user_name,
            vendor_uuid=order.vendor_uuid,
            vendor_comment=None,
            type_of_feedback=1,
            item_rating=None,
            vendor_rating=None,
            customer_rating=None,
            author_uuid=order.vendor_uuid,
            )
        

        db.session.add(get_stats_vendor)
        db.session.add(get_stats_buyer)
        db.session.add(add_new_feedback_for_vendor)
        db.session.add(add_new_feedback_for_customer)
        db.session.add(order)
        db.session.add(get_item)
        db.session.add(addmsg)
    db.session.flush()
    return True
