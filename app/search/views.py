from flask import jsonify
from app import db
from app.search import search
# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema


@search.route('/query/<string:searchstring>/<int:page>', methods=['GET'])
def main_search_results(searchstring, page):
    
    per_page_amount = 50
    if page is None:
        offset_limit = 0
        page = 1
    elif page == 1:
        offset_limit = 0
        page = 1
    else:
        offset_limit = (per_page_amount * page) - per_page_amount
        page = int(page)

    searchstring = str(searchstring)
    search_string = "%{}%".format(searchstring)


    get_market_items = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.item_title.ilike(search_string))\
        .limit(per_page_amount).offset(offset_limit)

    search_schema = Item_MarketItem_Schema(many=True)
    return jsonify(search_schema.dump(get_market_items))


@search.route('/query/count/<string:searchstring>', methods=['GET'])
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
