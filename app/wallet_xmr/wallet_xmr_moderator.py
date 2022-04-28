from app import db
from decimal import Decimal
from app.common.functions import floating_decimals

from app.classes.auth import Auth_User
from app.classes.user_orders import User_Orders
from app.wallet_xmr.wallet_xmr_work import xmr_send_coin_to_user
from app.common.functions import convert_local_to_xmr, convert_to_local_xmr


def finalize_order_dispute_xmr(order_uuid, percent_to_customer, percent_to_vendor):
    get_order = db.session\
        .query(User_Orders)\
        .filter(User_Orders.uuid == order_uuid)\
        .first()
    get_mod = db.session.query(Auth_User).filter(Auth_User.id == get_order.moderator_uuid).first()
    # get moderator fee
    mod_fee_percent = 0.05
    fee_for_freeport = Decimal(get_order.price_total_xmr) * Decimal(mod_fee_percent)
    amount_of_fee = floating_decimals(fee_for_freeport, 12)

    local_price = convert_to_local_xmr(get_order.price_total_xmr, 0)
    if local_price > 100:
        max_amount = convert_local_to_xmr(100, 1)
        amount_of_fee = floating_decimals(max_amount, 12)

    # subtract amount
    amount_left_after_mod_fee = Decimal(get_order.price_total_xmr) - amount_of_fee

    get_amount_to_vendor = amount_left_after_mod_fee * percent_to_vendor
    get_final_amount_to_vendor = floating_decimals(get_amount_to_vendor, 12)
    get_amount_to_customer = amount_left_after_mod_fee * percent_to_customer
    get_final_amount_to_customer = floating_decimals(get_amount_to_customer, 12)

    if amount_of_fee > 0:
        # send cut to moderator
        xmr_send_coin_to_user(amount=amount_of_fee,
                              user_id=get_mod.id,
                              order_uuid=get_order.uuid)
    if get_final_amount_to_vendor > 0:
        # send coin to vendor
        xmr_send_coin_to_user(amount=get_final_amount_to_vendor,
                              user_id=get_order.vendor_id,
                              order_uuid=get_order.uuid)
    if get_final_amount_to_customer > 0:
        # send coin to customer
        xmr_send_coin_to_user(amount=get_final_amount_to_customer,
                              user_id=get_order.customer_id,
                              order_uuid=get_order.uuid)

