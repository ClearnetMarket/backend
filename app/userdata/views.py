from flask import request, jsonify
from flask_login import current_user
from app.userdata import userdata
from app import db
from app.common.decorators import login_required
# models
from app.classes.auth import Auth_User, Auth_User_Schema
from app.classes.models import Query_Country, Query_Currency
from app.classes.checkout import Checkout_CheckoutShoppingCart
from app.classes.userdata import UserData_DefaultAddress
from app.classes.feedback import Feedback_Feedback, Feedback_Feedback_Schema
from app.classes.profile import Profile_StatisticsUser, Profile_StatisticsUser_Schema
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


@userdata.route('/user-info/<string:user_uuid>', methods=['GET'])
def userdata_home(user_uuid):
    """
    Returns all info about a user
    :return:
    """
 
    if request.method == 'GET':
        print(user_uuid)
        userdata = Auth_User.query\
            .filter(Auth_User.uuid == user_uuid)\
            .first()
        print(userdata.username)
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

    if request.method == 'PUT':
        user_address = UserData_DefaultAddress.query\
            .filter(UserData_DefaultAddress.uuid == current_user.uuid)\
            .first()
        if "address_name" in request.json:
            address_name = request.json["address_name"]
        else:
            address_name = None
        if "address" in request.json:
            address = request.json["address"]
        else:
            address = None
        if "country" in request.json:
            country = request.json["country"]
        else:
            country = None
        if "apt" in request.json:
            apt = request.json["apt"]
        else:
            apt = None
        if "city" in request.json:
            city = request.json["city"]
        else:
            city = None
        if "stateorprovence" in request.json:
            state_or_provence = request.json["stateorprovence"]
        else:
            state_or_provence = None
        if "zip" in request.json:
            zipcode = request.json["zip"]
        else:
            zipcode = None
        if "message" in request.json:
            message = request.json["message"]
        else:
            message = None

        if user_address:
            user_address.country = int(country)
            user_address.address = address
            user_address.address_name = address_name
            user_address.apt = apt
            user_address.city = city
            user_address.state_or_provence = state_or_provence
            user_address.zip_code = zipcode
            user_address.msg = message
            db.session.add(user_address)
        else:
            new_address = UserData_DefaultAddress(
                uuid=current_user.uuid,
                address_name = address_name,
                apt=apt,
                city=city,
                state_or_provence=state_or_provence,
                country=current_user.country,
                zip_code=zipcode,
                msg=message,
            )
            db.session.add(new_address)
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
        if user_address:
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
        else:
            return jsonify(({'status': "Address not found" }))

@userdata.route('/user-feedback/<string:user_uuid>', methods=['GET'])
def userdata_get_all_feedback(user_uuid):
    """
    Grabs all feedback from a user
    :return:
    """
    if request.method == 'GET':
        user_feedback = Feedback_Feedback.query\
            .filter_by(customer_uuid=user_uuid)\
            .filter_by(type_of_feedback=2)\
            .order_by(Feedback_Feedback.timestamp.desc())\
            .limit(100)
            
        user_schema = Feedback_Feedback_Schema(many=True)
        return jsonify(user_schema.dump(user_feedback))


@userdata.route('/user-feedback-stats/<string:user_uuid>', methods=['GET'])
def userdata_get_stats_feedback(user_uuid):
    """
    Grabs stats of feedback
    :return:
    """
    if request.method == 'GET':
        user_feedback = Feedback_Feedback.query\
            .filter_by(customer_uuid=user_uuid)\
            .filter_by(type_of_feedback=2)\
            .count()
        if user_feedback == 0:
            return jsonify({"total_feedback": 0,
                            'feedback_one': 0,
                            'feedback_two': 0,
                            'feedback_three': 0,
                            'feedback_four': 0,
                            'feedback_five': 0,
                            'feedback_six': 0,
                            'feedback_seven': 0,
                            'feedback_eight': 0,
                            'feedback_nine': 0,
                            'feedback_ten': 0,
                            })
        else:

            user_feedback_one = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=1)\
                .count()
            
            if user_feedback_one != 0:
                user_feedback_one_percent = (
                    (int(user_feedback_one) / int(user_feedback))*100)
            else:
                user_feedback_one_percent = 0
            user_feedback_two = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=2)\
                .count()
            if user_feedback_two != 0:
                user_feedback_two_percent = (
                    (int(user_feedback_two) / int(user_feedback))*100)
            else:
                user_feedback_two_percent = 0

            user_feedback_three = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=3)\
                .count()
            if user_feedback_three != 0:
                user_feedback_three_percent = (
                    (int(user_feedback_three) / int(user_feedback))*100)
            else:
                user_feedback_three_percent = 0

            user_feedback_four = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=4)\
                .count()
            if user_feedback_four != 0:
                user_feedback_four_percent = (
                    (int(user_feedback_four) / int(user_feedback))*100)
            else:
                user_feedback_four_percent = 0

            user_feedback_five = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=5)\
                .count()
            if user_feedback_five != 0:
                user_feedback_five_percent = (
                    (int(user_feedback_five) / int(user_feedback))*100)
            else:
                user_feedback_five_percent = 0

            user_feedback_six = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=6)\
                .count()
            if user_feedback_six != 0:
                user_feedback_six_percent = (
                    (int(user_feedback_six) / int(user_feedback))*100)
            else:
                user_feedback_six_percent = 0
    
            user_feedback_seven = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=7)\
                .count()
            if user_feedback_seven != 0:
                user_feedback_seven_percent = (
                    (int(user_feedback_seven) / int(user_feedback))*100)
            else:
                user_feedback_seven_percent = 0

            user_feedback_eight = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=8)\
                .count()
            if user_feedback_eight != 0:
                user_feedback_eight_percent = (
                    (int(user_feedback_eight) / int(user_feedback))*100)
            else:
                user_feedback_eight_percent = 0

            user_feedback_nine = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=9)\
                .count()
            if user_feedback_nine != 0:
                user_feedback_nine_percent = (
                    (int(user_feedback_nine) / int(user_feedback))*100)
            else:
                user_feedback_nine_percent = 0

            user_feedback_ten = Feedback_Feedback.query\
                .filter_by(customer_uuid=user_uuid)\
                .filter_by(customer_rating=10)\
                .count()
            if user_feedback_ten != 0:
                user_feedback_ten_percent = (
                    (int(user_feedback_ten) / int(user_feedback))*100)
            else:
                user_feedback_ten_percent = 0
            return jsonify({"total_feedback": user_feedback,
                            'feedback_one': user_feedback_one_percent,
                            'feedback_two': user_feedback_two_percent,
                            'feedback_three': user_feedback_three_percent,
                            'feedback_four': user_feedback_four_percent,
                            'feedback_five': user_feedback_five_percent,
                            'feedback_six': user_feedback_six_percent,
                            'feedback_seven': user_feedback_seven_percent,
                            'feedback_eight': user_feedback_eight_percent,
                            'feedback_nine': user_feedback_nine_percent,
                            'feedback_ten': user_feedback_ten_percent,
                            })


@userdata.route('/user-stats/<string:user_uuid>', methods=['GET'])
def userdata_get_stats_user(user_uuid):
    """
    Grabs stats of feedback
    :return:
    """
    if request.method == 'GET':
        get_user_stats = Profile_StatisticsUser.query\
        .filter_by(user_uuid=user_uuid)\
        .first()
        user_schema = Profile_StatisticsUser_Schema()
        return jsonify(user_schema.dump(get_user_stats))
