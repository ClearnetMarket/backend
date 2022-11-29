import os
from app.classes.wallet_bch import Bch_Prices
from app.classes.wallet_btc import Btc_Prices
from app.classes.wallet_xmr import Xmr_Prices
import random
import string
from decimal import Decimal


def convert_to_local_bch(amount, currency):
    getcurrentprice = Bch_Prices.query.filter_by(currency_id=currency).first()
    bt = getcurrentprice.price
    converted_price = Decimal(bt) * Decimal(amount)
    price_in_local_currency = floating_decimals(converted_price, 2)
    return price_in_local_currency


def convert_local_to_bch(amount, currency):
    getcurrentprice = Bch_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(amount) / Decimal(current_price)
    price_in_floats = floating_decimals(converted_price, 8)
    return price_in_floats


def convert_to_local_btc(amount, currency):
    getcurrentprice = Btc_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(current_price) * Decimal(amount)
    price_in_local_currency = floating_decimals(converted_price, 2)
    return price_in_local_currency


def convert_local_to_btc(amount, currency):
    getcurrentprice = Btc_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(amount) / Decimal(current_price)
    price_in_floats = floating_decimals(converted_price, 8)
    return price_in_floats


def convert_to_local_xmr(amount, currency):
    getcurrentprice = Xmr_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(current_price) * Decimal(amount)
    price_in_local_currency = floating_decimals(converted_price, 2)
    return price_in_local_currency


def convert_local_to_xmr(amount, currency):
    getcurrentprice = Xmr_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(amount) / Decimal(current_price)
    price_in_floats = floating_decimals(converted_price, 12)
    return price_in_floats


def genericprofile(path):
    user_id = str(path)
    cmd = 'cp /home/clearnet_webapp/info/user/user-unknown.png /home/info/user/' + user_id
    try:
        os.system(cmd)
    except OSError:  # Python >2.7
        pass


def mkdir_p(path):
    try:
        os.makedirs(path, 0o755)
    except:
        pass


def itemlocation(x):
    if 1 <= x <= 10000:
        return '1'
    elif 10001 <= x <= 20000:
        return '2'
    elif 20001 <= x <= 30000:
        return '3'
    elif 30001 <= x <= 40000:
        return '4'
    elif 40001 <= x <= 50000:
        return '5'
    elif 50001 <= x <= 60000:
        return '6'
    elif 60001 <= x <= 70000:
        return '7'
    elif 70001 <= x <= 80000:
        return '8'
    elif 80001 <= x <= 90000:
        return '9'
    elif 90001 <= x <= 100000:
        return '10'
    elif 100001 <= x <= 110000:
        return '11'
    elif 110001 <= x <= 120000:
        return '12'
    elif 120001 <= x <= 130000:
        return '13'
    elif 130001 <= x <= 140000:
        return '14'
    elif 140001 <= x <= 150000:
        return '15'
    elif 150001 <= x <= 160000:
        return '16'
    elif 160001 <= x <= 170000:
        return '17'
    elif 170001 <= x <= 180000:
        return '18'
    elif 180001 <= x <= 190000:
        return '19'
    elif 190001 <= x <= 200000:
        return '20'
    elif 200001 <= x <= 210000:
        return '21'
    elif 210001 <= x <= 220000:
        return '22'
    elif 220001 <= x <= 230000:
        return '23'
    elif 230001 <= x <= 240000:
        return '24'
    elif 240001 <= x <= 250000:
        return '25'
    elif 250001 <= x <= 260000:
        return '26'
    elif 260001 <= x <= 270000:
        return '27'
    elif 270001 <= x <= 280000:
        return '28'
    elif 280001 <= x <= 290000:
        return '29'
    elif 290001 <= x <= 300000:
        return '30'


def userimagelocation(user_id):
    if 1 <= user_id <= 10000:
        return '1'
    elif 10001 <= user_id <= 20000:
        return '2'
    elif 20001 <= user_id <= 30000:
        return '3'
    elif 30001 <= user_id <= 40000:
        return '4'
    elif 40001 <= user_id <= 50000:
        return '5'
    elif 50001 <= user_id <= 60000:
        return '6'
    elif 60001 <= user_id <= 70000:
        return '7'
    elif 70001 <= user_id <= 80000:
        return '8'
    elif 80001 <= user_id <= 90000:
        return '9'
    elif 90001 <= user_id <= 100000:
        return '10'
    elif 100001 <= user_id <= 110000:
        return '11'
    elif 110001 <= user_id <= 120000:
        return '12'
    elif 120001 <= user_id <= 130000:
        return '13'
    elif 130001 <= user_id <= 140000:
        return '14'
    elif 140001 <= user_id <= 150000:
        return '15'
    elif 150001 <= user_id <= 160000:
        return '16'
    elif 160001 <= user_id <= 170000:
        return '17'
    elif 170001 <= user_id <= 180000:
        return '18'
    elif 180001 <= user_id <= 190000:
        return '19'
    elif 190001 <= user_id <= 200000:
        return '20'
    elif 200001 <= user_id <= 210000:
        return '21'
    elif 210001 <= user_id <= 220000:
        return '22'
    elif 220001 <= user_id <= 230000:
        return '23'
    elif 230001 <= user_id <= 240000:
        return '24'
    elif 240001 <= user_id <= 250000:
        return '25'
    elif 250001 <= user_id <= 260000:
        return '26'
    elif 260001 <= user_id <= 270000:
        return '27'
    elif 270001 <= user_id <= 280000:
        return '28'
    elif 280001 <= user_id <= 290000:
        return '29'
    elif 290001 <= user_id <= 300000:
        return '30'


def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"  # first cast decimal as str
    return Decimal(prc.format(f_val))


def id_generator_picture1(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture2(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture3(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture4(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture5(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
