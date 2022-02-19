# coding=utf-8

from flask import Blueprint

orders = Blueprint('orders', __name__)

from . import views