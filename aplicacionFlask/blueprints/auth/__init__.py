from flask import Blueprint


auth_bp = Blueprint('auth', __name__)

print("__________INIT auth____________")

from . import routes
