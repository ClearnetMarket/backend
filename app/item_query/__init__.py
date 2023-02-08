# coding=utf-8

from flask import Blueprint

itemquery = Blueprint('itemquery', __name__)

from . import views