from app import db
from app.classes.achievements import Achievements_UserAchievements, Achievements_UserAchievementsRecent
from datetime import datetime

# id = 1
# a1 newbie


def newbie(user_id):
    now = datetime.utcnow()
    usera = db.session \
        .query(Achievements_UserAchievements)\
        .filter_by(user_id=user_id)\
        .first()
    usera.a1 = 1
    usera.a1_date = now

    addit = Achievements_UserAchievementsRecent(
        user_id=usera.user_id,
        username=usera.username,
        ach_id=1,
        achievement_date=now,
        viewed=0,
    )
    db.session.add(addit)
    db.session.add(usera)

# id=16
# a2


def Grassisgreeneronmyside(user_id):
    now = datetime.utcnow()
    usera = db.session\
        .query(Achievements_UserAchievements)\
        .filter_by(user_id=user_id)\
        .first()
    if usera.a2 != 1:
        usera.a2 = 1
        usera.a2_date = now

        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=16,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)
