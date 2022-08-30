from app import db, ma


class Achievements_WhichAch(db.Model):
    __tablename__ = 'achievements_which_ach'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    ach1 = db.Column(db.VARCHAR(140))
    ach2 = db.Column(db.VARCHAR(140))
    ach3 = db.Column(db.VARCHAR(140))
    ach4 = db.Column(db.VARCHAR(140))
    ach5 = db.Column(db.VARCHAR(140))

    ach1_cat = db.Column(db.VARCHAR(140))
    ach2_cat = db.Column(db.VARCHAR(140))
    ach3_cat = db.Column(db.VARCHAR(140))
    ach4_cat = db.Column(db.VARCHAR(140))
    ach5_cat = db.Column(db.VARCHAR(140))


class Achievements_WhichAch_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Achievements_WhichAch

    id = ma.auto_field()
    user_id = ma.auto_field()
    ach1 = ma.auto_field()
    ach2 = ma.auto_field()
    ach3 = ma.auto_field()
    ach4 = ma.auto_field()
    ach5 = ma.auto_field()
    ach1_cat = ma.auto_field()
    ach2_cat = ma.auto_field()
    ach3_cat = ma.auto_field()
    ach4_cat = ma.auto_field()
    ach5_cat = ma.auto_field()


class Achievements_UserAchievementsRecent(db.Model):
    __tablename__ = 'achievements_user_achievements_recent'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    username = db.Column(db.VARCHAR(50))

    ach_id = db.Column(db.INTEGER)
    achievement_date = db.Column(db.TIMESTAMP())
    viewed = db.Column(db.INTEGER)


class Achievements_UserAchievementsRecent_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Achievements_UserAchievementsRecent

    id = ma.auto_field()
    user_id = ma.auto_field()
    username = ma.auto_field()
    ach_id = ma.auto_field()
    achievement_date = ma.auto_field()
    viewed = ma.auto_field()


class Achievements_UserAchievements(db.Model):
    __tablename__ = 'achievements_user_achievements'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    username = db.Column(db.VARCHAR(50))
    experiencepoints = db.Column(db.INTEGER)
    level = db.Column(db.INTEGER)

    a1 = db.Column(db.INTEGER)
    a1_date = db.Column(db.TIMESTAMP())
    a2 = db.Column(db.INTEGER)
    a2_date = db.Column(db.TIMESTAMP())
    a3 = db.Column(db.INTEGER)
    a3_date = db.Column(db.TIMESTAMP())
    a4 = db.Column(db.INTEGER)
    a4_date = db.Column(db.TIMESTAMP())
    a5 = db.Column(db.INTEGER)
    a5_date = db.Column(db.TIMESTAMP())
    a6 = db.Column(db.INTEGER)
    a6_date = db.Column(db.TIMESTAMP())
    a7 = db.Column(db.INTEGER)
    a7_date = db.Column(db.TIMESTAMP())
    a8 = db.Column(db.INTEGER)
    a8_date = db.Column(db.TIMESTAMP())
    a9 = db.Column(db.INTEGER)
    a9_date = db.Column(db.TIMESTAMP())

    # exp levels
    e1 = db.Column(db.INTEGER)
    e1_date = db.Column(db.TIMESTAMP())
    e2 = db.Column(db.INTEGER)
    e2_date = db.Column(db.TIMESTAMP())
    e3 = db.Column(db.INTEGER)
    e3_date = db.Column(db.TIMESTAMP())
    e4 = db.Column(db.INTEGER)
    e4_date = db.Column(db.TIMESTAMP())
    e5 = db.Column(db.INTEGER)
    e5_date = db.Column(db.TIMESTAMP())
    e6 = db.Column(db.INTEGER)
    e6_date = db.Column(db.TIMESTAMP())
    e7 = db.Column(db.INTEGER)
    e7_date = db.Column(db.TIMESTAMP())
    e8 = db.Column(db.INTEGER)
    e8_date = db.Column(db.TIMESTAMP())
    e9 = db.Column(db.INTEGER)
    e9_date = db.Column(db.TIMESTAMP())

    # vendor achievs
    v1 = db.Column(db.INTEGER)
    v1_date = db.Column(db.TIMESTAMP())
    v2 = db.Column(db.INTEGER)
    v2_date = db.Column(db.TIMESTAMP())
    v3 = db.Column(db.INTEGER)
    v3_date = db.Column(db.TIMESTAMP())
    v4 = db.Column(db.INTEGER)
    v4_date = db.Column(db.TIMESTAMP())
    v5 = db.Column(db.INTEGER)
    v5_date = db.Column(db.TIMESTAMP())
    v6 = db.Column(db.INTEGER)
    v6_date = db.Column(db.TIMESTAMP())
    v7 = db.Column(db.INTEGER)
    v7_date = db.Column(db.TIMESTAMP())
    v8 = db.Column(db.INTEGER)
    v8_date = db.Column(db.TIMESTAMP())
    v9 = db.Column(db.INTEGER)
    v9_date = db.Column(db.TIMESTAMP())
    v10 = db.Column(db.INTEGER)
    v10_date = db.Column(db.TIMESTAMP())
    v11 = db.Column(db.INTEGER)
    v11_date = db.Column(db.TIMESTAMP())
    v12 = db.Column(db.INTEGER)
    v12_date = db.Column(db.TIMESTAMP())
    v13 = db.Column(db.INTEGER)
    v13_date = db.Column(db.TIMESTAMP())
    v14 = db.Column(db.INTEGER)
    v14_date = db.Column(db.TIMESTAMP())
    v15 = db.Column(db.INTEGER)
    v15_date = db.Column(db.TIMESTAMP())
    v16 = db.Column(db.INTEGER)
    v16_date = db.Column(db.TIMESTAMP())

    # first to do something
    u1 = db.Column(db.INTEGER)
    u1_date = db.Column(db.TIMESTAMP())
    u2 = db.Column(db.INTEGER)
    u2_date = db.Column(db.TIMESTAMP())
    u3 = db.Column(db.INTEGER)
    u3_date = db.Column(db.TIMESTAMP())
    u4 = db.Column(db.INTEGER)
    u4_date = db.Column(db.TIMESTAMP())
    u5 = db.Column(db.INTEGER)
    u5_date = db.Column(db.TIMESTAMP())

    # customer achievs
    c1 = db.Column(db.INTEGER)
    c1_date = db.Column(db.TIMESTAMP())
    c2 = db.Column(db.INTEGER)
    c2_date = db.Column(db.TIMESTAMP())
    c3 = db.Column(db.INTEGER)
    c3_date = db.Column(db.TIMESTAMP())
    c4 = db.Column(db.INTEGER)
    c4_date = db.Column(db.TIMESTAMP())
    c5 = db.Column(db.INTEGER)
    c5_date = db.Column(db.TIMESTAMP())
    c6 = db.Column(db.INTEGER)
    c6_date = db.Column(db.TIMESTAMP())
    c7 = db.Column(db.INTEGER)
    c7_date = db.Column(db.TIMESTAMP())
    c8 = db.Column(db.INTEGER)
    c8_date = db.Column(db.TIMESTAMP())
    c9 = db.Column(db.INTEGER)
    c9_date = db.Column(db.TIMESTAMP())
    c10 = db.Column(db.INTEGER)
    c10_date = db.Column(db.TIMESTAMP())
    c11 = db.Column(db.INTEGER)
    c11_date = db.Column(db.TIMESTAMP())
    c12 = db.Column(db.INTEGER)
    c12_date = db.Column(db.TIMESTAMP())

    # bitcoin achievs
    b1 = db.Column(db.INTEGER)
    b1_date = db.Column(db.TIMESTAMP())
    b2 = db.Column(db.INTEGER)
    b2_date = db.Column(db.TIMESTAMP())
    b3 = db.Column(db.INTEGER)
    b3_date = db.Column(db.TIMESTAMP())
    b4 = db.Column(db.INTEGER)
    b4_date = db.Column(db.TIMESTAMP())
    b5 = db.Column(db.INTEGER)
    b5_date = db.Column(db.TIMESTAMP())


class Achievements_UserAchievements_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Achievements_UserAchievements
    id = ma.auto_field()
    user_id = ma.auto_field()
    username = ma.auto_field()
    experiencepoints = ma.auto_field()
    level = ma.auto_field()

    a1 = ma.auto_field()
    a1_date = ma.auto_field()
    a2 = ma.auto_field()
    a2_date = ma.auto_field()
    a3 = ma.auto_field()
    a3_date = ma.auto_field()
    a4 = ma.auto_field()
    a4_date = ma.auto_field()
    a5 = ma.auto_field()
    a5_date = ma.auto_field()
    a6 = ma.auto_field()
    a6_date = ma.auto_field()
    a7 = ma.auto_field()
    a7_date = ma.auto_field()
    a8 = ma.auto_field()
    a8_date = ma.auto_field()
    a9 = ma.auto_field()
    a9_date = ma.auto_field()

    # exp levels
    e1 = ma.auto_field()
    e1_date = ma.auto_field()
    e2 = ma.auto_field()
    e2_date = ma.auto_field()
    e3 = ma.auto_field()
    e3_date = ma.auto_field()
    e4 = ma.auto_field()
    e4_date = ma.auto_field()
    e5 = ma.auto_field()
    e5_date = ma.auto_field()
    e6 = ma.auto_field()
    e6_date = ma.auto_field()
    e7 = ma.auto_field()
    e7_date = ma.auto_field()
    e8 = ma.auto_field()
    e8_date = ma.auto_field()
    e9 = ma.auto_field()
    e9_date = ma.auto_field()

    # vendor achievs
    v1 = ma.auto_field()
    v1_date = ma.auto_field()
    v2 = ma.auto_field()
    v2_date = ma.auto_field()
    v3 = ma.auto_field()
    v3_date = ma.auto_field()
    v4 = ma.auto_field()
    v4_date = ma.auto_field()
    v5 = ma.auto_field()
    v5_date = ma.auto_field()
    v6 = ma.auto_field()
    v6_date = ma.auto_field()
    v7 = ma.auto_field()
    v7_date = ma.auto_field()
    v8 = ma.auto_field()
    v8_date = ma.auto_field()
    v9 = ma.auto_field()
    v9_date = ma.auto_field()
    v10 = ma.auto_field()
    v10_date = ma.auto_field()
    v11 = ma.auto_field()
    v11_date = ma.auto_field()
    v12 = ma.auto_field()
    v12_date = ma.auto_field()
    v13 = ma.auto_field()
    v13_date = ma.auto_field()
    v14 = ma.auto_field()
    v14_date = ma.auto_field()
    v15 = ma.auto_field()
    v15_date = ma.auto_field()
    v16 = ma.auto_field()
    v16_date = ma.auto_field()

    # first to do something
    u1 = ma.auto_field()
    u1_date = ma.auto_field()
    u2 = ma.auto_field()
    u2_date = ma.auto_field()
    u3 = ma.auto_field()
    u3_date = ma.auto_field()
    u4 = ma.auto_field()
    u4_date = ma.auto_field()
    u5 = ma.auto_field()
    u5_date = ma.auto_field()

    # customer achievs
    c1 = ma.auto_field()
    c1_date = ma.auto_field()
    c2 = ma.auto_field()
    c2_date = ma.auto_field()
    c3 = ma.auto_field()
    c3_date = ma.auto_field()
    c4 = ma.auto_field()
    c4_date = ma.auto_field()
    c5 = ma.auto_field()
    c5_date = ma.auto_field()
    c6 = ma.auto_field()
    c6_date = ma.auto_field()
    c7 = ma.auto_field()
    c7_date = ma.auto_field()
    c8 = ma.auto_field()
    c8_date = ma.auto_field()
    c9 = ma.auto_field()
    c9_date = ma.auto_field()
    c10 = ma.auto_field()
    c10_date = ma.auto_field()
    c11 = ma.auto_field()
    c11_date = ma.auto_field()
    c12 = ma.auto_field()
    c12_date = ma.auto_field()

    # bitcoin achievs
    b1 = ma.auto_field()
    b1_date = ma.auto_field()
    b2 = ma.auto_field()
    b2_date = ma.auto_field()
    b3 = ma.auto_field()
    b3_date = ma.auto_field()
    b4 = ma.auto_field()
    b4_date = ma.auto_field()
    b5 = ma.auto_field()
    b5_date = ma.auto_field()


class Achievements(db.Model):
    __tablename__ = 'achievements_achievements'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    categoryid = db.Column(db.VARCHAR(20))
    categoryname = db.Column(db.VARCHAR(100))
    value = db.Column(db.INTEGER)
    category = db.Column(db.INTEGER)
    title = db.Column(db.String(350))
    description = db.Column(db.VARCHAR(350))
    dateadded = db.Column(db.TIMESTAMP())


class Achievements_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Achievements

    id = ma.auto_field()
    categoryid = ma.auto_field()
    categoryname = ma.auto_field()
    value = ma.auto_field()
    category = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    dateadded = ma.auto_field()