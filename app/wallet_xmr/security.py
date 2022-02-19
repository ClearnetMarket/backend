from app import db
from decimal import Decimal
from app.classes.wallet_xmr import Xmr_Wallet

def xmr_check_balance(user_id, amount):
    # The money requested during the trade
    userwallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    x = userwallet.currentbalance
    y = Decimal(amount)

    if x >= y:
        return 1
    else:
        return 0
