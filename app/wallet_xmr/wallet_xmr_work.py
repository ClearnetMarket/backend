from app import db, UPLOADED_FILES_DEST_USER
import datetime
import os
import qrcode
from decimal import Decimal
from app.common.functions import\
    floating_decimals,\
    userimagelocation

from app.wallet_xmr.security import xmr_check_balance
from app.wallet_xmr.wallet_xmr_transaction import xmr_add_transaction
from app.classes.wallet_xmr import \
    Xmr_Wallet, \
    Xmr_WalletWork, \
    Xmr_WalletFee, \
    Xmr_Unconfirmed
from app.classes.auth import Auth_User, Auth_UserFees
from app.classes.user_orders import User_Orders


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
    get_user = db.session\
        .query(Auth_User)\
        .get(user_id)
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
    userwallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=user_id)\
        .first()

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
    getwallet = db.session\
        .query(Xmr_WalletFee)\
        .get(1)
    walletfee = getwallet.amount
    a = xmr_check_balance(user_id=user_id, amount=amount)
    if a == 1:

        timestamp = datetime.datetime.utcnow()
        userswallet = db.session\
            .query(Xmr_Wallet)\
            .filter_by(user_id=user_id)\
            .first()
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
        pass


def xmr_send_coin_to_user_as_admin(amount, comment, user_id):
    """
    #to User
    # this function will move the coin from clearnets wallet_xmr to a user as an admin
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """
    type_transaction = 9
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
                        comment=comment,
                        balance=newbalance,
                        order_uuid=None,
                        item_uuid=None
                        )


def xmr_take_coin_to_user_as_admin(amount, comment, user_id):
    """
    # TO User
    # this function will move the coin from clearnets wallet_xmr to a user as an admin
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 10
    userswallet = db.session\
        .query(Xmr_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) - Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    xmr_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment=comment,
                        balance=newbalance,
                        order_uuid=None,
                        item_uuid=None
                        )


def xmr_send_coin_to_escrow(amount,  user_id, order_uuid):
    """
    # TO clearnet_webapp Wallet
    # this function will move the coin to clearnets wallet_btc from a user
    :param amount:
    :param user_id:
    :param order_uuid:
    :return:
    """
    passed_balance_check = xmr_check_balance(user_id=user_id, amount=amount)
    if passed_balance_check == 1:

        type_transaction = 4
        userwallet =db.session\
            .query(Xmr_Wallet)\
            .filter(Xmr_Wallet.user_id == user_id)\
            .first()
        curbal = Decimal(userwallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) - Decimal(amounttomod)
        userwallet.currentbalance = newbalance
        db.session.add(userwallet)
        xmr_add_transaction(category=type_transaction,
                            amount=amount,
                            user_id=user_id,
                            comment='Sent Coin To Escrow',
                            balance=newbalance,
                            order_uuid=order_uuid,
                            item_uuid=None
                            )
    else:
        pass


def xmr_send_coin_to_user(amount, user_id, order_uuid):
    """
    # TO User
    # this function will move the coin from clearnets wallet xmr to a user
    :param amount:
    :param user_id:
    :param order_uuid:
    :return:
    """

    type_transaction = 5

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
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )


def finalize_order_xmr(order_uuid):
    """
    Finalizes xmr order
    """
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.uuid == order_uuid) \
        .first()

    # get total
    total_amount_from_sale = get_order.price_total_xmr

    # get vendor fee
    get_vendor_fee = db.session\
        .query(Auth_UserFees)\
        .filter(Auth_UserFees.user_id == get_order.vendor_id)\
        .first()
    # percent of vendor fee from database
    vendor_fee_percent = get_vendor_fee.vendorfee

    # get fee for website
    fee_for_freeport = (Decimal(total_amount_from_sale) * Decimal(vendor_fee_percent))/100
    fee_for_freeport_exact = floating_decimals(fee_for_freeport, 12)
    print(fee_for_freeport_exact)
    # get amount to vendor
    amount_for_vendor = total_amount_from_sale - fee_for_freeport
    amount_for_vendor_exact = floating_decimals(amount_for_vendor, 12)
    print(amount_for_vendor_exact)
    # send fee to freeport
    xmr_send_coin_to_user(amount=fee_for_freeport_exact,
                          user_id=1,
                          order_uuid=get_order.uuid)

    # send coin to vendor
    xmr_send_coin_to_user(amount=amount_for_vendor_exact,
                          user_id=get_order.vendor_id,
                          order_uuid=get_order.uuid)


def xmr_refund_rejected_user(amount, user_id, order_uuid):
    """
    # TO User
    # this function will move the coin from clearnets wallet bch to a user
    # when a vendor rejects an order uses this function
    :param amount:
    :param order_uuid:
    :param user_id:
    :return:
    """

    type_transaction = 9

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
                        comment='Order Rejected',
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )
