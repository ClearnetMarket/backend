from ast import Pass
import os
from werkzeug.utils import secure_filename
from app import db
from flask_login import current_user
from app.auth.profileimage.item_image_resizer import imagespider
from app.common.functions import \
    id_generator_picture1

from app import UPLOADED_FILES_DEST_USER, CURRENT_SETTINGS
from app.classes.auth import Auth_User

base_url_prod = 'https://api.freeport.cash/common/user/'
base_url_local = 'http://localhost:5000/common/user/'


def deleteimg_noredirect(id, img):


    user = db.session\
        .query(Auth_User)\
        .filter_by(id=id)\
        .first()
    if user:
        if user.id == current_user.id:
            try:
                specific_folder = str(user.uuid)
            
                spacer = '/'

                pathtofile = str(UPLOADED_FILES_DEST_USER + spacer + specific_folder + spacer + img)
                file_extension = ".jpg"
                ext1 = '_225x'
               
                file0 = str(pathtofile + file_extension)
                file1 = str(pathtofile + ext1 + file_extension)
   
                if len(img) > 20:

                    if user.profileimage == img:
                        user.profileimage = None
                        db.session.add(user)
                        db.session.commit()
                        try:
                            os.remove(file0)
                        except Exception:
                            pass
                        try:
                            os.remove(file1)
                        except Exception:
                            pass
  
                    else:
                        pass
            except Exception:
                pass
        else:
            pass
    else:
        pass



def image1(formdata, user, directory_user_profile):
    id_pic1 = id_generator_picture1()
    # if the form has an image
    if formdata:
        deleteimg_noredirect(id=user.id, img=user.profileimage)
        filename = secure_filename(formdata.filename)
        # saves it to location
        imagepath = os.path.join(directory_user_profile, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic1 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(
            directory_user_profile, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if CURRENT_SETTINGS == 'PRODUCTION':

            if len(formdata.filename) > 2:
                user.profileimage = id_pic1
                user.profileimage_url_250 = base_url_prod + \
                    user.uuid + '/' + id_pic1 + "_225x.jpg"

                db.session.add(user)
                imagespider(base_path=directory_user_profile)
            else:
                user.profileimage = None
        else:

            if len(formdata.filename) > 2:
                user.profileimage = id_pic1
                user.profileimage_url_250 = base_url_local + \
                    user.uuid + '/' + id_pic1 + "_225x.jpg"

                db.session.add(user)
                imagespider(base_path=directory_user_profile)
            else:
                user.profileimage = None
    else:
        # nothing no changes
        if len(user.profileimage) > 5:
            pass
        else:
            # no image change to 0
            user.profileimage = None
