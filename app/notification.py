# 1 = sale
# 2 = message
# 3 = Feedback
# 4 = dispute
# 5 = return
# 6 = bitcoin credit
# 7 = Cancelled Order
# 8 = succesful return
# 9- sold out of item
# 55 - return vendor added return label

# 10 = Digital Trade
# 11 = Cancelled Digital Trade
# 12 = Success Digital Trade
# 13 = Dispute Digital Trade

# 15 = BTC Trade
# 16 = Cancelled BTC Trade
# 17 = Success BTC Trade
# 18 = Dispute BTC Trade

# 30 btc address error
# 31 too little btc to send offsite


#WALLET ERRORS
# Bitcoin BTC
# errors
# 100 =  too litte or too much at withdrawl
# 102 = wallet error
# 103 = btc address error
# 104 New Incomming Deposit
# 105 Bitcoin Sent

# Bitcoin Cash BCH
# errors
# 200 =  too litte or too much at withdrawl
# 202 = wallet error
# 203 = btc address error
# 204 New Incomming Deposit
# 205 Bitcoin Sent

# Monero XMR
# errors
# 300 =  too litte or too much at withdrawl
# 302 = wallet error
# 303 = btc address error
# 304 New Incomming Deposit
# 305 Bitcoin Sent



def notification(type, username, user_id, salenumber, bitcoin, bitcoincash, monero):
    from app import db
    from app.classes.message import Message_Notifications

    from datetime import datetime
    now = datetime.utcnow()
    addnotice = Message_Notifications(
        type=type,
        username=username,
        user_id=user_id,
        salenumber=salenumber,
        bitcoin=bitcoin,
        bitcoincash=bitcoincash,
        monero=monero,
        read=1,
        timestamp=now,
    )
    db.session.add(addnotice)
