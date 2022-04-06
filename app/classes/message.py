from app import db, ma
from datetime import datetime


class Message_Notifications(db.Model):
    __tablename__ = 'message_notifications'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    type = db.Column(db.INTEGER)
    username = db.Column(db.VARCHAR(40))
    user_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    salenumber = db.Column(db.INTEGER)
    bitcoin = db.Column(db.DECIMAL(20, 8))
    bitcoincash = db.Column(db.DECIMAL(20, 8))
    monero = db.Column(db.DECIMAL(20, 12))
    read = db.Column(db.INTEGER)


class Message_Chat(db.Model):
    __tablename__ = 'message_chat'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    orderid = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    author = db.Column(db.VARCHAR(40))
    author_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    body = db.Column(db.TEXT)
    admin = db.Column(db.INTEGER)
    issueid = db.Column(db.INTEGER)

class Message_Chat_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message_Chat
    id = ma.auto_field()
    orderid = ma.auto_field()
    type = ma.auto_field()
    author = ma.auto_field()
    author_id = ma.auto_field()
    timestamp = ma.auto_field()
    body = ma.auto_field()
    admin = ma.auto_field()
    issueid = ma.auto_field()

class Message_Post(db.Model):
    __tablename__ = 'message_post'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP(),
                          index=True,
                          default=datetime.utcnow())

class Message_Post_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message_Post
    id = ma.auto_field()
    timestamp =ma.auto_field()


class Message_PostUser(db.Model):
    __tablename__ = 'message_post_user'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)

    # type of message
    official = db.Column(db.Integer)
    dispute = db.Column(db.Integer)
    usermsg = db.Column(db.Integer)

    # info in msg
    body = db.Column(db.TEXT)
    subject = db.Column(db.Integer)

    timestamp = db.Column(db.TIMESTAMP(),
                          index=True,
                          default=datetime.utcnow())
    author_id = db.Column(db.Integer)

    itemid = db.Column(db.Integer)
    unread = db.Column(db.Integer)
    modid = db.Column(db.Integer)
    postid = db.Column(db.Integer)

    user_id = db.Column(db.Integer)
    username = db.Column(db.VARCHAR(40))

class Message_PostUser_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message_PostUser
    id = ma.auto_field()
    # type of message
    official = ma.auto_field()
    dispute = ma.auto_field()
    usermsg = ma.auto_field()

    # info in msg
    body = ma.auto_field()
    subject = ma.auto_field()

    timestamp = ma.auto_field()
    author_id = ma.auto_field()

    itemid = ma.auto_field()
    unread = ma.auto_field()
    modid = ma.auto_field()
    postid = ma.auto_field()

    user_id = ma.auto_field()
    username = ma.auto_field()


class Message_Comment(db.Model):
    __tablename__ = 'message_comment'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP(),
                          index=True,
                          default=datetime.utcnow())
    author_id = db.Column(db.Integer)
    author = db.Column(db.VARCHAR(40))
    post_id = db.Column(db.Integer)
    modid = db.Column(db.Integer)

class Message_Comment_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message_Comment
    id = ma.auto_field()
    body = ma.auto_field()
    timestamp = ma.auto_field()
    author_id = ma.auto_field()
    author = ma.auto_field()
    post_id = ma.auto_field()
    modid = ma.auto_field()


