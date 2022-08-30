from app import db, ma
from datetime import datetime


class Xmr_Prices(db.Model):
    __tablename__ = 'xmr_price'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))
    currency_id = db.Column(db.INTEGER)
    percent_change_twentyfour = db.Column(db.DECIMAL(50, 2))


class Xmr_Prices_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Xmr_Prices
    id = ma.auto_field()
    price = ma.auto_field()
    currency_id = ma.auto_field()
    percent_change_twentyfour = ma.auto_field()


class Xmr_Wallet(db.Model):
    __tablename__ = 'xmr_wallet'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    currentbalance = db.Column(db.DECIMAL(20, 12))
    address1 = db.Column(db.VARCHAR(500))
    address1status = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    transactioncount = db.Column(db.INTEGER)
    unconfirmed = db.Column(db.DECIMAL(20, 12))


class Xmr_Wallet_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Xmr_Wallet
    id = ma.auto_field()
    user_id = ma.auto_field()
    currentbalance = ma.auto_field()
    address1 = ma.auto_field()
    address1status = ma.auto_field()
    locked = ma.auto_field()
    transactioncount = ma.auto_field()
    unconfirmed = ma.auto_field()


class Xmr_Transactions(db.Model):
    __tablename__ = 'xmr_transactions'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    txid = db.Column(db.VARCHAR(500))
    amount = db.Column(db.DECIMAL(20, 12))
    balance = db.Column(db.DECIMAL(20, 12))
    block = db.Column(db.INTEGER)
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    address = db.Column(db.VARCHAR(500))
    note = db.Column(db.VARCHAR(500))
    fee = db.Column(db.DECIMAL(20, 12))
    item_uuid = db.Column(db.VARCHAR(140))
    digital_currency = db.Column(db.INTEGER)
    order_uuid = db.Column(db.VARCHAR(140))


class Xmr_Transactions_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Xmr_Transactions
    id = ma.auto_field()
    category = ma.auto_field()
    user_id = ma.auto_field()
    confirmations = ma.auto_field()
    confirmed = ma.auto_field()
    txid = ma.auto_field()
    amount = ma.auto_field()
    balance = ma.auto_field()
    block = ma.auto_field()
    created = ma.auto_field()
    address = ma.auto_field()
    note = ma.auto_field()
    fee = ma.auto_field()
   
    digital_currency = ma.auto_field()


class Xmr_TransOrphan(db.Model):
    __tablename__ = 'xmr_wallet_transaction_orphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xmr = db.Column(db.DECIMAL(20, 12))
    txid = db.Column(db.VARCHAR(500))


class Xmr_Unconfirmed(db.Model):
    __tablename__ = 'xmr_wallet_unconfirmed'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    unconfirmed1 = db.Column(db.DECIMAL(20, 12))
    unconfirmed2 = db.Column(db.DECIMAL(20, 12))
    unconfirmed3 = db.Column(db.DECIMAL(20, 12))
    unconfirmed4 = db.Column(db.DECIMAL(20, 12))
    unconfirmed5 = db.Column(db.DECIMAL(20, 12))
    txid1 = db.Column(db.VARCHAR(500))
    txid2 = db.Column(db.VARCHAR(500))
    txid3 = db.Column(db.VARCHAR(500))
    txid4 = db.Column(db.VARCHAR(500))
    txid5 = db.Column(db.VARCHAR(500))


class Xmr_Unconfirmed_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Xmr_Unconfirmed
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


class Xmr_WalletWork(db.Model):
    __tablename__ = 'xmr_wallet_work'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 12))
    sendto = db.Column(db.VARCHAR(500))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txnumber = db.Column(db.INTEGER)


class Xmr_WalletFee(db.Model):
    __tablename__ = 'xmr_wallet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.DECIMAL(20, 12))


class Xmr_WalletAddresses(db.Model):
    __tablename__ = 'xmr_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.VARCHAR(500))
    status = db.Column(db.INTEGER)


class Xmr_BlockHeight(db.Model):
    __tablename__ = 'xmr_blockheight'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blockheight = db.Column(db.INTEGER)
