from flask import request, jsonify
from flask_login import current_user
from app.userdata import userdata
from app import db
from app.common.decorators import login_required
# models
from app.classes.auth import Auth_User, Auth_User_Schema, user_schema, users_schema
from app.classes.models import Query_Country, Query_Currency
from app.classes.checkout import Checkout_CheckoutShoppingCart
from app.classes.userdata import UserData_DefaultAddress
# end models


@userdata.route('/user-cart-count', methods=['GET'])
@login_required
def userdata_get_shopping_cart_count():
    """
    Returns how many items are in a users count
    :return:
    """
    if request.method == 'GET':
        shopping_cart_count = Checkout_CheckoutShoppingCart.query\
            .filter(Checkout_CheckoutShoppingCart.customer_id == current_user.id)\
            .count()
 
        return jsonify({'status': shopping_cart_count})


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

        currency = Query_Currency.query\
            .filter(userdata.currency == Query_Currency.value)\
            .first()
        currency_name = currency.symbol
        country = Query_Country.query\
            .filter(userdata.country == Query_Country.value)\
            .first()
        countryname = country.name
        return jsonify(
            {'country': countryname,
             'currency': currency_name, }
        )


@userdata.route('/user-info', methods=['GET'])
@login_required
def userdata_home():
    """
    Returns all info about a user
    :return:
    """
 
    if request.method == 'GET':
        userdata = Auth_User.query\
            .filter(Auth_User.id == current_user.id)\
            .first()
        user_schema = Auth_User_Schema()
        return jsonify(user_schema.dump(userdata))


@userdata.route('/user-info-update', methods=['PUT'])
@login_required
def userdata_update():
    """
    Returns all info about a user
    :return:
    """
    if request.method == 'PUT':
        userdata = Auth_User.query\
            .filter(Auth_User.id == current_user.id)\
            .first()
        try:
            new_currency_id = request.json["currency"]['value']
        except:
            new_currency_id = None
        try:
            new_country_id = request.json["country"]['value']
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


@userdata.route('/defaultaddress', methods=['PUT'])
@login_required
def userdata_update_address():
    """
    Returns all info about a user
    :return:
    """
    print(request.json)
    if request.method == 'PUT':
        user_address = UserData_DefaultAddress.query\
            .filter(UserData_DefaultAddress.uuid == current_user.uuid)\
            .first()
        address_name = request.json["address_name"]
        address = request.json["address"]
        country = request.json["country"]
        apt = request.json["apt"]
        city = request.json["city"]
        state_or_provence = request.json["stateorprovence"]
        zipcode = request.json["zip"]
        message = request.json["message"]
        user_address.address_name = address_name
        user_address.address = address
        user_address.country = int(country)
        user_address.apt = apt
        user_address.city = city
        user_address.state_or_provence = state_or_provence
        user_address.zip_code = zipcode
        user_address.msg = message

        db.session.add(user_address)
        db.session.commit()

        return jsonify({"status": 'success'})
       

@userdata.route('/getdefaultaddress', methods=['GET'])
@login_required
def userdata_get_address():
    """
    Returns all info about a user
    :return:
    """
    if request.method == 'GET':
        user_address = UserData_DefaultAddress.query\
            .filter(UserData_DefaultAddress.uuid == current_user.uuid)\
            .first()


        return jsonify({
            'address_name': user_address.address_name,
            'address': user_address.address,
            'apt': user_address.apt,
            'city': user_address.city,
            'country': user_address.country,
            'state_or_provence': user_address.state_or_provence,
            'zip': user_address.zip_code,
            'message': user_address.msg,
        })
