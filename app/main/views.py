from flask import jsonify, Response
from app import app
from flask_wtf.csrf import generate_csrf



@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    def disallow(string): return 'Disallow: {0}'.format(string)
    return Response("User-agent: *\n{0}\n".format("\n".join([
        disallow('/bin/*'),
        disallow('/wallet_btc'),
        disallow('/wallet_bch'),
        disallow('/wallet_xmr'),
        disallow('/admin'),

    ])))


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return jsonify({"Status": "Api is online"}), 200


@app.route('/csrf', methods=['GET'])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail: CSRF cookie set"})
    response.headers.set("X_CSRFToken", token)
    return response
