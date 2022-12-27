from flask import request, jsonify
from flask_login import current_user, logout_user, login_user, login_required
from app.auth import auth
from app import db, bcrypt, UPLOADED_FILES_DEST_USER
from datetime import datetime
import os
from uuid import uuid4
from sqlalchemy.sql.expression import func
from app.common.functions import mkdir_p, userimagelocation
# models
from app.classes.models import Query_WordList,\
    Query_Country_Schema, \
    Query_Country,\
    Query_CurrencyList,\
    Query_CurrencyList_Schema
from app.classes.item import Item_MarketItem
from app.classes.userdata import UserData_History, UserData_DefaultAddress
from app.classes.profile import Profile_StatisticsUser
from app.classes.checkout import Checkout_ShoppingCartTotal
from app.classes.auth import \
    Auth_User, \
    Auth_UserFees, \
    Auth_AccountSeedWords

from app.wallet_bch.wallet_bch_work import bch_create_wallet
from app.wallet_btc.wallet_btc_work import btc_create_wallet
from app.wallet_xmr.wallet_xmr_work import xmr_create_wallet


@auth.route("/whoami", methods=["GET"])
@login_required
def check_session():
    """
    Checks auth token to ensure user is authenticated
    """
    api_key = request.headers.get('Authorization')
    print(api_key)
    if api_key:
        api_key = api_key.replace('bearer ', '', 1)
        user_exists = db.session\
                          .query(Auth_User)\
                          .filter(Auth_User.api_key == api_key)\
                          .first() is not None
        if user_exists:
            user = db.session\
                .query(Auth_User)\
                .filter(Auth_User.api_key == api_key)\
                .first()
            print(user)
            return jsonify({
                "login": True,
                'user': {'user_id': user.uuid,
                         'user_name': user.display_name,
                         'user_email': user.email,
                         'user_admin': user.admin_role,
                         'profile_image': user.profileimage,
                         'country': user.country,
                         'currency': user.currency,
                         'token': user.api_key
                         },
                'token': user.api_key
            }), 200
        else:
            return jsonify({"status": "error. user not found"}), 401
    else:
        return jsonify({"status": "error"}), 401


@auth.route("/amiconfirmed", methods=["GET"])
@login_required
def check_confirmed():
    """
    Checks to see if user confirmed with email or key
    """
    user = db.session\
        .query(Auth_User)\
        .filter(Auth_User.id == current_user.id)\
        .first()
    if user.confirmed == 0:
        confirmed = False
    else:
        confirmed = True

    return jsonify({"confirmed": confirmed}), 200


@auth.route("/logout", methods=["POST"])
def logout():
    """
    Logs a user out of session on backend
    """
    try:
        logout_user()
        return jsonify({'status': 'logged out'}), 200
    except Exception as e:
        print(e)
        return jsonify({"error", 'error'}), 400


@auth.route("/login", methods=["POST"])
def login():
    """
    Main post function to  a user
    """
    if request.method == "POST":

        username = request.json["username"]
        password = request.json["password"]
        user = db.session\
                   .query(Auth_User)\
                   .filter_by(username=username)\
                   .first() is not None
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        user = db.session\
            .query(Auth_User)\
            .filter_by(username=username)\
            .first()
        if not bcrypt.check_password_hash(user.password_hash, password):

            current_fails = int(user.fails)
            new_fails = current_fails + 1
            user.fails = new_fails
            db.session.add(user)
            db.session.commit()
            return jsonify({"error": "Unauthorized"}), 401

        user.locked = 0
        user.fails = 0
        db.session.add(user)
        db.session.commit()

        login_user(user)
        current_user.is_authenticated()
        current_user.is_active()

        return jsonify({
            "login": True,
            'user': {'user_id': user.uuid,
                     'user_name': user.display_name,
                     'user_email': user.email,
                     'profile_image': user.profileimage,
                     'country': user.country,
                     'currency': user.currency,
                     'admin_role': user.admin_role,
                     'token': user.api_key
                     },
            'token': user.api_key
        }), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401


@auth.route("/register", methods=["POST"])
def register_user():
    """
    Main post function to register a user
    """
    now = datetime.utcnow()

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    currency = request.json["currency"]
    country = request.json["country"]
    display_username = request.json["display_username"]
    pin = request.json["pin"]

    part_one_code = uuid4().hex
    part_two_code = uuid4().hex
    part_three_code = uuid4().hex
    key = part_one_code + part_two_code + part_three_code

    user_exists_email = db.session\
        .query(Auth_User)\
        .filter_by(email=email)\
        .first() is not None
    if user_exists_email:
        return jsonify({"error": "Email already exists"}), 409
    user_exists_username = db.session\
        .query(Auth_User)\
        .filter_by(username=username)\
        .first() is not None
    if user_exists_username:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = Auth_User(
        username=username,
        display_name=display_username,
        email=email,
        password_hash=hashed_password,
        member_since=now,
        wallet_pin=pin,
        profileimage='user-unknown.png',
        bio='',
        api_key=key,
        country=country,
        currency=currency,
        vendor_account=0,
        selling_from=country,
        last_seen=now,
        admin=0,
        admin_role=0,
        dispute=0,
        fails=0,
        locked=0,
        vacation=0,
        shopping_timer=now,
        lasttraded_timer=now,
        shard=1,
        usernode=0,
        confirmed=0,
        passwordpinallowed=0
    )

    db.session.add(new_user)
    db.session.flush()

    # create user stats
    stats = Profile_StatisticsUser(
        user_name=new_user.username,
        total_items_bought=0,
        total_btc_spent=0,
        total_btc_recieved=0,
        total_bch_spent=0,
        total_bch_recieved=0,
        total_reviews=0,
        started_buying=now,
        diff_partners=0,
        total_achievements=0,
        user_uuid=new_user.uuid,
        user_rating=0,
        total_trades=0,
        dispute_count=0,
        items_flagged=0,
        total_usd_spent=0,
    )

    # create browser history
    browserhistory = UserData_History(
        user_id=new_user.id,
        recent_cat_1=1,
        recent_cat_1_date=now,
        recent_cat_2=2,
        recent_cat_2_date=now,
        recent_cat_3=3,
        recent_cat_3_date=now,
        recent_cat_4=4,
        recent_cat_4_date=now,
        recent_cat_5=7,
        recent_cat_5_date=now,
    )
    user_address = UserData_DefaultAddress(
        uuid=new_user.uuid,
        address_name='',
        address='',
        apt='',
        city='',
        country=country,
        state_or_provence='',
        zip_code='',
        msg=''
    )
    # create checkout_shopping_cart for user
    newcart = Checkout_ShoppingCartTotal(
        customer_id=new_user.id,
        # btc
        btc_sum_of_item=0,
        btc_price=0,
        btc_shipping_price=0,
        btc_total_price=0,
        # bch
        bch_sum_of_item=0,
        bch_price=0,
        bch_shipping_price=0,
        bch_total_price=0,
        # xmr
        xmr_sum_of_item=0,
        xmr_price=0,
        xmr_shipping_price=0,
        xmr_total_price=0,
    )

    # user fees
    setfees = Auth_UserFees(user_id=new_user.id,
                            buyerfee=0,
                            buyerfee_time=now,
                            vendorfee=3,
                            vendorfee_time=now,
                            )

    db.session.add(setfees)
    db.session.add(browserhistory)
    db.session.add(stats)
    db.session.add(newcart)
    db.session.add(user_address)

    # create user directory
    getuserlocation = userimagelocation(user_id=new_user.id)
    userfolderlocation = os.path.join(UPLOADED_FILES_DEST_USER,
                                      getuserlocation,
                                      str(new_user.uuid))
    mkdir_p(path=userfolderlocation)
    # creates wallets in the database cash wallet in db
    bch_create_wallet(user_id=new_user.id)
    btc_create_wallet(user_id=new_user.id)
    xmr_create_wallet(user_id=new_user.id)

    db.session.commit()
    # log user in as active not sure if needed with frontend
    login_user(new_user)
    current_user.is_authenticated()
    current_user.is_active()

    return jsonify({
        "login": True,
        'user': {'user_id': new_user.uuid,
                 'user_name': new_user.display_name,
                 'user_email': new_user.email,
                 'profile_image': new_user.profileimage,
                 'country': new_user.country,
                 'currency': new_user.currency,
                 'admin_role': new_user.admin_role,
                 'token': new_user.api_key
                 },
        'token':  new_user.api_key
    }), 200


@auth.route("/account-seed", methods=["GET"])
@login_required
def account_seed():
    """"
    Gets the account seed for a user
    """
    if request.method == 'GET':
        userseed = db.session\
            .query(Auth_AccountSeedWords) \
            .filter(Auth_AccountSeedWords.user_id == current_user.id) \
            .first()

        if userseed is None:
            word_list = []
            get_words = db.session\
                .query(Query_WordList)\
                .order_by(func.random())\
                .limit(6)
            for f in get_words:
                word_list.append(f.text)
            word00 = str(word_list[0]).lower()
            word01 = str(word_list[1]).lower()
            word02 = str(word_list[2]).lower()
            word03 = str(word_list[3]).lower()
            word04 = str(word_list[4]).lower()
            word05 = str(word_list[5]).lower()
            addseedtodb = Auth_AccountSeedWords(user_id=current_user.id,
                                                word00=word00,
                                                word01=word01,
                                                word02=word02,
                                                word03=word03,
                                                word04=word04,
                                                word05=word05,
                                                )
            db.session.add(addseedtodb)
            db.session.commit()
        else:
            word00 = userseed.word00
            word01 = userseed.word01
            word02 = userseed.word02
            word03 = userseed.word03
            word04 = userseed.word04
            word05 = userseed.word05

        return jsonify({
            'word1': word00,
            'word2': word01,
            'word3': word02,
            'word4': word03,
            'word5': word04,
            'word6': word05,
        }), 200


@auth.route("/accountseedconfirm", methods=["POST"])
@login_required
def confirm_seed():

    if request.method == 'POST':
        user = db.session\
            .query(Auth_User) \
            .filter(Auth_User.id == current_user.id)\
            .first()

        if request.method == 'POST':
            userseed = db.session\
                            .query(Auth_AccountSeedWords) \
                            .filter(Auth_AccountSeedWords.user_id == user.id)\
                            .first() is not None
            if userseed:
                userseed = db.session\
                    .query(Auth_AccountSeedWords) \
                    .filter(Auth_AccountSeedWords.user_id == user.id)\
                    .first()
                word0 = str(request.json["word0"])
                word1 = str(request.json["word1"])
                word2 = str(request.json["word2"])
                word3 = str(request.json["word3"])
                word4 = str(request.json["word4"])
                word5 = str(request.json["word5"])
                if word0 != userseed.word00:
                    return jsonify({"error 1": "Seed does not match"}), 409
                if word1 != userseed.word01:
                    return jsonify({"error 2": "Seed does not match"}), 409
                if word2 != userseed.word02:
                    return jsonify({"error 3": "Seed does not match"}), 409
                if word3 != userseed.word03:
                    return jsonify({"error": "Seed does not match 4"}), 409
                if word4 != userseed.word04:
                    return jsonify({"error": "Seed does not match 5"}), 409
                if word5 != userseed.word05:
                    return jsonify({"error": "Seed does not match 6"}), 409

                user.confirmed = 1

                db.session.add(user)
                db.session.commit()
                return jsonify({
                    'status': 'success'
                }), 200
            else:
                return jsonify({"error": "Seed does not exist"}), 409


@auth.route('/unlock-account', methods=['POST'])
def retrieve_seed_to_unlock_account():

    if request.method == 'POST':
        word0 = request.json["word0"]
        word1 = request.json["word1"]
        word2 = request.json["word3"]
        word3 = request.json["word4"]
        word4 = request.json["word5"]
        word5 = request.json["word6"]

        # match the seed to the user
        userseed = db.session\
            .query(Auth_AccountSeedWords)\
            .filter(Auth_AccountSeedWords.word00 == word0)\
            .filter(Auth_AccountSeedWords.word01 == word1)\
            .filter(Auth_AccountSeedWords.word02 == word2)\
            .filter(Auth_AccountSeedWords.word03 == word3)\
            .filter(Auth_AccountSeedWords.word04 == word4)\
            .filter(Auth_AccountSeedWords.word05 == word5)\
            .first()

        if userseed is not None:
            user = db.session\
                .query(Auth_User)\
                .filter(Auth_User.id == userseed.user_id)\
                .first()
            user.passwordpinallowed = 1

            db.session.add(user)
            db.session.commit()

            login_user(user)
            current_user.is_authenticated()
            current_user.is_active()
            return jsonify({'status': 'Account Unlocked'}), 200
        else:
            return jsonify({'error': 'Incorrect Seed'}), 409


@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user = db.session\
            .query(Auth_User) \
            .filter(Auth_User.id == current_user.id) \
            .first()

        new_password = request.json["password"]
        new_password_confirm = request.json["password_confirm"]
        if str(new_password) == str(new_password_confirm):
            hashed_password = bcrypt.generate_password_hash(new_password)
            user.password_hash = hashed_password
            user.passwordpinallowed = 0
            db.session.add(user)
            db.session.commit()
            return jsonify({"status": "success"}), 200

        else:
            return jsonify({"error": "Incorrect Passwords"}), 409


@auth.route('/change-pin', methods=['POST'])
@login_required
def change_pin():

    if request.method == 'POST':

        user = db.session\
            .query(Auth_User) \
            .filter(Auth_User.id == current_user.id) \
            .first()

        old_pin = request.json["old_pin"]
        new_pin = request.json["new_pin"]
        password = request.json["password"]

        if user.passwordpinallowed == 1:
            if not bcrypt.check_password_hash(user.password, password):
                return jsonify({"error": "Unauthorized"}), 401
            if not bcrypt.check_password_hash(user.wallet_pin, old_pin):
                return jsonify({"error": "Unauthorized"}), 401

            hashed_pin = bcrypt.generate_password_hash(new_pin)
            user.wallet_pin = hashed_pin
            user.passwordpinallowed = 0
            db.session.add(user)
            db.session.commit()

            return jsonify({"status": "success"}), 409
        return jsonify({"error": "Must unlock account to change password"}), 409


@auth.route("/vacation-on", methods=["POST"])
def vacation_on():
    user_id = current_user.id
    user = db.session\
        .query(Auth_User) \
        .filter(Auth_User.id == user_id) \
        .first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    # get physical items
    aitems = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == user.id)\
        .all()
    if user.vacation == 0:
        # Go into vacation mode
        user.vacation = 1
        db.session.add(user)
        if aitems:
            for a in aitems:
                a.online = 0
                db.session.add(a)
        db.session.commit()
        return jsonify({"status": "Vacation Mode Enabled"}), 200
    else:
        return jsonify({"error": "Vacation Mode already enabled"}), 409


@auth.route("/vacation-off", methods=["POST"])
def vacation_off():

    user = db.session\
        .query(Auth_User) \
        .filter(Auth_User.id == current_user.id) \
        .first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if user.vacation == 1:
        # Go into vacation mode
        user.vacation = 0
        db.session.add(user)
        db.session.commit()

        return jsonify({"status": "Vacation Mode Disabled"}), 200
    else:
        return jsonify({"error": "Vacation Mode already disabled"}), 409


@auth.route('/query/country', methods=['GET'])
def get_country_list():
    """
    Returns list of Countrys
    :return:
    """
    if request.method == 'GET':
        country_list = db.session\
            .query(Query_Country)\
            .order_by(Query_Country.name.asc())\
            .all()
        country_schema = Query_Country_Schema(many=True)
        return jsonify(country_schema.dump(country_list))


@auth.route('/query/currency', methods=['GET'])
def get_currency_list():
    """
    Returns list of currencys 
    :return:
    """
    if request.method == 'GET':
        currency_list = db.session\
            .query(Query_CurrencyList)\
            .order_by(Query_CurrencyList.value.asc())\
            .all()
        currency_schema = Query_CurrencyList_Schema(many=True)
        return jsonify(currency_schema.dump(currency_list))
