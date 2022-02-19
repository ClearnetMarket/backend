# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

vendororders = Blueprint('vendororders', __name__)

from . import views