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
    node = db.Column(db.VARCHAR(40))
    created = db.Column(db.TIMESTAMP())

    vendor_name = db.Column(db.String(140))
    vendor_display_name = db.Column(db.String(140))
    vendor_uuid = db.Column(db.String(140))
    vendor_id = db.Column(db.INTEGER)

    category_name_0 = db.Column(db.VARCHAR(140))
    category_id_0 = db.Column(db.Integer)

    origin_country = db.Column(db.INTEGER)
    origin_country_name = db.Column(db.VARCHAR(150))

    international = db.Column(db.INTEGER)

    item_title = db.Column(db.VARCHAR(500))
    item_count = db.Column(db.INTEGER)
    item_description = db.Column(db.TEXT)
    item_condition = db.Column(db.INTEGER)
    keywords = db.Column(db.VARCHAR(300))

    price = db.Column(db.DECIMAL(20, 2))
    currency = db.Column(db.INTEGER)
    currency_symbol = db.Column(db.VARCHAR(10))

    digital_currency_1 = db.Column(db.BOOLEAN)
    digital_currency_2 = db.Column(db.BOOLEAN)
    digital_currency_3 = db.Column(db.BOOLEAN)
    shipping_free = db.Column(db.BOOLEAN)
    shipping_two = db.Column(db.BOOLEAN)
    shipping_three = db.Column(db.BOOLEAN)

    image_one_server = db.Column(db.VARCHAR(2000))
    image_two_server = db.Column(db.VARCHAR(2000))
    image_three_server = db.Column(db.VARCHAR(2000))
    image_four_server = db.Column(db.VARCHAR(2000))

    image_one_url = db.Column(db.VARCHAR(3000))
    image_two_url = db.Column(db.VARCHAR(3000))
    image_three_url = db.Column(db.VARCHAR(3000))
    image_four_url = db.Column(db.VARCHAR(3000))

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

        fields = ('uuid', 'online', 'created', 'price', 'vendor_name', 'node_id', 'vendor_uuid',
                  'origin_country_name', 'currency_symbol', 'destination_country_one_name',
                  'destination_country_two_name', 'destination_country_three_name',
                  'destination_country_four_name', 'destination_country_five_name',
                  'item_title', 'item_count', 'item_description', 'currency',
                  'item_condition', 'keywords', 'price',
                  'digital_currency_1', 'digital_currency_2', 'digital_currency_3',
                  'image_one_url', 'image_two_url', 'image_three_url', 'image_four_url',
                  'image_one_server', 'image_two_server', 'image_three_server', 'image_four_server',
                  'shipping_free', 'shipping_two', 'shipping_three', 'shipping_info_0', 'shipping_day_0',
                  'shipping_info_2',
                  'shipping_price_2', 'shipping_day_2', 'shipping_info_3', 'shipping_price_3', 'shipping_day_3',
                  'view_count',
                  'item_rating', 'review_count', 'total_sold', 'vendor_display_name'
                  )


item_schema = Item_MarketItem_Schema()
items_schema = Item_MarketItem_Schema(many=True)
