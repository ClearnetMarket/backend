from app import db, UPLOADED_FILES_DEST_USER
from app.common.functions import floating_decimals, userimagelocation
from app.notification import notification
from app.wallet_bch.wallet_bch_transaction import bch_add_transaction
from app.wallet_bch.wallet_bch_security import bch_check_balance
from decimal import Decimal
import datetime
import os
import qrcode
# models
from app.classes.auth import Auth_User, Auth_UserFees

from app.classes.wallet_bch import \
    Bch_Wallet, \
    Bch_WalletAddresses, \
    Bch_WalletFee, \
    Bch_WalletUnconfirmed, \
    Bch_WalletWork
from app.classes.user_orders import User_Orders



