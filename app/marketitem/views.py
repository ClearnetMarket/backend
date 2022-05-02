from flask import url_for, request, session, jsonify

from app.marketitem import marketitem
from app import db

# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema
from app.classes.admin import Admin_Flagged, Admin_Flagged_Schema

@marketitem.route('/<string:item_id>', methods=['GET'])
def marketitem_item_main(item_id):
    """
    Queues the main item
    :return:
    """
    if request.method == 'GET':
        item_for_sale = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.uuid == item_id)\
            .first()
        if item_for_sale:
            item_schema = Item_MarketItem_Schema()
            result = item_schema.dump(item_for_sale)
            return jsonify(result), 200
        else:
            jsonify({"Error": "No Item exists"}), 404

@marketitem.route('/item/flagged/<string:item_id>', methods=['GET'])
def marketitem_item_flagged(item_id):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':

        flagged_item = db.session\
            .query(Admin_Flagged)\
            .filter_by(listingid=item_id)\
            .first()
        if flagged_item:
            return jsonify({"item_id": flagged_item.listingid,
                            "item_id_number_reports": flagged_item.howmany,
                            })
        else:
            jsonify({"Error": "No flagged items"}), 401


@marketitem.route('/info/<string:item_uuid>', methods=['GET'])
def marketitem_item_info_title(item_uuid):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':
        item_for_sale = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.uuid == item_uuid)\
            .first()
    
        return jsonify({"item_title": item_for_sale.item_title})


@marketitem.route('/count/<string:item_uuid>', methods=['GET'])
def marketitem_add_view(item_uuid):
    """
    Grabs stats of the vendor
    :return:
    """
    if request.method == 'GET':
        item_for_sale = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.uuid == item_uuid)\
            .first()
        current_count = item_for_sale.view_count
        new_count = current_count + 1
        item_for_sale.view_count = new_count
        db.session.add(item_for_sale)
        db.session.commit()

        return jsonify({"item_title": item_for_sale.item_title})
