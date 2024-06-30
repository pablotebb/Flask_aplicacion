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

  
@app.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    if request.method == 'POST' and 'profile_pic' in request.files:
        file = request.files['profile_pic']
        filename = secure_filename(file.filename)
        
        # Guardar el archivo temporalmente
        temp_filepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        file.save(temp_filepath)

        # Redimensionar la imagen
        image = Image.open(temp_filepath)
        image.thumbnail((150, 150))
        # image.save(temp_filepath)

        # Guardar la imagen final
        # final_filepath = photos.save(temp_filepath)
        # os.remove(temp_filepath)  # Eliminar el archivo temporal
        
        # Guardar la imagen redimensionada en un objeto BytesIO
        image_bytes = BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)
        
        # Crear un nuevo objeto FileStorage para la imagen redimensionada
        resized_file = FileStorage(image_bytes, filename=filename, content_type=file.content_type)
        
        # Guardar la imagen final
        final_filepath = photos.save(resized_file)
        print(f'Final filepath: {final_filepath}')  # Agregar esta línea para depuración
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        # Actualizar la base de datos con la ruta del archivo final
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')
  



# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


