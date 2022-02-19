from app import db
from datetime import datetime
from app.classes.wallet_xmr import Xmr_Transactions

# this function will move the coin from holdings back to vendor.  This is for vendor verification
def xmr_add_transaction(category, amount, user_id, orderid, balance, senderid, comment):
    now = datetime.utcnow()
    orderid = int(orderid)

    trans = Xmr_Transactions(
        category=category,
        user_id=user_id,
        senderid=senderid,
        confirmations=0,
        txid='',
        amount=amount,
        balance=balance,
        block=0,
        created=now,
        address='',
        note=comment,
        fee=0,
        orderid=orderid,
        digital_currency=3,
        confirmed=0,
    )
    db.session.add(trans)


