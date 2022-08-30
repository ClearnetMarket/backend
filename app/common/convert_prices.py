from app.classes.wallet_bch import Bch_Prices
from app.classes.wallet_btc import Btc_Prices
from app.classes.wallet_xmr import Xmr_Prices
from decimal import Decimal


def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"  # first cast decimal as str
    return Decimal(prc.format(f_val))


# BITCOIN
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


# BITCOIN CASH
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


# MONERO
def convert_to_local_xmr(amount, currency):
    getcurrentprice = Xmr_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    converted_price = Decimal(current_price) * Decimal(amount)
    price_in_local_currency = floating_decimals(converted_price, 2)
    return price_in_local_currency


def convert_local_to_xmr(amount, currency):
    getcurrentprice = Xmr_Prices.query.filter_by(currency_id=currency).first()
    current_price = getcurrentprice.price
    print(current_price)
    converted_price = Decimal(amount) / Decimal(current_price)
    price_in_floats = floating_decimals(converted_price, 12)

    return price_in_floats
