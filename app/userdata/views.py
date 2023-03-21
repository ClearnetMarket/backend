from flask import request, jsonify
from flask_login import current_user
from app.userdata import userdata
from app import db
from app.common.decorators import login_required
from app.common.functions import floating_decimals
# models
from app.classes.auth import Auth_User, Auth_User_Schema
from app.classes.models import Query_Country, Query_Currency
from app.classes.checkout import Checkout_CheckoutShoppingCart
from app.classes.userdata import UserData_DefaultAddress
from app.classes.feedback import Feedback_Feedback,\
    Feedback_Feedback_Schema
from app.classes.profile import Profile_StatisticsUser,\
    Profile_StatisticsUser_Schema,\
    Profile_StatisticsVendor_Schema,\
    Profile_StatisticsVendor
# end models


@userdata.route('/user-cart-count', methods=['GET'])
@login_required
def userdata_get_shopping_cart_count():
    """
    Returns how many items are in a users count
    :return:
    """
    shopping_cart_count = db.session\
        .query(Checkout_CheckoutShoppingCart)\
        .filter(Checkout_CheckoutShoppingCart.customer_id == current_user.id)\
        .count()

    if shopping_cart_count is None:
        return jsonify({'amount': '0'})

    return jsonify({'success': "Got amount successfully",
                    'amount': shopping_cart_count
                })


@userdata.route('/country-currency', methods=['GET'])
@login_required
def userdata_country_currency():
    """
    Returns all info about a user
    :return:
    """
    currency = db.session\
        .query(Query_Currency)\
        .filter(current_user.currency == Query_Currency.value)\
        .first()
    if currency is None:
        return jsonify({'error': 'Error: Currency not Found'})
    currency_name = currency.symbol
    country = db.session\
        .query(Query_Country)\
        .filter(current_user.country == Query_Country.value)\
        .first()
    if currency is None:
        return jsonify({'error': 'Error: Country not Found'})
    countryname = country.name
    return jsonify({'success': "Info success",
                    'country': countryname,
                    'currency': currency_name
                    })


@userdata.route('/user-info/<string:user_uuid>', methods=['GET'])
def userdata_home(user_uuid):
    """
    Returns all info about a user
    :return:
    """
    userdata_user = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == user_uuid)\
        .first()

    user_schema = Auth_User_Schema()
    return jsonify(user_schema.dump(userdata_user))


@userdata.route('/user-info-update', methods=['PUT'])
@login_required
def userdata_update():
    """
    Returns all info about a user
    :return:
    """
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

        return jsonify({"success": 'Updated userprofile'})
    else:
        return jsonify({"error": 'Error:  Couldnt update profile'})


@userdata.route('/defaultaddress', methods=['PUT'])
@login_required
def userdata_update_address():
    """
    Returns all info about a user
    :return:
    """
    user_address = db.session\
        .query(UserData_DefaultAddress)\
        .filter(UserData_DefaultAddress.uuid == current_user.uuid)\
        .first()
    if not user_address:
        return jsonify({"error": 'Error:  Could not find User Address'})

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
            address_name=address_name,
            apt=apt,
            city=city,
            state_or_provence=state_or_provence,
            country=current_user.country,
            zip_code=zipcode,
            msg=message,
        )
        db.session.add(new_address)
    db.session.commit()
    return jsonify({"success": 'Updated address'})


@userdata.route('/getdefaultaddress', methods=['GET'])
@login_required
def userdata_get_address():
    """
    Returns all info about a user
    :return:
    """
    user_address = db.session\
        .query(UserData_DefaultAddress)\
        .filter(UserData_DefaultAddress.uuid == current_user.uuid)\
        .first()
    if user_address is None:
        return jsonify(({'error': "Error:  Address not found"}))

    return jsonify({
        "success": "success",
        'address_name': user_address.address_name,
        'address': user_address.address,
        'apt': user_address.apt,
        'city': user_address.city,
        'country': user_address.country,
        'state_or_provence': user_address.state_or_provence,
        'zip': user_address.zip_code,
        'message': user_address.msg,
    })


@userdata.route('/user-feedback/<string:user_uuid>', methods=['GET'])
def userdata_get_all_feedback(user_uuid):
    """
    Grabs all feedback from a user
    :return:
    """
    user_feedback = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(type_of_feedback=2)\
        .order_by(Feedback_Feedback.timestamp.desc())\
        .limit(10)

    user_schema = Feedback_Feedback_Schema(many=True)
    return jsonify(user_schema.dump(user_feedback))


@userdata.route('/user-feedback-stats/<string:user_uuid>', methods=['GET'])
def userdata_get_stats_feedback(user_uuid):
    """
    Grabs stats of feedback for customer
    :return:
    """

    user_feedback = db.session\
        .query(Feedback_Feedback)\
        .filter(Feedback_Feedback.customer_uuid==user_uuid)\
        .filter(Feedback_Feedback.author_uuid != user_uuid)\
        .count()

    if user_feedback == 0:
        return jsonify({
                        "success": "success",
                        "total_feedback": 0,
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

    user_feedback_one = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=1)\
        .count()

    if user_feedback_one != 0:
        user_feedback_one_percent = (
            (int(user_feedback_one) / int(user_feedback))*100)
    else:
        user_feedback_one_percent = 0
    user_feedback_two = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=2)\
        .count()
    if user_feedback_two != 0:
        user_feedback_two_percent = (
            (int(user_feedback_two) / int(user_feedback))*100)
    else:
        user_feedback_two_percent = 0

    user_feedback_three = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=3)\
        .count()
    if user_feedback_three != 0:
        user_feedback_three_percent = (
            (int(user_feedback_three) / int(user_feedback))*100)
    else:
        user_feedback_three_percent = 0

    user_feedback_four = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=4)\
        .count()
    if user_feedback_four != 0:
        user_feedback_four_percent = (
            (int(user_feedback_four) / int(user_feedback))*100)
    else:
        user_feedback_four_percent = 0

    user_feedback_five = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=5)\
        .count()
    if user_feedback_five != 0:
        user_feedback_five_percent = (
            (int(user_feedback_five) / int(user_feedback))*100)
    else:
        user_feedback_five_percent = 0

    user_feedback_six = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=6)\
        .count()
    if user_feedback_six != 0:
        user_feedback_six_percent = (
            (int(user_feedback_six) / int(user_feedback))*100)
    else:
        user_feedback_six_percent = 0

    user_feedback_seven = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=7)\
        .count()
    if user_feedback_seven != 0:
        user_feedback_seven_percent = (
            (int(user_feedback_seven) / int(user_feedback))*100)
    else:
        user_feedback_seven_percent = 0

    user_feedback_eight = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=8)\
        .count()
    if user_feedback_eight != 0:
        user_feedback_eight_percent = (
            (int(user_feedback_eight) / int(user_feedback))*100)
    else:
        user_feedback_eight_percent = 0

    user_feedback_nine = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=9)\
        .count()
    if user_feedback_nine != 0:
        user_feedback_nine_percent = (
            (int(user_feedback_nine) / int(user_feedback))*100)
    else:
        user_feedback_nine_percent = 0

    user_feedback_ten = db.session\
        .query(Feedback_Feedback)\
        .filter_by(customer_uuid=user_uuid)\
        .filter_by(customer_rating=10)\
        .count()
    if user_feedback_ten != 0:
        user_feedback_ten_percent = (
            (int(user_feedback_ten) / int(user_feedback))*100)
    else:
        user_feedback_ten_percent = 0
    return jsonify({
                    "success": "success",
                    "total_feedback": floating_decimals(user_feedback, 2),
                    'feedback_one': floating_decimals(user_feedback_one_percent, 2),
                    'feedback_two': floating_decimals(user_feedback_two_percent, 2),
                    'feedback_three': floating_decimals(user_feedback_three_percent, 2),
                    'feedback_four': floating_decimals(user_feedback_four_percent, 2),
                    'feedback_five': floating_decimals(user_feedback_five_percent, 2),
                    'feedback_six': floating_decimals(user_feedback_six_percent, 2),
                    'feedback_seven': floating_decimals(user_feedback_seven_percent, 2),
                    'feedback_eight': floating_decimals(user_feedback_eight_percent, 2),
                    'feedback_nine': floating_decimals(user_feedback_nine_percent, 2),
                    'feedback_ten': floating_decimals(user_feedback_ten_percent, 2),
                    })


@userdata.route('/user-stats/<string:user_uuid>', methods=['GET'])
def userdata_get_stats_user(user_uuid):
    """
    Grabs stats of feedback for buyting
    :return:
    """

    get_user_stats = db.session\
                    .query(Profile_StatisticsUser)\
                    .filter_by(user_uuid=user_uuid)\
                    .first()
    user_schema = Profile_StatisticsUser_Schema()
    return jsonify(user_schema.dump(get_user_stats))


@userdata.route('/vendor-stats/<string:user_uuid>', methods=['GET'])
def userdata_get_stats_vendor(user_uuid):
    """
    Grabs stats of feedback for selling
    :return:
    """

    get_user_stats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter_by(vendor_uuid=user_uuid)\
        .first()

    user_schema = Profile_StatisticsVendor_Schema()
    return jsonify(user_schema.dump(get_user_stats))
