from app import db
from app.classes.achievements import Achievements_UserAchievements, Achievements_UserAchievementsRecent

from datetime import datetime

# id=14


def likemoneyinthebank(user_id):
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    now = datetime.utcnow()
    if usera.b1 != 1:
        usera.b1 = 1
        usera.b1_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=14,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass

# id=18


def withdrawl(user_id):
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    now = datetime.utcnow()
    if usera.b2 != 1:
        usera.b2 = 1
        usera.b2_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=18,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass
