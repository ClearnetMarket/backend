# coding=utf-8

from flask import Blueprint

userdata = Blueprint('userdata', __name__)

from . import views