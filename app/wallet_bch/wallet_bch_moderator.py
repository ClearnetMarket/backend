from app import db
from app.common.functions import floating_decimals
from decimal import Decimal
# models
from app.classes.auth import Auth_User
from app.classes.user_orders import User_Orders
# end models
# btc imports
from app.wallet_bch.wallet_bch_work import bch_send_coin_to_user
from app.common.functions import convert_local_to_bch, convert_to_local_bch


def finalize_order_dispute_bch(order_uuid, percent_to_customer, percent_to_vendor):
    get_order = db.session\
        .query(User_Orders)\
        .filter(User_Orders.uuid == order_uuid)\
        .first()
    get_mod = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == get_order.moderator_uuid)\
        .first()
    # get moderator fee
    mod_fee_percent = 0.05
    fee_for_freeport = Decimal(get_order.price_total_bch) * Decimal(mod_fee_percent)
    amount_of_fee = floating_decimals(fee_for_freeport, 8)

    local_price = convert_to_local_bch(get_order.price_total_bch, 0)
    if local_price > 100:
        max_amount = convert_local_to_bch(100, 1)
        amount_of_fee = floating_decimals(max_amount, 8)

    # subtract amount
    amount_left_after_mod_fee = Decimal(get_order.price_total_bch) - amount_of_fee

    get_amount_to_vendor = amount_left_after_mod_fee * percent_to_vendor
    get_final_amount_to_vendor = floating_decimals(get_amount_to_vendor, 8)
    get_amount_to_customer = amount_left_after_mod_fee * percent_to_customer
    get_final_amount_to_customer = floating_decimals(get_amount_to_customer, 8)

    if amount_of_fee > 0:
        # send cut to moderator
        bch_send_coin_to_user(amount=amount_of_fee,
                              user_id=get_mod.id,
                              order_uuid=get_order.uuid)
    if get_final_amount_to_vendor > 0:
        # send coin to vendor
        bch_send_coin_to_user(amount=get_final_amount_to_vendor,
                              user_id=get_order.vendor_id,
                              order_uuid=get_order.uuid)
    if get_final_amount_to_customer > 0:
        # send coin to customer
        bch_send_coin_to_user(amount=get_final_amount_to_customer,
                              user_id=get_order.customer_id,
                              order_uuid=get_order.uuid)
