from flask import jsonify
from app import db
from app.search import search
# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema


@search.route('/query/<string:searchstring>', methods=['GET'])
def main_search_results(searchstring):

    searchstring = str(searchstring)

    search_string = "%{}%".format(searchstring)

    get_market_items = db.session\
                        .query(Item_MarketItem)\
                        .filter(Item_MarketItem.item_title.ilike(search_string))\
                        .limit(50)

    search_schema = Item_MarketItem_Schema(many=True)
    return jsonify(search_schema.dump(get_market_items))


@search.route('/query/<string:searchstring>/count', methods=['GET'])
def main_search_results_count(searchstring):

    searchstring = str(searchstring)

    search_string = "%{}%".format(searchstring)

    get_market_items_count = db.session \
                                .query(Item_MarketItem) \
                                .filter(Item_MarketItem.item_title.ilike(search_string))\
                                .count()

    return jsonify({
        "success": "success",
        "count": get_market_items_count})
