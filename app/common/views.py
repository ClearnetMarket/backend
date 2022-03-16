from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import current_user
from app.common import common
from app import db, UPLOADED_FILES_DEST_USER, UPLOADED_FILES_DEST_ITEM


@common.route('/<path:filename>')
def image_forsale_file(filename):
    try:
        return send_from_directory(UPLOADED_FILES_DEST_ITEM, filename, as_attachment=False)
    except:
        return url_for('static', filename='images/nobanner.png')
