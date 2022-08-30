from app import db, ma


class Promoted_Item(db.Model):
    __tablename__ = 'promoted_item'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    itemid = db.Column(db.INTEGER)


class Promoted_Item_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Promoted_Item
    id = ma.auto_field()
    itemid = ma.auto_field()

