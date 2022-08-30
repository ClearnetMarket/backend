from app import db, ma


class UserData_History(db.Model):
    __tablename__ = 'userdata_userhistory'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    recent_cat_1 = db.Column(db.INTEGER)
    recent_cat_1_date = db.Column(db.TIMESTAMP())
    recent_cat_2 = db.Column(db.INTEGER)
    recent_cat_2_date = db.Column(db.TIMESTAMP())
    recent_cat_3 = db.Column(db.INTEGER)
    recent_cat_3_date = db.Column(db.TIMESTAMP())
    recent_cat_4 = db.Column(db.INTEGER)
    recent_cat_4_date = db.Column(db.TIMESTAMP())
    recent_cat_5 = db.Column(db.INTEGER)
    recent_cat_5_date = db.Column(db.TIMESTAMP())


class UserData_History_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData_History


class UserData_DefaultAddress(db.Model):
    __tablename__ = 'userdata_defaultaddress'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.VARCHAR(40))
    address_name = db.Column(db.VARCHAR(1000))
    address = db.Column(db.VARCHAR(1000))
    apt = db.Column(db.VARCHAR(1000))
    city = db.Column(db.VARCHAR(1000))
    country = db.Column(db.INTEGER)
    state_or_provence = db.Column(db.VARCHAR(1000))
    zip_code = db.Column(db.VARCHAR(200))
    msg = db.Column(db.VARCHAR(2500))


class UserData_DefaultAddress_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData_DefaultAddress
