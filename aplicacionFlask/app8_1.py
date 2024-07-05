from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image
import os
from io import BytesIO
from werkzeug.datastructures import FileStorage
from validar_contrasena import validar_contrasena
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# from models import Usuario  # Asegúrate de que esto apunta al lugar correcto
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
import datetime
import pyotp
import qrcode
import io


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Configurar la URI de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_TIMEOUT'] = 60  # Aumenta el tiempo de espera a 60 segundos

# app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'



db = SQLAlchemy(app)
mail = Mail(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

s = URLSafeTimedSerializer(app.secret_key)


      
# Resto del código de la aplicación...

  



# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


