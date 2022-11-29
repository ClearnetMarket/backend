from app import db, ma
from datetime import datetime


class Bch_Wallet(db.Model):
    __tablename__ = 'bch_wallet'
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


class Bch_Wallet_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bch_Wallet

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


class Bch_Prices(db.Model):
    __tablename__ = 'bch_price'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))
    currency_id = db.Column(db.INTEGER)
    percent_change_twentyfour = db.Column(db.DECIMAL(50, 2))


class Bch_Prices_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bch_Prices

    id = ma.auto_field()
    price = ma.auto_field()
    currency_id = ma.auto_field()
    percent_change_twentyfour = ma.auto_field()


class Bch_WalletTransferOrphan(db.Model):
    __tablename__ = 'bch_transaction_orphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))
    bchaddress = db.Column(db.VARCHAR(500))
    txid = db.Column(db.VARCHAR(500))


class Bch_WalletUnconfirmed(db.Model):
    __tablename__ = 'bch_wallet_unconfirmed_transaction'
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


class Bch_WalletUnconfirmed_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bch_WalletUnconfirmed

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


class Bch_WalletWork(db.Model):
    __tablename__ = 'bch_wallet_work'
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


class Bch_WalletAddresses(db.Model):
    __tablename__ = 'bch_wallet_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bchaddress = db.Column(db.VARCHAR(500))
    status = db.Column(db.INTEGER)


class Bch_WalletFee(db.Model):
    __tablename__ = 'bch_wallet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))


class Bch_WalletTransactions(db.Model):
    __tablename__ = 'bch_transactions'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    txid = db.Column(db.VARCHAR(500))
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.VARCHAR(500))
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbch = db.Column(db.VARCHAR(500))
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


class Bch_WalletTransactions_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bch_WalletTransactions

    id = ma.auto_field()
    category = ma.auto_field()
    user_id = ma.auto_field()
    confirmations = ma.auto_field()
    txid = ma.auto_field()
    amount = ma.auto_field()
    blockhash = ma.auto_field()
    timeoft = ma.auto_field()
    timerecieved = ma.auto_field()
    commentbch = ma.auto_field()
    otheraccount = ma.auto_field()
    address = ma.auto_field()
    fee = ma.auto_field()
    created = ma.auto_field()
    balance = ma.auto_field()

    confirmed = ma.auto_field()
    confirmed_fee = ma.auto_field()
    digital_currency = ma.auto_field()