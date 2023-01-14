from app import db, ma


class Feedback_Feedback(db.Model):
    __tablename__ = 'feedback_feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    timestamp = db.Column(db.TIMESTAMP())
    order_uuid = db.Column(db.VARCHAR(40))
    item_uuid = db.Column(db.VARCHAR(40))
    customer_name = db.Column(db.VARCHAR(100))
    customer_uuid = db.Column(db.VARCHAR(40))
    vendor_name = db.Column(db.VARCHAR(40))
    vendor_uuid = db.Column(db.VARCHAR(40))
    vendor_comment = db.Column(db.TEXT)
    type_of_feedback = db.Column(db.INTEGER)
    item_rating = db.Column(db.DECIMAL(4, 2))
    vendor_rating = db.Column(db.DECIMAL(4, 2))
    customer_rating = db.Column(db.DECIMAL(4, 2))
    author_uuid = db.Column(db.VARCHAR(40))
    review_of_vendor = db.Column(db.TEXT)
    review_of_customer = db.Column(db.TEXT)
    title_of_item = db.Column(db.VARCHAR(500))
    
class Feedback_Feedback_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback_Feedback
