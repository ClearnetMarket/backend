from flask import request, jsonify
from app import db, bcrypt, UPLOADED_FILES_DEST_USER
from app.wallet_xmr import wallet_xmr
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin
from flask_login import current_user
import os
from app.notification import notification
from app.common.functions import floating_decimals
from app.common.decorators import login_required
from wallet_xmr.security import xmr_check_balance
from wallet_xmr.transaction import xmr_add_transaction
from decimal import Decimal
# models
from app.classes.auth import Auth_User
from app.classes.wallet_xmr import\
    Xmr_Transactions,\
    Xmr_Transactions_Schema,\
    Xmr_Wallet, \
    Xmr_WalletFee,  \
    Xmr_Prices
# end models


@wallet_xmr.route('/price', methods=['GET'])

def xmr_price_usd():
    """
    Gets current price of bitcoin cash
    :return:
    """

    price_xmr_usd = Xmr_Prices.query.filter_by(currency_id=0).first()
    if price_xmr_usd.price > 0:
        try:
            price_xmr_usd = str(price_xmr_usd.price)
        except:
            price_xmr_usd = 0
        return jsonify({
            "price_xmr_usd": price_xmr_usd,
        })
    else:
        return jsonify({
            "price_xmr_usd": 'error',
        })


@wallet_xmr.route('/balance', methods=['GET'])
@login_required
def xmr_balance_plus_unconfirmed():
    """
    Gets current balance and any unconfirmed transactions
    :return:
    """

    userwallet = Xmr_Wallet.query.filter_by(user_id=current_user.id).first()
    
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
    transactfull = Xmr_Transactions.query\
        .filter(Xmr_Transactions.user_id == current_user.id)\
        .order_by(Xmr_Transactions.id.desc())\
        .limit(50)

    transactions_list = Xmr_Transactions_Schema(many=True)
    return jsonify(transactions_list.dump(transactfull)), 200


@wallet_xmr.route('/receive', methods=['GET'])
@login_required
def xmr_receive():

    wallet = Xmr_Wallet.query.filter_by(user_id=current_user.id).first()

    qr = wallet.address1 + '.png'
    wallet_qr_code = os.path.join(UPLOADED_FILES_DEST_USER, str(current_user.uuid), 'qr', qr)
    

    return jsonify({"xmr_address": wallet.address1,
                    "xmr_qr_code": wallet_qr_code
                        }), 200


@wallet_xmr.route('/send', methods=['GET', 'POST'])
@login_required
@login_required
def xmr_send():

    user = Auth_User.query.filter_by(id=current_user.id).first()
    wallet = Xmr_Wallet.query.filter_by(user_id=current_user.id).first()
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


def xmr_send_coin_to_escrow(amount, comment, user_id):
    """
    # TO clearnet_webapp Wallet
    # this function will move the coin to clearnets wallet_btc from a user
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """
    passed_balance_check = xmr_check_balance(user_id=user_id, amount=amount)
    if passed_balance_check == 1:
      
            type_transaction = 4
            userwallet = Xmr_Wallet.query.filter(Xmr_Wallet.user_id==user_id).first()
            curbal = Decimal(userwallet.currentbalance)
            amounttomod = Decimal(amount)
            newbalance = Decimal(curbal) - Decimal(amounttomod)
            userwallet.currentbalance = newbalance
            db.session.add(userwallet)

            oid = int(comment)
            xmr_add_transaction(category=type_transaction,
                               amount=amount,
                               user_id=user_id,
                               comment='Sent Coin To Escrow',
                               orderid=oid,
                               balance=newbalance
                               )

    else:
        notification(
            type=34,
            username='',
            user_id=user_id,
            salenumber=comment,
            bitcoin=amount
        )
