

from app import db, ma

class Notification_Notifications(db.Model):
    __tablename__ = 'notification_notifications'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.VARCHAR(40))
    user_uuid = db.Column(db.VARCHAR(40))
    timestamp = db.Column(db.TIMESTAMP())
    message = db.Column(db.VARCHAR(400))
    read = db.Column(db.INTEGER)

class Notification_Notifications_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification_Notifications

