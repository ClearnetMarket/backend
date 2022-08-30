# coding=utf-8
from app import db, ma


class Query_AdType(db.Model):
    __tablename__ = 'query_adtype'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_AdType_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_AdType
    id = ma.auto_field()
    value = ma.auto_field()
    text = ma.auto_field()


class Query_WordList(db.Model):
    __tablename__ = 'query_word_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.VARCHAR(100))


class Query_WordList_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_WordList
    id = ma.auto_field()
    text = ma.auto_field()


class Query_Shard(db.Model):
    __tablename__ = 'query_shard'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Shard_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Shard
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_RequestCancel(db.Model):
    __tablename__ = 'query_request_cancel'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_RequestCancel_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_RequestCancel
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_RequestReturn(db.Model):
    __tablename__ = 'query_request_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_RequestReturn_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_RequestCancel
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Return(db.Model):
    __tablename__ = 'query_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Return_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Return
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Margin(db.Model):
    __tablename__ = 'query_margin'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(20, 8))
    text = db.Column(db.VARCHAR(140))


class Query_Margin_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Margin
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_MainSearch(db.Model):
    __tablename__ = 'query_main_search'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_MainSearch_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_MainSearch
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_WebsiteFeedback(db.Model):
    __tablename__ = 'query_website_feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_WebsiteFeedback_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_WebsiteFeedback
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Carriers(db.Model):
    __tablename__ = 'query_carriers'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Carriers_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Carriers
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_CurrencyList(db.Model):
    __tablename__ = 'query_currency_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_CurrencyList_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Carriers
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_CountLow(db.Model):
    __tablename__ = 'query_count_low'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_CountLow_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Carriers
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_PhysDig(db.Model):
    __tablename__ = 'query_phys_or_dig'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_PhysDig_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Carriers
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_ItemOrder(db.Model):
    __tablename__ = 'query_item_order'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemOrder_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_ItemOrder
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_ItemCount(db.Model):
    __tablename__ = 'query_item_count'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemCount_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_ItemCount
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Timer(db.Model):
    __tablename__ = 'query_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Timer_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_ItemCount
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_ItemCondition(db.Model):
    __tablename__ = 'query_item_condition'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemCondition_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_ItemCondition
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Continents(db.Model):
    __tablename__ = 'query_continents'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Continents_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Continents
    id = ma.auto_field()
    text = ma.auto_field()
    value = ma.auto_field()


class Query_Currency(db.Model):
    __tablename__ = 'query_currency'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Integer)
    symbol = db.Column(db.VARCHAR(140))


class Query_Currency_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Currency
    id = ma.auto_field()
    value = ma.auto_field()
    symbol = ma.auto_field()


class Query_Country(db.Model):
    __tablename__ = 'query_countries'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ab = db.Column(db.VARCHAR(10))
    name = db.Column(db.VARCHAR(140))
    value = db.Column(db.INTEGER)


class Query_Country_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Query_Country
    id = ma.auto_field()
    ab = ma.auto_field()
    name = ma.auto_field()
    value = ma.auto_field()
