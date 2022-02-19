from flask import url_for, request, session, jsonify

from app.marketitem import marketitem
from app import db

# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema
from app.classes.admin import Admin_Flagged, Admin_Flagged_Schema

@marketitem.route('/item/<string:item_id>', methods=['GET'])
def marketitem_item_main(item_id):
    """
    Queues the main item
    :return:
    """
    if request.method == 'GET':
        item_for_sale = Item_MarketItem.query.get(item_id)
        if item_for_sale:
            item_schema = Item_MarketItem_Schema(many=True)
            return jsonify(item_schema.dump(item_for_sale))
        else:
            jsonify({"error": "Item doesnt exist"}), 401


@marketitem.route('/item/flagged/<string:item_id>', methods=['GET'])
def marketitem_item_flagged(item_id):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':

        flagged_item = Admin_Flagged.query \
        .filter_by(listingid=item_id)\
        .first()
        if flagged_item:
            return jsonify({"item_id": flagged_item.listingid,
                            "item_id_number_reports": flagged_item.howmany,
                            })
        else:
            jsonify({"Error": "No flagged items"}), 401
