from flask import jsonify

from app.search import search

# models
from app.classes.category import Category_Categories
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema

# LOCAL TO CRYPTOCURRENCY PRICE
@search.route('/query/<string:searchstring>', methods=['GET'])
def btc_price_from_user_currency(searchstring):

    searchstring = str(searchstring)
  
    search = "%{}%".format(searchstring)
    get_market_items = Item_MarketItem.query\
    .filter(Item_MarketItem.item_title.ilike(search))\
    .limit(50)

    search_schema = Item_MarketItem_Schema(many=True)
    return jsonify(search_schema.dump(get_market_items))
