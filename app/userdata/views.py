from flask import request, session, jsonify
from flask_login import current_user
from app.userdata import userdata
from app import db
from app.common.decorators import login_required
# models
from app.classes.auth import Auth_User, Auth_User_Schema
from app.classes.models import Query_Country, Query_Currency
# end models

@userdata.route('/country-currency', methods=['GET'])
@login_required
def userdata_country_currency():
    """
    Returns all info about a user
    :return:
    """

    if request.method == 'GET':

        userdata = db.session\
            .query(Auth_User)\
            .filter(Auth_User.id == current_user.id)\
            .first()

        currency = Query_Currency.query.filter(userdata.currency==Query_Currency.code).first()
        currency_name = currency.symbol
        country = Query_Country.query.filter(userdata.country==Query_Country.numericcode).first()
        countryname =  country.name
        return jsonify(
            {'country': countryname,
            'currency': currency_name,}
        )


@userdata.route('/user-info', methods=['GET'])
@login_required
def userdata_home():
    """
    Returns all info about a user
    :return:
    """

    if request.method == 'GET':

        userdata = db.session\
            .query(Auth_User)\
            .filter(Auth_User.id == current_user.id)\
            .first()

        user_schema = Auth_User_Schema(many=True)
    
        return jsonify(user_schema.dump(userdata))


@userdata.route('/user-info-update', methods=['PUT'])
@login_required
def userdata_update():
    """
    Returns all info about a user
    :return:
    """

    if request.method == 'PUT':
        print(request.json)
        userdata = db.session\
            .query(Auth_User)\
            .filter(Auth_User.id == current_user.id)\
            .first()
        try:
            new_currency_id = request.json["currency"]['value']
        except:
            new_currency_id = None
        try:
            new_country_id = request.json["country"]['numericcode']
        except:
            new_country_id = None

        if new_currency_id is not None:
            userdata.currency = new_currency_id
        else:
            userdata.currency = userdata.currency
        if new_country_id is not None:
    
            userdata.country = new_country_id
        else:
             userdata.country = userdata.country
        if new_country_id or new_currency_id:
            db.session.add(userdata)
            db.session.commit()

            return jsonify({"status": 'success'})
        else:
            return jsonify({"status": 'error'})
    else:
        return jsonify({"status": 'error'})


