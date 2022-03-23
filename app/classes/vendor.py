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


class Vendor_VendorVerification(db.Model):
    __tablename__ = 'vendor_verification_level'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.INTEGER)
    vendor_level = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    amount = db.Column(db.DECIMAL(20, 8))

class Vendor_VendorVerification_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_VendorVerification
    id = ma.auto_field()
    vendor_id = ma.auto_field()
    vendor_level = ma.auto_field()
    timestamp = ma.auto_field()
    amount = ma.auto_field()

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


class Vendor_EbaySearchItem(db.Model):
    __tablename__ = 'vendor_ebay_item'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,  primary_key=True,autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    itemebayid = db.Column(db.BIGINT)
    itemtitle = db.Column(db.VARCHAR(500))
    itemprice = db.Column(db.DECIMAL(20, 4))
    itemquantity = db.Column(db.INTEGER)
    item_condition = db.Column(db.INTEGER)
    itemcategory = db.Column(db.VARCHAR(300))
    status = db.Column(db.INTEGER)
    errortext = db.Column(db.TEXT)


class Vendor_EbaySearchItem_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_EbaySearchItem


class Vendor_Notification(db.Model):
    __tablename__ = 'vendor_notification_alert'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    """
    Used to inform vendor of new issues on vendor bar
    """
    id = db.Column(db.Integer,  primary_key=True,autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER) 
    new_feedback = db.Column(db.INTEGER)
    new_disputes = db.Column(db.INTEGER)
    new_orders = db.Column(db.INTEGER)
    new_returns = db.Column(db.INTEGER)



class Vendor_Notification_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_EbaySearchItem
