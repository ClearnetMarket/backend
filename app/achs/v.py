from app import db
from app.classes.achievements import Achievements_UserAchievements, Achievements_UserAchievementsRecent
from datetime import datetime

# vendor awards
# v1
# id=12


def firstsale(user_id):
    now = datetime.utcnow()
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    if usera.v1 != 1:
        usera.v1 = 1
        usera.v1_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=12,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass


# v2
# id 13
def firsttrade(user_id):
    now = datetime.utcnow()
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    if usera.v2 != 1:
        usera.v2 = 1
        usera.v2_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=13,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass
# v3
# id 17


def obtainedtrustlevel(user_id):
    now = datetime.utcnow()
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    if usera.v3 != 1:
        usera.v3 = 1
        usera.v3_date = now
        addit = Achievements_UserAchievementsRecent(
            user_id=usera.user_id,
            username=usera.username,
            ach_id=17,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass


# v4
# id 11
def becamevendor(user_id):
    now = datetime.utcnow()
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    if usera.v4 != 1:
        usera.v4 = 1
        usera.v4_date = now
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


# customer awards
# id=32-35
def howmanytrades_vendor(user_id, number):
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    now = datetime.utcnow()
    if number >= 10:
        if usera.v11 != 1:
            usera.v11 = 1
            usera.v11_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=36,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 100:
        if usera.v12 != 1:
            usera.v12 = 1
            usera.v12_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=37,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 1000:
        if usera.v13 != 1:
            usera.v13 = 1
            usera.v13_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=38,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 2500:
        if usera.v14 != 1:
            usera.v14 = 1
            usera.v14_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=39,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 5000:
        if usera.v15 != 1:
            usera.v15 = 1
            usera.v15_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=40,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 10300:
        if usera.v16 != 1:
            usera.v16 = 1
            usera.v16_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=41,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass


# customer awards
# id=32-35
def howmanyitemssold_vendor(user_id, number):
    usera = db.session.query(Achievements_UserAchievements).filter_by(
        user_id=user_id).first()
    now = datetime.utcnow()
    if number >= 10:
        if usera.v5 != 1:
            usera.v5 = 1
            usera.v5_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=26,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 100:
        if usera.v6 != 1:
            usera.v6 = 1
            usera.v6_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=27,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 1000:
        if usera.v7 != 1:
            usera.v7 = 1
            usera.v7_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=28,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 2500:
        if usera.v8 != 1:
            usera.v8 = 1
            usera.v8_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=29,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 5000:
        if usera.v9 != 1:
            usera.v9 = 1
            usera.v9_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=30,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
    if number >= 10000:
        if usera.v10 != 1:
            usera.v10 = 1
            usera.v10_date = now
            addit = Achievements_UserAchievementsRecent(
                user_id=usera.user_id,
                username=usera.username,
                ach_id=31,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass
