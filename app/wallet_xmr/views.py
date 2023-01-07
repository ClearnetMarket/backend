from flask import request, jsonify
from flask_login import current_user
from app import db, bcrypt, UPLOADED_FILES_DEST_USER
import os
from decimal import Decimal
from app.common.functions import floating_decimals
from app.common.decorators import login_required
from app.wallet_xmr import wallet_xmr
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin
# models
from app.classes.auth import Auth_User
from app.classes.wallet_xmr import\
    Xmr_Transactions,\
    Xmr_Transactions_Schema,\
    Xmr_Wallet, \
    Xmr_WalletFee,  \
    Xmr_Prices
# end models


@wallet_xmr.route('/price/usd', methods=['GET'])
def xmr_price_anonymous():
    """
    Gets current price of bitcoin cash
    :return:
    """
    price_xmr = db.session\
        .query(Xmr_Prices)\
        .filter_by(currency_id=0)\
        .first()
    if price_xmr.price > 0:
        try:
            price_xmr = str(price_xmr.price)
        except:
            price_xmr = 0

        return jsonify({
            "price_xmr": price_xmr,
        })
    else:
        return jsonify({
            "price_xmr": 'error',
        })
        
@wallet_xmr.route('/price', methods=['GET'])
@login_required
def xmr_price_for_user():
    """
    Gets current price of bitcoin cash
    :return:
    """
    price_xmr = db.session\
        .query(Xmr_Prices)\
        .filter_by(currency_id=current_user.currency)\
        .first()
    if price_xmr.price > 0:
        try:
            price_xmr = str(price_xmr.price)
        except:
            price_xmr = 0

        return jsonify({
            "price_xmr": price_xmr,
        })
    else:
        return jsonify({
            "price_xmr": 'error',
        })


@wallet_xmr.route('/balance', methods=['GET'])
@login_required
def xmr_balance_plus_unconfirmed():
    """
    Gets current balance and any unconfirmed transactions
    :return:
    """
    userwallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    try:
        userbalance = str(userwallet.currentbalance)
        unconfirmed = str(userwallet.unconfirmed)
    except:
        userbalance = 0
        unconfirmed = 0

    return jsonify({
        "xmr_balance": userbalance,
        "xmr_unconfirmed": unconfirmed,
    })


@wallet_xmr.route('/transactions', methods=['GET'])
@login_required
def xmr_transactions():

    # Get Transaction history
    transactfull = db.session\
        .query(Xmr_Transactions)\
        .filter(Xmr_Transactions.user_id == current_user.id)\
        .order_by(Xmr_Transactions.id.desc())\
        .limit(50)

    transactions_list = Xmr_Transactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_xmr.route('/receive', methods=['GET'])
@login_required
def xmr_receive():

    wallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()

    qr = wallet.address1 + '.png'
    wallet_qr_code = os.path.join(UPLOADED_FILES_DEST_USER, str(current_user.uuid), 'qr', qr)
    
    return jsonify({"xmr_address": wallet.address1,
                    "xmr_qr_code": wallet_qr_code
                        }), 200


@wallet_xmr.route('/send', methods=['GET', 'POST'])
@login_required
def xmr_send():

    user = db.session\
        .query(Auth_User)\
        .filter_by(id=current_user.id)\
        .first()
    wallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    # get walletfee
    walletthefee = db.session\
        .query(Xmr_WalletFee)\
        .filter_by(id=1)\
        .first()
    wfee = Decimal(walletthefee.xmr)

    # form variables
    walletpin = request.json["walletpin"]
    send_to_address = request.json["send_to_address"]
    amount = request.json["amount"]

    if user.dispute == 0:
        if bcrypt.check_password_hash(user.walletpin, walletpin):
            # test wallet for security
            walbal = Decimal(wallet.currentbalance)
            amount2withfee = Decimal(amount) + Decimal(wfee)
            # greater than amount with fee
            if floating_decimals(walbal, 12) >= floating_decimals(amount2withfee, 12):
                # greater than fee
                if Decimal(amount) > Decimal(wfee):
                    # add to wallet_xmr work
                    xmr_send_coin(
                        user_id=user.id,
                        sendto=send_to_address,
                        amount=amount,
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
    else:
        return jsonify({"error": "Account is locked due to dispute"}), 409
