
from app import db, ma
from datetime import datetime


class Message_Post(db.Model):
    __tablename__ = 'message_post'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    user_one_uuid = db.Column(db.VARCHAR(40))
    user_two_uuid = db.Column(db.VARCHAR(40))
    mod_uuid = db.Column(db.VARCHAR(40))
    timestamp = db.Column(db.TIMESTAMP(),
                          index=True,
                          default=datetime.utcnow())


class Message_Chat(db.Model):
    __tablename__ = 'message_chat'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    timestamp = db.Column(db.TIMESTAMP())
    order_uuid = db.Column(db.VARCHAR(40))
    item_uuid = db.Column(db.VARCHAR(40))
    user_one = db.Column(db.VARCHAR(140))
    user_one_uuid = db.Column(db.VARCHAR(40))
    user_two = db.Column(db.VARCHAR(140))
    user_two_uuid = db.Column(db.VARCHAR(40))
    mod_name = db.Column(db.VARCHAR(140))
    mod_uuid = db.Column(db.VARCHAR(40))
    body = db.Column(db.TEXT)
    admin = db.Column(db.INTEGER)
    post_id = db.Column(db.Integer)
    read = db.Column(db.Integer)
    who_commented = db.Column(db.Integer)


class Message_Chat_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message_Chat

msg_schema = Message_Chat_Schema()
msgs_schema = Message_Chat_Schema(many=True)
