from flask import request,  jsonify
from sqlalchemy import func
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
            .filter(Category_Categories.value != 0)\
            .order_by(Category_Categories.name.asc())\
            .all()
        cats_schema = Category_Categories_Schema(many=True)
        return jsonify(cats_schema.dump(get_cats))


# Electronics
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
            .filter(Item_MarketItem.category_id_0 == 2) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(electronicsfull))


# Apparal
@category.route('/query/index/apparal', methods=['GET'])
def get_categories_apparal():
    """
    Grabs a category for front page
    Electronics
    :return:
    """
    if request.method == 'GET':

        electronicsfull = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 25) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(electronicsfull))


# SmartPhones
@category.route('/query/index/smartphones', methods=['GET'])
def get_categories_smartphone():
    """
    Grabs a category for front page
    SmartPhones
    :return:
    """
    if request.method == 'GET':

        smartphones_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 4) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(smartphones_full))


# Automotive
@category.route('/query/index/automotive', methods=['GET'])
def get_categories_automotive():
    """
    Grabs a category for front page
    automotive
    :return:
    """
    if request.method == 'GET':

        automotive_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 9) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(automotive_full))


# hobbies
@category.route('/query/index/hobbies', methods=['GET'])
def get_categories_hobbies():
    """
    Grabs a category for front page
    hobbies
    :return:
    """
    if request.method == 'GET':

        hobbies_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 8) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(hobbies_full))


# gold
@category.route('/query/index/jewelryandgold', methods=['GET'])
def get_categories_gold():
    """
    Grabs a category for front page
    gold and jewelry
    :return:
    """
    if request.method == 'GET':

        gold_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 22) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(gold_full))


# home and garden
@category.route('/query/index/homegarden', methods=['GET'])
def get_categories_homegarden():
    """
    Grabs a category for front page
    home and garden
    :return:
    """
    if request.method == 'GET':

        home_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 10) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(home_full))


# computers and parts
@category.route('/query/index/computersandparts', methods=['GET'])
def get_categories_computers():
    """
    Grabs a category for front page
    computer
    :return:
    """
    if request.method == 'GET':

        computer_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 12) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(computer_full))


# Book movies
@category.route('/query/index/computersandparts', methods=['GET'])
def get_categories_books():
    """
    Grabs a category for front page
    books and movies
    :return:
    """
    if request.method == 'GET':

        booksandmovies_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 30) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(booksandmovies_full))


# Digital Items
@category.route('/query/index/digital', methods=['GET'])
def get_categories_digital():
    """
    Grabs a category for front page
    digital items
    :return:
    """
    if request.method == 'GET':

        digital_full = db.session \
            .query(Item_MarketItem) \
            .filter(Item_MarketItem.online == 1) \
            .filter(Item_MarketItem.category_id_0 == 100) \
            .order_by(func.random()) \
            .limit(10)

        item_schema = Item_MarketItem_Schema(many=True)
        return jsonify(item_schema.dump(digital_full))
