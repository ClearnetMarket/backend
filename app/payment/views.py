from flask import request, jsonify
from flask_login import login_required, current_user
import datetime
from app import db
from app.payment import payment
from app.classes.user import Auth_User
from app.classes.payment import Payment
from app.classes.checkout import Checkout_ShoppingCartTotal
from app.classes.wallet_bch import Bch_Wallet
from app.classes.wallet_btc import Btc_Wallet
from app.classes.wallet_xmr import Xmr_Wallet
    
# payment status
# 0 = created from order
# 1 = Awaiting Deposit
# 2 = confirming
# 3 = payment confirmed and done

"""
##TODO Figure how to do multiple currencies at once?
"""
@payment.route('/create/<int:payment_currency>', methods=['POST'])
@login_required
def payment_create(payment_currency):
    now = datetime.utcnow()
    
    get_user = db.session\
        .query(Auth_User)\
        .filter(Auth_User.id == current_user.id)\
        .first()
    
    cart_total = db.session \
        .query(Checkout_ShoppingCartTotal) \
        .filter_by(customer_id=current_user.id) \
        .first()
        
    user_xmr_wallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    user_btc_wallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(Btc_Wallet.user_id == current_user.id)\
        .first()
    user_bch_wallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    
    create_new_payment = Payment(
        user_uuid=get_user.uuid,
        payment_coin=payment_currency,
        status = 0,
        created = now,
        completed = None,
        expected_amount_btc = None,
        expected_amount_bch = None,
        expected_amount_xmr = None,
        address_expecting_coin = "",
        txid = None
    )
    db.session.add(create_new_payment)
    db.session.create()

@payment.route('/', methods=['GET'])
@login_required
def payment_main():
    pass


@payment.route('/create/<int:payment_currency>', methods=['DELETE'])
@login_required
def payment_delete(payment_currency):
    pass
