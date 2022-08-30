from app import db, ma
from uuid import uuid4


def get_uuid_item():
    return uuid4().hex


class Vendor_NotShipping(db.Model):
    __tablename__ = 'vendor_not_shipping_country'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    code = db.Column(db.INTEGER)
    name = db.Column(db.VARCHAR(40))


class Vendor_NotShipping_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_NotShipping
    id = ma.auto_field()
    code = ma.auto_field()
    name = ma.auto_field()


class Vendor_Duration(db.Model):
    __tablename__ = 'vendor_duration_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    time = db.Column(db.VARCHAR(140))
    displaytime = db.Column(db.VARCHAR(140))


class Vendor_Duration_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Duration
    id = ma.auto_field()
    time = ma.auto_field()
    displaytime = ma.auto_field()


class Vendor_Notification(db.Model):
    __tablename__ = 'vendor_notification_alert'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    """
    Used to inform vendor of new issues on vendor bar
    """
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER) 
    new_feedback = db.Column(db.INTEGER)
    new_disputes = db.Column(db.INTEGER)
    new_orders = db.Column(db.INTEGER)
    new_returns = db.Column(db.INTEGER)


class Vendor_Notification_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Notification


class Vendor_ExactAddress(db.Model):
    __tablename__ = 'vendor_exact_address'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.VARCHAR(40))

    city = db.Column(db.VARCHAR(1000))
    country = db.Column(db.INTEGER)
    state_or_provence = db.Column(db.VARCHAR(1000))
    zip_code = db.Column(db.VARCHAR(200))


class Vendor_ExactAddress_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_ExactAddress
