from flask import  jsonify
from flask_login import current_user
from app.vendorcreate import vendorcreate
from app import db, UPLOADED_FILES_DEST_ITEM
import os
from uuid import uuid4
from app.common.functions import mkdir_p
from app.common.decorators import login_required
from app.classes.item import Item_MarketItem, items_schema
import shutil
from app.vendor.item_management.check_online import put_online_allowed


@vendorcreate.route('/itemsforsale/<int:page>', methods=['GET'])
@login_required
def vendorcreate_items_for_sale_query(page):
    """
    Provides the vendors item list.
    :return:
    """
    per_page_amount = 10
    if page is None:
        offset_limit = 0
        page = 1
    elif page == 1:
        offset_limit = 0
        page = 1
    else:
        offset_limit = (per_page_amount * page) - per_page_amount
        page = int(page)
        
    forsale = db.session\
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.vendor_id == current_user.id)\
        .order_by(Item_MarketItem.id.asc())\
        .limit(per_page_amount).offset(offset_limit)

    return items_schema.jsonify(forsale)

@vendorcreate.route('/itemsforsale', methods=['GET'])
@login_required
def vendorcreate_items_for_sale():
    """
    Provides the vendors item list.
    :return:
    """
    change_status = False
    forsale = db.session\
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.vendor_id == current_user.id)\
        .order_by(Item_MarketItem.id.desc())\
        .all()
    for f in forsale:
        check_if_allowed = put_online_allowed(item=f)
        if check_if_allowed is not True:

            f.online = 0
            change_status = True
        # add  to database
        db.session.add(f)
    if change_status is True:
        db.session.commit()
    return items_schema.jsonify(forsale)

@vendorcreate.route('/itemsforsale/count', methods=['GET'])
@login_required
def vendorcreate_items_for_sale_count():
    """
    Provides the vendors item list.
    :return:
    """

    for_sale_count = db.session\
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.vendor_id == current_user.id)\
        .order_by(Item_MarketItem.id.desc())\
        .count()
    if for_sale_count is None:
        return jsonify({'error': 'Error: Could not find Vendor Item.'})

    return jsonify({
        "success": "success",
        'count': for_sale_count})


@vendorcreate.route('/clone-item/<string:uuid>', methods=['GET'])
@login_required
def vendorcreate_clone_item(uuid):
    """
    given an item id, this will create a new folder on storage, and recopy the data with a new id
    :param uuid:
    :return:
    """
    # get item we are cloning
    vendoritem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == uuid)\
        .first()
    if vendoritem is None:
        return jsonify({'error': 'Error: Could not find Vendor Item.'})
    get_uuid_item = uuid4().hex

    if vendoritem.vendor_id != current_user.id:
        return jsonify({'error': 'Error: Incorrect Item Found.'})
    # make sure user doesn't have to many listings
    vendoritem_count = db.session\
        .query(Item_MarketItem)\
        .filter_by(vendor_id=current_user.id)\
        .count()
    if vendoritem_count > 100:
        return jsonify({'error': 'Error: Max Items reached.  Please create a ticket to allow for more items.'})

    item = Item_MarketItem(
        uuid=get_uuid_item,
        online=0,
        node=vendoritem.node,
        created=vendoritem.created,
        vendor_name=vendoritem.vendor_name,
        vendor_display_name=vendoritem.vendor_display_name,
        vendor_uuid=vendoritem.vendor_uuid,
        vendor_id=vendoritem.vendor_id,
        category_name_0=vendoritem.category_name_0,
        category_id_0=vendoritem.category_id_0,
        origin_country=vendoritem.origin_country,
        international=vendoritem.international,
        item_title=vendoritem.item_title,
        item_count=vendoritem.item_count,
        item_description=vendoritem.item_description,
        item_condition=vendoritem.item_condition,
        keywords=vendoritem.keywords,
        price=vendoritem.price,
        currency=vendoritem.currency,
        digital_currency_1=vendoritem.digital_currency_1,
        digital_currency_2=vendoritem.digital_currency_2,
        digital_currency_3=vendoritem.digital_currency_3,
        shipping_free=vendoritem.shipping_free,
        shipping_two=vendoritem.shipping_two,
        shipping_three=vendoritem.shipping_three,
        image_one_server=vendoritem.image_one_server,
        image_two_server=vendoritem.image_two_server,
        image_three_server=vendoritem.image_three_server,
        image_four_server=vendoritem.image_four_server,
        image_one_url_250=vendoritem.image_one_url_250,
        image_two_url_250=vendoritem.image_two_url_250,
        image_three_url_250=vendoritem.image_three_url_250,
        image_four_url_250=vendoritem.image_four_url_250,
        image_one_url_500=vendoritem.image_one_url_250,
        image_two_url_500=vendoritem.image_two_url_250,
        image_three_url_500=vendoritem.image_three_url_250,
        image_four_url_500=vendoritem.image_four_url_250,
        shipping_info_0=vendoritem.shipping_info_0,
        shipping_day_0=vendoritem.shipping_day_0,
        shipping_info_2=vendoritem.shipping_info_2,
        shipping_price_2=vendoritem.shipping_price_2,
        shipping_day_2=vendoritem.shipping_day_2,
        shipping_info_3=vendoritem.shipping_info_3,
        shipping_price_3=vendoritem.shipping_price_3,
        shipping_day_3=vendoritem.shipping_day_3,
        view_count=vendoritem.view_count,
        item_rating=vendoritem.item_rating,
        review_count=vendoritem.review_count,
        total_sold=vendoritem.total_sold,
    )
    # image item to dabase but dont commit yet ..
    db.session.add(item)
    db.session.flush()
    # IMAGES
    # get location of node
    oldirectory = UPLOADED_FILES_DEST_ITEM + '/' + str(vendoritem.node) + '/' + str(vendoritem.uuid) + '/'
    # New Directory
    # get directory of item to be cloned using uuid
    newfolderdir = '/' + str(vendoritem.node) + '/' + str(item.uuid) + '/'
    newdirectory = UPLOADED_FILES_DEST_ITEM + newfolderdir
    # loop over the files and copy them
    # make the directory
    try:
        mkdir_p(path=newdirectory)
        for file_name in os.listdir(oldirectory):
            full_file_name = os.path.join(oldirectory, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, newdirectory)
    except:
        pass
    # query the newly added item, and change the id's accordingly
    item.node = vendoritem.node
    # commit to db
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': 'Success'})


@vendorcreate.route('/delete-item/<string:uuid>', methods=['DELETE'])
@login_required
def vendorcreate_delete_item(uuid):
    """
    Delete all images and the item data from database
    :param uuid:
    :return:
    """
    ext_1 = '_225x.jpg'
    ext_2 = '_500x.jpg'
    file_extension1 = '.jpg'
    vendoritem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == uuid)\
        .first()

    if vendoritem is None:
        return jsonify({'error': 'Error: Couldnt find vendor item.'})
    if vendoritem.vendor_id != current_user.id:
        return jsonify({'error': 'Error: Incorrect item found'})

    # gets the node for the folder
    getitemlocation = str(vendoritem.node)
    # Gets items folder id on server
    specific_folder = str(vendoritem.uuid)
    # returns path of the folder minus extension at end
    if vendoritem.image_one_server:
        pathtofile1 = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                   getitemlocation,
                                   specific_folder,
                                   vendoritem.image_one_server)
        file10 = pathtofile1 + file_extension1
        file11 = pathtofile1 + ext_1
        file12 = pathtofile1 + ext_2
        try:
            os.remove(file10)
        except:
            pass
        try:
            os.remove(file11)
            os.remove(file12)
        except:
            pass

    if vendoritem.image_two_server:
        pathtofile2 = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                   getitemlocation,
                                   specific_folder,
                                   vendoritem.image_two_server)
        file20 = pathtofile2 + file_extension1
        file21 = pathtofile2 + ext_1
        file22 = pathtofile2 + ext_2
        try:
            os.remove(file20)
        except:
            pass
        try:
            os.remove(file21)
            os.remove(file22)
        except:
            pass

    if vendoritem.image_three_server:
        pathtofile3 = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                   getitemlocation,
                                   specific_folder,
                                   vendoritem.image_three_server)
        file30 = pathtofile3 + file_extension1
        file31 = pathtofile3 + ext_1
        file32 = pathtofile3 + ext_2
        try:
            os.remove(file30)
        except:
            pass
        try:
            os.remove(file31)
            os.remove(file32)
        except:
            pass

    if vendoritem.image_four_server:
        pathtofile4 = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                   getitemlocation,
                                   specific_folder,
                                   vendoritem.image_four_server)
        file40 = pathtofile4 + file_extension1
        file41 = pathtofile4 + ext_1
        file42 = pathtofile4 + ext_2
        try:
            os.remove(file40)
        except:
            pass
        try:
            os.remove(file41)
            os.remove(file42)
        except:
            pass
    try:
        pathtofolder = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                    getitemlocation,
                                    specific_folder)
        shutil.rmtree(pathtofolder)
    except:
        pass
    db.session.delete(vendoritem)
    db.session.commit()
    return jsonify({'success': 'Deleted Item Successfully'})

