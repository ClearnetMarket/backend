from app import db
from datetime import datetime
from app.classes.wallet_bch import Bch_WalletTransactions


def bch_add_transaction(category, amount, user_id, comment, balance, order_uuid, item_uuid):
    """
    # this function will move the coin from holdings back to vendor.  This is for vendor verification
    :param category:
    :param amount:
    :param user_id:
    :param comment:
    :param order_uuid:
    :param item_uuid:
    :param balance:
    :return:
    """
    try:

        now = datetime.utcnow()
        comment = str(comment)

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
            commentbch=comment,
            amount=amount,
            balance=balance,
            digital_currency=2,
            order_uuid=order_uuid,
            item_uuid=item_uuid,
        )
        db.session.add(trans)

    except Exception as e:
        
        print(str(e))
