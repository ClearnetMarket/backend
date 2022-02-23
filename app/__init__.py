# coding=utf-8
from flask import Flask, jsonify, json
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.orm import sessionmaker
from werkzeug.routing import BaseConverter
import decimal
from config import ApplicationConfig
from flask_login import LoginManager

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


app.config.from_object(ApplicationConfig)
session = sessionmaker()

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


app.url_map.converters['regex'] = RegexConverter
app.json_encoder = DecimalEncoder
app.jinja_env.autoescape = True


# configuration
app.url_map.converters['regex'] = RegexConverter
UPLOADED_FILES_DEST_USER= ApplicationConfig.UPLOADED_FILES_DEST_USER
UPLOADED_FILES_DEST_ITEM = ApplicationConfig.UPLOADED_FILES_DEST_ITEM
UPLOADED_FILES_DEST =   ApplicationConfig.UPLOADED_FILES_DEST
UPLOADED_FILES_ALLOW =  ApplicationConfig.UPLOADED_FILES_ALLOW

app.config['UPLOADED_FILES_DEST_USER'] = ApplicationConfig.UPLOADED_FILES_DEST_USER
app.config['UPLOADED_FILES_DEST_ITEM'] = ApplicationConfig.UPLOADED_FILES_DEST_ITEM
app.config['UPLOADED_FILES_DEST'] = ApplicationConfig.UPLOADED_FILES_DEST
app.config['UPLOADED_FILES_ALLOW'] = ApplicationConfig.UPLOADED_FILES_ALLOW
app.config['MAX_CONTENT_LENGTH'] = ApplicationConfig.MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = ApplicationConfig.SECRET_KEY
app.config['DEBUG'] = ApplicationConfig.DEBUG

app.config['SESSION_TYPE'] = ApplicationConfig.SESSION_TYPE
app.config['SESSION_COOKIE_NAME'] = ApplicationConfig.SESSION_COOKIE_NAME
app.config['SESSION_COOKIE_SECURE'] = ApplicationConfig.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = ApplicationConfig.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = ApplicationConfig.SESSION_COOKIE_SAMESITE
app.config['SESSION_PERMANENT'] = ApplicationConfig.SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = ApplicationConfig.SESSION_USE_SIGNER
app.config['SESSION_REDIS'] = ApplicationConfig.SESSION_REDIS

# app.config['CORS_ORIGINS'] = ApplicationConfig.CORS_ORIGINS
# app.config['CORS_SEND_WILDCARD'] = ApplicationConfig.CORS_SEND_WILDCARD
# app.config['CORS_SUPPORT_CREDENTIALS'] = ApplicationConfig.CORS_SUPPORT_CREDENTIALS



session.configure(bind=ApplicationConfig.SQLALCHEMY_DATABASE_URI_0)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
server_session = Session(app)
mail = Mail(app)
ma = Marshmallow(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.anonymous_user = "Guest"


@login_manager.user_loader
def load_user(user_id):
    from app.classes.auth import Auth_User
    x = db.session.query(Auth_User).filter(Auth_User.id == int(user_id)).first()
    return x

CORS(app,
     headers=['Content-Type', 'Authorization'], 
     expose_headers='Authorization')

# bind a function after each request, even if an exception is encountered.
@app.teardown_request
def teardown_request(response_or_exc):
    db.session.remove()

@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    db.session.remove()

@app.errorhandler(500)
def internal_error500():
    return jsonify({"error": "Internal Error 500"}), 500

@app.errorhandler(502)
def internal_error502(error):
    return jsonify({"error": "Internal Error 502"}), 502

@app.errorhandler(404)
def internal_error404(error):
    return jsonify({"error": "Internal Error 400"}), 400

@app.errorhandler(401)
def internal_error404(error):
    return jsonify({"error": "Internal Error 401"}), 401

@app.errorhandler(400)
def internal_error400(error):
    return jsonify({"error": "Internal Error 400"}), 400

@app.errorhandler(413)
def to_large_file(error):
    return jsonify({"error": "File is too large.  Use a smaller image/file."}), 413

@app.errorhandler(403)
def internal_error403(error):
    return jsonify({"error": "Internal Error 403"}), 403

@app.errorhandler(405)
def internal_error(error):
    return jsonify({"error": "Internal Error 405"}), 405



# link locations
from .main import main as main_blueprint
app.register_blueprint(main_blueprint, url_prefix='/main')

# from .achievements import achievements as achievements_blueprint
# app.register_blueprint(achievements_blueprint, url_prefix='/achievements')
#
# from .admin import admin as admin_blueprint
# app.register_blueprint(admin_blueprint, url_prefix='/admin')
#
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from .orders import orders as orders_blueprint
app.register_blueprint(orders_blueprint, url_prefix='/orders')

# from .search import search as search_blueprint
# app.register_blueprint(search_blueprint, url_prefix='/search')
#
from .marketitem import marketitem as marketitem_blueprint
app.register_blueprint(marketitem_blueprint, url_prefix='/item')

from .customerservice import customerservice as customerservice_blueprint
app.register_blueprint(customerservice_blueprint, url_prefix='/customer-service')

from .category import category as category_blueprint
app.register_blueprint(category_blueprint, url_prefix='/category')

# from .userdata import userdata as userdata_blueprint
# app.register_blueprint(userdata_blueprint, url_prefix='/info')
#
# from .message import message as message_blueprint
# app.register_blueprint(message_blueprint, url_prefix='/message')
#
# from .profile import profile as profile_blueprint
# app.register_blueprint(profile_blueprint, url_prefix='/profile')
#
# from .affiliate import affiliate as affiliate_blueprint
# app.register_blueprint(affiliate_blueprint, url_prefix='/affiliate')
#
# from .promote import promote as promote_blueprint
# app.register_blueprint(promote_blueprint, url_prefix='/promote')
#
# from .checkout import checkout as checkout_blueprint
# app.register_blueprint(checkout_blueprint, url_prefix='/checkout')
#
# from .vendorcreate import vendorcreate as vendorcreate_blueprint
# app.register_blueprint(vendorcreate_blueprint, url_prefix='/vendor-create')
#
# from .vendorcreateitem import vendorcreateitem as vendorcreateitem_blueprint
# app.register_blueprint(vendorcreateitem_blueprint, url_prefix='/vendor-create-item')
#
# from .vendorverification import vendorverification as vendorverification_blueprint
# app.register_blueprint(vendorverification_blueprint, url_prefix='/vendor-verification')
#
# from .vendor import vendor as vendor_blueprint
# app.register_blueprint(vendor_blueprint, url_prefix='/vendor')
#

# bch wallet
from app.wallet_bch import wallet_bch as wallet_bch_blueprint
app.register_blueprint(wallet_bch_blueprint, url_prefix='/bch')
# btc
from app.wallet_btc import wallet_btc as wallet_btc_blueprint
app.register_blueprint(wallet_btc_blueprint, url_prefix='/btc')
# xmr
from app.wallet_xmr import wallet_xmr as wallet_xmr_blueprint
app.register_blueprint(wallet_xmr_blueprint, url_prefix='/xmr')

with app.app_context():
    db.create_all()
