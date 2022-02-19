from flask import request, session, jsonify
from app import db, bcrypt
from app.wallet_bch import wallet_bch
from app.wallet_bch.wallet_bch_work import bch_send_coin

from datetime import datetime
from app.common.functions import floating_decimals
from app.common.decorators import login_required
from app.achs.b import likemoneyinthebank,withdrawl
from decimal import Decimal

# models
from app.classes.auth import Auth_User
from app.classes.wallet_bch import\
    Bch_WalletTransactions,\
    Bch_WalletTransactions_Schema, \
    Bch_Wallet,\
    Bch_WalletFee
# end models


@wallet_bch.route('/balance', methods=['GET'])
@login_required
def bch_balance_plus_unconfirmed():
    """
    Gets current balance and any unconirmed transactions
    :return:
    """
    user_id = session.get("user_id")
    userwallet = Bch_Wallet.query.filter_by(user_id=user_id).first()
    if userwallet.currentbalance > 0:
        likemoneyinthebank(user_id=user_id)
        db.session.commit()
    try:
        userbalance = Decimal(userwallet.currentbalance)
        unconfirmed = Decimal(userwallet.unconfirmed)
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
    user_id = session.get("user_id")
    # Get Transaction history
    transactfull = Bch_WalletTransactions.query\
        .filter(Bch_WalletTransactions.user_id == user_id.id)\
        .order_by(Bch_WalletTransactions.id.desc())\
        .limit(50)

    transactions_list = Bch_WalletTransactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200

@wallet_bch.route('/receive', methods=['GET'])
@login_required
def bch_receive():
    user_id = session.get("user_id")
    wallet = Bch_Wallet.query.filter_by(user_id=user_id.id).first()
    return jsonify({"bch_address": wallet.address1}), 200

@wallet_bch.route('/send', methods=['GET', 'POST'])
@login_required
@login_required
def bch_send():

    user_id = session.get("user_id")
    # Get wallet_btc
    user = Auth_User.query.filter_by(id=user_id).first()
    wallet = Bch_Wallet.query.filter_by(user_id=user_id).first()
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
                        user_id=user_id,
                        sendto=send_to_address,
                        amount=amount,
                        comment=comment_on_blockchain
                    )
                    # achievement
                    withdrawl(user_id=user_id)
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

