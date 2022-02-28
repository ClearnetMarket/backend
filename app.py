# coding=utf-8
from app import app


PORT = 5000
HOST = '0.0.0.0'
use_reloader = True
DEBUG = True

app.run(host=HOST,
        port=PORT, 
        threaded=True,
        debug=True,
        use_reloader=use_reloader)
