from flask import jsonify, Response
from app import app
from flask_wtf.csrf import generate_csrf


@app.after_request
def add_headers(response):
    # has to have http + ip + port or wont work
    # ip of where requests come from ie vue app
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5010'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, authorization, Access-Control-Allow-Headers,' \
                                                       ' Origin,Accept, X-Requested-With, Content-Type,' \
                                                       ' Access-Control-Request-Method, Access-Control-Request-Headers'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'

    return response


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
    return jsonify({"ping": "pong"}), 200


@app.route('/csrf', methods=['GET'])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail: CSRF cookie set"})
    response.headers.set("X_CSRFToken", token)
    return response
