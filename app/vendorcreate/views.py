from flask import  jsonify
from flask_login import current_user
from app.vendorcreate import vendorcreate

from app import UPLOADED_FILES_DEST, UPLOADED_FILES_DEST_ITEM
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from decimal import Decimal


from app.common.decorators import login_required

from app.classes.auth import Auth_User

from app.classes.item import \
    Item_MarketItem

from app.classes.wallet_bch import *



@vendorcreate.route('/myitems', methods=['GET'])
@login_required
def vendorcreate_items_for_sale():
    """
    Provides the vendors item list.
  
    :return:
    """
    forsale = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == current_user.id)\
        .order_by(Item_MarketItem.total_sold.desc(), Item_MarketItem.online.desc(), Item_MarketItem.id.desc())\
        .all()

    return jsonify({
            "items": forsale
        })


