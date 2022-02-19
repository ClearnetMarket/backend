from app import db
from app.classes.wallet_bch import  Bch_Wallet
from decimal import Decimal


def bch_check_balance(user_id, amount):
    # The money requested during the trade
    userwallet = db.session\
        .query(Bch_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    theusersbalance = userwallet.currentbalance
    theamountrequested = Decimal(amount)

    if theusersbalance >= theamountrequested:
        return 1
    else:
        return 0
