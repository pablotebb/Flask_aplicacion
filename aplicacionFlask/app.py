from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from io import BytesIO
from werkzeug.datastructures import FileStorage
from validar_contrasena import validar_contrasena
from flask_uploads import configure_uploads, patch_request_class
from config import Config
from extensions import db, migrate, mail, photos
import datetime
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)
   
    print("UPLOADED_PHOTOS_DEST: ", app.config["UPLOADED_PHOTOS_DEST"])
    mipath = app.config["UPLOADED_PHOTOS_DEST"]
    print("auth_bp: ", auth_bp)

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
