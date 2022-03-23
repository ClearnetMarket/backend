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
    Checkout_ShoppingCartTotal
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
from app.common.functions import \
    floating_decimals, \
    convert_local_to_bch
from app.userdata.views import \
    userdata_different_trading_partners_user, \
    userdata_different_trading_partners_vendor


@checkout.route('/payment/<string:itemid>', methods=['POST'])
@login_required
def create_checkout_order(userid):
    """
    Sends the Payments for the cryptocurrencies
    """


    # Total cart

    cart = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer_uui == current_user.uuid,
                Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()

    for k in cart:
        sellerfee = db.session.query(Auth_UserFees).filter(
            Auth_UserFees.user_id == k.vendor_id).first()
        physicalitemfee = sellerfee.vendorfee
        if k.selected_currency == 1:
            price_per_item_btc = Decimal(k.final_price_btc) / Decimal(k.quantity_of_item)
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 8))
            fee_btc = (floating_decimals((dbfeetopercent * k.final_price_btc), 8))
            fee_xmr = 0
            fee_bch = 0
            price_total_xmr = 0
            price_total_bch = 0
            price_per_item_xmr = 0
            price_per_item_bch = 0
            shipping_price_xmr = 0
            shipping_price_bch = 0
            
        if k.selected_currency == 2:
            price_per_item_bch = Decimal(k.final_price_bch) / Decimal(k.quantity_of_item)
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 8))
            fee_bch = (floating_decimals((dbfeetopercent * k.final_price_bch), 8))
            fee_btc = 0
            fee_xmr = 0
            price_total_btc = 0
            price_total_xmr = 0
            price_per_item_btc = 0
            price_per_item_xmr = 0
            shipping_price_btc = 0
            shipping_price_xmr = 0

        if k.selected_currency == 3:
            price_per_item_xmr = Decimal(k.final_price_xmr) / Decimal(k.quantity_of_item)
            dbfeetopercent = (floating_decimals((physicalitemfee/100), 12))
            fee_xmr = (floating_decimals((dbfeetopercent * k.final_price_xmr), 12))
            fee_btc = 0
            fee_bch = 0
            price_total_btc = 0
            price_total_bch = 0
            price_per_item_btc = 0
            price_per_item_bch = 0
            shipping_price_btc = 0
            shipping_price_bch = 0
         
        order = User_Orders(
            title_of_item = k.title_of_item,
            item_uuid = k.item_uuid,
            image_one = k.image_of_item,
            quantity = k.quantity_of_item,
            vendor_user_name = k.vendor,
            vendor_uuid = k.vendor_uuid,
            vendor_id = k.vendor_id,
            customer_user_name = k.customer,
            customer_uuid = k.customer_uuid,
            customer_id = k.customer_id,
            currency = k.currency,
            incart = 1,
            new_order = 0,
            accepted_order = 0,
            waiting_order = 0,
            disputed_order = 0,
            disputed_timer = 0,
            moderator_uuid = None,
            delivered_order = 0,
            date_shipped = None,
            completed = 0,
            completed_time = None,
            released = 0,
            private_note = None,
            escrow = 0,
            request_cancel =0, 
            reason_cancel = None,
            cancelled = 0,
            shipping_price_btc = shipping_price_btc,
            shipping_price_bch = shipping_price_bch,
            shipping_price_xmr = shipping_price_xmr,
            shipping_description = None,
            vendor_feedback = None,
            user_feedback =  None,
            digital_currency = k.digital_currency,
            fee_btc = fee_btc,
            fee_bch = fee_bch,
            fee_xmr = fee_xmr,
            price_total_btc = price_total_btc,
            price_total_bch = price_total_bch,
            price_total_xmr = price_total_xmr,
            price_per_item_btc = price_per_item_btc,
            price_per_item_bch = price_per_item_bch,
            price_per_item_xmr = price_per_item_xmr,
                )
        db.session.add(order)
        db.session.commit()
        return jsonify({'status': 'success'})

@checkout.route('/payment/<string:itemid>', methods=['POST'])
@login_required
def checkout_make_payment(userid):
    """
    Sends the Payments for the cryptocurrencies
    """

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
            .filter(Item_MarketItem.uuid==order.item_uuid) \
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
            txtmsg=msg.txtmsg,
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
            price_of_item_order = floating_decimals((order.price_total_btc + order.shipping_price), 8)
            if current_cart_total_btc > 0:
                btc_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )
        if order.digital_currency == 2:
            price_of_item_order = floating_decimals((order.price_total_bch + order.shipping_price), 8)
            if current_cart_total_bch > 0:
                bch_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )

        if order.digital_currency == 3:
            price_of_item_order = floating_decimals((order.price_total_xmr + order.shipping_price_xmr), 12)
            if current_cart_total_xmr > 0:
                xmr_send_coin_to_escrow(
                    amount=price_of_item_order,
                    comment=order.id,
                    user_id=order.customer_id
                )
        # check if item is now offline
        put_item_offline(get_item.uuid)
        # commit to database
        db.session.add(order)
        db.session.add(get_item)
        db.session.add(addmsg)
        db.session.commit()
        return jsonify({'status': 'success'})


@checkout.route('/saveforlater/<int:cartid>', methods=['POST'])
@login_required
def checkout_save_for_later(cartid):
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
def checkout_update_payment_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """

    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id==cartid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=cartitem.item_id) \
        .first()
    new_currency = request.json["new_currency"]
    new_currency = int(new_currency)
    if new_currency == 1:
        if getitem.digital_currency_1 is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_currency = new_currency
            return jsonify({'status': 'success'})
    if new_currency == 2:
        if getitem.digital_currency_2 is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_currency = new_currency
            return jsonify({'status': 'success'})
    if new_currency == 3:
        if getitem.digital_currency_3 is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_currency = new_currency
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


@checkout.route('/changepaymentoption/<int:cartid>', methods=['POST'])
@login_required
def checkout_update_shipping_option(cartid):
    """
    Updates the quanity of the item in the shopping cart
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

            cartitem.final_shipping_price_btc = 0

            return jsonify({'status': 'success'})
    if new_shipping == 2:
        if getitem.shipping_two is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_2

            cartitem.final_shipping_price_bch = 0
            return jsonify({'status': 'success'})
    if new_shipping == 3:
        if getitem.shipping_three is False:
            return jsonify({'status': 'error'})
        else:
            cartitem.selected_shipping = new_shipping
            cartitem.selected_shipping_description = getitem.shipping_info_3
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


def update_total_price(cartitemid):
    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id == cartitemid)\
        .first()
        ## TODO  Add shipping and total cost of each item
        ## TODO ADD total costs for eholw item??? Another function
        ## one function for each item?


@checkout.route('/updateamount/<int:cartid>', methods=['POST'])
@login_required
def checkout_update_quantity(cartid):
    """
    Updates the quanity of the item in the shopping cart
    """

    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id==cartid)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem) \
        .filter_by(id=cartitem.item_id) \
        .first()
    new_amount = request.json["new_amount"]
    if new_amount > getitem.item_count:
         return jsonify({'status': 'error'})
    if cartitem.customer_id != current_user.id:
        return jsonify({'status': 'error'})

    cartitem.quantity_of_item = new_amount
    db.session.add(cartitem)
    db.session.commit()
    return jsonify({'status': 'success'})


@checkout.route('/saveforlater/<int:cartid>', methods=['POST'])
@login_required
def checkout_save_for_later(cartid):
    """
    Delete the message sent to the user
    """

    cartitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.id == cartid)\
        .first()
    if cartitem.customer_id != current_user.id:
        return jsonify({'status': 'success'})

    db.session.delete(cartitem)
    db.session.commit()
    return jsonify({'status': 'success'})


def put_item_offline(itemid):
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


@checkout.route('/info/delete/<string:itemid>', methods=['POST'])
@login_required
def checkout_delete_secret_info(itemid):
    """
    Delete the message sent to the user
    """
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
    get_cart = db.session\
        .query(Checkout_ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()
    the_item = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid)\
        .first()
    if the_item:
        if get_cart.btcprice == 0 and get_cart.btc_cash_price == 0:
            return jsonify({'status': 'Error. No Items in your shopping cart.'})
        else:
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
    gettotalcart = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer=user.id) \
        .first()
    gettotalcart.btc_sum_of_item = 0
    gettotalcart.btc_price = 0
    gettotalcart.btc_shipping_price = 0
    gettotalcart.btc_total_price = 0

    gettotalcart.bch_sum_of_item = 0
    gettotalcart.bch_price = 0
    gettotalcart.bch_shipping_price = 0
    gettotalcart.bch_total_price = 0

    gettotalcart.xmr_sum_of_item = 0
    gettotalcart.xmr_price = 0
    gettotalcart.xmr_shipping_price = 0
    gettotalcart.xmr_total_price = 0
    db.session.add(gettotalcart)

    # delete items in cart
    for f in cart:
        db.session.delete(f)
    db.session.flush()

def checkout_delete_private_msg(userid):
    """
    Deletes the private message
    """
    oldmsg = db.session\
        .query(Service_ShippingSecret)\
        .filter_by(user_id=user.id, orderid=0)\
        .first()
    db.session.delete(oldmsg)
    db.session.flush()


@checkout.route('/movecartitem/<string:itemid>', methods=['POST'])
@login_required
def checkout_move_cart_item(itemid):
    """
    Moves the item from cart to saved for later
    """
    theitem = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.uuid == itemid)\
        .first()
    if theitem:
        if theitem.customer_id == current_user.id:
            getcart = Checkout_CheckoutShoppingCart.query\
                .filter(current_user.id == Checkout_CheckoutShoppingCart.customer_id)\
                .filter(Checkout_CheckoutShoppingCart.savedforlater == 0)
            cartamount = getcart.count()
            if int(cartamount) > 5:
                theitem.savedforlater = 1
                db.session.add(theitem)
                db.session.commit()
            else:
                theitem.savedforlater = 0
                db.session.add(theitem)
                db.session.commit()
        else:
           return jsonify({'status': 'Error.  No Items in your cart'})
    else:
        return jsonify({'status': 'Error. Item doesnt exist.'})

@checkout.route('/cart', methods=['POST'])
@login_required
def shopping_cart():
    now = datetime.utcnow()
    # Total cart
    user = Auth_User.query\
        .filter_by(username=current_user.username)\
        .first()
    cart = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.customer == current_user.username,
                Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()
    gettotalcart = Checkout_ShoppingCartTotal.query\
        .filter_by(customer=user.id)\
        .first()

    # see if orders previous..delete them
    user_orders = db.session\
        .query(User_Orders)\
        .filter(User_Orders.customer_id == user.id)\
        .filter(User_Orders.type == 1)\
        .filter(User_Orders.incart == 1)\
        .all()

    # see if msg
    msg = Service_ShippingSecret.query\
        .filter_by(user_id=user.id, orderid=0)\
        .first()
    if msg:
        db.session.delete(msg)

    for i in user_orders:
        db.session.delete(i)
    # Saved for later cart

    cartsaved = Checkout_CheckoutShoppingCart.query\
        .filter(Checkout_CheckoutShoppingCart.customer == user.username, Checkout_CheckoutShoppingCart.savedforlater == 1)\
        .all()

    # timer
    fiftenminutes = timedelta(minutes=15)
    fromnow = datetime.utcnow() + fiftenminutes

    # Bitcoin
    btc_pricelist = []
    btc_shipping_pricelist = []
    btc_wallet = Btc_Wallet.query\
        .filter_by(user_id=user.id)\
        .first()
    # Bitcoin cash
    bch_pricelist = []
    bch_shipping_pricelist = []
    bch_wallet = Bch_Wallet.query\
        .filter_by(user_id=user.id)\
        .first()
    # Monero
    xmr_pricelist = []
    xmr_shipping_pricelist = []
    xmr_wallet = Xmr_Wallet.query\
        .filter_by(user_id=user.id)\
        .first()
    # First query item get latest price/info/etc
    for cart_item in cart:
        # see if still exists
        try:
            getitem = db.session\
                .query(Item_MarketItem)\
                .filter(Item_MarketItem.id == cart_item.item_id)\
                .first()
        except Exception:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'status': 'Error. Item doesnt exist.'})
       
        # price
        try:
            cart_item.price_of_item = getitem.price
        except Exception:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'status': 'Error. Item is not available. It has been removed from your cart.'})

        # supply
        try:
            cart_item.vendorsupply = getitem.item_count
            if cart_item.vendorsupply <= 0:
                flash(i.title_of_item + " has been sold out.  It has been removed from your cart",
                      category="success")
                db.session.delete(cart_item)
                db.session.commit()
                return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
        except Exception:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(cart_item)
            db.session.commit()
            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))

        # shipping
        try:
            if cart_item.shipping_free == 0 and cart_item.shipping_two == 0 and cart_item.shipping_three == 0:
                flash("Item#" + str(i.id) +
                      ": Doesnt have a shipping method", category="danger")
                db.session.delete(cart_item)
                db.session.commit()
                return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
        except Exception:
            return redirect(url_for('index', username=current_user.username))

        # shipping1
     
        cart_item.shipping_info_0 = getitem.shipping_info_0,
        cart_item.shipping_day_least_0 = getitem.shipping_day_least_0,
        cart_item.shipping_day_most_0 = getitem.shipping_day_most_0,

        # shipping2
        cart_item.shipping_info_2 = getitem.shipping_info_2,
        cart_item.shipping_price_2 = getitem.shipping_price_2,
        cart_item.shipping_day_least_2 = getitem.shipping_day_least_2,
        cart_item.shipping_day_most_2 = getitem.shipping_day_most_2,

        # shipping 3
        cart_item.shipping_info_3 = getitem.shipping_info_3,
        cart_item.shipping_price_3 = getitem.shipping_price_3,
        cart_item.shipping_day_least_3 = getitem.shipping_day_least_3,
        cart_item.shipping_day_most_3 = getitem.shipping_day_most_3,

        db.session.add(cart_item)
        db.session.flush()

        # if bitcoin cash
        # selected currency 3 = btc cash

        # get price
        getcurrentprice = db.session\
            .query(Bch_Prices)\
            .filter(Bch_Prices.currency_id == cart_item.currency)\
            .first()

        btc_cash_bt = getcurrentprice.price
        btc_cash_z = Decimal(cart_item.price_of_item) / Decimal(btc_cash_bt)

        # combined price
        itemamount = (Decimal(cart_item.quantity_of_item))
        itemandquant = (floating_decimals(itemamount * btc_cash_z, 8))
        cart_item.final_price = itemandquant

        # Get shipping
        if cart_item.selected_shipping == 1:
            btc_cash_shipprice2 = 0
            cart_item.final_shipping_price = 0
            cart_item.selected_shipping_description = str(getitem.shipping_info_0) \
                + ': ' + '(' + str(getitem.shipping_day_least_0) \
                + ' days to ' + str(getitem.shipping_day_most_0) \
                + ' days)'

        elif cart_item.selected_shipping == 2:
            # PRICE
            # get shipping price local currency
            shipprice = Decimal(getitem.shipping_price_2)

            # convert it to btc cash
            btc_cash_shiprice1 = Decimal(convert_local_to_bch(amount=shipprice,
                                                              currency=getitem.currency))

            # get it formatted correctly
            btc_cash_shipprice2 = (floating_decimals(btc_cash_shiprice1, 8))

            # times the shipping price times quantity
            shippingtotal = Decimal(itemamount) * Decimal(btc_cash_shipprice2)

            # return shipping price
            btc_cash_shiprice = (floating_decimals(shippingtotal, 8))

            # SHIPPING
            cart_item.selected_shipping_description = str(getitem.shipping_info_2) \
                + ': ' + '(' \
                + str(getitem.shipping_day_least_2) \
                + ' days to ' \
                + str(getitem.shipping_day_most_2) \
                + ' days)'

            cart_item.final_shipping_price = btc_cash_shiprice

        elif cart_item.selected_shipping == 3:
            # PRICE
            # get shipping price local currency
            shipprice = Decimal(getitem.shipping_price_3)
            # convert it to btc cash
            btc_cash_shiprice1 = (convert_local_to_bch(amount=shipprice,
                                                       currency=getitem.currency))
            # get it formatted correctly
            btc_cash_shipprice2 = (floating_decimals(btc_cash_shiprice1, 8))
            # times the shipping price times quantity
            shippingtotal = Decimal(itemamount) * Decimal(btc_cash_shipprice2)
            # return shipping price
            btc_cash_shiprice = (floating_decimals(shippingtotal, 8))

            # SHIPPING
            # concat info for shipping information
            cart_item.selected_shipping_description = str(getitem.shipping_info_2) \
                + ': ' \
                + '(' \
                + str(getitem.shipping_day_least_3) \
                + ' days to ' \
                + str(getitem.shipping_day_most_3) \
                + ' days)'

            cart_item.final_shipping_price = btc_cash_shiprice

        else:
            # see what shipping is avaliable as first choice ..
            if cart_item.shipping_free == 1:
                btc_cash_shipprice2 = 0
                cart_item.selected_shipping_description = 0
            elif cart_item.shipping_two == 1:
                btc_cash_shipprice2 = convert_local_to_bch(amount=cart_item.shipping_price_2, currency=cart_item.currency)
                cart_item.selected_shipping_description = cart_item.shipping_info_2
            elif cart_item.shipping_two == 1:
                btc_cash_shipprice2 = convert_local_to_bch(amount=cart_item.shipping_price_3, currency=cart_item.currency)
                cart_item.selected_shipping_description = cart_item.shipping_info_3
            else:
                btc_cash_shipprice2 = 0
                cart_item.selected_shipping_description = 0

        # add totals to list for adding to shopping cart total
        bch_pricelist.append((btc_cash_z, cart_item.quantity_of_item))
        bch_shipping_pricelist.append(
            (btc_cash_shipprice2, cart_item.quantity_of_item))

        # Add to shopping cart
        db.session.add(cart_item)
        db.session.flush()
    ###
    # TOTALS for shopping cart total
    ###

    # BTC CASH
    # multiply items in list together
    xx = tuple(a * b for a, b in bch_pricelist)
    # add to get total
    bb = ("{0:.8f}".format(sum(xx)))
    btc_cash_sum = sum(j for cart_item, j in bch_pricelist)

    gettotalcart.btc_cash_sumofitem = btc_cash_sum
    gettotalcart.btc_cash_price = bb

    # shipping loop
    dd = tuple(t*h for t, h in bch_shipping_pricelist)
    # add to get total
    ee = ("{0:.8f}".format(sum(dd)))
    gettotalcart.shipping_btc_cashprice = ee
    # get total
    btc_cash_thetotal = Decimal(bb) + Decimal(ee)
    gettotalcart.total_btc_cash_price = btc_cash_thetotal
    # remove/set affiliate
    gettotalcart.percent_off_order = 0
    gettotalcart.btc_cash_off = 0
    gettotalcart.btc_off = 0

    db.session.add(gettotalcart)

    # Relatedqueries
    # gets queries of related subcategory..if not enough will do main category
    # related to first item only currently
    # get price
    getcurrentprice = db.session\
        .query(Bch_Prices) \
        .filter(Bch_Prices.currency_id == current_user.currency) \
        .first()

    db.session.commit()

            if form.update.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
                else:
                    for y in cart:
                        # get to see whats checked
                        try:
                            checkbox = request.form.getlist(
                                ('checkit-' + str(y.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        try:
                            quant = request.form.getlist(
                                ('quant-' + str(y.id)))
                            # find out quant of whats checked
                            newquant = quant[0]
                        except Exception:
                            newquant = y.quantity_of_item
                            pass
                        try:
                            getcurrency = request.form.getlist(
                                ('currency-' + str(y.id)))
                            # find out quant of whats checked
                            thecurrency = getcurrency[0]
                        except Exception:
                            thecurrency = 0
                            pass
                        try:
                            shipmethod = request.form.getlist(('shipit-' + str(y.id)))
                            # find out quantity of whats checked
                            shipmethodchosen = shipmethod[0]
                        except Exception:
                            shipmethodchosen = 0
                            pass
                        # query that specific item in shopping cart then update it
                        if valueincheckbox == 0:
                            pass
                        else:
                            # check to see if they picked a shipping method
                            if int(y.id) == int(valueincheckbox):
                                # see if item exists and check its shipping
                                markett = db.session.query(Item_MarketItem) \
                                    .filter(y.item_id == Item_MarketItem.id).first()
                                if int(markett.item_count) < int(newquant):
                                    flash("Vendor does not have that much",
                                          category="danger")
                                    return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
                                else:
                                    y.quantity_of_item = newquant
                                    y.selected_currency = thecurrency

                                    if 1 <= int(shipmethodchosen) <= 3:
                                        y.selected_shipping = shipmethodchosen
                                    else:
                                        flash(
                                            "Please select a shipping method.", category="danger")
                                        return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
                                    db.session.add(y)
                                    db.session.commit()
                    return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))

            elif form.delete.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
                else:
                    for itemtobedeleted in cart:
                        try:
                            # get ites checked
                            checkbox = request.form.getlist(
                                ('checkit-' + str(itemtobedeleted.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        if valueincheckbox == 0:
                            pass
                        else:
                            # match item checked to cart
                            cartitem = db.session.query(Checkout_CheckoutShoppingCart).filter_by(
                                id=valueincheckbox).first()
                            # if owner
                            if cartitem.customer == current_user.username:
                                # delete it
                                db.session.delete(cartitem)
                                db.session.commit()
                    return jsonify({'status': 'success'})

            elif form.saveforlater.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    return jsonify({'status': 'error'})
                else:
                    for y in cart:
                        try:
                            checkbox = request.form.getlist(
                                ('checkit-' + str(y.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        if valueincheckbox == 0:
                            pass
                        else:
                            cartitem = db.session.query(Checkout_CheckoutShoppingCart).filter_by(
                                id=valueincheckbox).first()
                            if cartitem.customer == current_user.username:
                                cartitem.savedforlater = 1

                                db.session.add(cartitem)
                                db.session.commit()
                    return jsonify({'status': 'success'})







