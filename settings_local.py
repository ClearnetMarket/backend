
import redis
from dotenv import load_dotenv
import os

load_dotenv()

class ApplicationConfig:
    """
    Basic Configuration for a generic User
    """
    CURRENT_SETTINGS = 'LOCAL'
    # databases info
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PW = 'postgres'
    POSTGRES_SERVER = 'database:5432'
    POSTGRES_DBNAME00 = 'clearnet'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}/{}".format(POSTGRES_USERNAME,
                                                                           POSTGRES_PW,
                                                                           POSTGRES_SERVER,
                                                                           POSTGRES_DBNAME00
                                                                           )
    SQLALCHEMY_BINDS = {'clearnet': SQLALCHEMY_DATABASE_URI}
    # sqlalchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAP_HTTP_EXCEPTIONS = True
    PROPAGATE_EXCEPTIONS = True

    DEBUG = True

    UPLOADED_FILES_DEST_ITEM = '/data/item'
    UPLOADED_FILES_DEST_USER = '/data/user'


    # file uploads
    UPLOADED_FILES_ALLOW = ['png', 'jpeg', 'jpg', 'png', 'gif']
    MAX_CONTENT_LENGTH = 5 * 2500 * 2500
    ALLOWED_EXTENSIONS = ['png', 'jpeg', 'jpg', 'png', 'gif']

    # secret keys
    SECRET_KEY = "youwillneverguessthiskeycia"

    # sessions
    SESSION_COOKIE_NAME = "CSRFTOKEN"
    SESSION_PROTECTION = "strong"
    SESSION_COOKIE_SAMESITE = "Strict"
    # NEED SSL for this to work or be True!!!
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    
    # redis config
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url("redis://redis:6379")

    # CORS
    ORIGIN_URL = "http://localhost:8080"
    CORS_SEND_WILDCARD = False
    CORS_SUPPORT_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = None
    CORS_ALLOW_HEADERS = "*"
    CORS_ORIGIN_WHITELIST = ['http://localhost',
                             'http://localhost:5000',
                             'localhost:8080']



    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEFAULT_SENDER = '"donotreply@freeport.cash" <donotreply@freeport.cash>'
    MAIL_DEBUG = True
    TESTING = False
    MAIL_SUPPRESS_SEND = False

