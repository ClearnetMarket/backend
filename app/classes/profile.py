from app import db, ma


class Profile_Userreviews(db.Model):
    __tablename__ = 'profile_user_reviews'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.VARCHAR(40))
    order_id = db.Column(db.INTEGER)
    customer_id = db.Column(db.INTEGER)
    review = db.Column(db.TEXT)
    dateofreview = db.Column(db.TIMESTAMP())
    rating = db.Column(db.INTEGER)

class Profile_Userreviews_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_Userreviews
    id = ma.auto_field()
    customer = ma.auto_field()
    order_id = ma.auto_field()
    customer_id = ma.auto_field()
    review = ma.auto_field()
    dateofreview = ma.auto_field()
    rating = ma.auto_field()


class Profile_FeedbackComments(db.Model):
    __tablename__ = 'profile_feedback_comments'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP())
    author_id = db.Column(db.Integer)
    feedback_id = db.Column(db.Integer)
    sale_id = db.Column(db.Integer)

class Profile_FeedbackComments_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_FeedbackComments
    id = ma.auto_field()
    body = ma.auto_field()
    timestamp = ma.auto_field()
    author_id = ma.auto_field()
    feedback_id = ma.auto_field()
    sale_id = ma.auto_field()


class Profile_Exptable(db.Model):
    __tablename__ = 'profile_exp_table'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())

class Profile_Exptable_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_Exptable
    id = ma.auto_field()
    user_id = ma.auto_field()
    type = ma.auto_field()
    amount = ma.auto_field()
    timestamp = ma.auto_field()


class Profile_StatisticsVendor(db.Model):
    __tablename__ = 'profile_stats_vendor'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    username = db.Column(db.VARCHAR(40))
    vendorid = db.Column(db.INTEGER)
    totalsales = db.Column(db.INTEGER)
    totaltrades = db.Column(db.INTEGER)
    totalreviews = db.Column(db.INTEGER)
    startedselling = db.Column(db.TIMESTAMP())
    vendorrating = db.Column(db.DECIMAL(4, 2))
    avgitemrating = db.Column(db.DECIMAL(4, 2))
    diffpartners = db.Column(db.INTEGER)
    disputecount = db.Column(db.INTEGER)
    beenflagged = db.Column(db.INTEGER)
    totalbtcspent = db.Column(db.DECIMAL(20, 8))
    totalbtcrecieved = db.Column(db.DECIMAL(20, 8))
    totalbtccashspent = db.Column(db.DECIMAL(20, 8))
    totalbtccashrecieved = db.Column(db.DECIMAL(20, 8))
    totalxmrspent = db.Column(db.DECIMAL(20, 12))
    totalxmrrecieved = db.Column(db.DECIMAL(20, 12))
    totalusdmade = db.Column(db.DECIMAL(20, 2))

class Profile_StatisticsVendor_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_StatisticsVendor
    id = ma.auto_field()
    username = ma.auto_field()
    vendorid = ma.auto_field()
    totalsales = ma.auto_field()
    totaltrades = ma.auto_field()
    totalreviews = ma.auto_field()
    startedselling = ma.auto_field()
    vendorrating = ma.auto_field()
    avgitemrating = ma.auto_field()
    diffpartners = ma.auto_field()
    disputecount = ma.auto_field()
    beenflagged = ma.auto_field()
    totalbtcspent = ma.auto_field()
    totalbtcrecieved = ma.auto_field()
    totalbtccashspent = ma.auto_field()
    totalbtccashrecieved = ma.auto_field()
    totalxmrspent = ma.auto_field()
    totalxmrrecieved = ma.auto_field()
    totalusdmade = ma.auto_field()

class Profile_StatisticsUser(db.Model):
    __tablename__ = 'profile_stats_user'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    username = db.Column(db.VARCHAR(40))
    user_id = db.Column(db.INTEGER)
    totalitemsbought = db.Column(db.INTEGER)
    totaltrades = db.Column(db.INTEGER)
    totalreviews = db.Column(db.INTEGER)
    startedbuying = db.Column(db.TIMESTAMP())
    diffpartners = db.Column(db.INTEGER)
    totalachievements = db.Column(db.INTEGER)
    userrating = db.Column(db.DECIMAL(4, 2))
    disputecount = db.Column(db.INTEGER)
    itemsflagged = db.Column(db.INTEGER)
    totalbtcspent = db.Column(db.DECIMAL(20, 8))
    totalbtcrecieved = db.Column(db.DECIMAL(20, 8))
    totalbtccashspent = db.Column(db.DECIMAL(20, 8))
    totalbtccashrecieved = db.Column(db.DECIMAL(20, 8))
    totalxmrspent = db.Column(db.DECIMAL(20, 12))
    totalxmrrecieved = db.Column(db.DECIMAL(20, 12))
    totalusdspent = db.Column(db.DECIMAL(20, 2))

class Profile_StatisticsUser_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile_StatisticsUser

    id = ma.auto_field()
    username = ma.auto_field()
    user_id = ma.auto_field()
    totalitemsbought = ma.auto_field()
    totaltrades = ma.auto_field()
    totalreviews = ma.auto_field()
    startedbuying = ma.auto_field()
    diffpartners = ma.auto_field()
    totalachievements = ma.auto_field()
    userrating = ma.auto_field()
    disputecount = ma.auto_field()
    itemsflagged = ma.auto_field()
    totalbtcspent = ma.auto_field()
    totalbtcrecieved = ma.auto_field()
    totalbtccashspent = ma.auto_field()
    totalbtccashrecieved = ma.auto_field()
    totalxmrspent = ma.auto_field()
    totalxmrrecieved = ma.auto_field()
    totalusdspent = ma.auto_field()
