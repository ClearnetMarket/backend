from flask import url_for, request, session, jsonify, Response
from app.main import main
from app import db, app, UPLOADED_FILES_DEST
from datetime import datetime
import os
from decimal import Decimal
from sqlalchemy.sql.expression import func

# models
from app.classes.category import Category_Categories, Category_Categories_Schema



@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    def Disallow(string): return 'Disallow: {0}'.format(string)
    return Response("User-agent: *\n{0}\n".format("\n".join([
        Disallow('/bin/*'),
        Disallow('/wallet_btc'),
        Disallow('/wallet_bch'),
        Disallow('/wallet_xmr'),
        Disallow('/admin'),
    ])))


@app.route('/')
def index():
    return jsonify({"hello": "world"})