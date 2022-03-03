from flask import Blueprint

vendorcreate = Blueprint('vendorcreate', __name__)
from . import views