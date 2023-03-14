from flask import request,  jsonify
from app.item_query import itemquery
from app import db
# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema


@itemquery.route('/query/all', methods=['GET'])
def get_items_all():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    todayfeaturedfull = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.online == 1) \
        .filter(Item_MarketItem.image_one_server != '') \
        .filter(Item_MarketItem.item_count != 0) \
        .order_by(Item_MarketItem.created.desc()) \
        .limit(10)

    item_schema = Item_MarketItem_Schema(many=True)
    return jsonify(item_schema.dump(todayfeaturedfull))


@itemquery.route('/query/todayfeatured', methods=['GET'])
def get_items_today_featured():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    todayfeaturedfull = db.session \
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.online == 1) \
        .filter(Item_MarketItem.image_one_server != '') \
        .filter(Item_MarketItem.item_count != 0) \
        .order_by(Item_MarketItem.created.desc()) \
        .limit(10)

    item_schema = Item_MarketItem_Schema(many=True)
    return jsonify(item_schema.dump(todayfeaturedfull))
