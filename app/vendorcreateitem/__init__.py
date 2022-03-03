from flask import Blueprint

vendorcreateitem = Blueprint('vendorcreateitem', __name__)

from . import views