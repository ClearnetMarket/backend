from app import db, ma


class Admin_ClearnetFee(db.Model):
    __tablename__ = 'admin_clearnet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    itempurchase = db.Column(db.DECIMAL(20, 2))


class Admin_ClearnetProfitBtc(db.Model):
    __tablename__ = 'admin_clearnet_profit_btc'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Admin_ClearnetProfitBCH(db.Model):
    __tablename__ = 'admin_clearnet_profit_bch'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Admin_ClearnetProfitXMR(db.Model):
    __tablename__ = 'admin_clearnet_profit_xmr'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 12))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 12))


class Admin_ClearnetFeeHoldings(db.Model):
    __tablename__ = 'admin_clearnet_fee_holdings'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Admin_ClearnetFeeHoldingsBCH(db.Model):
    __tablename__ = 'admin_clearnet_fee_holdings_bch'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))

class Admin_ClearnetFeeHoldingsXMR(db.Model):
    __tablename__ = 'admin_clearnet_fee_holdings_xmr'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 12))
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 12))


class Admin_ClearnetHoldingsBtc(db.Model):
    __tablename__ = 'admin_clearnet_holdings_btc'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class Admin_ClearnetHoldingsBCH(db.Model):
    __tablename__ = 'admin_clearnet_holdings_bch'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class Admin_Flagged(db.Model):
    __tablename__ = 'admin_flagged'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    vendorname = db.Column(db.VARCHAR(40))
    howmany = db.Column(db.INTEGER)
    typeitem = db.Column(db.INTEGER)
    listingid = db.Column(db.INTEGER)
    listingtitle = db.Column(db.INTEGER)
    flagged_user_id_1 = db.Column(db.INTEGER)
    flagged_user_id_2 = db.Column(db.INTEGER)
    flagged_user_id_3 = db.Column(db.INTEGER)
    flagged_user_id_4 = db.Column(db.INTEGER)
    flagged_user_id_5 = db.Column(db.INTEGER)


class Admin_Flagged_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin_Flagged

    id = ma.auto_field()
    user_id = ma.auto_field()
    vendorname = ma.auto_field()
    howmany = ma.auto_field()
    typeitem = ma.auto_field()
    listingid = ma.auto_field()
    listingtitle = ma.auto_field()
    flagged_user_id_1 = ma.auto_field()
    flagged_user_id_2 = ma.auto_field()
    flagged_user_id_3 = ma.auto_field()
    flagged_user_id_4 = ma.auto_field()
    flagged_user_id_5 = ma.auto_field()

