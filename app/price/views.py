from flask import jsonify
from flask_login import login_required, current_user
from app.price import price
from app import db
import datetime
# models
from app.classes.wallet_btc import Btc_Prices, Btc_Wallet
from app.classes.wallet_bch import Bch_Prices, Bch_Wallet
from app.classes.wallet_xmr import Xmr_Prices, Xmr_Wallet
from app.common.convert_prices import *



# LOCAL TO CRYPTOCURRENCY PRICE
@price.route('/btcprice/<string:currency>/<string:price>', methods=['GET'])
def btc_price_from_user_currency(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in bitcoin
    :return:
    """
    decimal_price = Decimal(price)
    current_btc_price = convert_local_to_btc(
        amount=decimal_price, currency=currency)

    return jsonify({"coin": current_btc_price})


@price.route('/bchprice/<string:currency>/<string:price>', methods=['GET'])
def bch_price_from_user_currency(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in bitcoin cash
    :return:
    """
    decimal_price = Decimal(price)
    current_bch_price = convert_local_to_bch(
        amount=decimal_price, currency=currency)
    return jsonify({"coin": current_bch_price})


@price.route('/xmrprice/<string:currency>/<string:price>', methods=['GET'])
def xmr_price_from_user_currency(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in monero
    :return:
    """
    decimal_price = Decimal(price)
    current_xmr_price = convert_local_to_xmr(amount=decimal_price, currency=currency)
    return jsonify({"coin": current_xmr_price})


# CURRENCY TO LOCAL
@price.route('/btcprice/local/<string:currency>/<int:price>', methods=['GET'])
def local_price_from_btc(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in bitcoin
    :return:
    """
    current_local_price_from_btc = convert_to_local_btc(
        amount=price, currency=currency)
    return jsonify({"coin": current_local_price_from_btc})


@price.route('/bchprice/local/<string:currency>/<int:price>', methods=['GET'])
def local_price_from_bch(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in bitcoin cash
    :return:
    """
    current_local_price_from_bch = convert_to_local_bch(
        amount=price, currency=currency)
    return jsonify({"coin": current_local_price_from_bch})


@price.route('/xmrprice/local/<string:currency>/<int:price>', methods=['GET'])
def local_price_from_xmr(currency, price):
    """
    Given a user currency example USD and the price Example 10.00 
     Returns price in monero
    :return:
    """
    current_local_price_from_xmr = convert_to_local_xmr(
        amount=price, currency=currency)
    return jsonify({"coin": current_local_price_from_xmr})





@price.route('/wallets/total/<string:currency>', methods=['GET'])
@login_required
def get_total_wallet(currency):
    """
    Calculates the total price in usd of all wallets combined
     Returns price in monero
    :return:
    """
    xmrwallet = db.session\
        .query(Xmr_Wallet)\
        .filter(Xmr_Wallet.user_id == current_user.id)\
        .first()
    bchwallet = db.session\
        .query(Bch_Wallet)\
        .filter(Bch_Wallet.user_id == current_user.id)\
        .first()
    btcwallet = db.session\
        .query(Btc_Wallet)\
        .filter(Btc_Wallet.user_id == current_user.id)\
        .first()
    current_local_price_from_btc = convert_to_local_btc(
        amount=btcwallet.currentbalance, currency=currency)
    current_local_price_from_bch = convert_to_local_bch(
        amount=bchwallet.currentbalance, currency=currency)
    current_local_price_from_xmr = convert_to_local_xmr(
        amount=xmrwallet.currentbalance, currency=currency)
    print(current_local_price_from_xmr)
    current_amounts_in_wallet = Decimal(current_local_price_from_btc) + Decimal(current_local_price_from_bch) + Decimal(current_local_price_from_xmr)

    return jsonify({"coin": current_amounts_in_wallet})
