from app.classes.item import Item_MarketItem
from app import UPLOADED_FILES_DEST_ITEM, db
from app.common.functions import itemlocation
from flask import url_for, send_from_directory
from app.common import common
from app import UPLOADED_FILES_DEST_ITEM
import os




@common.route('/<string:uuid>/<path:filename>')
def image_forsale_file(uuid, filename):
    """
    Takes UUID of User and 
    """
    try:
        get_item_id = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.uuid == uuid)\
            .first()

        getimagesubfolder = itemlocation(x=get_item_id.id)
    
        directory_of_file = UPLOADED_FILES_DEST_ITEM
       
        thefile = os.path.join(getimagesubfolder, uuid, filename)
      
        return send_from_directory(directory=directory_of_file, path=thefile, as_attachment=False)
    except Exception as e:
        return "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png"
