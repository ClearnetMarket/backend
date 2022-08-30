from app import db, ma
from datetime import datetime


class Btc_Prices(db.Model):
    __tablename__ = 'btc_price'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))
    currency_id = db.Column(db.INTEGER)
    percent_change_twentyfour = db.Column(db.DECIMAL(50, 2))


class Btc_Prices_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Btc_Prices
    id = ma.auto_field()
    price = ma.auto_field()
    currency_id = ma.auto_field()
    percent_change_twentyfour = ma.auto_field()


class Btc_Wallet(db.Model):
    __tablename__ = 'btc_wallet'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    currentbalance = db.Column(db.DECIMAL(20, 8))
    address1 = db.Column(db.VARCHAR(500))
    address1status = db.Column(db.INTEGER)
    address2 = db.Column(db.VARCHAR(500))
    address2status = db.Column(db.INTEGER)
    address3 = db.Column(db.VARCHAR(500))
    address3status = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    transactioncount = db.Column(db.INTEGER)
    unconfirmed = db.Column(db.DECIMAL(20, 8))


class Btc_Wallet_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Btc_Wallet
    id = ma.auto_field()
    user_id = ma.auto_field()
    currentbalance = ma.auto_field()
    address1 = ma.auto_field()
    address1status = ma.auto_field()
    address2 = ma.auto_field()
    address2status = ma.auto_field()
    address3 = ma.auto_field()
    address3status = ma.auto_field()
    locked = ma.auto_field()
    transactioncount = ma.auto_field()
    unconfirmed = ma.auto_field()


class Btc_Unconfirmed(db.Model):
    __tablename__ = 'btc_unconfirmed'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    unconfirmed1 = db.Column(db.DECIMAL(20, 8))
    unconfirmed2 = db.Column(db.DECIMAL(20, 8))
    unconfirmed3 = db.Column(db.DECIMAL(20, 8))
    unconfirmed4 = db.Column(db.DECIMAL(20, 8))
    unconfirmed5 = db.Column(db.DECIMAL(20, 8))
    txid1 = db.Column(db.VARCHAR(500))
    txid2 = db.Column(db.VARCHAR(500))
    txid3 = db.Column(db.VARCHAR(500))
    txid4 = db.Column(db.VARCHAR(500))
    txid5 = db.Column(db.VARCHAR(500))


class Btc_Unconfirmed_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Btc_Unconfirmed
    id = ma.auto_field()
    user_id = ma.auto_field()
    unconfirmed1 = ma.auto_field()
    unconfirmed2 = ma.auto_field()
    unconfirmed3 = ma.auto_field()
    unconfirmed4 = ma.auto_field()
    unconfirmed5 = ma.auto_field()
    txid1 = ma.auto_field()
    txid2 = ma.auto_field()
    txid3 = ma.auto_field()
    txid4 = ma.auto_field()
    txid5 = ma.auto_field()


class Btc_WalletWork(db.Model):
    __tablename__ = 'btc_wallet_work'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 8))
    sendto = db.Column(db.VARCHAR(500))
    comment = db.Column(db.VARCHAR(500))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txtcomment = db.Column(db.VARCHAR(500))


class Btc_WalletAddresses(db.Model):
    __tablename__ = 'btc_wallet_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btcaddress = db.Column(db.VARCHAR(500))
    status = db.Column(db.INTEGER)


class Btc_TransactionsBtc(db.Model):
    __tablename__ = 'btc_transactions'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    category = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    txid = db.Column(db.VARCHAR(500))
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.VARCHAR(500))
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbtc = db.Column(db.VARCHAR(500))
    otheraccount = db.Column(db.INTEGER)
    address = db.Column(db.VARCHAR(500))
    fee = db.Column(db.DECIMAL(20, 8))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    balance = db.Column(db.DECIMAL(20, 8))
    item_uuid = db.Column(db.VARCHAR(140))
    confirmed = db.Column(db.INTEGER)
    confirmed_fee = db.Column(db.DECIMAL(20, 8))
    digital_currency = db.Column(db.INTEGER)
    order_uuid = db.Column(db.VARCHAR(140))
    

class Btc_TransactionsBtc_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Btc_TransactionsBtc
    id = ma.auto_field()
    user_id = ma.auto_field()
    category = ma.auto_field()
    confirmations = ma.auto_field()
    txid = ma.auto_field()
    amount = ma.auto_field()
    blockhash = ma.auto_field()
    timeoft = ma.auto_field()
    timerecieved = ma.auto_field()
    commentbtc = ma.auto_field()
    otheraccount = ma.auto_field()
    address = ma.auto_field()
    fee = ma.auto_field()
    created = ma.auto_field()
    balance = ma.auto_field()

    confirmed = ma.auto_field()
    confirmed_fee = ma.auto_field()
    digital_currency = ma.auto_field()


class Btc_WalletFee(db.Model):
    __tablename__ = 'btc_wallet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))


class Btc_TransOrphan(db.Model):
    __tablename__ = 'btc_transaction_orphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))
    btcaddress = db.Column(db.VARCHAR(500))
    txid = db.Column(db.VARCHAR(500))
