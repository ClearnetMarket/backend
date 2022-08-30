from app import db, ma


class Service_ShippingSecret(db.Model):
    __tablename__ = 'service_shipping_secret'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    txtmsg = db.Column(db.TEXT)
    orderid = db.Column(db.INTEGER)


class Service_ShippingSecret_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_ShippingSecret
    id = ma.auto_field()
    user_id = ma.auto_field()
    timestamp = ma.auto_field()
    txtmsg = ma.auto_field()
    orderid = ma.auto_field()


class Service_Returns(db.Model):
    __tablename__ = 'service_returns'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    name = db.Column(db.VARCHAR(500))
    street = db.Column(db.VARCHAR(500))
    city = db.Column(db.VARCHAR(300))
    state = db.Column(db.VARCHAR(140))
    country = db.Column(db.VARCHAR(400))
    zip = db.Column(db.VARCHAR(140))
    message = db.Column(db.TEXT)


class Service_Returns_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Returns
    id = ma.auto_field()
    ordernumber = ma.auto_field()
    name = ma.auto_field()
    street = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    country = ma.auto_field()
    zip = ma.auto_field()
    message = ma.auto_field()


class Service_DefaultReturns(db.Model):
    __tablename__ = 'servicedefault_return_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(500))
    street =  db.Column(db.VARCHAR(400))
    city = db.Column(db.VARCHAR(300))
    state = db.Column(db.VARCHAR(140))
    country = db.Column(db.VARCHAR(400))
    zip = db.Column(db.VARCHAR(140))
    message = db.Column(db.TEXT)
    username = db.Column(db.VARCHAR(40))
    user_id = db.Column(db.INTEGER)


class Service_DefaultReturns_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_DefaultReturns
    id = ma.auto_field()
    name = ma.auto_field()
    street =  ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    country = ma.auto_field()
    zip = ma.auto_field()
    message = ma.auto_field()
    username = ma.auto_field()
    user_id = ma.auto_field()


class Service_ReturnsTracking(db.Model):
    __tablename__ = 'service_return_tracking'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    customername = db.Column(db.VARCHAR(40))
    customerid = db.Column(db.INTEGER)
    vendorname = db.Column(db.VARCHAR(40))
    vendorid = db.Column(db.INTEGER)
    carrier = db.Column(db.INTEGER)
    trackingnumber = db.Column(db.VARCHAR(500))
    othercarrier = db.Column(db.VARCHAR(500))


class Service_ReturnsTracking_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_ReturnsTracking
    id = ma.auto_field()
    ordernumber = ma.auto_field()
    timestamp = ma.auto_field()
    customername = ma.auto_field()
    customerid = ma.auto_field()
    vendorname = ma.auto_field()
    vendorid = ma.auto_field()
    carrier = ma.auto_field()
    trackingnumber = ma.auto_field()
    othercarrier = ma.auto_field()


class Service_Tracking(db.Model):
    __tablename__ = 'service_tracking'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.INTEGER)
    tracking1 = db.Column(db.VARCHAR(500))
    carrier1 = db.Column(db.VARCHAR(500))
    othercarrier1 = db.Column(db.VARCHAR(500))
    tracking2 = db.Column(db.VARCHAR(500))
    carrier2 = db.Column(db.VARCHAR(500))
    othercarrier2 = db.Column(db.VARCHAR(500))
    tracking3 = db.Column(db.VARCHAR(500))
    carrier3 = db.Column(db.VARCHAR(500))
    othercarrier3 = db.Column(db.VARCHAR(500))


class Service_Tracking_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tracking
    id = ma.auto_field()
    sale_id = ma.auto_field()
    tracking1 = ma.auto_field()
    carrier1 = ma.auto_field()
    othercarrier1 = ma.auto_field()
    tracking2 = ma.auto_field()
    carrier2 = ma.auto_field()
    othercarrier2 = ma.auto_field()
    tracking3 = ma.auto_field()
    carrier3 = ma.auto_field()
    othercarrier3 = ma.auto_field()


class Service_UpdateLog(db.Model):
    __tablename__ = 'service_update_log'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.INTEGER)
    body = db.Column(db.INTEGER)
    dateofupdate = db.Column(db.TIMESTAMP())


class Service_UpdateLog_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_UpdateLog
    id = ma.auto_field()
    header = ma.auto_field()
    body = ma.auto_field()
    dateofupdate = ma.auto_field()


class Service_CustomerServiceItem(db.Model):
    __tablename__ = 'service_customer_issue_selection'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue = db.Column(db.VARCHAR(400))


class Service_CustomerServiceItem_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_CustomerServiceItem
    id = ma.auto_field()
    issue = ma.auto_field()


class Service_WebsiteFeedback(db.Model):
    __tablename__ = 'service_website_feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(40))
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    comment = db.Column(db.TEXT)
    email = db.Column(db.VARCHAR(350))
    timestamp = db.Column(db.TIMESTAMP())


class Service_WebsiteFeedback_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_WebsiteFeedback
    id = ma.auto_field()
    username = ma.auto_field()
    user_id = ma.auto_field()
    type = ma.auto_field()
    comment = ma.auto_field()
    email = ma.auto_field()
    timestamp = ma.auto_field()


class Service_Issue(db.Model):
    __tablename__ = 'service_issues'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.VARCHAR(140))
    author_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    admin = db.Column(db.INTEGER)
    status = db.Column(db.INTEGER)


class Service_Issue_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Issue
    id = ma.auto_field()
    author = ma.auto_field()
    author_id = ma.auto_field()
    timestamp = ma.auto_field()
    admin = ma.auto_field()
    status = ma.auto_field()