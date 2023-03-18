from flask import jsonify
from flask_login import current_user
from app.marketitem import marketitem
from app import db

# models
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema
from app.classes.admin import Admin_Flagged


@marketitem.route('/<string:item_id>', methods=['GET'])
def marketitem_item_main(item_id):
    """
    Queues the main item
    :return:
    """
    item_for_sale = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == item_id)\
        .first()
    if not item_for_sale:
        jsonify({"error": "Error:  No Item exists"}), 200
    item_schema = Item_MarketItem_Schema()
    result = item_schema.dump(item_for_sale)

    return jsonify(result), 200


@marketitem.route('/item/flagged/<string:item_id>', methods=['GET'])
def marketitem_item_flagged(item_id):
    """
    Grabs stats of the vendor
    :return:
    """
    flagged_item = db.session\
        .query(Admin_Flagged)\
        .filter_by(listingid=item_id)\
        .first()
    if not flagged_item:
        jsonify({"error": "Error: No flagged items"}), 200

    return jsonify({"success": "success",
                    "item_id": flagged_item.listingid,
                    "item_id_number_reports": flagged_item.howmany,
                    })


@marketitem.route('/info/<string:item_uuid>', methods=['GET'])
def marketitem_item_info_title(item_uuid):
    """
    Grabs stats of the vendor
    :return:
    """
    item_for_sale = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == item_uuid)\
        .first()

    return jsonify({
        "success": "success",
        "item_title": item_for_sale.item_title})


@marketitem.route('/count/<string:item_uuid>', methods=['GET'])
def marketitem_add_view(item_uuid):
    """
    Grabs stats of the vendor
    :return:
    """

    item_for_sale = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == item_uuid)\
        .first()
    if current_user.is_authenticated:
        if item_for_sale.vendor_uuid == current_user.uuid:
            return jsonify({"success": "View Count Not Increased"})
    current_count = item_for_sale.view_count
    new_count = current_count + 1
    item_for_sale.view_count = new_count
    db.session.add(item_for_sale)
    db.session.commit()

    return jsonify({
        "success": "success",
        "item_title": item_for_sale.item_title})
