from ast import Pass
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
    id_generator_picture5, \
    itemlocation
from app import UPLOADED_FILES_DEST_ITEM
from app.classes.item import \
    Item_MarketItem


def deleteimg_noredirect(id, img):
    try:
        vendoritem = Item_MarketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.uuid)
                    getimagesubfolder = itemlocation(x=id)
                    spacer = '/'

                    pathtofile = str(UPLOADED_FILES_DEST_ITEM + spacer + getimagesubfolder + spacer + specific_folder + spacer + img)
                    print(pathtofile)
                    file_extension = ".jpg"
                    ext1 = '_225x'
                    ext2 = '_500x'
                    file0 = str(pathtofile + file_extension)
                    file1 = str(pathtofile + ext1 + file_extension)


                    if len(img) > 20:

                        if vendoritem.image_one == img:
                            vendoritem.image_one = '0'
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

                        elif vendoritem.image_two == img:
                            vendoritem.image_two = '0'
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

                        elif vendoritem.image_three == img:
                            vendoritem.image_three = '0'
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

                        elif vendoritem.image_four == img:
                            vendoritem.image_four = '0'
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

                        elif vendoritem.image_five == img:
                            vendoritem.image_five = '0'
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
                        else:
                            pass
                except Exception:
                    pass
            else:
                pass
        else:
            pass
    except:
        pass


def image1(formdata, item, directoryifitemlisting):
    id_pic1 = id_generator_picture1()
    # if the form has an image
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.image_one)
        filename = secure_filename(formdata.filename)
        print(f" filename is {filename}")
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
        newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)

        if len(formdata.filename) > 2:
            item.image_one = id_pic1
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.image_one = "0"
    else:
        # nothing no changes
        if len(item.image_one) > 5:
            pass
        else:
            # no image change to 0
            item.image_one = "0"


def image2(formdata, item, directoryifitemlisting):
    id_pic2 = id_generator_picture2()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.image_two)
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
        if len(formdata.filename) > 2:
            item.image_two = id_pic2
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.image_two = "0"
    else:
        if item.image_two:
            if len(item.image_two) > 5:
                pass
        else:
            item.image_two = "0"


def image3(formdata, item, directoryifitemlisting):
    id_pic3 = id_generator_picture3()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.image_three)
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
        if len(formdata.filename) > 5:
            # add profile to db
            item.image_three = id_pic3
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.image_three = "0"

    else:
        if item.image_three is not None:
            if len(item.image_three) > 5:
                pass
        else:
            item.image_three = "0"


def image4(formdata, item, directoryifitemlisting):
    id_pic4 = id_generator_picture4()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.image_four)
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
        if len(formdata.filename) > 2:

            # add profile to db
            item.image_four = id_pic4
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.image_four = "0"
    else:
        if item.image_four:
            if len(item.image_four) > 5:
                pass
        else:
            item.image_four = "0"


def image5(formdata, item, directoryifitemlisting):
    id_pic5 = id_generator_picture5()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.image_five)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic5 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(
            directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if len(formdata.filename) > 2:

            # add profile to db
            item.image_five = id_pic5
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.image_five = "0"
    else:
        if item.image_five:
            if len(item.image_five) > 5:
                pass
        else:
            item.image_five = "0"
