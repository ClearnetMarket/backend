
from flask import request, jsonify
from flask_login import current_user
from app.vendorcreateitem import vendorcreateitem
from app import UPLOADED_FILES_DEST_ITEM
from werkzeug.datastructures import CombinedMultiDict
import os
from app.common.decorators import login_required
from app.common.functions import mkdir_p

# models
from app.classes.item import Item_MarketItem
from app.classes.wallet_bch import *
from app.classes.models import *
from app.classes.category import *


@vendorcreateitem.route('/query/country', methods=['GET'])
def vendorcreateitem_get_country_list():
    """
    Returns list of Countrys
    :return:
    """
    if request.method == 'GET':
        country_list = Query_Country.query.order_by(Query_Country.name.asc()).all()

        country_schema = Query_Country_Schema(many=True)
        return jsonify(country_schema.dump(country_list))


@vendorcreateitem.route('/query/currency', methods=['GET'])
def vendorcreateitem_get_currency_list():
    """
    Returns list of currencys 
    :return:
    """
    if request.method == 'GET':
        currency_list = Query_CurrencyList.query.order_by(Query_CurrencyList.value.asc()).all()
        currency_schema = Query_CurrencyList_Schema(many=True)

        return jsonify(currency_schema.dump(currency_list))



@vendorcreateitem.route('/query/condition', methods=['GET'])
def vendorcreateitem_get_item_condition_list():
    """
    Returns list of item condition 
    :return:
    """
    if request.method == 'GET':

        condition_list = Query_ItemCondition.query.order_by(Query_ItemCondition.value.asc()).all()
        condition_schema = Query_ItemCondition_Schema(many=True)

        return jsonify(condition_schema.dump(condition_list))



@vendorcreateitem.route('/query/category', methods=['GET'])
def vendorcreateitem_get_item_category_list():
    """
    Returns list of item category 
    :return:
    """
    if request.method == 'GET':
        category_list = Category_Categories.query.order_by(Category_Categories.name.asc()).all()
        category_schema = Category_Categories_Schema(many=True)

        return jsonify(category_schema.dump(category_list))


@vendorcreateitem.route('/create-item-info', methods=['POST'])
@login_required
def create_item_info():
    """
    First page of vendor create item
    """
    if request.method == 'POST':
        
        now = datetime.utcnow()
        title = request.json["title"]
        digital_currency_1 = request.json["digital_currency_1"]
        digital_currency_2 = request.json["digital_currency_2"]
        digital_currency_3 = request.json["digital_currency_3"]
        currency = request.json["currency"]
        item_condition = request.json["item_condition"]
        item_count = request.json["item_count"]
        category_name_0 = request.json["category_name_0"]
        category_id_0 = request.json["category_name_0"]
        price = request.json["price"]
        currency = request.json["currency"]
        keywords = request.json["keywords"]

        # create image of item in database
        item = Item_MarketItem(
            string_node_id=1,
            category_name_0=category_name_0,
            category_id_0=category_id_0,
            digital_currency_1=digital_currency_1,
            digital_currency_2=digital_currency_2,
            digital_currency_3=digital_currency_3,
            created=now,
            vendor_name=current_user.username,
            vendor_id=current_user.id,
            origin_country=0,
            destination_country_one=0,
            destination_country_two=0,
            destination_country_three=0,
            destination_country_four=0,
            destination_country_five=0,
            item_title=title,
            item_count=item_count,
            item_description='',
            item_refund_policy='',
            price=price,
            currency=currency,
            item_condition=item_condition,
            total_sold=0,
            keywords=keywords,
            return_allowed=0,
            shipping_free=True,
            shipping_info_0='',
            shipping_two=0,
            shipping_three=0,
            shipping_day_least_0=0,
            shipping_day_most_0=0,
            shipping_info_2='',
            shipping_price_2=0,
            shipping_day_least_2=0,
            shipping_day_most_2=0,
            shipping_info_3='',
            shipping_price_3=0,
            shipping_day_least_3=0,
            shipping_day_most_3=0,
            not_shipping_1=0,
            not_shipping_2=0,
            not_shipping_3=0,
            not_shipping_4=0,
            not_shipping_5=0,
            not_shipping_6=0,
            details=False,
            details_1='',
            details_1_answer='',
            details_2='',
            details_2_answer='',
            details_3='',
            details_3_answer='',
            details_4='',
            details_4_answer='',
            details_5='',
            details_5_answer='',
            view_count=0,
            item_rating=0,
            review_count=0,
            online=0,
            ad_item=0,
            ad_item_level=0,
            ad_item_timer=now,
        )

        # add image to database
        db.session.add(item)
        db.session.commit()

        return jsonify({
            "status": 'success',
        })
