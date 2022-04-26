from app import db, UPLOADED_FILES_DEST_USER
import datetime
import os
import qrcode
from decimal import Decimal
from app.common.functions import\
    floating_decimals,\
    userimagelocation
from app.notification import notification
from app.wallet_xmr.security import xmr_check_balance
from app.wallet_xmr.wallet_xmr_transaction import xmr_add_transaction
from app.classes.wallet_xmr import \
    Xmr_Wallet, \
    Xmr_WalletWork, \
    Xmr_WalletFee, \
    Xmr_Unconfirmed
from app.classes.auth import Auth_User, Auth_UserFees
from app.classes.user_orders import User_Orders


def finalize_order_xmr(order_uuid, percent_to_customer, percent_to_vendor):
    pass
