from flask import Blueprint

user_bp = Blueprint('user', __name__)

print("__________INIT user____________")

from . import routes