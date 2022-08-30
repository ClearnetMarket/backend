from app import db, ma


class Profile_StatisticsVendor(db.Model):
    __tablename__ = 'profile_stats_vendor'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_name = db.Column(db.VARCHAR(140))
    vendor_uuid = db.Column(db.VARCHAR(140))
    total_sales = db.Column(db.INTEGER)
    total_reviews = db.Column(db.INTEGER)
    started_selling = db.Column(db.TIMESTAMP())
    vendor_rating = db.Column(db.DECIMAL(4, 2))
    avg_item_rating = db.Column(db.DECIMAL(4, 2))
    diff_partners = db.Column(db.INTEGER)
    dispute_count = db.Column(db.INTEGER)
    been_flagged = db.Column(db.INTEGER)
    total_btc_spent = db.Column(db.DECIMAL(20, 8))
    total_btc_recieved = db.Column(db.DECIMAL(20, 8))
    total_bch_spent = db.Column(db.DECIMAL(20, 8))
    total_bch_recieved = db.Column(db.DECIMAL(20, 8))
    total_xmr_spent = db.Column(db.DECIMAL(20, 12))
    total_xmr_recieved = db.Column(db.DECIMAL(20, 12))
    total_usd_made = db.Column(db.DECIMAL(20, 2))


class Profile_StatisticsVendor_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_StatisticsVendor


class Profile_StatisticsUser(db.Model):
    __tablename__ = 'profile_stats_user'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_name = db.Column(db.VARCHAR(140))
    user_uuid = db.Column(db.VARCHAR(140))
    total_items_bought = db.Column(db.INTEGER)
    total_trades = db.Column(db.INTEGER)
    total_reviews = db.Column(db.INTEGER)
    started_buying = db.Column(db.TIMESTAMP())
    diff_partners = db.Column(db.INTEGER)
    total_achievements = db.Column(db.INTEGER)
    user_rating = db.Column(db.DECIMAL(4, 2))
    dispute_count = db.Column(db.INTEGER)
    items_flagged = db.Column(db.INTEGER)
    total_btc_spent = db.Column(db.DECIMAL(20, 8))
    total_btc_recieved = db.Column(db.DECIMAL(20, 8))
    total_bch_spent = db.Column(db.DECIMAL(20, 8))
    total_bch_recieved = db.Column(db.DECIMAL(20, 8))
    total_xmr_spent = db.Column(db.DECIMAL(20, 12))
    total_xmr_recieved = db.Column(db.DECIMAL(20, 12))
    total_usd_spent = db.Column(db.DECIMAL(20, 2))


class Profile_StatisticsUser_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_StatisticsUser
