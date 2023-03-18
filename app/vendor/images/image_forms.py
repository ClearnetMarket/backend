
import os
from werkzeug.utils import secure_filename
from app import db
from flask_login import current_user
from app.vendor.images.item_image_resizer import imagespider
from app.common.functions import \
    id_generator_picture1, \
    id_generator_picture2, \
    id_generator_picture3, \
    id_generator_picture4, \
    itemlocation
from app import UPLOADED_FILES_DEST_ITEM, ApplicationConfig
from app.classes.item import \
    Item_MarketItem

base_url_prod = 'https://api.freeport.cash/common/item/'
base_url_local = 'http://localhost:5000/common/item/'

def deleteimg_noredirect(id, img):


    vendoritem = db.session\
        .query(Item_MarketItem)\
        .filter_by(id=id)\
        .first()

    if len(img) < 20:
        pass
    else:
        if vendoritem is None:
            pass
        else:
            if vendoritem.vendor_id != current_user.id:
                pass
            else:
                specific_folder = str(vendoritem.uuid)
                getimagesubfolder = itemlocation(x=id)
                spacer = '/'

                pathtofile = str(UPLOADED_FILES_DEST_ITEM + spacer +
                                 getimagesubfolder + spacer +
                                 specific_folder + spacer + img)
                file_extension = ".jpg"
                ext1 = '_225x'
                ext2 = '_500x'
                file0 = str(pathtofile + file_extension)
                file1 = str(pathtofile + ext1 + file_extension)
                file2 = str(pathtofile + ext2 + file_extension)


                if vendoritem.image_one == img:
                    vendoritem.image_one = None
                    db.session.add(vendoritem)
                    db.session.commit()
                    try:
                        os.remove(file0)
                    except Exception:
                        pass
                    try:
                        os.remove(file1)
                    except Exception:
                        pass
                    try:
                        os.remove(file2)
                    except Exception:
                        pass

                elif vendoritem.image_two == img:
                    vendoritem.image_two = None
                    db.session.add(vendoritem)
                    db.session.commit()
                    try:
                        os.remove(file0)
                    except Exception:
                        pass
                    try:
                        os.remove(file1)
                    except Exception:
                        pass
                    try:
                        os.remove(file2)
                    except Exception:
                        pass
                elif vendoritem.image_three == img:
                    vendoritem.image_three = None
                    db.session.add(vendoritem)
                    db.session.commit()
                    try:
                        os.remove(file0)
                    except Exception:
                        pass
                    try:
                        os.remove(file1)
                    except Exception:
                        pass
                    try:
                        os.remove(file2)
                    except Exception:
                        pass
                elif vendoritem.image_four == img:
                    vendoritem.image_four = None
                    db.session.add(vendoritem)
                    db.session.commit()
                    try:
                        os.remove(file0)
                    except Exception:
                        pass
                    try:
                        os.remove(file1)
                    except Exception:
                        pass
                    try:
                        os.remove(file2)
                    except Exception:
                        pass
                elif vendoritem.image_five == img:
                    vendoritem.image_five = None
                    db.session.add(vendoritem)
                    db.session.commit()
                    try:
                        os.remove(file0)
                    except Exception:
                        pass
                    try:
                        os.remove(file1)
                    except Exception:
                        pass
                    try:
                        os.remove(file2)
                    except Exception:
                        pass
                else:
                    pass



def image1(formdata, item, directoryifitemlisting):
    id_pic1 = id_generator_picture1()
    # if the form has an image
    if formdata is None:

        # nothing no changes
        if len(item.image_one_server) > 5:
            pass
        else:
            # no image change to 0
            item.image_one_server = None
    else:
        deleteimg_noredirect(id=item.id, img=item.image_one_server)
        filename = secure_filename(formdata.filename)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic1 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(
            directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if ApplicationConfig.CURRENT_SETTINGS == 'PRODUCTION':
            if len(formdata.filename) > 2:
                item.image_one_server = id_pic1
                item.image_one_url_250 = base_url_prod + \
                    item.uuid + '/' + id_pic1 + "_225x.jpg"
                item.image_one_url_500 = base_url_prod + \
                    item.uuid + '/' + id_pic1 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_one_server = None
        else:
            if len(formdata.filename) > 2:
                item.image_one_server = id_pic1
                item.image_one_url_250 = base_url_local + \
                    item.uuid + '/' + id_pic1 + "_225x.jpg"
                item.image_one_url_500 = base_url_local + \
                    item.uuid + '/' + id_pic1 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_one_server = None



def image2(formdata, item, directoryifitemlisting):
    id_pic2 = id_generator_picture2()
    if formdata is None:
        if item.image_two_server:
            if len(item.image_two_server) > 5:
                pass
        else:
            item.image_two_server = None

    else:
        deleteimg_noredirect(id=item.id, img=item.image_two_server)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic2 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination2 = os.path.join(
            directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination2)

        if ApplicationConfig.CURRENT_SETTINGS == 'PRODUCTION':

            if len(formdata.filename) > 2:
                item.image_two_server = id_pic2
                item.image_two_url_250 = base_url_prod + \
                    item.uuid + '/' + id_pic2 + "_225x.jpg"
                item.image_two_url_500 = base_url_prod + \
                    item.uuid + '/' + id_pic2 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_two_server = None
        else:

            if len(formdata.filename) > 2:
                item.image_two_server = id_pic2
                item.image_two_url_250 = base_url_local + \
                    item.uuid + '/' + id_pic2 + "_225x.jpg"
                item.image_two_url_500 = base_url_local + \
                    item.uuid + '/' + id_pic2 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_two_server = None

def image3(formdata, item, directoryifitemlisting):
    id_pic3 = id_generator_picture3()
    if formdata is None:
        if item.image_three_server is not None:
            if len(item.image_three_server) > 5:
                pass
        else:
            item.image_three_server = None
    else:
        deleteimg_noredirect(id=item.id, img=item.image_three_server)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(
            imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic3 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(
            directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)

        if ApplicationConfig.CURRENT_SETTINGS == 'PRODUCTION':
            if len(formdata.filename) > 2:
                item.image_three_server = id_pic3
                item.image_three_url_250 = base_url_prod + \
                    item.uuid + '/' + id_pic3 + "_225x.jpg"
                item.image_three_url_500 = base_url_prod + \
                    item.uuid + '/' + id_pic3 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_three_server = None
        else:
            if len(formdata.filename) > 2:
                item.image_three_server = id_pic3
                item.image_three_url_250 = base_url_local + \
                    item.uuid + '/' + id_pic3 + "_225x.jpg"
                item.image_three_url_500 = base_url_local + \
                    item.uuid + '/' + id_pic3 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_three_server = None



def image4(formdata, item, directoryifitemlisting):
    id_pic4 = id_generator_picture4()
    if formdata is None:
        if item.image_four_server:
            if len(item.image_four_server) > 5:
                pass
        else:
            item.image_four_server = None
    else:
        deleteimg_noredirect(id=item.id, img=item.image_four_server)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic4 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(
            directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)

        if ApplicationConfig.CURRENT_SETTINGS == 'PRODUCTION':

            if len(formdata.filename) > 2:
                item.image_four_server = id_pic4
                item.image_four_url_250 = base_url_prod + \
                    item.uuid + '/' + id_pic4 + "_225x.jpg"
                item.image_four_url_500 = base_url_prod + \
                    item.uuid + '/' + id_pic4 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_four_server = None
        else:

            if len(formdata.filename) > 2:
                item.image_four_server = id_pic4
                item.image_four_url_250 = base_url_local + \
                    item.uuid + '/' + id_pic4 + "_225x.jpg"
                item.image_four_url_500 = base_url_local + \
                    item.uuid + '/' + id_pic4 + "_500x.jpg"
                db.session.add(item)
                imagespider(base_path=directoryifitemlisting)
            else:
                item.image_four_server = None
