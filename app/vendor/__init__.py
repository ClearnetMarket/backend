# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

vendor = Blueprint('vendor', __name__)

from . import views