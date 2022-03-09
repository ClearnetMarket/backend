from app import db, ma
from uuid import uuid4

def get_uuid_item():
    return uuid4().hex


class Item_ItemtoDelete(db.Model):
    __tablename__ = 'item_to_delete'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True,
                   nullable=False)
    itemid = db.Column(db.Integer)

class Item_ItemtoDelete_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item_ItemtoDelete
    id = ma.auto_field()
    itemid = ma.auto_field()


class Item_MarketItem(db.Model):
    __tablename__ = 'item_market_item'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True,
                   nullable=False)

    uuid = db.Column(db.String(32), default=get_uuid_item)
    online = db.Column(db.INTEGER)
    string_node_id = db.Column(db.VARCHAR(40))
    created = db.Column(db.TIMESTAMP())

    vendor_name = db.Column(db.String(140))
    vendor_id = db.Column(db.INTEGER)

    category_name_0 = db.Column(db.VARCHAR(140))
    category_id_0 = db.Column(db.Integer)

    origin_country = db.Column(db.INTEGER)
    destination_country_one = db.Column(db.INTEGER)
    destination_country_two = db.Column(db.INTEGER)
    destination_country_three = db.Column(db.INTEGER)
    destination_country_four = db.Column(db.INTEGER)
    destination_country_five = db.Column(db.INTEGER)

    item_title = db.Column(db.VARCHAR(500))
    item_count = db.Column(db.INTEGER)
    item_description = db.Column(db.TEXT)
    item_condition = db.Column(db.INTEGER)
    keywords = db.Column(db.VARCHAR(300))

    price = db.Column(db.DECIMAL(20, 2))
    currency = db.Column(db.INTEGER)
    digital_currency_1 = db.Column(db.BOOLEAN)
    digital_currency_2 = db.Column(db.BOOLEAN)
    digital_currency_3 = db.Column(db.BOOLEAN)

    image_one = db.Column(db.VARCHAR(100))
    image_two = db.Column(db.VARCHAR(100))
    image_three = db.Column(db.VARCHAR(100))
    image_four = db.Column(db.VARCHAR(100))
    image_five = db.Column(db.VARCHAR(100))

    shipping_free = db.Column(db.BOOLEAN)
    shipping_two = db.Column(db.BOOLEAN)
    shipping_three = db.Column(db.BOOLEAN)

    shipping_info_0 = db.Column(db.VARCHAR(500))
    shipping_day_0 = db.Column(db.INTEGER)

    shipping_info_2 = db.Column(db.VARCHAR(500))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_2 = db.Column(db.INTEGER)

    shipping_info_3 = db.Column(db.VARCHAR(500))
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_3 = db.Column(db.INTEGER)

    view_count = db.Column(db.INTEGER)
    item_rating = db.Column(db.DECIMAL(20, 2))
    review_count = db.Column(db.INTEGER)
    total_sold = db.Column(db.INTEGER)


    def __str__(self):
        return 'marketitem %s' % self.id

    def __repr__(self):
        return '<Auth_User %r>' % self.username

class Item_MarketItem_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item_MarketItem


    uuid = ma.auto_field()
    online = ma.auto_field()
    created = db.Column(db.TIMESTAMP())
    price = db.Column(db.DECIMAL(20, 2))
    vendor_name = ma.auto_field()
    vendor_id = ma.auto_field()

    string_node_id = ma.auto_field()

    origin_country = ma.auto_field()
    destination_country_one = ma.auto_field()
    destination_country_two = ma.auto_field()
    destination_country_three = ma.auto_field()
    destination_country_four = ma.auto_field()
    destination_country_five = ma.auto_field()

    item_title = ma.auto_field()
    item_count = ma.auto_field()
    item_description = ma.auto_field()
    keywords = ma.auto_field()
    item_condition = ma.auto_field()

    image_one = ma.auto_field()
    image_two = ma.auto_field()
    image_three = ma.auto_field()
    image_four = ma.auto_field()
    image_five = ma.auto_field()



    view_count = ma.auto_field()
    item_rating = ma.auto_field()
    review_count = ma.auto_field()
    total_sold = ma.auto_field()

    shipping_free = ma.auto_field()
    shipping_two = ma.auto_field()
    shipping_three = ma.auto_field()

    shipping_info_0 = ma.auto_field()
    shipping_day_0 = ma.auto_field()

    shipping_info_2 = ma.auto_field()
    shipping_price_2 = ma.auto_field()
    shipping_day_2 = ma.auto_field()

    shipping_info_3 = ma.auto_field()
    shipping_price_3 = ma.auto_field()
    shipping_day_3 = ma.auto_field()



    currency = ma.auto_field()
    digital_currency_1 = ma.auto_field()
    digital_currency_2 = ma.auto_field()
    digital_currency_3 = ma.auto_field()

    # Category_Categories
    category_name_0 = ma.auto_field()
    category_id_0 = ma.auto_field()
