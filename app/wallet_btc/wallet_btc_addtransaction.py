from app import db
from datetime import datetime
from app.classes.wallet_btc import Btc_TransactionsBtc

# type 1: wallet withdrawl
# type 2: send bitcoin offsite
# type 4: send coin to escrow
# type 5: send coin to user
# type 6: send coin to agoras profit
# type 7: send coin to holdings
# type 8: send coin from holdings


def btc_add_transaction(category, amount, user_id, comment, balance, order_uuid, item_uuid):
    """

    """
    try:
        now = datetime.utcnow()
        comment = str(comment)

        trans = Btc_TransactionsBtc(
            category=category,
            user_id=user_id,
            confirmations=0,
            confirmed=1,
            txid='',
            blockhash='',
            timeoft=0,
            timerecieved=0,
            otheraccount=0,
            address='',
            fee=0,
            created=now,
            commentbtc=comment,
            amount=amount,
            balance=balance,
            digital_currency=1,
            confirmed_fee=0,
            order_uuid=order_uuid,
            item_uuid=item_uuid
        )
        db.session.add(trans)

    except:
        pass
