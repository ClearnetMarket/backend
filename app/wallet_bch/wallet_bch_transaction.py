from app import db
from datetime import datetime
from app.classes.wallet_bch import Bch_WalletTransactions


def bch_add_transaction(category, amount, user_id, comment, shard, orderid, balance):
    """
    # this function will move the coin from holdings back to vendor.  This is for vendor verification
    :param category:
    :param amount:
    :param user_id:
    :param comment:
    :param shard:
    :param orderid:
    :param balance:
    :return:
    """
    try:

        now = datetime.utcnow()
        comment = str(comment)
        orderid = int(orderid)

        trans = Bch_WalletTransactions(
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
            shard=shard,
            orderid=orderid,
            balance=balance,
            digital_currency=3
        )
        db.session.add(trans)

    except Exception as e:
        print("transaction error")
        print(str(e))
