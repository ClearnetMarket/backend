from flask import request, session, jsonify
from sqlalchemy import or_, func
from app.category import category
from app import db

# models
from app.classes.category import Category_Categories, Category_Categories_Schema
from app.classes.item import Item_MarketItem, Item_MarketItem_Schema

@category.route('/sidebar', methods=['GET'])
def get_categories_sidebar():
    """
    Function grabs category for the sidebar
    :return:
    """
    if request.method == 'GET':

        get_cats = db.session\
            .query(Category_Categories)\
            .filter(Category_Categories.value != 1000, Category_Categories.value != 0)\
            .order_by(Category_Categories.name.asc())\
            .all()
        cats_schema = Category_Categories_Schema(many=True)
        return jsonify(cats_schema.dump(get_cats))


@category.route('/query/index/todayfeatured', methods=['GET'])
def get_categories_today_featured():
    """
    Used on index.  Grabs today's featured items
    :return:
    """
    if request.method == 'GET':
        
        todayfeaturedfull = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.image_one_server != '') \
            .order_by(Item_MarketItem.created.desc()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(todayfeaturedfull))


@category.route('/query/index/electronics', methods=['GET'])
def get_categories_electronics():
    """
    Grabs a category for front page
    Electronics
    :return:
    """
    if request.method == 'GET':
        electronicsfull = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.image_one_server != '') \
            .filter(Item_MarketItem.category_id_0 == 9) \
            .order_by(func.random()) \
            .limit(10)

        category_schema = Category_Categories_Schema(many=True)
        return jsonify(category_schema.dump(electronicsfull))


