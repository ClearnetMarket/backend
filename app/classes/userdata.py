from app import db, ma


class UserData_History(db.Model):
    __tablename__ = 'userdata_userhistory'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    recentcat1 = db.Column(db.INTEGER)
    recentcat1date = db.Column(db.TIMESTAMP())
    recentcat2 = db.Column(db.INTEGER)
    recentcat2date = db.Column(db.TIMESTAMP())
    recentcat3 = db.Column(db.INTEGER)
    recentcat3date = db.Column(db.TIMESTAMP())
    recentcat4 = db.Column(db.INTEGER)
    recentcat4date = db.Column(db.TIMESTAMP())
    recentcat5 = db.Column(db.INTEGER)
    recentcat5date = db.Column(db.TIMESTAMP())

class UserData_History_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData_History
    id = ma.auto_field()
    user_id = ma.auto_field()
    recentcat1 = ma.auto_field()
    recentcat1date = ma.auto_field()
    recentcat2 = ma.auto_field()
    recentcat2date = ma.auto_field()
    recentcat3 = ma.auto_field()
    recentcat3date = ma.auto_field()
    recentcat4 = ma.auto_field()
    recentcat4date = ma.auto_field()
    recentcat5 = ma.auto_field()
    recentcat5date = ma.auto_field()


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
