
from flask import request, jsonify
from flask_login import current_user
from app.vendorcreateitem import vendorcreateitem
from app import UPLOADED_FILES_DEST_ITEM
import os
from datetime import datetime
import shutil
from app.common.decorators import login_required
from app.common.functions import mkdir_p, itemlocation
# models
from app.classes.item import Item_MarketItem
from app.classes.auth import Auth_User
from app.classes.models import *
from app.classes.category import Category_Categories, Category_Categories_Schema
from app.vendor.images.image_forms import image1, image2, image3, image4


@vendorcreateitem.route('/query/country', methods=['GET'])
def vendorcreateitem_get_country_list():
    """
    Returns list of Countrys
    :return:
    """
    if request.method == 'GET':
        country_list = Query_Country.query.order_by(
            Query_Country.name.asc()).all()
        country_schema = Query_Country_Schema(many=True)
        return jsonify(country_schema.dump(country_list))


@vendorcreateitem.route('/query/currency', methods=['GET'])
def vendorcreateitem_get_currency_list():
    """
    Returns list of currencys 
    :return:
    """
    if request.method == 'GET':
        currency_list = Query_CurrencyList.query.order_by(
            Query_CurrencyList.value.asc()).all()
        currency_schema = Query_CurrencyList_Schema(many=True)

        return jsonify(currency_schema.dump(currency_list))


@vendorcreateitem.route('/query/condition', methods=['GET'])
def vendorcreateitem_get_item_condition_list():
    """
    Returns list of item condition 
    :return:
    """
    if request.method == 'GET':

        condition_list = Query_ItemCondition.query.order_by(
            Query_ItemCondition.value.asc()).all()
        condition_schema = Query_ItemCondition_Schema(many=True)

        return jsonify(condition_schema.dump(condition_list))


@vendorcreateitem.route('/query/category', methods=['GET'])
def vendorcreateitem_get_item_category_list():
    """
    Returns list of item category 
    :return:
    """
    if request.method == 'GET':
        category_list = Category_Categories.query.order_by(
            Category_Categories.name.asc()).all()
        category_schema = Category_Categories_Schema(many=True)

        return jsonify(category_schema.dump(category_list))


@vendorcreateitem.route('/create-item', methods=['GET'])
@login_required
def create_item():
    if request.method == 'GET':
        now = datetime.utcnow()
        see_if_empty_item = Item_MarketItem.query\
            .filter(Item_MarketItem.vendor_id == current_user.id, Item_MarketItem.item_title == '')\
            .first()

        if see_if_empty_item:
            return jsonify({"status": 'success',
                            'item_id': see_if_empty_item.uuid})
        else:
            createnewitemtemp = Item_MarketItem(
                created=now,
                node=1,
                vendor_name=current_user.username,
                vendor_id=current_user.id,
                vendor_uuid=current_user.uuid,
                vendor_display_name=current_user.display_name,
                item_title='',
                item_count=0,
                item_description='',
                item_condition=0,
                keywords='',
                category_name_0='',
                category_id_0=0,

                price=0,
                currency=current_user.currency,
                currency_symbol='',
                digital_currency_1=0,
                digital_currency_2=0,
                digital_currency_3=0,

                shipping_free=False,
                shipping_two=False,
                shipping_three=False,
                shipping_day_0=0,
                shipping_info_free='',

                shipping_price_2=0,
                shipping_day_2=0,
                shipping_info_2='',
                shipping_price_3=0,
                shipping_info_3='',
                shipping_day_3=0,
                image_one_url=None,
                image_two_url=None,
                image_three_url=None,
                image_four_url=None,


                image_one_server=None,
                image_two_server=None,
                image_three_server=None,
                image_four_server=None,


                origin_country=current_user.country,
                origin_country_name='',
                destination_country_one=0,
                destination_country_one_name='',
                destination_country_two=0,
                destination_country_two_name='',
                destination_country_three=0,
                destination_country_three_name='',
                destination_country_four=0,
                destination_country_four_name='',

                view_count=0,
                item_rating=0,
                review_count=0,
                online=0,
                total_sold=0
            )
            db.session.add(createnewitemtemp)
            db.session.commit()

            getimagesubfolder = itemlocation(x=createnewitemtemp.id)
            directoryifitemlisting = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(createnewitemtemp.uuid)))
            mkdir_p(path=directoryifitemlisting)

            return jsonify({"status": 'success',
                            'item_id': createnewitemtemp.uuid})


@vendorcreateitem.route('/create-item-main/<string:uuid>', methods=['POST'])
def create_item_info(uuid):
    """
    Creates the Vendor Item
    """

    now = datetime.utcnow()
    item = Item_MarketItem.query\
        .filter(Item_MarketItem.uuid == uuid, Item_MarketItem.vendor_id == current_user.id) \
        .first()

    get_currency_symbol = Query_Currency.query.filter(
        Query_Currency.value == current_user.currency).first()
    currency_symbol = get_currency_symbol.name
    # accept bitcoin
    digital_currency_1 = request.json["digital_currency_1"]
    if digital_currency_1 == '':
        digital_currency_1 = False

    # accept bitcoin cash
    digital_currency_2 = request.json["digital_currency_2"]
    if digital_currency_2 == '':
        digital_currency_2 = False

    # accept monero
    digital_currency_3 = request.json["digital_currency_3"]
    if digital_currency_3 == '':
        digital_currency_3 = False
    # Free shipping toggle
    free_shipping = request.json["free_shipping"]

    if free_shipping == '':
        free_shipping = False

    shipping_2 = request.json["shipping_2"]
    if shipping_2 == '':
        shipping_2 = False

    shipping_3 = request.json["shipping_3"]
    if shipping_3 == '':
        shipping_3 = False

    title = request.json["item_title"]
    # Item Condition Query
    if request.json["item_condition"] == '':
        return jsonify({"status": 'error'})
    else:
        item_condition = request.json["item_condition"]
        item_condition = item_condition

    # Item Count
    item_count = request.json["item_count"]
    item_count = int(item_count)
    if item_count > 0:
        item_count = int(item_count)
    else:
        return jsonify({"status": 'error'})

    # Category
    if request.json["category_id_0"] == '':
        get_category_query = None
        category_value = None
        category_name = None
        return jsonify({"status": 'error', })
    else:
        category = request.json["category_id_0"]
        get_category_query = Category_Categories.query\
            .filter(Category_Categories.value == category)\
            .first_or_404()
        category_value = get_category_query.value
        category_name = get_category_query.name

    # Price
    price = request.json["price"]

    # Keywords
    keywords = request.json["keywords"]

    # Free shipping days
    free_shipping_days = request.json["free_shipping_days"]
    if free_shipping_days == '':
        free_shipping_days = 0

    # Shipping two days
    shipping_2_days = request.json["shipping_2_days"]
    if shipping_2_days == '':
        shipping_2_days = 0
    # Shipping two price
    shipping_2_price = request.json["shipping_2_price"]
    if shipping_2_price == '':
        shipping_2_price = 0

    # Shipping three days
    shipping_3_days = request.json["shipping_3_days"]
    if shipping_3_days == '':
        shipping_3_days = 0
    # Shipping three price
    shipping_3_price = request.json["shipping_3_price"]
    if shipping_3_price == '':
        shipping_3_price = 0

    # Shipping to Country One
    if request.json["shipping_to_country_one"] == '':
        shipping_to_country_one = 1000
    else:
        shipping_to_country_one = request.json["shipping_to_country_one"]

        get_name_country_one = Query_Country.query\
            .filter(Query_Country.value == shipping_to_country_one)\
            .first()
        shipping_to_country_one_name = get_name_country_one.name

    # Shipping to Country two
    if request.json["shipping_to_country_two"] == '':
        shipping_to_country_two = 0
    else:
        shipping_to_country_two = request.json["shipping_to_country_two"]
        get_name_country_two = Query_Country.query\
            .filter(Query_Country.value == shipping_to_country_two)\
            .first()
        shipping_to_country_two_name = get_name_country_two.name

    # Shipping to Country One
    if request.json["shipping_to_country_three"] == '':
        shipping_to_country_three = 0
    else:
        shipping_to_country_three = request.json["shipping_to_country_three"]
        get_name_country_three = Query_Country.query\
            .filter(Query_Country.value == shipping_to_country_three)\
            .first()
        shipping_to_country_three_name = get_name_country_three.name

    # Shipping to Country four
    if request.json["shipping_to_country_four"] == '':
        shipping_to_country_four = 0
    else:
        shipping_to_country_four = request.json["shipping_to_country_four"]
        get_name_country_four = Query_Country.query\
            .filter(Query_Country.value == shipping_to_country_four)\
            .first()
        shipping_to_country_four_name = get_name_country_four.name

    item_description = request.json["item_description"]

    # Shipping info
    shipinfofree = f'Takes {free_shipping_days} days for Free'
    shipinfo2 = f'Takes {shipping_2_days} days for {shipping_2_price}{currency_symbol}'
    shipinfo3 = f'Takes {shipping_3_days} days for {shipping_3_price}{currency_symbol}'

    # create image of item in database
    item = Item_MarketItem.query\
        .filter(Item_MarketItem.uuid == uuid, Item_MarketItem.vendor_id == current_user.id)\
        .first()



    item.created = now
    item.vendor_name = current_user.username
    item.vendor_id = current_user.id
    item.vendor_uuid = current_user.uuid
    item.vendor_display_name = current_user.display_name
    item.item_title = title
    item.item_count = item_count
    item.item_description = item_description
    item.item_condition = item_condition
    item.keywords = keywords
    item.category_name_0 = category_name
    item.category_id_0 = category_value
    item.price = price
    item.currency = current_user.currency
    item.currency_symbol = currency_symbol,
    item.digital_currency_1 = digital_currency_1
    item.digital_currency_2 = digital_currency_2
    item.digital_currency_3 = digital_currency_3
    item.shipping_free = free_shipping
    item.shipping_two = shipping_2
    item.shipping_three = shipping_3
    item.shipping_day_0 = free_shipping_days
    item.shipping_info_0 = shipinfofree
    item.shipping_price_2 = shipping_2_price
    item.shipping_day_2 = shipping_2_days
    item.shipping_info_2 = shipinfo2
    item.shipping_price_3 = shipping_3_price
    item.shipping_day_3 = shipping_3_days
    item.shipping_info_3 = shipinfo3
    item.destination_country_one = shipping_to_country_one
    item.destination_country_one_name = shipping_to_country_one_name
    item.destination_country_two = shipping_to_country_two
    item.destination_country_two_name = shipping_to_country_two_name
    item.destination_country_three = shipping_to_country_three
    item.destination_country_three_name = shipping_to_country_three_name
    item.destination_country_four = shipping_to_country_four
    item.destination_country_four_name = shipping_to_country_four_name

    # add  to database
    db.session.add(item)
    db.session.commit()

    getimagesubfolder = itemlocation(x=item.id)
    directoryifitemlisting = os.path.join(
        UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(item.uuid)))
    mkdir_p(directoryifitemlisting)
    return jsonify({"status": 'success'}), 200


@vendorcreateitem.route('/create-item-images/<string:uuid>', methods=['POST', 'OPTIONS'])
def create_item_images(uuid):
    """
    Creates the Vendor Item
    """
    # next, try to login using Basic Auth
    api_key_auth = request.headers.get('Authorization')
    if api_key_auth:
        api_key = api_key_auth.replace('bearer ', '', 1)
        current_user = Auth_User.query.filter_by(api_key=api_key).first()
        see_if_user_allowed = Item_MarketItem.query.filter(
            Item_MarketItem.uuid == uuid, Item_MarketItem.vendor_id == current_user.id).first() is not None
        if see_if_user_allowed:

            item = Item_MarketItem.query\
                .filter(Item_MarketItem.uuid == uuid, Item_MarketItem.vendor_id == current_user.id) \
                .first()
            # node location
            getimagesubfolder = itemlocation(x=item.id)
            item.node = getimagesubfolder
            # directory of image
            directoryifitemlisting = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(item.uuid)))
            # create the image
            mkdir_p(directoryifitemlisting)

            try:
                image_main = request.files['image_main']

                image1(formdata=image_main, item=item,
                       directoryifitemlisting=directoryifitemlisting)
            except Exception as e:
                pass

            try:
                image_two = request.files['image_two']
                image2(formdata=image_two, item=item,
                       directoryifitemlisting=directoryifitemlisting)
            except Exception as e:
                pass

            try:
                image_three = request.files['image_three']
                image3(formdata=image_three, item=item,
                       directoryifitemlisting=directoryifitemlisting)
            except Exception as e:
                pass

            try:
                image_four = request.files['image_four']
                image4(formdata=image_four,  item=item,
                       directoryifitemlisting=directoryifitemlisting)
            except Exception as e:
                pass

            db.session.add(item)
            db.session.commit()

            return jsonify({"status": 'success'})
        else:
            return jsonify({"error": 'no_api_key'})
    else:
        return jsonify({"error": 'no_api_key'})


@vendorcreateitem.route('/delete-image/<string:uuid>/<string:imagename>', methods=['DELETE'])
@login_required
def delete_item_images(uuid, imagename):
    """
    gets specific id and image, it will delete on the server accordingly
    :param id:
    :param img:
    :return:
    """
    item = db.session.query(Item_MarketItem).filter_by(uuid=uuid).first()
    if item:
        if item.vendor_id == current_user.id:
            # get folder for item id
            specific_folder = str(item.uuid)
            # get node location
            getitemlocation = itemlocation(x=item.id)
            # get path of item on folder
            pathtofile = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, imagename)

            ext_1 = '_225x.jpg'
            ext_2 = '_500x.jpg'
            file0 = pathtofile + ".jpg"
            file1 = pathtofile + ext_1
            file2 = pathtofile + ext_2

            if len(imagename) > 20:
                if item.image_one_server == imagename:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_one_server = None
                    item.image_one_url = None
                    db.session.add(item)
                    db.session.commit()
                if item.image_two_server == imagename:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_two_server = None
                    item.image_two_url = None
                    db.session.add(item)
                    db.session.commit()
                if item.image_three_server == imagename:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_three_server = None
                    item.image_three_url = None
                    db.session.add(item)
                    db.session.commit()
                if item.image_four_server == imagename:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_four_server = None
                    item.image_four_url = None
                    db.session.add(item)
                    db.session.commit()

                return jsonify({"status": 'Image Deleted'})
            else:
                return jsonify({"error": 'No Images match description'})
        else:
            return jsonify({"error": 'Not Authorized'})
    else:
        return jsonify({"error": 'Large Error'})
