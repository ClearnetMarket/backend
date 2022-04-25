from app import db, UPLOADED_FILES_DEST_USER
import datetime, os, qrcode
from decimal import Decimal
from app.common.functions import\
    floating_decimals,\
    userimagelocation
from app.notification import notification
from app.wallet_xmr.security import xmr_check_balance
from app.wallet_xmr.transaction import xmr_add_transaction
from app.classes.wallet_xmr import \
    Xmr_Wallet, \
    Xmr_WalletWork, \
    Xmr_WalletFee, \
    Xmr_Unconfirmed
from app.classes.auth import Auth_User

def xmr_create_wallet(user_id):
    """
    This creates the wallet and gives it a random payment id for
    deposites
    :param user_id:
    :return:
    """
    timestamp = datetime.datetime.utcnow()

    monero_newunconfirmed = Xmr_Unconfirmed(
        user_id=user_id,
        unconfirmed1=0,
        unconfirmed2=0,
        unconfirmed3=0,
        unconfirmed4=0,
        unconfirmed5=0,
        txid1='',
        txid2='',
        txid3='',
        txid4='',
        txid5='',
    )

    # creates wallet_btc in db
    monero_wallet_create = Xmr_Wallet(user_id=user_id,
                               currentbalance=0,
                               unconfirmed=0,
                               address1='',
                               address1status=1,
                               locked=0,
                               transactioncount=0,
                               )
    monero_wallet_work = Xmr_WalletWork(
        user_id=user_id,
        type=2,
        amount=0,
        sendto='',
        txnumber=0,
        created=timestamp,
    )
    
    db.session.add(monero_wallet_work)
    db.session.add(monero_newunconfirmed)
    db.session.add(monero_wallet_create)

    xmr_create_qr_code(user_id=user_id, address=monero_wallet_create.address1)


def xmr_create_qr_code(user_id, address):
    # find path of the user
    getuserlocation = userimagelocation(user_id=user_id)
    get_user = Auth_User.query.get(user_id)
    thepath = os.path.join(UPLOADED_FILES_DEST_USER,
     getuserlocation,
      str(get_user.uuid))
    path_plus_filename = thepath + '/' + address + '.png'
    qr = qrcode.QRCode(
                        version=None,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=5,
                        )
    qr.add_data(address)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path_plus_filename)


def xmr_wallet_status(user_id):
    """
    This will check if the wallet is normal,
    if not it creates a new wallet
    :param user_id:
    :return:
    """
    userwallet = db.session.query(Xmr_Wallet).filter_by(user_id=user_id).first()

    if userwallet:
        pass
    else:
        xmr_create_wallet(user_id=user_id)


def xmr_send_coin(user_id, sendto, amount):
    """
    # OFF SITE
    # withdrawl
    :param user_id:
    :param sendto:
    :param amount:
    :return:
    """
    getwallet = Xmr_WalletFee.query.get(1)
    walletfee = getwallet.amount
    a = xmr_check_balance(user_id=user_id, amount=amount)
    if a == 1:

        timestamp = datetime.utcnow()
        userswallet = db.session.query(Xmr_Wallet).filter_by(user_id=user_id).first()
        # turn sting to a decimal
        amountdecimal = Decimal(amount)
        # make decimal 8th power
        amounttomod = floating_decimals(amountdecimal, 12)
        # gets current balance
        curbalance = floating_decimals(userswallet.currentbalance, 12)
        # gets amount and fee
        amountandfee = floating_decimals(amounttomod + walletfee, 12)
        # subtracts amount and fee from current balance
        y = floating_decimals(curbalance - amountandfee, 12)
        # set balance as new amount
        userswallet.currentbalance = floating_decimals(y, 12)
        wallet = Xmr_WalletWork(
            user_id=user_id,
            type=1,
            amount=amount,
            sendto=sendto,
            created=timestamp,
        )
        db.session.add(wallet)
        db.session.add(userswallet)
    else:
        #TODO error notification
        pass




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
        userwallet = Xmr_Wallet.query.filter(
            Xmr_Wallet.user_id == user_id).first()
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

def xmr_send_coin_to_user(amount, comment, user_id):
    """
    # TO User
    # this function will move the coin from clearnets wallet xmr to a user
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 5
    oid = int(comment)

    userswallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    xmr_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment='Transaction',
                        orderid=oid,
                        balance=newbalance
                        )

