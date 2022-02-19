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


class UserData_Feedback(db.Model):
    __tablename__ = 'userdata_feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customername = db.Column(db.VARCHAR(40))
    sale_id = db.Column(db.INTEGER)
    vendorname = db.Column(db.VARCHAR(40))
    vendorid = db.Column(db.INTEGER)
    comment = db.Column(db.TEXT)
    item_rating = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    vendorrating = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    addedtodb = db.Column(db.INTEGER)
    author_id = db.Column(db.INTEGER)

class UserData_Feedback_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserData_Feedback
    id = ma.auto_field()
    customername = ma.auto_field()
    sale_id = ma.auto_field()
    vendorname = ma.auto_field()
    vendorid = ma.auto_field()
    comment = ma.auto_field()
    item_rating = ma.auto_field()
    item_id = ma.auto_field()
    type = ma.auto_field()
    vendorrating = ma.auto_field()
    timestamp = ma.auto_field()
    addedtodb = ma.auto_field()
    author_id = ma.auto_field()

