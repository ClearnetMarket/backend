from flask import  jsonify
from flask_login import current_user, login_required
from app.checkout import checkout
from app import db
from datetime import datetime, timedelta
from decimal import Decimal
import calendar
# models
from app.classes.checkout import\
    Checkout_CheckoutShoppingCart,\
    Checkout_ShoppingCartTotal,\
    Checkout_CheckoutShoppingCart_Schema,\
    Checkout_ShoppingCartTotal_Schema

from app.classes.wallet_bch import Bch_Prices
from app.classes.auth import Auth_User, Auth_UserFees
from app.classes.item import \
    Item_MarketItem, \
    Checkout_CheckoutShoppingCart, \
    Checkout_ShoppingCartTotal
from app.classes.service import \
    Service_ShippingSecret

from app.classes.vendor import \
    Vendor_Orders

from app.classes.wallet_bch import \
    Bch_Wallet

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




@checkout.route('/movecartitem/<int:id>', methods=['POST'])
@login_required
def checkout_move_cart_item(id):

    theitem = Checkout_CheckoutShoppingCart.query.get(id)
    if theitem:
        if theitem.customer_id == current_user.id:
            getcart = db.session\
                .query(Checkout_CheckoutShoppingCart)\
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

            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
    else:

        return redirect(url_for('index', username=current_user.username))

# end models
@checkout.route('/cat', methods=['POST'])
@login_required
def shopping_cart():
    """
    :return:
    """
    now = datetime.utcnow()
    form = shoppingcartForm(request.form)

    # Total cart
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()
    cart = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer == current_user.username,
                Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()
    gettotalcart = db.session\
        .query(Checkout_ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # see if orders previous..delete them
    user_orders = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.customer_id == user.id)\
        .filter(Vendor_Orders.type == 1)\
        .filter(Vendor_Orders.incart == 1)\
        .all()

    # see if msg
    msg = db.session\
        .query(Service_ShippingSecret)\
        .filter_by(user_id=user.id, orderid=0)\
        .first()
    if msg:
        db.session.delete(msg)

    for i in user_orders:
        db.session.delete(i)

    # Saved for later cart
    try:
        cartsaved = db.session\
            .query(Checkout_CheckoutShoppingCart)\
            .filter(Checkout_CheckoutShoppingCart.customer == user.username, Checkout_CheckoutShoppingCart.savedforlater == 1)\
            .all()
    except Exception:
        cartsaved = 0
    # timer
    fiftenminutes = timedelta(minutes=15)
    fromnow = datetime.utcnow() + fiftenminutes

    # Bitcoin cash
    BTC_CASH_pricelist = []
    BTC_CASH_shipping_pricelist = []
    btc_cash_wallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user.id)\
        .first()

    # First query item get latest price/info/etc
    for i in cart:
        # see if still exists
        try:
            getitem = db.session\
                .query(Item_MarketItem)\
                .filter(Item_MarketItem.id == i.item_id)\
                .first()
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))

        # image
        try:
            i.string_auction_id = '/' + str(i.item_id) + '/'
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
        try:
            i.image_of_item = getitem.image_one
        except Exception as e:
            i.image_of_item = '0'

        # price
        try:
            i.price_of_item = getitem.price
        except Exception:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))

        # supply
        try:
            i.vendorsupply = getitem.item_count
            if i.vendorsupply <= 0:
                flash(i.title_of_item + " has been sold out.  It has been removed from your cart",
                      category="success")
                db.session.delete(i)
                db.session.commit()
                return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))

        # shipping
        try:
            if i.shipping_free == 0 and i.shipping_two == 0 and i.shipping_three == 0:
                flash("Item#" + str(i.id) +
                      ": Doesnt have a shipping method", category="danger")
                db.session.delete(i)
                db.session.commit()
                return redirect(url_for('checkout.checkout_shopping_cart', username=current_user.username))
        except Exception:
            return redirect(url_for('index', username=current_user.username))

        # shipping1
        try:
            i.shipping_info_0 = getitem.shipping_info_0,
            i.shipping_day_least_0 = getitem.shipping_day_least_0,
            i.shipping_day_most_0 = getitem.shipping_day_most_0,

        except Exception:
            i.shipping_info_0 = '',
            i.shipping_day_least_0 = '',
            i.shipping_day_most_0 = '',

        # shipping2
        try:
            i.shipping_info_2 = getitem.shipping_info_2,
            i.shipping_price_2 = getitem.shipping_price_2,
            i.shipping_day_least_2 = getitem.shipping_day_least_2,
            i.shipping_day_most_2 = getitem.shipping_day_most_2,

        except Exception:
            i.shipping_info_2 = '',
            i.shipping_price_2 = '',
            i.shipping_day_least_2 = '',
            i.shipping_day_most_2 = '',

        # shipping 3
        try:
            i.shipping_info_3 = getitem.shipping_info_3,
            i.shipping_price_3 = getitem.shipping_price_3,
            i.shipping_day_least_3 = getitem.shipping_day_least_3,
            i.shipping_day_most_3 = getitem.shipping_day_most_3,

        except Exception:
            i.shipping_info_3 = '',
            i.shipping_price_3 = '',
            i.shipping_day_least_3 = '',
            i.shipping_day_most_3 = '',

        db.session.add(i)
        db.session.flush()

        # if bitcoin cash
        # selected currency 3 = btc cash

        # get price
        getcurrentprice = db.session\
            .query(Bch_Prices)\
            .filter(Bch_Prices.currency_id == i.currency)\
            .first()

        btc_cash_bt = getcurrentprice.price
        btc_cash_z = Decimal(i.price_of_item) / Decimal(btc_cash_bt)

        # combined price
        itemamount = (Decimal(i.quantity_of_item))
        itemandquant = (floating_decimals(itemamount * btc_cash_z, 8))
        i.final_price = itemandquant

        # Get shipping
        if i.selected_shipping == 1:
            btc_cash_shipprice2 = 0
            i.final_shipping_price = 0
            i.selected_shipping_description = str(getitem.shipping_info_0) \
                + ': ' + '(' + str(getitem.shipping_day_least_0) \
                + ' days to ' + str(getitem.shipping_day_most_0) \
                + ' days)'

        elif i.selected_shipping == 2:
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
            i.selected_shipping_description = str(getitem.shipping_info_2) \
                + ': ' + '(' \
                + str(getitem.shipping_day_least_2) \
                + ' days to ' \
                + str(getitem.shipping_day_most_2) \
                + ' days)'

            i.final_shipping_price = btc_cash_shiprice

        elif i.selected_shipping == 3:
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
            i.selected_shipping_description = str(getitem.shipping_info_2) \
                + ': ' \
                + '(' \
                + str(getitem.shipping_day_least_3) \
                + ' days to ' \
                + str(getitem.shipping_day_most_3) \
                + ' days)'

            i.final_shipping_price = btc_cash_shiprice

        else:
            # see what shipping is avaliable as first choice ..
            if i.shipping_free == 1:
                btc_cash_shipprice2 = 0
                i.selected_shipping_description = 0
            elif i.shipping_two == 1:
                btc_cash_shipprice2 = convert_local_to_bch(
                    amount=i.shipping_price_2, currency=i.currency)
                i.selected_shipping_description = i.shipping_info_2
            elif i.shipping_two == 1:
                btc_cash_shipprice2 = convert_local_to_bch(
                    amount=i.shipping_price_3, currency=i.currency)
                i.selected_shipping_description = i.shipping_info_3
            else:
                btc_cash_shipprice2 = 0
                i.selected_shipping_description = 0

        # add totals to list for adding to shopping cart total
        BTC_CASH_pricelist.append((btc_cash_z, i.quantity_of_item))
        BTC_CASH_shipping_pricelist.append(
            (btc_cash_shipprice2, i.quantity_of_item))

        # Add to shopping cart
        db.session.add(i)
        db.session.flush()
    ###
    # TOTALS for shopping cart total
    ###

    # BTC CASH
    # multiply items in list together
    xx = tuple(a * b for a, b in BTC_CASH_pricelist)
    # add to get total
    bb = ("{0:.8f}".format(sum(xx)))
    btc_cash_sum = sum(j for i, j in BTC_CASH_pricelist)

    gettotalcart.btc_cash_sumofitem = btc_cash_sum
    gettotalcart.btc_cash_price = bb

    # shipping loop
    dd = tuple(t*h for t, h in BTC_CASH_shipping_pricelist)
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
    cart1 = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer_id == user.id, Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .first()


    # get price
    getcurrentprice = db.session\
        .query(Bch_Prices) \
        .filter(Bch_Prices.currency_id == current_user.currency) \
        .first()

    db.session.commit()

    if request.method == "POST":
        try:
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
                            shipmethod = request.form.getlist(
                                ('shipit-' + str(y.id)))
                            # find out quant of whats checked
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

            elif form.gotocheckout.data:
                if gettotalcart.btcprice == 0 and gettotalcart.total_btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
                else:
                    for k in cart:
                        if k.selected_currency == 3:
                            # get price
                            getcurrentprice = db.session.query(Bch_Prices) \
                                .filter(Bch_Prices.currency_id == k.currency).first()
                        elif k.selected_currency == 2:
                            # get price
                            getcurrentprice = db.session.query(Bch_Prices) \
                                .filter(Bch_Prices.currency_id == k.currency).first()
                        else:
                            pass
                        priceofeach = Decimal(
                            k.final_price) / Decimal(k.quantity_of_item)

                        # # get the vendor fee currently
                        # #get the vendor match to userfees
                        getvendor = k.vendor_id
                        sellerfee = db.session.query(Auth_UserFees).filter(Auth_UserFees.user_id == getvendor).first()
                        physicalitemfee = sellerfee.vendorfee
                        dbfeetopercent = (floating_decimals((physicalitemfee/100), 8))
                        fee = (floating_decimals((dbfeetopercent * k.final_price), 8))
                        # addfee to main amount requested
                        order = Vendor_Orders(
                            type=1,
                            vendor='',
                            vendor_id=0,
                            quantity=k.quantity_of_item,
                            title=k.title_of_item,
                            new_order=1,
                            accepted_order=0,
                            waiting_order=0,
                            delivered_order=0,
                            customer=current_user.username,
                            customer_id=current_user.id,
                            age=datetime.utcnow(),
                            returncancelage=datetime.utcnow(),
                            return_by=datetime.utcnow() + timedelta(days=14),
                            private_note='',
                            escrow=0,
                            disputed_order=0,
                            item_id=k.item_id,
                            string_auction_id=k.string_auction_id,
                            string_node_id=k.string_node_id,
                            image_one=k.image_of_item,
                            request_cancel=0,
                            reason_cancel=0,
                            overallreason=0,
                            request_return=0,
                            currency=k.currency,
                            return_id=0,
                            cancelled=0,
                            feedback=0,
                            userfeedback=0,
                            completed=0,
                            completed_time=now,
                            disputedtimer=datetime.utcnow(),
                            modid=0,
                            incart=1,
                            fee=fee,
                            shipdescription=k.selected_shipping_description,
                            return_allowed=k.return_allowed,
                            buyorsell=0,
                            released=0,
                            return_quantity=0,
                            return_amount=0,
                            digital_currency=k.selected_currency,
                            price=k.final_price,
                            price_peritem=priceofeach,
                            perbtc=getcurrentprice.price,
                            shipping_price=k.final_shipping_price,
                            price_beforediscount=0,
                            affiliate_discount_percent=0,
                            affiliate_code='0',
                            affiliate_discount_btc=0,
                            affiliate_discount_btc_cash=0,
                            affiliate_profit=0,
                        )
                        db.session.add(order)

                    user.shopping_timer = fromnow
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'status': 'success'})

            else:
                db.session.rollback()
                return jsonify({'status': 'error'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error'})


checkout.route('/checkout', methods=['GET', 'POST'])


@website_offline
@login_required
def checkout():
    # forms
    secretinfo = custominfo()
    secretinfoDelete = custominfoDelete()
    finalize = checkoutForm()
    promogift = promoandgiftform()

    promocodesadded = []
    # get user and car
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()

    gettotalcart = db.session\
        .query(Checkout_ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # turn back if issue
    if gettotalcart.btc_sumofitem == 0 and gettotalcart.btc_cash_sumofitem == 0:
        flash("No Items in your Shopping Cart.", category="danger")
        return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))
    if datetime.utcnow() >= user.shopping_timer:
        flash("Time ran out.  Please try again.", category="danger")
        return redirect(url_for('checkout.checkout_shopping_cart', username=user.username))

    # see if user has the Coin
    btc_cash_wallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user.id)\
        .first()
    gettotalcart = db.session\
        .query(Checkout_ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # if user doesnt have enough money
    if Decimal(btc_cash_wallet.currentbalance) <= Decimal(gettotalcart.totalbtcprice):
        flash("Not enough coin in wallet ...", category="danger")
        return redirect(url_for('index'))

    # queries
    cart = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer == current_user.username, Checkout_CheckoutShoppingCart.savedforlater == 0)\
        .all()

    # get the orders
    orders = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.customer_id == user.id)\
        .filter(Vendor_Orders.type == 1).filter(Vendor_Orders.incart == 1)\
        .group_by(Vendor_Orders.id.asc())\
        .all()

    # see if promo code was added
    for promo in orders:
        if promo.affiliate_code != '0':
            promocodesadded.append(promo.affiliate_code)
    if len(promocodesadded) == 0:
        promocodewasadded = 0
    else:
        promocodewasadded = 1

    # get the message
    msg = db.session.query(Service_ShippingSecret).filter_by(
        user_id=user.id, orderid=0).first()
    if msg:
        secretmsg = 0
    else:
        secretmsg = 1

    # timer
    userstimeincart = user.shopping_timer
    timestamp = calendar.timegm(userstimeincart.utctimetuple()) * 1000

    if request.method == "POST":
        if current_user.id == gettotalcart.customer:
            # security to see if cart is empty
            if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                flash("No Items in your Shopping Cart.", category="danger")
                return redirect(url_for('checkout.checkout_shopping_cart'))
            if datetime.utcnow() >= user.shopping_timer:
                flash("Time ran out.  Please try again", category="danger")
                return redirect(url_for('checkout.checkout_shopping_cart'))

            # user added an address
            if secretinfo.custommsgbtn.data:
                # check to see if time ran out
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                elif datetime.utcnow() >= user.shopping_timer:
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                else:
                    if secretinfo.validate_on_submit():
                        try:
                            z = secretinfo.privatemsg.data
                            addmsg = Service_ShippingSecret(
                                user_id=current_user.id,
                                txtmsg=str(z),
                                timestamp=datetime.utcnow(),
                                orderid=0
                            )
                            db.session.add(addmsg)
                            db.session.commit()
                            return redirect(url_for('item.checkout'))
                        except Exception:
                            db.session.rollback()
                            return redirect(url_for('checkout.checkout_shopping_cart'))
                    else:
                        flash("Private Message form error. "
                              "10-2500 characters long required. No special characters allowed.",
                              category="danger")
                        return redirect(url_for('item.checkout'))

            # user deleted his message
            elif secretinfoDelete.deletemsgbtn.data:
                # check to see if cart items
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                # check to see if timer ran out
                elif datetime.utcnow() >= user.shopping_timer:
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                else:
                    db.session.delete(msg)
                    db.session.commit()
                    flash("Private Message deleted", category="danger")
                    return redirect(url_for('item.checkout'))

       
            # user confirmed payment
            elif finalize.MakePayment.data:

                # check to see if cart isnt empty
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    order = None
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                # check to see if time still
                elif datetime.utcnow() >= user.shopping_timer:
                    order = None
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('checkout.checkout_shopping_cart'))
                else:
                    # add security here before proceeding
                    userwallet_btc_cash = db.session\
                        .query(Bch_Wallet)\
                        .filter_by(user_id=user.id)\
                        .first()

                    thecurrentcarttotal_btc_cash = Decimal(
                        gettotalcart.total_btc_cash_price)

                    if thecurrentcarttotal_btc_cash > 0:
                        if Decimal(userwallet_btc_cash.currentbalance) <= thecurrentcarttotal_btc_cash:
                            flash("Not enough coin in bitcoin cash wallet",
                                  category="danger")
                            return redirect(url_for('wallet_btc.walletReceive', username=current_user.username))

                    # see if message
                    if (len(msg.txtmsg)) < 5:
                        flash("Message not long enough", category="danger")
                        return redirect(url_for('item.checkout'))
                    # customer has the coin. proceed
                    # loop through ORDERS. sendinc coin and doing transactions 1 by 1
                    # this does not loop through the shopping cart
                    for specificitemincart in orders:
                        # get the item
                        # get specific item being purchased
                        try:
                            getitem = db.session\
                                .query(Item_MarketItem) \
                                .filter_by(id=specificitemincart.item_id) \
                                .first()
                        except Exception:
                            db.session.delete(specificitemincart)
                            db.session.commit()
                            flash(
                                "Could Not find Item. Perhaps the vendor removed it.", category="danger")
                            return redirect(url_for('wallet_btc.walletReceive', username=current_user.username))

                        # update the order to notify vendor
                        specificitemincart.incart = 0
                        specificitemincart.vendor = getitem.vendor_name,
                        specificitemincart.vendor_id = getitem.vendor_id,
                        # k.shipto_secretmsg = msg.txtmsg

                        # add total sold to item
                        newsold = int(getitem.total_sold) + \
                            int(specificitemincart.quantity)
                        newquantleft = int(getitem.item_count) - \
                            int(specificitemincart.quantity)
                        getitem.total_sold = newsold
                        getitem.item_count = newquantleft

                        # add diff trading partners
                        userdata_different_trading_partners_user(user_id=specificitemincart.customer_id,
                                                                 otherid=specificitemincart.vendor_id)

                        # add diff trading partners
                        userdata_different_trading_partners_vendor(user_id=specificitemincart.vendor_id,
                                                                   otherid=specificitemincart.customer_id)

                        # notify vendor
                        notification(type=1,
                                     username=specificitemincart.vendor,
                                     user_id=specificitemincart.vendor_id,
                                     salenumber=specificitemincart.id,
                                     bitcoin=0)

                        notification(type=112,
                                     username=specificitemincart.customer,
                                     user_id=specificitemincart.customer_id,
                                     salenumber=specificitemincart.id,
                                     bitcoin=0)

                        # for each time..do a coin move
                        # get price of shipping+item * quantity
                        priceofitemorder = floating_decimals((specificitemincart.price
                                                              + specificitemincart.shipping_price), 8)

                        # transactions are added in the sendcoin functions
                        # subtraction of balances occur there also
                        # send bitcoin

                        bch_send_coin_to_escrow(
                            amount=priceofitemorder,
                            comment=specificitemincart.id,
                            user_id=specificitemincart.customer_id
                        )

                        # achievement for first purchase
                        # in a loop since could be ten items

                        # add a message for each order
                        addmsg = Service_ShippingSecret(
                            user_id=current_user.id,
                            txtmsg=msg.txtmsg,
                            timestamp=datetime.utcnow(),
                            orderid=specificitemincart.id
                        )

                        db.session.add(specificitemincart)
                        db.session.add(getitem)
                        db.session.add(addmsg)
                        db.session.flush()

                        # turn off if item is less than one
                        if getitem.item_count < 1:

                            getitem.online = 0
                            db.session.add(getitem)

                            # send notification to vendor saying its all sold out
                            notification(type=9,
                                         username=specificitemincart.vendor,
                                         user_id=getitem.vendor_id,
                                         salenumber=getitem.id,
                                         bitcoin=0)

                # FINISHED loop
                # delete and clear everything
                # query for users message
                oldmsg = db.session\
                    .query(Service_ShippingSecret)\
                    .filter_by(user_id=user.id, orderid=0)\
                    .first()
                db.session.delete(oldmsg)

                # clear user shoppingcarttotal
                gettotalcart = db.session \
                    .query(Checkout_ShoppingCartTotal) \
                    .filter_by(customer=user.id) \
                    .first()
                gettotalcart.totalbtcprice = 0
                gettotalcart.btcprice = 0
                gettotalcart.shippingbtcprice = 0

                # remove affiliate code
                gettotalcart.percent_off_order = 0
                gettotalcart.btc_cash_off = 0
                gettotalcart.btc_off = 0
                db.session.add(gettotalcart)

                # delete items in cart
                for f in cart:
                    db.session.delete(f)


                db.session.commit()
                flash("Successful Order.", category="success")
                return redirect(url_for('orders.orders_home'))

        # not specific form information made
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('item.checkout', username=user.username))

    return render_template('/item/checkout.html',
                           promogift=promogift,
                           secretinfo=secretinfo,
                           secretinfoDelete=secretinfoDelete,
                           finalize=finalize,
                           secretmsg=secretmsg,
                           msg=msg,
                           order=orders,
                           cart=cart,
                           btc_cash_wallet=btc_cash_wallet,
                           timestamp=timestamp,
                           gettotalcart=gettotalcart,
                           promocodewasadded=promocodewasadded
                           )
