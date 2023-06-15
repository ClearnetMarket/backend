from app.classes.item import Item_MarketItem
from app.classes.auth import Auth_User
from app import db, UPLOADED_FILES_DEST_USER
from app.common.functions import itemlocation
from flask import send_from_directory
from app.common import common
from app import UPLOADED_FILES_DEST_ITEM
import os


@common.route('/item/<string:uuid>/<path:filename>')
def image_forsale_file(uuid, filename):
    """
    Takes UUID of item and filename 
    """

    get_item_id = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.uuid == uuid)\
        .first()
    try:
        getimagesubfolder = itemlocation(x=get_item_id.id)


    except:
        getimagesubfolder = '1'
    directory_of_file = UPLOADED_FILES_DEST_ITEM

    thefile = os.path.join(getimagesubfolder, uuid, filename)
    

    return send_from_directory(directory=directory_of_file, path=thefile, as_attachment=False)



@common.route('/user/<string:uuid>/<path:filename>')
def image_user_profile_file(uuid, filename):
    """
    Takes UUID of User and  id
    """

    get_user_id = db.session\
        .query(Auth_User)\
        .filter(Auth_User.uuid == uuid)\
        .first()

    getimagesubfolder = itemlocation(x=get_user_id.id)

    directory_of_file = UPLOADED_FILES_DEST_USER

    thefile = os.path.join(getimagesubfolder, uuid, filename)

    return send_from_directory(directory=directory_of_file, path=thefile, as_attachment=False)
