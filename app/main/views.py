from flask import  jsonify, Response
from app import app
from flask_wtf.csrf import generate_csrf





@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
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


@app.route('/', methods=['GET'])
def index():
    return jsonify({"ping": "pong"})


@app.route('/csrf', methods=['GET'])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail: CSRF cookie set"})
    response.headers.set("X_CSRFToken", token)
    return response