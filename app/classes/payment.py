from app import db, ma
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # gets payment user uuid
    user_uuid = db.Column(db.VARCHAR(40))
    # what type of coin user sending
    payment_coin = db.Column(db.INTEGER)
    # status is not yet sent, confirming, etc
    status = db.Column(db.INTEGER)
    # when payment was created
    created = db.Column(db.TIMESTAMP())
    # when payment was confirmed
    completed = db.Column(db.TIMESTAMP())
    # how much payment freeport is expecting
    expected_amount_btc = db.Column(db.DECIMAL(20, 8))
    expected_amount_bch = db.Column(db.DECIMAL(20, 8))
    expected_amount_xmr = db.Column(db.DECIMAL(20, 12))
    # what address to use to send coin
    address_expecting_coin = db.Column(db.TIMESTAMP())
    # txid on blockchain
    txid = db.Column(db.VARCHAR(500))
    



class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment

    id = ma.auto_field()
    user_uuid = ma.auto_field()
    payment_coin = ma.auto_field()
    status = ma.auto_field()
    created = ma.auto_field()
    completed = ma.auto_field()
    expected_amount_btc = ma.auto_field()
    expected_amount_bch = ma.auto_field()
    expected_amount_xmr = ma.auto_field()
    address_expecting_coin = ma.auto_field()
    txid = ma.auto_field()
