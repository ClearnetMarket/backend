from flask import request, jsonify
from app import db, bcrypt
from app.wallet_btc import wallet_btc
from app.wallet_btc.wallet_btc_work import btc_send_coin
from flask_login import current_user
from app.common.functions import floating_decimals
from app.common.decorators import login_required
from decimal import Decimal
# models
from app.classes.auth import Auth_User
from app.classes.wallet_btc import \
    Btc_TransactionsBtc,\
    Btc_TransactionsBtc_Schema,\
    Btc_Wallet, \
    Btc_WalletFee, \
    Btc_Prices
# end models

@wallet_btc.route('/price', methods=['GET'])
def btc_price_usd():
    """
    Gets current price of bitcoin cash
    :return:
    """
    price_btc_usd = Btc_Prices.query.filter_by(currency_id=0).first()
    if price_btc_usd.price > 0:
        try:
            price_btc_usd = str(price_btc_usd.price)
        except:
            price_btc_usd = 0
        return jsonify({
            "btc_price_usd": price_btc_usd,
        })
    else:
        return jsonify({
            "btc_price_usd": 'error',
        })


@wallet_btc.route('/balance', methods=['GET'])
@login_required
def btc_balance_plus_unconfirmed():
    """
    Gets current balance and any unconirmed transactions
    :return:
    """
    userwallet = Btc_Wallet.query.filter(Btc_Wallet.user_id == current_user.id).first()
    try:
        userbalance = str(userwallet.currentbalance)
        unconfirmed = str(userwallet.unconfirmed)
    except Exception as e:
        userbalance = 0
        unconfirmed = 0

    return jsonify({
        "btc_balance": userbalance,
        "btc_unconfirmed": unconfirmed,
    })

@wallet_btc.route('/transactions', methods=['GET'])
@login_required
def btc_transactions():

    # Get Transaction history
    transactfull = Btc_TransactionsBtc.query\
        .filter(Btc_TransactionsBtc.user_id == current_user.id)\
        .order_by(Btc_TransactionsBtc.id.desc())\
        .limit(50)

    transactions_list = Btc_TransactionsBtc_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_btc.route('/receive', methods=['GET'])
@login_required
def btc_receive():
    userwallet = Btc_Wallet.query.filter(Btc_Wallet.user_id == current_user.id).first()
    return jsonify({"btc_address": userwallet.address1}), 200


@wallet_btc.route('/send', methods=['POST'])
@login_required
def btc_send():
    # Get wallet
    user = Auth_User.query.filter_by(id=current_user.id).first()
    userwallet = Btc_Wallet.query.filter_by(Btc_Wallet.user_id == current_user.id).first()
    # get wallet fee
    walletthefee = Btc_WalletFee.query.filter_by(id=1).first()
    wfee = Decimal(walletthefee.btc)

    # form variables
    walletpin = request.json["walletpin"]
    send_to_address = request.json["send_to_address"]
    comment_on_blockchain = request.json["comment_on_blockchain"]
    amount = request.json["amount"]

    if user.dispute == 0:
        if bcrypt.check_password_hash(user.walletpin, walletpin):
            # test wallet btc stuff for security
            walbal = Decimal(userwallet.currentbalance)
            amount2withfee = Decimal(amount) + Decimal(wfee)
            # greater than amount with fee
            if floating_decimals(walbal, 8) >= floating_decimals(amount2withfee, 8):
                # greater than fee
                if Decimal(amount) > Decimal(wfee):
                    # add to wallet work
                    btc_send_coin(
                        user_id=user.id,
                        sendto=send_to_address,
                        amount=amount,
                        comment=comment_on_blockchain
                    )
                    db.session.commit()
                    return jsonify({"status": "request sent to wallet"}), 200
                else:
                    return jsonify({"error": f"Cannot withdraw amount less than wallet fee: {str(wfee)}"}), 409
            else:
                return jsonify({"error": f"Cannot withdraw amount less than wallet fee: {str(wfee)}"}), 409
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

