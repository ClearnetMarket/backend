from flask import  jsonify
from flask_login import current_user
from app.vendorcreate import vendorcreate
from app import db, UPLOADED_FILES_DEST_ITEM
import os, shutil
from uuid import uuid4
from app.common.functions import mkdir_p
from app.common.decorators import login_required
from app.classes.item import Item_MarketItem, items_schema
import shutil


@vendorcreate.route('/itemsforsale', methods=['GET'])
@login_required
def vendorcreate_items_for_sale():
    """
    Provides the vendors item list.
  
    :return:
    """
    forsale = db.session\
        .query(Item_MarketItem) \
        .filter(Item_MarketItem.vendor_id == current_user.id)\
        .order_by(Item_MarketItem.id.desc())\
        .all()

    return items_schema.jsonify(forsale)


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

    get_uuid_item = uuid4().hex

    if vendoritem:
        if vendoritem.vendor_id == current_user.id:
            # make sure user doesn't have to many listings
            vendoritem_count = db.session\
                .query(Item_MarketItem)\
                .filter_by(vendor_id=current_user.id)\
                .count()
            if vendoritem_count < 100:

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
                    destination_country_one=vendoritem.destination_country_one,
                    destination_country_two=vendoritem.destination_country_two,
                    destination_country_three=vendoritem.destination_country_three,
                    destination_country_four=vendoritem.destination_country_four,
                    destination_country_five=vendoritem.destination_country_five,
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
                    image_one_url=vendoritem.image_one_url,
                    image_two_url=vendoritem.image_two_url,
                    image_three_url=vendoritem.image_three_url,
                    image_four_url=vendoritem.image_four_url,
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
                mkdir_p(path=newdirectory)
                for file_name in os.listdir(oldirectory):
                    full_file_name = os.path.join(oldirectory, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, newdirectory)

                # query the newly added item, and change the id's accordingly
                item.node = vendoritem.node 
                # commit to db
                db.session.add(item)
                db.session.commit()
                return jsonify({'status': 'Success'}) 
            else:
                return jsonify({'error': '100 items max'}) 
        else:
            return jsonify({'error': 'error'}) 
    else:
        return jsonify({'error': 'error'}) 
     

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
    if vendoritem:
        if vendoritem.vendor_id == current_user.id:
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

            pathtofolder = os.path.join(UPLOADED_FILES_DEST_ITEM,
                                        getitemlocation,
                                        specific_folder)
            shutil.rmtree(pathtofolder)

            db.session.delete(vendoritem)
            db.session.commit()
            return jsonify({'status': 'Deleted Item'}) 
        else:
            return jsonify({'error': 'error'})  
    else:
        return jsonify({'error': 'error'}) 
