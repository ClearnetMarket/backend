from flask import request, jsonify
from flask_login import current_user, login_required
from app import db
from app.wallet_bch import wallet_bch
from app.wallet_bch.wallet_bch_work import bch_send_coin
from app.common.functions import floating_decimals
from decimal import Decimal

# models
from app.classes.auth import Auth_User
from app.classes.wallet_bch import\
    Bch_WalletTransactions,\
    Bch_WalletTransactions_Schema, \
    Bch_Wallet,\
    Bch_WalletFee, \
    Bch_Prices
# end models


@wallet_bch.route('/price/usd', methods=['GET'])
def bch_price_anonymous():
    """
    Gets current price of bitcoin cash
    :return:
    """

    price_bch = db.session\
        .query(Bch_Prices)\
        .filter_by(currency_id=0)\
        .first()

    if price_bch.price <= 0:
        return jsonify({
            "error": 'Error:  No Price Found',
        })
    try:
        price_bch = str(price_bch.price)
    except:
        price_bch = 0

    return jsonify({
        "success": "success",
        "bch_price": price_bch,
        })

        
@wallet_bch.route('/price', methods=['GET'])
@login_required
def bch_price_for_user():
    """
    Gets current price of bitcoin cash
    :return:
    """
    price_bch = db.session\
            .query(Bch_Prices)\
            .filter_by(currency_id=current_user.currency)\
            .first()

    if price_bch.price <= 0:
        return jsonify({
            "error": 'Error:  No Price Found',
        })
    try:
        price_bch = str(price_bch.price)
    except:
        price_bch = 0

    return jsonify({
        "success": "success",
        "bch_price": price_bch,
    })


@wallet_bch.route('/balance', methods=['GET'])
@login_required
def bch_balance_plus_unconfirmed():
    """
    Gets current balance and any unconirmed transactions
    :return:
    """
    userwallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    try:
        userbalance = str(userwallet.currentbalance)
        unconfirmed = str(userwallet.unconfirmed)
    except:
        userbalance = 0
        unconfirmed = 0

    return jsonify({
        "success": "success",
        "bch_balance": userbalance,
        "bch_unconfirmed": unconfirmed,
    })


@wallet_bch.route('/transactions/<int:page>', methods=['GET'])
@login_required
def bch_transactions(page):

    per_page_amount = 50
    if page is None:
        offset_limit = 0
        page = 1
    elif page == 1:
        offset_limit = 0
        page = 1
    else:
        offset_limit = (per_page_amount * page) - per_page_amount
        page = int(page)



    # Get Transaction history
    transactfull = db.session\
        .query(Bch_WalletTransactions)\
        .filter(Bch_WalletTransactions.user_id == current_user.id)\
        .order_by(Bch_WalletTransactions.id.desc())\
        .limit(per_page_amount).offset(offset_limit)

    transactions_list = Bch_WalletTransactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_bch.route('/transactions/count', methods=['GET'])
@login_required
def bch_transactions_count():


    # Get Transaction history
    transactfull = db.session\
        .query(Bch_WalletTransactions)\
        .filter(Bch_WalletTransactions.user_id == current_user.id)\
        .order_by(Bch_WalletTransactions.id.desc())\
        .count()

    transactions_list = Bch_WalletTransactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_bch.route('/receive', methods=['GET'])
@login_required
def bch_receive():
    
    wallet = db.session\
        .query(Bch_Wallet)\
        .filter(Bch_Wallet.user_id == current_user.id)\
        .first()
    return jsonify({
        "success": "success",
        "bch_address": wallet.address1}), 200


@wallet_bch.route('/send', methods=['POST'])
@login_required
def bch_send():
    # form variables
    send_to_address = request.json["send_to_address"]
    comment_on_blockchain = request.json["comment_on_blockchain"]
    amount = request.json["amount"]

    # Get wallet_btc
    user = db.session\
        .query(Auth_User)\
        .filter_by(id=current_user.id)\
        .first()
    wallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    # get walletfee
    walletthefee = db.session\
        .query(Bch_WalletFee)\
        .filter_by(id=1)\
        .first()
    wfee = Decimal(walletthefee.bch)

    if user.dispute != 0:
        return jsonify({"error": f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}"}), 200

    # test wallet btc stuff for security
    walbal = Decimal(wallet.currentbalance)
    amount2withfee = Decimal(amount) + Decimal(wfee)
    # greater than amount with fee
    if floating_decimals(walbal, 8) <= floating_decimals(amount2withfee, 8):
        return jsonify({"error": f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}"}), 200
    # greater than fee
    if Decimal(amount) < Decimal(wfee):
        return jsonify({"error": f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}"}), 200
    # add to wallet_btc work
    bch_send_coin(
        user_id=current_user.id,
        sendto=send_to_address,
        amount=amount,
        comment=comment_on_blockchain
    )

    db.session.commit()
    return jsonify({"success": "request sent to wallet"}), 200




    

