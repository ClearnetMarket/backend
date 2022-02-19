# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

category = Blueprint('category', __name__)

from . import views