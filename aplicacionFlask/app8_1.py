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

# Definición del modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=False)
    otp_secret = db.Column(db.String(16), nullable=True)
   

    def __repr__(self):
        return f'<Usuario {self.username}>'
      
# Resto del código de la aplicación...

# Decorador para rutas protegidas (para proteger rutas que requieren autenticación)
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    nombre = "Pablo"
    print("NOMBRE:", nombre)
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']

        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact2.html')

        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact2.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['contrasena']
        user_profile_pic = ""
        user_created_at = datetime.datetime.now()
        user_is_active = True
      
        
    
        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')
          
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado.')
            return render_template('register.html')
          
        try:
            validar_contrasena(password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('register.html')
          
        print("NOMBRE:", username)
        print("CONTRASEÑA:", password)

        # Crear nuevo usuario
        nuevo_usuario = Usuario(username=username, email=email, password=password, profile_pic=user_profile_pic, created_at= user_created_at, is_active=user_is_active)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
         # Enviar correo de verificación
        token = s.dumps(email, salt='email-confirm-salt')
        msg = Message('Confirma tu correo electrónico', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = f'Para activar tu cuenta, haz clic en el siguiente enlace: {link}'
        mail.send(msg)

        flash('Se ha enviado un enlace de verificación a tu correo electrónico.')
        return redirect(url_for('login'))
    return render_template('register.html')
  
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace de verificación ha expirado. Por favor, solicita un nuevo enlace.')
        return redirect(url_for('resend_verification'))
    except Exception as e:
        flash('Enlace de verificación inválido. Por favor, solicita un nuevo enlace.')
        return redirect(url_for('resend_verification'))

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.is_active = True
        db.session.commit()
        flash('Tu cuenta ha sido activada exitosamente.')
    else:
        flash('La verificación de correo falló.')
    return redirect(url_for('login'))

@app.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and not usuario.is_active:
            token = s.dumps(email, salt='email-confirm-salt')
            msg = Message('Confirma tu correo electrónico', sender='your-email@example.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = f'Para activar tu cuenta, haz clic en el siguiente enlace: {link}'
            mail.send(msg)
            flash('Se ha enviado un nuevo enlace de verificación a tu correo electrónico.')
        else:
            flash('Correo electrónico no registrado o cuenta ya activada.')
    return render_template('resend_verification.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']

        usuario = Usuario.query.filter_by(username=username, password=password).first()

        if usuario and usuario.is_active:
            if pyotp.TOTP(usuario.otp_secret).verify(otp):
                session['username'] = username
                flash('Has iniciado sesión exitosamente.')
                return redirect(url_for('profile'))
            else:
                flash('Código OTP inválido.')
        elif usuario and not usuario.is_active:
            flash('Tu cuenta no está activada. Por favor, verifica tu correo electrónico.')
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('login.html')
  
# Añadimos la ruta /logout para cerrar la sesión.
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('home'))
  
@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            token = s.dumps(email, salt='email-reset-salt')
            msg = Message('Restablecer Contraseña', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            link = url_for('reset_token', token=token, _external=True)
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {link}'
            mail.send(msg)
            flash('Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
            return redirect(url_for('login'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.')
            return render_template('reset_request.html')
    return render_template('reset_request.html')
  
@app.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        email = s.loads(token, salt='email-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace de restablecimiento ha expirado.')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios.')
            return render_template('reset_token.html', token=token)

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden.')
            return render_template('reset_token.html', token=token)
          
        try:
            validar_contrasena(new_password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('reset_request.html')

        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = new_password
        db.session.commit()

        flash('Tu contraseña ha sido restablecida exitosamente.')
        return redirect(url_for('login'))

    return render_template('reset_token.html', token=token)
  
# Añadimos la ruta /profile que está protegida por el decorador login_required.
@app.route('/profile')
@login_required
def profile():
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    return render_template('profile.html', usuario=usuario)
  

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario.password != current_password:
            flash('La contraseña actual es incorrecta')
            return render_template('change_password.html')

        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden')
            return render_template('change_password.html')
          
        try:
            validar_contrasena(new_password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('change_password.html')

        usuario.password = new_password
        db.session.commit()

        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('profile'))
    return render_template('change_password.html')
  
@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        db.session.delete(usuario)
        db.session.commit()
        session.pop('username', None)
        flash('Cuenta eliminada exitosamente')
        return redirect(url_for('home'))
    return render_template('delete_account.html')

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']

        if not new_username or not new_email:
            flash('Todos los campos son obligatorios')
            return render_template('update_profile.html')

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if Usuario.query.filter_by(username=new_username).first() and new_username != username:
            flash('El nombre de usuario ya está en uso')
            return render_template('update_profile.html')

        if Usuario.query.filter_by(email=new_email).first() and new_email != usuario.email:
            flash('El correo electrónico ya está en uso')
            return render_template('update_profile.html')

        usuario.username = new_username
        usuario.email = new_email
        db.session.commit()
        session['username'] = new_username

        flash('Perfil actualizado exitosamente')
        return redirect(url_for('profile'))
    return render_template('update_profile.html')
  
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
  
@app.route('/setup_2fa')
@login_required
def setup_2fa():
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario.otp_secret:
        usuario.otp_secret = pyotp.random_base32()
        db.session.commit()

    otp_uri = pyotp.totp.TOTP(usuario.otp_secret).provisioning_uri(username, issuer_name="Your Flask App")
    qr = qrcode.make(otp_uri)
    img = io.BytesIO()
    qr.save(img)
    img.seek(0)

    return send_file(img, mimetype="image/png")


# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


