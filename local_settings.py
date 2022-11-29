from passwords import \
    mailuser, \
    mailpass
import os
import redis



class ApplicationConfig:
    """
    Basic Configuration for a generic User
    """
    CURRENT_SETTINGS = 'LOCAL'
    # databases info
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PW = 'password'
    POSTGRES_SERVER = 'database:5432'
    POSTGRES_DBNAME00 = 'clearnet'
    SQLALCHEMY_DATABASE_URI_0 = "postgresql+psycopg2://{}:{}@{}/{}".format(POSTGRES_USERNAME,
                                                                           POSTGRES_PW,
                                                                           POSTGRES_SERVER,
                                                                           POSTGRES_DBNAME00
                                                                           )
    SQLALCHEMY_BINDS = {'clearnet': SQLALCHEMY_DATABASE_URI_0}

    DEBUG = True

    UPLOADED_FILES_DEST = '/data/items'
    UPLOADED_FILES_DEST_ITEM = '/data/item'
    UPLOADED_FILES_DEST_USER = '/data/user'

    proc_name = 'runProduction:app'
    workers = 4
    
    worker_rlimit_nofile = 20000
    worker_connections = 1024

    # file uploads
    UPLOADED_FILES_ALLOW = ['png', 'jpeg', 'jpg', 'png', 'gif']
    MAX_CONTENT_LENGTH = 5 * 2500 * 2500
    ALLOWED_EXTENSIONS = ['png', 'jpeg', 'jpg', 'png', 'gif']

    # secret keys
    SECRET_KEY = "youwillneverguessthiskeycia"

    # sessions
    ORIGIN_URL = "localhost"
    SESSION_COOKIE_NAME = "freeport_session"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # redis config
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url("redis://redis:6379")

    # CORS
    CORS_ORIGINS = "*"
    CORS_SEND_WILDCARD = False
    CORS_SUPPORT_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = None
    CORS_ALLOW_HEADERS = "*"

    # sqlalchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAP_HTTP_EXCEPTIONS = True
    PROPAGATE_EXCEPTIONS = True

    ALLOWED_HOSTS = [
        '127.0.0.1',
        '0.0.0.0',
        'localhost'
    ]

    CORS_ORIGIN_WHITELIST = [
                'http://127.0.0.1:5173',
                'http://0.0.0.0:5173'
                'http://localhost:5173'

    ]


