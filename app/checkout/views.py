from flask import jsonify, request
from flask_login import current_user, login_required
from app.checkout import checkout
from app import db
from app.notification import notification
from datetime import datetime, timedelta
from decimal import Decimal
import calendar
# models
from app.classes.checkout import\
    Checkout_CheckoutShoppingCart,\
    Checkout_ShoppingCartTotal,\
    Checkout_CheckoutShoppingCart_Schema, \
    Checkout_ShoppingCartTotal_Schema
from app.classes.auth import\
    Auth_User,\
    Auth_UserFees
from app.classes.item import \
    Item_MarketItem, \
    Checkout_CheckoutShoppingCart, \
    Checkout_ShoppingCartTotal
from app.classes.service import \
    Service_ShippingSecret
from app.classes.vendor import \
    User_Orders
from app.classes.wallet_btc import Btc_Wallet, Btc_Prices
from app.classes.wallet_bch import Bch_Wallet, Bch_Prices
from app.classes.wallet_xmr import Xmr_Wallet, Xmr_Prices
# endmodels

from app.wallet_bch.wallet_bch_work import bch_send_coin_to_escrow
from app.wallet_btc.wallet_btc_work import btc_send_coin_to_escrow
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin_to_escrow
from app.common.functions import floating_decimals, convert_local_to_bch, convert_local_to_btc, convert_local_to_xmr
from app.userdata.views import \
    userdata_different_trading_partners_user, \
    userdata_different_trading_partners_vendor



# Shopping cart page
def cart_calculate_item_shipping_and_price_cart(cartitemid):

    """
    # calculates shopping cart table
    Function takes cart if of item in shopping cart
    THen it determines the currency being used
    Converts the local price to cryptocurrency prices
    determines quantity and calculates price
    """
    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id == cartitemid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=cartitemid) \
        .first()

    # BITCOIN
    if cartitem.selected_currency == 1:

        ## SHIPPING
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

        ## PRICING
        btc_itemprice = Decimal(getitem.price_of_item)
        btc_price_per_item = Decimal(convert_local_to_btc(amount=btc_itemprice, currency=getitem.currency))
        btc_price_formatted = (floating_decimals(btc_price_per_item, 8))
        btc_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(btc_price_formatted)
        btc_price_final = (floating_decimals(btc_pricing_multiply, 8))
        cartitem.final_price_btc = btc_price_final

    # BITCOIN CASH
    if cartitem.selected_currency == 2:

        ## SHIPPING
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
        bch_shippingtotal = Decimal(cartitem.quantity_of_item) *  Decimal(bch_shipprice_formatted)
        # return shipping price
        bch_ship_price_final = (floating_decimals(bch_shippingtotal, 8))
        # set variable in database
        cartitem.final_shipping_price_bch = bch_ship_price_final
        
        ## PRICING
        bch_itemprice = Decimal(getitem.price_of_item)
        bch_price_per_item = Decimal(convert_local_to_bch(amount=bch_itemprice, currency=getitem.currency))
        bch_price_formatted = (floating_decimals(bch_price_per_item, 8))
        bch_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(bch_price_formatted)
        bch_price_final = (floating_decimals(bch_pricing_multiply, 8))
        cartitem.final_price_bch = bch_price_final

    # Monero
    if cartitem.selected_currency == 3:
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

        ## PRICING
        xmr_itemprice = Decimal(getitem.price_of_item)
        xmr_price_per_item = Decimal(convert_local_to_xmr(amount=xmr_itemprice, currency=getitem.currency))
        xmr_price_formatted = (floating_decimals(xmr_price_per_item, 12))
        xmr_pricing_multiply = Decimal(cartitem.quantity_of_item) * Decimal(xmr_price_formatted)
        xmr_price_final = (floating_decimals(xmr_pricing_multiply, 12))
        cartitem.final_price_xmr = xmr_price_final


def cart_calculate_total_price(user_id):

    """
    # Calculates cart total table
    First it gets the total cart, all cart items, and wallets of each user
    Then Loop through each cart item appending it to the list
        - appends total price of item
        - appends 

    """
    total_cart = Checkout_ShoppingCartTotal.query\
        .filter(Checkout_ShoppingCartTotal.customer_id == user_id)\
        .first()
    shopping_cart = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()

    # Bitcoin
    btc_pricelist = []
    btc_shipping_pricelist = []

    # Bitcoin cash
    bch_pricelist = []
    bch_shipping_pricelist = []

    # Monero
    xmr_pricelist = []
    xmr_shipping_pricelist = []

    for cart in shopping_cart:
        if cart.selected_currency == 1:

            btc_pricelist.append(cart.final_price_btc)
            btc_shipping_pricelist.append(cart.final_shipping_price_btc)
            
            ##TODO
        elif cart.selected_currency == 2:
        
            bch_pricelist.append(cart.final_price_bch)
            bch_shipping_pricelist.append(cart.final_shipping_price_bch)
        else:
            xmr_pricelist.append(cart.final_price_xmr)
            xmr_shipping_pricelist.append(cart.final_shipping_price_xmr)

    # get sum of prices in list
    btc_sum_of_item = len(btc_pricelist)
    total_cart.btc_sum_of_item = btc_sum_of_item
    # get sum of prices in list
    btc_formatted_total_price = ("{0:.8f}".format(sum(btc_pricelist)))
    # get sum of shipping prices
    btc_formatted_total_shipping_price=( "{0:.8f}".format(sum(btc_shipping_pricelist)))
    total_cart.price = btc_formatted_total_price 
    total_cart.btc_shipping_price = btc_formatted_total_shipping_price
    # get total price
    btc_add_total = Decimal(btc_formatted_total_price) + Decimal(btc_formatted_total_shipping_price)
    total_cart.btc_total_price = btc_add_total

    # get sum of prices in list
    bch_sum_of_item = len(bch_pricelist)
    total_cart.bch_sum_of_item = bch_sum_of_item
    bch_formatted_total_price = ("{0:.8f}".format(sum(bch_pricelist)))
    # get sum of shipping prices
    bch_formatted_total_shipping_price = ("{0:.8f}".format(sum(bch_shipping_pricelist)))
    total_cart.price = bch_formatted_total_price 
    total_cart.bch_shipping_price = bch_formatted_total_shipping_price
    # get total price
    bch_add_total = Decimal(bch_formatted_total_price) + Decimal(bch_formatted_total_shipping_price)
    total_cart.bch_total_price = bch_add_total

    # get sum of prices in list
    xmr_sum_of_item = len(xmr_pricelist)
    total_cart.xmr_sum_of_item = xmr_sum_of_item
    # get sum of prices in list
    xmr_formatted_total_price = ("{0:.12f}".format(sum(xmr_pricelist)))
    # get sum of shipping prices
    xmr_formatted_total_shipping_price = ("{0:.12f}".format(sum(xmr_shipping_pricelist)))
    total_cart.price = xmr_formatted_total_price 
    total_cart.xmr_shipping_price = xmr_formatted_total_shipping_price
    # get total price
    xmr_add_total = Decimal(xmr_formatted_total_price) + Decimal(xmr_formatted_total_shipping_price)
    total_cart.xmr_total_price = xmr_add_total

    db.session.add(total_cart)

@checkout.route('/changepaymentoption/<int:cartid>', methods=['POST'])
@login_required
def cart_update_shipping_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
    Triggers function to update shipping 
    """

    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id == cartid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=cartitem.item_id) \
        .first()

    new_shipping = request.json["new_shipping_option"]
    new_shipping = int(new_shipping)
    if new_shipping == 1:
        if getitem.shipping_free is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_0
    if new_shipping == 2:
        if getitem.shipping_two is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_2
    if new_shipping == 3:
        if getitem.shipping_three is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_3
           
    db.session.flush()
    cart_calculate_item_shipping_and_price_cart(cartitem.id)
    cart_calculate_total_price(cartitem.customer_id)
    return jsonify({'status': 'success'})

@checkout.route('/movecartitem/<string:itemid>', methods=['POST'])
@login_required
def cart_move_cart_item(itemid):
    """
    Moves the item from cart to saved for later
    """
    the_cart_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid)\
        .first()
    if the_cart_item:
        if the_cart_item.customer_id == current_user.id:
            the_cart_item.savedforlater = 1
            db.session.add(the_cart_item)
            db.session.commit()
            cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
            cart_calculate_total_price(the_cart_item.customer_id)
        else:
           return jsonify({'status': 'Error.  No Items in your cart'})
    else:
        return jsonify({'status': 'Error. Item doesnt exist.'})

@checkout.route('/saveforlater/<int:cartid>', methods=['POST'])
@login_required
def cart_save_for_later(cartid):
    """
    Delete the message sent to the user
    """

    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id==cartid)\
        .first()
    if cartitem.customer_id != current_user.id:
        return jsonify({'status': 'success'})
    cartitem.savedforlater = 1
    db.session.add(cartitem)
    db.session.commit()
    return jsonify({'status': 'success'})

@checkout.route('/changepaymentoption/<int:cartid>', methods=['POST'])
@login_required
def cart_update_payment_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """

    the_cart_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id==cartid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=the_cart_item.item_id) \
        .first()
    new_currency = request.json["new_currency"]
    new_currency = int(new_currency)
    if new_currency == 1:
        if getitem.digital_currency_1 is False:
            return jsonify({'status': 'error'})
        else:
            the_cart_item.selected_currency = new_currency
            return jsonify({'status': 'success'})
    if new_currency == 2:
        if getitem.digital_currency_2 is False:
            return jsonify({'status': 'error'})
        else:
            the_cart_item.selected_currency = new_currency
            return jsonify({'status': 'success'})
    if new_currency == 3:
        if getitem.digital_currency_3 is False:
            return jsonify({'status': 'error'})
        else:
            the_cart_item.selected_currency = new_currency
            return jsonify({'status': 'success'})
    cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
    cart_calculate_total_price(the_cart_item.customer_id)
    db.session.add(the_cart_item)
    db.session.commit()
    return jsonify({'status': 'error'})

@checkout.route('/updateamount/<int:cartid>', methods=['POST'])
@login_required
def cart_update_quantity(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """

    the_cart_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id==cartid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=the_cart_item.item_id) \
        .first()
    new_amount = request.json["new_amount"]
    if new_amount > getitem.item_count:
         return jsonify({'status': 'error'})
    if the_cart_item.customer_id != current_user.id:
        return jsonify({'status': 'error'})

    the_cart_item.quantity_of_item = new_amount
    cart_calculate_item_shipping_and_price_cart(the_cart_item.id)
    cart_calculate_total_price(the_cart_item.customer_id)
    db.session.add(the_cart_item)
    db.session.commit()
    return jsonify({'status': 'success'})

@checkout.route('/payment/<string:itemid>', methods=['POST'])
@login_required
def cart_checkout_order(userid):
    """
    Sends the Payments for the cryptocurrencies
    """
    # Total cart
    cart = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()

    for k in cart:
        sellerfee = Auth_UserFees.query\
            .filter(Auth_UserFees.user_id == k.vendor_id)\
            .first()
        physicalitemfee = sellerfee.vendorfee
        if k.selected_currency == 1:
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 8))
            fee_btc = (floating_decimals((dbfeetopercent * k.final_price_btc), 8))
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

        if k.selected_currency == 2:
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 8))
            fee_bch = (floating_decimals((dbfeetopercent * k.final_price_bch), 8))
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
            shipping_price_bch = k.finalfinal_shipping_price_bch
            
        if k.selected_currency == 3:
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 12))
            fee_xmr = (floating_decimals((dbfeetopercent * k.final_price_xmr), 12))
            fee_btc = 0
            fee_bch = 0
            price_total_btc = 0
            price_total_bch = 0
            price_total_xmr = k.final_price_xmr
            price_per_item_btc = 0
            price_per_item_bch = 0
            price_per_item_xmr = Decimal(k.final_price_xmr) / Decimal(k.quantity_of_item)
            shipping_price_btc = 0
            shipping_price_bch = 0
            shipping_price_xmr = k.final_shipping_price_xmr
            
        order = User_Orders(
            title_of_item=k.title_of_item,
            item_uuid=k.item_uuid,
            image_one=k.image_of_item,
            quantity=k.quantity_of_item,
            vendor_user_name=k.vendor,
            vendor_uuid=k.vendor_uuid,
            vendor_id=k.vendor_id,
            customer_user_name=k.customer,
            customer_uuid=k.customer_uuid,
            customer_id=k.customer_id,
            currency=k.currency,
            incart=1,
            new_order=0,
            accepted_order=0,
            waiting_order=0,
            disputed_order=0,
            disputed_timer=0,
            moderator_uuid=None,
            delivered_order=0,
            date_shipped=None,
            completed=0,
            completed_time=None,
            released=0,
            private_note=None,
            escrow=0,
            request_cancel=0,
            reason_cancel=None,
            cancelled=0,
            shipping_price_btc=shipping_price_btc,
            shipping_price_bch=shipping_price_bch,
            shipping_price_xmr=shipping_price_xmr,
            shipping_description=None,
            vendor_feedback=None,
            user_feedback=None,
            digital_currency=k.digital_currency,
            fee_btc=fee_btc,
            fee_bch=fee_bch,
            fee_xmr=fee_xmr,
            price_total_btc=price_total_btc,
            price_total_bch=price_total_bch,
            price_total_xmr=price_total_xmr,
            price_per_item_btc=price_per_item_btc,
            price_per_item_bch=price_per_item_bch,
            price_per_item_xmr=price_per_item_xmr,
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'status': 'success'})




# Checkout page
@checkout.route('/payment/<string:itemid>', methods=['POST'])
@login_required
def checkout_make_payment(userid):
    """
    Sends the Payments for the cryptocurrencies
    """
    user = Auth_User
    cart_total = db.session\
        .query(Checkout_ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # turn back if issue
    if cart_total.btc_sum_of_item == 0 and cart_total.bch_sum_of_item == 0 and cart_total.xmr_sum_of_tems:
        return jsonify({'status': 'Error.  No Money in your wallet'})
    if datetime.utcnow() >= user.shopping_timer:
        return jsonify({'status': 'Error.  Time Ran out to make the purchase'})

    # add security here before proceeding
    userwallet_bch = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user.id)\
        .first()
    userwallet_btc = db.session\
        .query(Btc_Wallet)\
        .filter_by(user_id=user.id)\
        .first()
    userwallet_xmr = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=user.id)\
        .first()
    # See if customer has the coin
    current_cart_total_bch = Decimal(cart_total.bch_total_price)
    if current_cart_total_bch > 0:
        if Decimal(userwallet_bch.currentbalance) <= current_cart_total_bch:
           return jsonify({'status': 'Error.  Not Enough BCH in your wallet'})

    current_cart_total_btc = Decimal(cart_total.btc_total_price)
    if current_cart_total_btc > 0:
        if Decimal(userwallet_btc.currentbalance) <= current_cart_total_btc:
           return jsonify({'status': 'Error.  Not Enough BTC in your wallet'})

    current_cart_total_xmr = Decimal(cart_total.xmr_total_price)
    if current_cart_total_xmr > 0:
        if Decimal(userwallet_xmr.currentbalance) <= current_cart_total_xmr:
           return jsonify({'status': 'Error.  Not Enough XMR in your wallet'})

    # get the orders
    orders = db.session\
        .query(User_Orders)\
        .filter(User_Orders.customer_uuid == user.uuid)\
        .filter(User_Orders.incart == 1)\
        .group_by(User_Orders.id.asc())\
        .all()

    # loop through ORDERS. send ccoin and doing transactions 1 by 1.. this does not loop through the shopping cart
    # creates orders
    for order in orders:
        get_item = Item_MarketItem.query\
            .filter(Item_MarketItem.uuid == order.item_uuid) \
            .first()

        # update the order to notify vendor
        order.incart = 0
        order.vendor_user_name = get_item.vendor_name
        order.vendor_id = get_item.vendor_id
        order.vendor_uuid = get_item.vendor_uuid

        # add total sold to item
        newsold = int(get_item.total_sold) + int(order.quantity)
        newquantleft = int(get_item.item_count) - int(order.quantity)
        get_item.total_sold = newsold
        get_item.item_count = newquantleft

        # add diff trading partners
        userdata_different_trading_partners_user(user_id=order.customer_id,
                                                 otherid=order.vendor_id)

        # add diff trading partners
        userdata_different_trading_partners_vendor(user_id=order.vendor_id,
                                                   otherid=order.customer_id)

        # add a message for each order
        addmsg = Service_ShippingSecret(
            user_id=current_user.id,
            txtmsg=order.private_note,
            timestamp=datetime.utcnow(),
            orderid=order.id
        )
        # notify vendor
        notification(type=1,
                     username=order.vendor_user_name,
                     user_id=order.vendor_id,
                     salenumber=order.id,
                     bitcoin=0)

        notification(type=112,
                     username=order.customer_user_name,
                     user_id=order.customer_id,
                     salenumber=order.id,
                     bitcoin=0)

        if order.digital_currency == 1:
            price_of_item_order = floating_decimals(
                (order.price_total_btc + order.shipping_price), 8)
            if current_cart_total_btc > 0:
                btc_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )
        if order.digital_currency == 2:
            price_of_item_order = floating_decimals(
                (order.price_total_bch + order.shipping_price), 8)
            if current_cart_total_bch > 0:
                bch_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )

        if order.digital_currency == 3:
            price_of_item_order = floating_decimals(
                (order.price_total_xmr + order.shipping_price_xmr), 12)
            if current_cart_total_xmr > 0:
                xmr_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )
        # check if item is now offline
        checkoutput_item_offline()(get_item.uuid)

        # commit to database
        db.session.add(order)
        db.session.add(get_item)
        db.session.add(addmsg)
        db.session.commit()
        return jsonify({'status': 'success'})

@checkout.route('/info/delete/<string:itemid>', methods=['POST'])
@login_required
def checkout_delete_secret_info(itemid):
    """
    Delete the message sent to the user
    """
    user = Auth_User.query\
        .filter_by(username=current_user.username)\
        .first()
    get_cart = Checkout_ShoppingCartTotal.query\
        .filter_by(customer=user.id)\
        .first()
    the_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid)\
        .first()
    if the_item:
        if get_cart.btc_price == 0 and get_cart.bch_price == 0:
            return jsonify({'status': 'Error. No Items in your shopping cart.'})
        else:
            # get the message
            msg = Service_ShippingSecret.query\
                .filter_by(user_id=user.id, orderid=0)\
                .first()
            db.session.delete(msg)
            db.session.commit()
            return jsonify({'status': 'success'})

@checkout.route('/info/add/<string:itemid>', methods=['POST'])
@login_required
def checkout_add_secret_info(itemid):
    """
    Delete the message sent to the user
    """
    the_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid)\
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
    
        return jsonify({'status': 'success'})

def checkout_clear_shopping_cart(userid):
    """
    Puts totals of cart to zero
    Then deletes all items in the regular cat
    """
    # clear user shoppingcarttotal
    user = Auth_User.query\
        .filter_by(username=current_user.username)\
        .first()
    get_total_cart_for_user = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer=user.id) \
        .first()

    get_shopping_cart = Checkout_CheckoutShoppingCart.query\
        .filter(get_shopping_cart.custer_id == userid)\
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
    user = Auth_User.query.filter(Auth_User.id==userid).first()
    oldmsg = db.session\
        .query(Service_ShippingSecret)\
        .filter_by(user_id=user.id, orderid=0)\
        .first()
    db.session.delete(oldmsg)
    db.session.flush()

def checkoutput_item_offline(itemid):
    """
    If user bought last or only item..take vendors item offline
    """
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=itemid) \
        .first()
        # turn off if item is less than one
    if getitem.item_count < 1:

        getitem.online = 0
        db.session.add(getitem)

        # send notification to vendor saying its all sold out
        notification(type=9,
                        username=getitem.vendor_name,
                        user_id=getitem.vendor_id,
                        salenumber=getitem.uuid,
                        bitcoin=0)


@checkout.route('/data/incart', methods=['POST'])
@login_required
def data_shopping_cart_in_cart():
    """
    Returns items in the shopping cart
    """
    if request.method == 'GET':
        cart = db.session\
            .query(Checkout_CheckoutShoppingCart)\
            .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                    Checkout_CheckoutShoppingCart.savedforlater == 0)\
            .first() is not None

        if cart:
            cart_items = db.session\
                .query(Checkout_CheckoutShoppingCart)\
                .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                        Checkout_CheckoutShoppingCart.savedforlater == 0)\
                .all()
            item_schema = Checkout_CheckoutShoppingCart_Schema()
            result = item_schema.dump(cart_items)
            return jsonify(result), 200
        else:
            jsonify({"Error": "No items in your cart exist"}), 404


@checkout.route('/data/saved', methods=['POST'])
@login_required
def data_shopping_cart_in_saved():
    """
    Returns items in the shopping cart
    """
    if request.method == 'GET':
        cart = db.session\
            .query(Checkout_CheckoutShoppingCart)\
            .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                    Checkout_CheckoutShoppingCart.savedforlater == 1)\
            .first() is not None

        if cart:
            cart_items = db.session\
                .query(Checkout_CheckoutShoppingCart)\
                .filter(Checkout_CheckoutShoppingCart.customer_uuid == current_user.uuid,
                        Checkout_CheckoutShoppingCart.savedforlater == 1)\
                .all()
            item_schema = Checkout_CheckoutShoppingCart_Schema()
            result = item_schema.dump(cart_items)
            return jsonify(result), 200
        else:
            jsonify({"Error": "No items in your cart exist"}), 404
