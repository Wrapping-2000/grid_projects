from flask import Blueprint

excel = Blueprint('excel', __name__)

from . import views