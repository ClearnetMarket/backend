from app import db, ma


class Category_Categories(db.Model):
    __tablename__ = 'category_categories'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=False)
    cat_id = db.Column(db.VARCHAR(300))
    name = db.Column(db.VARCHAR(300))
    cat_icon = db.Column(db.VARCHAR(30))


class Category_Categories_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category_Categories
        fields = ('id', 'cat_id', 'name', 'cat_icon')
    id = ma.auto_field()
    cat_id = ma.auto_field()
    name = ma.auto_field()
    cat_icon = ma.auto_field()
