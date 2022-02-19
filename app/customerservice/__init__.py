# coding=utf-8
from flask import Blueprint


customerservice = Blueprint('customerservice', __name__)


from . import views