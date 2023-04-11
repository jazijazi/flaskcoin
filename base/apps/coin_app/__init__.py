from flask import Blueprint

coins = Blueprint('coins' , __name__ , url_prefix='/')

from . import views
from . import models