from flask import request, session, jsonify
from flask_login import current_user, logout_user, login_user
from app.auth import auth
from app import db, bcrypt, UPLOADED_FILES_DEST_USER, login_manager
from datetime import datetime
import os
import base64
import functools
from sqlalchemy.sql.expression import func
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.common.functions import mkdir_p, userimagelocation
from app.common.decorators import \
    login_required
# models
from app.classes.models import Query_WordList, Query_Country_Schema, Query_Country, Query_CurrencyList, Query_CurrencyList_Schema
from app.classes.item import Item_MarketItem
from app.achs.a import newbie
from app.classes.userdata import \
    UserData_History

from app.classes.profile import Profile_StatisticsUser

from app.classes.checkout import \
    Checkout_ShoppingCartTotal
from app.classes.achievements import \
    Achievements_UserAchievements, \
    Achievements_WhichAch
from app.classes.auth import \
    Auth_User, \
    Auth_UserFees, \
    Auth_AccountSeedWords

from app.wallet_bch.wallet_bch_work import bch_create_wallet
from app.wallet_btc.wallet_btc_work import btc_create_wallet
from app.wallet_xmr.wallet_xmr_work import xmr_create_wallet
from flask_cors import cross_origin


# @auth.route("/getsession", methods=["GET"])
# @login_manager.request_loader
# def check_session():
#     print("checking user...")
#     x = request.headers
#     y = (x["Authorization"][7:])
#     print(session)
#     if session['_id'] == y:

#         print("found")
#         print(x['Authorization'])


#     if current_user.is_authenticated:
#         print("checking user...")
#         return jsonify({
#         "login": True,
#         'user': {'user_id': current_user.uuid,
#                 'user_name': current_user.username,
#                 'user_email': current_user.email,
#                 'profile_image': current_user.profileimage,
#                 'country': current_user.country,
#                 'currency': current_user.currency,
#          },
#         'token': session['_id']
#     }), 200

#     else:
#         print('not authenticated')
#         return jsonify({"login": False})

@auth.route("/getsession", methods=["GET"])
@cross_origin()
@login_manager.request_loader
def check_session():
   # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        print(api_key)
        user_exists = Auth_User.query.filter(Auth_User.api_key==api_key).first() is not None
      
        if user_exists:
            user = Auth_User.query.filter(Auth_User.api_key==api_key).first()
            print(user.username)
            print(user.id)
            return jsonify({
            "login": True,
            'user': {'user_id': user.uuid,
                    'user_name': user.username,
                    'user_email': user.email,
                    'profile_image': user.profileimage,
                    'country': user.country,
                    'currency': user.currency,
            },
            'token': user.api_key
                }), 200
        else:
            return jsonify({"status": "error. user not found"})
    else:
        return jsonify({"status": "error"})


@auth.route("/logout", methods=["GET"])
def logout():
    try:
        current_user.is_authenticated = False
        logout_user()
        return jsonify({'status': 'logged out'}), 200
    except UnmappedInstanceError:

        return jsonify({'status': 'error'}), 400

@auth.route("/login", methods=["POST"])
def auth_login_user_post():

    username = request.json["username"]
    password = request.json["password"]
    user = Auth_User.query.filter_by(username=username).first()
    print("logging in")
    print(username)
    print(password)
    if user is None:
        return jsonify({"error": "Unauthorized"})
    if not bcrypt.check_password_hash(user.password_hash, password):
        x = int(user.fails)
        y = x + 1
        user.fails = y
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
                'user_name': user.username,
                'user_email': user.email,
                'profile_image': user.profileimage,
                'country': user.country,
                'currency': user.currency,
         },
        'token': session['_id']
    }), 200

@auth.route("/register", methods=["POST"])
def register_user():

    from uuid import uuid4
    now = datetime.utcnow()
    shard = 1


    x =  uuid4().hex
    y = uuid4().hex
    c = uuid4().hex
    key = x+y+c

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    currency = request.json["currency"]
    country = request.json["country"]

    currency_value = currency['value']
    country_value = country['numericcode']
    user_exists_email = Auth_User.query.filter_by(email=email).first() is not None
    if user_exists_email:
        return jsonify({"error": "User already exists"}), 409
    user_exists_username = Auth_User.query.filter_by(username=username).first() is not None
    if user_exists_username:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = Auth_User(
            username=username,
            email='',
            password_hash=hashed_password,
            member_since=now,
            wallet_pin='',
            profileimage='user-unknown.png',
            stringuserdir=0,
            bio='',
            api_key=key,
            country=country_value,
            currency=currency_value,
            vendor_account=0,
            selling_from=0,
            last_seen=now,
            admin=0,
            admin_role=0,
            dispute=0,
            fails=0,
            locked=0,
            vacation=0,
            shopping_timer=now,
            lasttraded_timer=now,
            shard=shard,
            usernode=0,
            affiliate_account=0,
            confirmed=0,
            passwordpinallowed=0
             )

    db.session.add(new_user)
    db.session.commit()
    # db.session.flush()

    # # create user stats
    # stats = Profile_StatisticsUser(
    #     username=new_user.username,
    #     totalitemsbought=0,
    #     totalbtcspent=0,
    #     totalbtcrecieved=0,
    #     totalbtccashspent=0,
    #     totalbtccashrecieved=0,
    #     totalreviews=0,
    #     startedbuying=now,
    #     diffpartners=0,
    #     totalachievements=0,
    #     user_id=new_user.id,
    #     userrating=0,
    #     totaltrades=0,
    #     disputecount=0,
    #     itemsflagged=0,
    #     totalusdspent=0,
    # )

    # # create which achs they pick
    # achselect = Achievements_WhichAch(
    #     user_id=new_user.id,
    #     ach1='0',
    #     ach2='0',
    #     ach3='0',
    #     ach4='0',
    #     ach5='0',
    #     ach1_cat='0',
    #     ach2_cat='0',
    #     ach3_cat='0',
    #     ach4_cat='0',
    #     ach5_cat='0',
    # )

    # # create users achs
    # ach = Achievements_UserAchievements(
    #     user_id=new_user.id,
    #     username=new_user.username,
    #     experiencepoints=0,
    #     level=1,
    # )

    # # create browser history
    # browserhistory = UserData_History(
    #     user_id=new_user.id,
    #     recentcat1=1,
    #     recentcat1date=now,
    #     recentcat2=2,
    #     recentcat2date=now,
    #     recentcat3=3,
    #     recentcat3date=now,
    #     recentcat4=4,
    #     recentcat4date=now,
    #     recentcat5=7,
    #     recentcat5date=now,
    # )

    # # create checkout_shopping_cart for user
    # newcart = Checkout_ShoppingCartTotal(
    #     customer=new_user.id,
    #     btc_cash_sumofitem=0,
    #     btc_cash_price=0,
    #     shipping_btc_cashprice=0,
    #     total_btc_cash_price=0,
    #     percent_off_order=0,
    #     btc_cash_off=0,
    # )

    # setfees = Auth_UserFees(user_id=new_user.id,
    #                         buyerfee=0,
    #                         buyerfee_time=now,
    #                         vendorfee=2,
    #                         vendorfee_time=now,
    #                         )

    # db.session.add(setfees)
    # db.session.add(ach)
    # db.session.add(browserhistory)
    # db.session.add(achselect)
    # db.session.add(stats)
    # db.session.add(newcart)

    # # creates wallets in the database cash wallet in db
    # bch_create_wallet(user_id=new_user.id)
    # btc_create_wallet(user_id=new_user.id)
    # xmr_create_wallet(user_id=new_user.id)

    # # achievement
    # newbie(user_id=new_user.id)
    # # make a user a directory
    # db.session.commit()


    # getuserlocation = userimagelocation(user_id=new_user.id)
    # userfolderlocation = os.path.join(UPLOADED_FILES_DEST_USER,
    #                                   getuserlocation,
    #                                   str(new_user.id))
    # mkdir_p(path=userfolderlocation)

   
    login_user(new_user)
    current_user.is_authenticated()
    current_user.is_active()
    print(session)
    return jsonify({
        "login": True,
        'user': {'user_id': new_user.uuid,
                'user_name': new_user.username,
                'user_email': new_user.email,
                'profile_image': new_user.profileimage,
                'country': new_user.country,
                'currency': new_user.currency,
         },
        'token':  new_user.currency
    }), 200





@auth.route("/login", methods=["GET"])
@login_required
def account_seed():
    user_id = session.get("user_id")

    userseed = Auth_AccountSeedWords.query \
        .filter(Auth_AccountSeedWords.user_id == user_id) \
        .first()
    if request.method == 'GET':
        if userseed is None:
            word_list = []
            get_words = Query_WordList.query.order_by(func.random()).limit(6)
            for f in get_words:
                word_list.append(f.text)
            word00 = str(word_list[0]).lower()
            word01 = str(word_list[1]).lower()
            word02 = str(word_list[2]).lower()
            word03 = str(word_list[3]).lower()
            word04 = str(word_list[4]).lower()
            word05 = str(word_list[5]).lower()
            addseedtodb = Auth_AccountSeedWords(user_id=user_id,
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
    user_id = session.get("user_id")
    user = Auth_User.query \
        .filter(Auth_User.id == user_id)\
        .first()

    if request.method == 'POST':
        userseed = db.session.query(Auth_AccountSeedWords) \
            .filter(user.id == Auth_AccountSeedWords.user_id)\
            .first() is not None
        if userseed:
            word0 = request.json["word0"]
            word1 = request.json["word1"]
            word2 = request.json["word3"]
            word3 = request.json["word4"]
            word4 = request.json["word5"]
            word5 = request.json["word6"]
            if word0 == userseed.word00 and \
                word1 == userseed.word01 and \
                word2 == userseed.word02 and \
                word3 == userseed.word03 and \
                word4 == userseed.word04 and \
                word5 == userseed.word05:

                user.confirmed = 1


                db.session.add(user)
                db.session.commit()
                return jsonify({
                    'status': 'Account Confirmed'
                }), 200
            else:
                return jsonify({"error": "Seed does not match"}), 409
        else:
            return jsonify({"error": "Seed does not exist"}), 409


@auth.route('/change-pin', methods=['POST'])
@login_required
def change_pin():

    if request.method == 'POST':
        user_id = session.get("user_id")
        user = Auth_User.query \
            .filter(Auth_User.id == user_id) \
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


@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session.get("user_id")
        user = Auth_User.query \
            .filter(Auth_User.id == user_id) \
            .first()
        if user.passwordpinallowed == 1:
            new_password = request.json["newpassword"]

            hashed_password = bcrypt.generate_password_hash(new_password)

            user.password_hash = hashed_password
            user.passwordpinallowed = 0
            db.session.add(user)
            db.session.commit()

            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Must unlock account to change password"}), 409


@auth.route('/unlock-account', methods=['POST'])
@login_required
def retrieve_seed_to_unlock_account():

    if request.method == 'POST':
        word0 = request.json["word0"]
        word1 = request.json["word1"]
        word2 = request.json["word3"]
        word3 = request.json["word4"]
        word4 = request.json["word5"]
        word5 = request.json["word6"]

        # match the seed to the user
        userseed = Auth_AccountSeedWords.query\
            .filter(Auth_AccountSeedWords.word00 == word0)\
            .filter(Auth_AccountSeedWords.word01 == word1)\
            .filter(Auth_AccountSeedWords.word02 == word2)\
            .filter(Auth_AccountSeedWords.word03 == word3)\
            .filter(Auth_AccountSeedWords.word04 == word4)\
            .filter(Auth_AccountSeedWords.word05 == word5)\
            .first()

        if userseed is not None:
            user = Auth_User.query.filter(Auth_User.id == userseed.user_id).first()
            user.passwordpinallowed = 1

            db.session.add(user)
            db.session.commit()

            login_user(user)
            current_user.is_authenticated()
            current_user.is_active()
            return jsonify({'status': 'Account Unlocked'}), 200
        else:
            return jsonify({'error': 'Incorrect Seed'}), 409


@auth.route("/vacation-on", methods=["POST"])
def vacation_on():
    user_id = session.get("user_id")
    user = Auth_User.query \
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
        return jsonify({
            "status": "Vacation Mode Enabled",
        }), 200
    else:
        return jsonify({
            "error": "Vacation Mode already enabled",
        }), 409


@auth.route("/vacation-off", methods=["POST"])
def vacation_off():
    user_id = session.get("user_id")
    user = Auth_User.query \
        .filter(Auth_User.id == user_id) \
        .first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if user.vacation == 1:
        # Go into vacation mode
        user.vacation = 0
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "status": "Vacation Mode Disabled",
        }), 200
    else:
        return jsonify({
            "error": "Vacation Mode already disabled",
        }), 409



@auth.route('/query/country', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_country_list():
    """
    Returns list of Countrys
    :return:
    """
    if request.method == 'GET':
        country_list = Query_Country.query.order_by(Query_Country.name.asc()).all()

        country_schema = Query_Country_Schema(many=True)
        return jsonify(country_schema.dump(country_list))


@auth.route('/query/currency', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_currency_list():
    """
    Returns list of currencys 
    :return:
    """
    print(request.data)
    if request.method == 'GET':

        currency_list = Query_CurrencyList.query.order_by(Query_CurrencyList.value.asc()).all()

        currency_schema = Query_CurrencyList_Schema(many=True)
    
        return jsonify(currency_schema.dump(currency_list))
