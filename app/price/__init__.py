# coding=utf-8
from flask import Blueprint

price = Blueprint('price', __name__)

from . import views