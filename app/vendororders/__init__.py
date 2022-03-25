# coding=utf-8

from flask import Blueprint

vendororders = Blueprint('vendororders', __name__)

from . import views