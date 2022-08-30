from flask import url_for, send_from_directory
from app.common import common
from app import UPLOADED_FILES_DEST_ITEM


@common.route('/<path:filename>')
def image_forsale_file(filename):
    try:
        return send_from_directory(UPLOADED_FILES_DEST_ITEM, filename, as_attachment=False)
    except Exception as e:
        print(str(e))
        return url_for('static', filename='images/nobanner.png')
