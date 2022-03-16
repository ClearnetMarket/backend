from flask import request, session, jsonify
from app import db, bcrypt
from app.wallet_bch import wallet_bch
from app.wallet_bch.wallet_bch_work import bch_send_coin
from flask_login import current_user, login_required
from datetime import datetime
from app.common.functions import floating_decimals

from app.achs.b import likemoneyinthebank,withdrawl
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

@wallet_bch.route('/price', methods=['GET'])

def bch_price_usd():
    """
    Gets current price of bitcoin cash
    :return:
    """

    price_bch_usd = Bch_Prices.query.filter_by(currency_id=0).first()

    if price_bch_usd.price > 0:
        try:
            price_bch_usd = str(price_bch_usd.price)
        except:
            price_bch_usd = 0
 
        return jsonify({
            "bch_price_usd": price_bch_usd,
        })
    else:
        return jsonify({
            "bch_price_usd": '0',
        })


@wallet_bch.route('/balance', methods=['GET'])
@login_required
def bch_balance_plus_unconfirmed():
    """
    Gets current balance and any unconirmed transactions
    :return:
    """

    userwallet = Bch_Wallet.query.filter_by(user_id=current_user.id).first()
 
    try:
        userbalance = str(userwallet.currentbalance)
        unconfirmed = str(userwallet.unconfirmed)
    except:
        userbalance = 0
        unconfirmed = 0

    return jsonify({
        "bch_balance": userbalance,
        "bch_unconfirmed": unconfirmed,
    })

@wallet_bch.route('/transactions', methods=['GET'])
@login_required
def bch_transactions():
    
    # Get Transaction history
    transactfull = Bch_WalletTransactions.query\
        .filter(Bch_WalletTransactions.user_id == current_user.id)\
        .order_by(Bch_WalletTransactions.id.desc())\
        .limit(50)

    transactions_list = Bch_WalletTransactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200

@wallet_bch.route('/receive', methods=['GET'])
@login_required
def bch_receive():
    
    wallet = Bch_Wallet.query.filter(Bch_Wallet.user_id==current_user.id).first()
    print(wallet)
    print(wallet.address1)
    return jsonify({"bch_address": wallet.address1}), 200

@wallet_bch.route('/send', methods=['POST'])
@login_required
def bch_send():

    # Get wallet_btc
    user = Auth_User.query.filter_by(id=current_user.id).first()
    wallet = Bch_Wallet.query.filter_by(user_id=current_user.id).first()
    # get walletfee
    walletthefee = Bch_WalletFee.query.filter_by(id=1).first()
    wfee = Decimal(walletthefee.bch)

    # form variables
    walletpin = request.json["walletpin"]
    send_to_address = request.json["send_to_address"]
    comment_on_blockchain = request.json["comment_on_blockchain"]
    amount = request.json["amount"]

    if user.dispute == 0:
        if bcrypt.check_password_hash(user.walletpin, walletpin):
            # test wallet btc stuff for security
            walbal = Decimal(wallet.currentbalance)
            amount2withfee = Decimal(amount) + Decimal(wfee)
            # greater than amount with fee
            if floating_decimals(walbal, 8) >= floating_decimals(amount2withfee, 8):
                # greater than fee
                if Decimal(amount) > Decimal(wfee):
                    # add to wallet_btc work
                    bch_send_coin(
                        user_id=current_user.id,
                        sendto=send_to_address,
                        amount=amount,
                        comment=comment_on_blockchain
                    )
                    # achievement
                    withdrawl(user_id=current_user.id)
                    db.session.commit()
                    return jsonify({"status": "request sent to wallet"}), 200
                else:
                    return jsonify({"error": f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}"}), 409
            else:
                return jsonify({"error": f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}"}), 409
        else:
            current_fails = int(user.fails)
            new_fail_amount = current_fails + 1
            user.fails = new_fail_amount
            db.session.add(user)
            if int(user.fails) == 5:
                user.locked = 1
            db.session.add(user)
            db.session.commit()

            return jsonify({"error": "Unauthorized"}), 409

