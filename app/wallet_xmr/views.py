from flask import request, session, jsonify
from app import db, bcrypt
from app.wallet_xmr import wallet_xmr
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin

from datetime import datetime
from app.common.functions import floating_decimals
from app.common.decorators import login_required
from app.achs.b import likemoneyinthebank,withdrawl
from decimal import Decimal

# models
from app.classes.auth import Auth_User
from app.classes.wallet_xmr import\
    Xmr_Transactions,\
    Xmr_Transactions_Schema,\
    Xmr_Wallet, \
    Xmr_WalletFee
# end models

@wallet_xmr.route('/balance', methods=['GET'])
@login_required
def xmr_balance_plus_unconfirmed():
    """
    Gets current balance and any unconirmed transactions
    :return:
    """
    user_id = session.get("user_id")
    userwallet = Xmr_Wallet.query.filter_by(user_id=user_id).first()
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
        "xmr_balance": userbalance,
        "xmr_unconfirmed": unconfirmed,
    })

@wallet_xmr.route('/transactions', methods=['GET'])
@login_required
def xmr_transactions():
    user_id = session.get("user_id")
    # Get Transaction history
    transactfull = Xmr_Transactions.query\
        .filter(Xmr_Transactions.user_id == user_id.id)\
        .order_by(Xmr_Transactions.id.desc())\
        .limit(50)

    transactions_list = Xmr_Transactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_xmr.route('/receive', methods=['GET'])
@login_required
def xmr_receive():
    user_id = session.get("user_id")
    wallet = Xmr_Wallet.query.filter_by(user_id=user_id.id).first()
    return jsonify({"xmr_address": wallet.address1}), 200


@wallet_xmr.route('/send', methods=['GET', 'POST'])
@login_required
@login_required
def xmr_send():

    user_id = session.get("user_id")
    # Get wallet
    user = Auth_User.query.filter_by(id=user_id).first()
    wallet = Xmr_Wallet.query.filter_by(user_id=user_id).first()
    # get walletfee
    walletthefee = Xmr_WalletFee.query.filter_by(id=1).first()
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
                        user_id=user_id,
                        sendto=send_to_address,
                        amount=amount,
                    )
                    # achievement
                    withdrawl(user_id=user_id)
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
