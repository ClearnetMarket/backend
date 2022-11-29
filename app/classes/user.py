from app import db
from datetime import datetime


class Auth_User(db.Model):
    __tablename__ = 'auth_users'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    uuid = db.Column(db.String(32))
    api_key = db.Column(db.TEXT)
    username = db.Column(db.VARCHAR(40))
    display_name = db.Column(db.VARCHAR(140))
    password_hash = db.Column(db.TEXT)
    member_since = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    email = db.Column(db.VARCHAR(350))
    wallet_pin = db.Column(db.VARCHAR(5))
    profileimage = db.Column(db.VARCHAR(100))
    bio = db.Column(db.TEXT)
    country = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    vendor_account = db.Column(db.INTEGER)
    selling_from = db.Column(db.VARCHAR(100))
    last_seen = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    admin = db.Column(db.INTEGER)
    admin_role = db.Column(db.INTEGER)
    dispute = db.Column(db.INTEGER)
    fails = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    vacation = db.Column(db.INTEGER)
    shopping_timer = db.Column(db.TIMESTAMP())
    shard = db.Column(db.INTEGER)
    usernode = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    passwordpinallowed = db.Column(db.INTEGER)

    def __init__(self,
                 username,
                 password_hash,
                 member_since,
                 email,
                 wallet_pin,
                 profileimage,
                 display_name,
                 bio,
                 api_key,
                 country,
                 currency,
                 vendor_account,
                 selling_from,
                 last_seen,
                 admin,
                 admin_role,
                 dispute,
                 fails,
                 locked,
                 vacation,
                 shopping_timer,
                 lasttraded_timer,
                 shard,
                 usernode,
                 confirmed,
                 passwordpinallowed,
                 ):
        self.username = username
        self.password_hash = password_hash
        self.member_since = member_since
        self.email = email
        self.wallet_pin = wallet_pin
        self.profileimage = profileimage
        self.display_name = display_name
        self.bio = bio
        self.api_key = api_key
        self.country = country
        self.currency = currency
        self.vendor_account = vendor_account
        self.selling_from = selling_from
        self.last_seen = last_seen
        self.admin = admin
        self.admin_role = admin_role
        self.dispute = dispute
        self.fails = fails
        self.locked = locked
        self.vacation = vacation
        self.shopping_timer = shopping_timer
        self.lasttraded_timer = lasttraded_timer
        self.shard = shard
        self.usernode = usernode

        self.confirmed = confirmed
        self.passwordpinallowed = passwordpinallowed

