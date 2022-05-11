from app import db, UPLOADED_FILES_DEST_USER
from app.common.functions import\
    floating_decimals, \
    userimagelocation

from app.wallet_btc.wallet_btc_addtransaction import btc_add_transaction
from app.wallet_btc.wallet_btc_security import btc_check_balance
from decimal import Decimal
import datetime
import os
import qrcode
# models
from app.classes.auth import Auth_User, Auth_UserFees
from app.classes.user_orders import User_Orders

from app.classes.wallet_btc import \
    Btc_Unconfirmed, \
    Btc_Wallet, \
    Btc_WalletAddresses, \
    Btc_WalletFee, \
    Btc_WalletWork
# end models


def btc_create_wallet(user_id):
    """
    This function creates the wallet for bitcoin and puts  first address there
    if wallet exists it adds an address to wallet
    :param user_id:
    :return:
    """

    userswallet = db.session\
                    .query(Btc_Wallet)\
                    .filter(Btc_Wallet.user_id == user_id)\
                    .first()

    if userswallet:
        # find a new clean address
        getnewaddress = db.session\
            .query(Btc_WalletAddresses) \
            .filter(Btc_WalletAddresses.status == 0) \
            .first()

        # sets users wallet with this
        userswallet.address1 = getnewaddress.btcaddress
        userswallet.address1status = 1
        db.session.add(userswallet)

        # update address in listing as used
        getnewaddress.user_id = user_id
        db.session.add(getnewaddress)
        db.session.flush()

        # create qr code
        btc_create_qr_code(user_id=user_id, address=userswallet.address1)
    else:

        # create a new wallet
        btc_walletcreate = Btc_Wallet(user_id=user_id,
                                      currentbalance=0,
                                      unconfirmed=0,
                                      address1='',
                                      address1status=0,
                                      address2='',
                                      address2status=0,
                                      address3='',
                                      address3status=0,
                                      locked=0,
                                      transactioncount=0
                                      )
        db.session.add(btc_walletcreate)

        btc_newunconfirmed = Btc_Unconfirmed(
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
        db.session.add(btc_newunconfirmed)
        db.session.flush()

        getnewaddress = db.session \
            .query(Btc_WalletAddresses) \
            .filter(Btc_WalletAddresses.status == 0) \
            .first()

        btc_walletcreate.address1 = getnewaddress.btcaddress
        btc_walletcreate.address1status = 1
        db.session.add(btc_walletcreate)

        getnewaddress.user_id = user_id
        getnewaddress.status = 1
        db.session.add(getnewaddress)

        # create qr code
        btc_create_qr_code(user_id=user_id, address=btc_walletcreate.address1)


def btc_create_qr_code(user_id, address):
    # find path of the user
    getuserlocation = userimagelocation(user_id=user_id)
    get_user = Auth_User.query.get(user_id)
    thepath = os.path.join(UPLOADED_FILES_DEST_USER,
                           getuserlocation, str(get_user.uuid))
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


def btc_wallet_status(user_id):
    """
    This function checks status opf the wallet
    :param user_id:
    :return:
    """
    userswallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(Btc_Wallet.user_id == user_id)\
        .first()
    getuser = db.session\
        .query(Auth_User)\
        .filter(Auth_User.id == user_id)\
        .first()
    if userswallet:
        try:
            if userswallet.address1status == 0 \
                    and userswallet.address2status == 0 \
                    and userswallet.address2status == 0:
                btc_create_wallet(user_id=user_id)

        except Exception as e:
            userswallet.address1 = ''
            userswallet.address1status = 0
            userswallet.address2 = ''
            userswallet.address2status = 0
            userswallet.address3 = ''
            userswallet.address3status = 0

            db.session.add(userswallet)
    else:
        # creates wallet_btc in db
        btc_create_wallet(user_id=getuser.id)


def btc_send_coin(user_id, sendto, amount, comment):
    """
    Add work order to send off site
    :param user_id:
    :param sendto:
    :param amount:
    :param comment:
    :return:
    """
    timestamp = datetime.datetime.utcnow()
    getwallet = db.session\
        .query(Btc_WalletFee)\
        .filter_by(id=1)\
        .first()
    walletfee = getwallet.btc
    a = btc_check_balance(user_id=user_id, amount=amount)
    if a == 1:

        strcomment = str(comment)
        type_transaction = 2
        userswallet = db.session\
            .query(Btc_Wallet)\
            .filter_by(user_id=user_id)\
            .first()

        wallet = Btc_WalletWork(
            user_id=user_id,
            type=type_transaction,
            amount=amount,
            sendto=sendto,
            comment=0,
            created=timestamp,
            txtcomment=strcomment,
        )

        db.session.add(wallet)

        # turn sting to a decimal
        amountdecimal = Decimal(amount)
        # make decimal 8th power
        amounttomod = floating_decimals(amountdecimal, 8)
        # gets current balance
        curbalance = floating_decimals(userswallet.currentbalance, 8)
        # gets amount and fee
        amountandfee = floating_decimals(amounttomod + walletfee, 8)
        # subtracts amount and fee from current balance
        y = floating_decimals(curbalance - amountandfee, 8)
        # set balance as new amount
        userswallet.currentbalance = floating_decimals(y, 8)

        db.session.add(userswallet)

    else:
        pass


##INNER FUNCTIONS
def btc_send_coin_to_user_as_admin(amount, comment, user_id, order_uuid):
    """
    #to User
    # this function will move the coin from clearnets wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 9

    userswallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment=comment,
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )


def btc_take_coin_to_user_as_admin(amount, user_id, order_uuid):
    """
    # TO User
    # this function will move the coin from clearnets wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 10

    userswallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) - Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment='Admin moved money',
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )


def btc_send_coin_to_escrow(amount, user_id, order_uuid):
    """
    # TO clearnet_webapp Wallet
    # this function will move the coin to clearnets wallet_btc from a user
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """
    a = btc_check_balance(user_id=user_id, amount=amount)
    if a == 1:
        try:
            type_transaction = 4
            userswallet = db.session\
                .query(Btc_Wallet)\
                .filter_by(user_id=user_id)\
                .first()
            curbal = Decimal(userswallet.currentbalance)
            amounttomod = Decimal(amount)
            newbalance = Decimal(curbal) - Decimal(amounttomod)
            userswallet.currentbalance = newbalance
            db.session.add(userswallet)

            btc_add_transaction(category=type_transaction,
                                amount=amount,
                                user_id=user_id,
                                comment='Sent Coin To Escrow',
                                balance=newbalance,
                                order_uuid=order_uuid,
                                item_uuid=None
                                )

        except Exception as e:
            pass
    else:
        pass


def btc_send_coin_to_user(amount, user_id, order_uuid):
    """
    #TO User
    ##this function will move the coin from clearnets wallet btc to a user
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 5

    userswallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment='Transaction',
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )


def finalize_order_btc(order_uuid):
    """
    Finalizes btc order
    """
    
    get_order = db.session \
        .query(User_Orders) \
        .filter(User_Orders.uuid == order_uuid) \
        .first()

    # get total
    total_amount_from_sale = get_order.price_total_btc
   
    # get vendor fee
    get_vendor_fee = Auth_UserFees.query\
        .filter(Auth_UserFees.user_id == get_order.vendor_id)\
        .first()
    vendor_fee_percent = get_vendor_fee.vendorfee
    fee_for_freeport = (Decimal(total_amount_from_sale) * Decimal(vendor_fee_percent))/100
    fee_for_freeport_exact = floating_decimals(fee_for_freeport, 8)

    amount_for_vendor = total_amount_from_sale - fee_for_freeport
    amount_for_vendor_exact = floating_decimals(amount_for_vendor, 8)

    print("finalizing order btc")
    print(total_amount_from_sale)
    print(fee_for_freeport_exact)
    print(amount_for_vendor_exact)
    # send fee to freeport
    btc_send_coin_to_user(amount=fee_for_freeport_exact,
                          user_id=1,
                          order_uuid=get_order.uuid)

    # send coin to vendor
    btc_send_coin_to_user(amount=amount_for_vendor_exact,
                          user_id=get_order.vendor_id,
                          order_uuid=get_order.uuid)


def btc_refund_rejected_user(amount, user_id, order_uuid):
    """
    # TO User
    # this function will move the coin from clearnets wallet bch to a user
    # when a vendor rejects an order uses this function
    :param amount:
    :param comment:
    :param user_id:
    :return:
    """

    type_transaction = 9

    userswallet = db.session\
        .query(Btc_Wallet)\
        .filter_by(user_id=user_id)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_add_transaction(category=type_transaction,
                        amount=amount,
                        user_id=user_id,
                        comment='Order Rejected',
                        balance=newbalance,
                        order_uuid=order_uuid,
                        item_uuid=None
                        )
