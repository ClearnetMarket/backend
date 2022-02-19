from app import db
from app.classes.achievements import Achievements_UserAchievements, Achievements_UserAchievementsRecent
from datetime import datetime


# unique awards
def first1000users(user_id):
    pass


def vendor_become_vendor(user_id):
    now = datetime.utcnow()
    usera = db.session \
        .query(Achievements_UserAchievements) \
        .filter_by(user_id=user_id) \
        .first()
    if usera.v1 != 1:
        # 11
        usera.v1 = 1
        usera.v1_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=11,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass
