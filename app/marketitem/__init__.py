# coding=utf-8

from flask import Blueprint

marketitem = Blueprint('marketitem', __name__)

from . import views