from flask import Blueprint

main_bp = Blueprint('main', __name__)

print("__________INIT main____________")

from . import routes