from flask import Flask, Blueprint, app, render_template, request, flash, redirect, send_file, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image
from . import user_bp
from extensions import db
from models import Usuario
from validar_contrasena import validar_contrasena
# from config import Config
import os
from io import BytesIO
from app import photos
import pyotp
import qrcode
import io
from config import Config


app3 = Flask(__name__)
app3.config.from_object(Config)

print("____________________USER ROUTES____________________")

# user_bp = Blueprint('user', __name__)

# Decorador para rutas protegidas (para proteger rutas que requieren autenticación)
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
  

# Añadimos la ruta /profile que está protegida por el decorador login_required.
@user_bp.route('/profile')
@login_required
def profile():
  
    print(f"""
    ----------
    /PROFILE
    ----------
    """)
    
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    
    print(f"""
    ------------------------------------------------------------------------
    username = session['username'] => {username} 
    usuario = Usuario.query.filter_by(username=username).first() => {usuario}
    ------------------------------------------------------------------------
    """)
    
    return render_template('profile.html', usuario=usuario)

@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    print(f"""
    ----------------
    /change_password
    ----------------
    """)
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        print(f"""
        -------------------------------------
        current_password = {current_password}
        new_password = {new_password}
        confirm_password = {confirm_password}      
        -------------------------------------
        """)

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        
        print(f"""
        -----------------------------------------------------------
        username = session['username'] => {username}
        usuario = Usuario.query.filter_by(username=username).first() => {usuario}
        usuario.password = {usuario.password}
        -----------------------------------------------------------
        """)
        

        if usuario.password != current_password:
            flash('La contraseña actual es incorrecta')
            return render_template('change_password.html')
          
        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden')
            return render_template('change_password.html')

        try:
            validar_contrasena(new_password)
        except ValueError as e:
            flash(e)
            return render_template('change_password.html')

        usuario.password = new_password
        print(f"""
        -------------------------------------
        usuario.password = {usuario.password}
        -------------------------------------
        """)
        db.session.commit()

        flash('Contraseña actualizada con éxito')
        return redirect(url_for('user.profile'))
    return render_template('change_password.html')

@user_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():

    print(f"""
    ----------------
    /delete_account
    ----------------
    """)
  
    if request.method == 'POST':
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        
        print(f"""
        ------------------------------------------------------------
        username = session['username'] => {username}
        usuario = Usuario.query.filter_by(username=username).first() => {usuario}
        ------------------------------------------------------------
        """)

        db.session.delete(usuario)
        print(f"""
        --------------------------
        db.session.delete(usuario)
        --------------------------
        """)
        db.session.commit()
        session.pop('username', None)
        print(f"""
        -----------------------------
        session.pop('username', None)
        -----------------------------
        """)
        flash('Cuenta eliminada exitosamente')
        return redirect(url_for('main.home'))
    return render_template('delete_account.html')
  
  

# NO SALE
@user_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
  
    print(f"""
    ----------------
    /update_profile
    ----------------
    """)
  
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        
        print(f"""
        ------------------------------
        new_username = {new_username}
        new_email    = {new_email}      
        ------------------------------
        """)

        if not new_username or not new_email:
            flash('Todos los campos son obligatorios')
            return render_template('update_profile.html')

        sesion_username = session['username']
        usuario = Usuario.query.filter_by(username=sesion_username).first()
        
        print(f"""
        ------------------------------------------------------------------
        sesion_username = session['username'] => {sesion_username}
        usuario = Usuario.query.filter_by(username=sesion_username).first() => {usuario}
        ------------------------------------------------------------------
        """)
        
        print(f"""
        ------------------------------------------------------------------
        Usuario.query.filter_by(username=new_username).first() = {Usuario.query.filter_by(username=new_username).first()}
        Usuario.query.filter_by(email=new_email).first() = {Usuario.query.filter_by(email=new_email).first()}
        ------------------------------------------------------------------
        """)
        
        if Usuario.query.filter_by(username=new_username).first() and new_username != sesion_username:
            flash('El nombre de usuario ya está en uso')
            return render_template('update_profile.html')

        if Usuario.query.filter_by(email=new_email).first() and new_email != usuario.email:
            flash('El correo electrónico ya está en uso')
            return render_template('update_profile.html')

        usuario.username = new_username
        usuario.email = new_email
        
        print(f"""
        -------------------------------------
        usuario.username = {usuario.username}
        usuario.email = {usuario.email}
        -------------------------------------
        """)
        
        db.session.commit()
        session['username'] = new_username
        
        print(f"""
        -----------------------------------------------------------
        session['username'] = new_username => {session['username']}
        -----------------------------------------------------------
        """)

        flash('Perfil actualizado exitosamente')
        return redirect(url_for('user.profile'))
    return render_template('update_profile.html')
  
@user_bp.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    print(f"""
    --------------------
    /upload_profile_pic
    -------------------
    """)
    if request.method == 'POST' and 'profile_pic' in request.files:
        file = request.files['profile_pic']
        filename = secure_filename(file.filename)
        
        print(f"""
        ------------------------------------------------------
        file = request.files['profile_pic'] => {file}
        filename = secure_filename(file.filename) => {filename}
        ------------------------------------------------------
        """)
        
        # Guardar el archivo temporalmente
        temp_filepath = os.path.join(app3.config['UPLOADED_PHOTOS_DEST'], filename)
        print(f"""
        ------------------------------------------------------
         temp_filepath = os.path.join(app3.config['UPLOADED_PHOTOS_DEST'], filename) => {temp_filepath}
        ------------------------------------------------------
        """)
        file.save(temp_filepath)
        
        

        # Redimensionar la imagen
        image = Image.open(temp_filepath)
        print(f"""
        ------------------------------------------------------
        image = Image.open(temp_filepath) => {image}
        ------------------------------------------------------
        """)
        
        image.thumbnail((150, 150))
        # image.save(temp_filepath)

        # Guardar la imagen final
        # final_filepath = photos.save(temp_filepath)
        # osNaNpxove(temp_filepath)  # Eliminar el archivo temporal
        
        # Guardar la imagen redimensionada en un objeto BytesIO
        image_bytes = BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)
        
        # Crear un nuevo objeto FileStorage para la imagen redimensionada
        resized_file = FileStorage(image_bytes, filename=filename, content_type=file.content_type)
        
        print(f"""
        ----------------------------------------------------------
        resized_file = FileStorage(image_bytes, filename=filename, content_type=file.content_type) => {resized_file}
        ----------------------------------------------------------
        """)
        
        # Guardar la imagen final
        final_filepath = photos.save(resized_file)
        print(f"""
        ----------------------------------------------------------
        final_filepath = photos.save(resized_file) => {final_filepath}
        ----------------------------------------------------------
        """)
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        # Actualizar la base de datos con la ruta del archivo final
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        print(f"""
        ----------------------------------------------------------
        username = session['username'] => {username}
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath => {usuario}
        ----------------------------------------------------------
        """)
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('user.profile'))
    return render_template('upload_profile_pic.html')
  

@user_bp.route('/setup_2fa')
@login_required
def setup_2fa():
    print(f"""
    --------------------
    /setup_2fa
    -------------------
    """)
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    
    print(f"""
    ----------------------------------------------------------
    username = session['username'] => {username}
    usuario = Usuario.query.filter_by(username=username).first() _ 
    => {usuario}
    usuario.otp_secret = {usuario.otp_secret}
    ----------------------------------------------------------
    """)

    if not usuario.otp_secret:
        usuario.otp_secret = pyotp.random_base32()
        print(f"""
        ----------------------------------------------------------
        usuario.otp_secret = pyotp.random_base32() => {usuario.otp_secret}
        ----------------------------------------------------------
        """)

        db.session.commit()

    otp_uri = pyotp.totp.TOTP(usuario.otp_secret).provisioning_uri(username, issuer_name="Your Flask App")
    qr = qrcode.make(otp_uri)
    img = io.BytesIO()
    print(f"""
    ----------------------------------------------------------
    otp_uri = pyotp.totp.TOTP(usuario.otp_secret).provisioning_uri(username, issuer_name="Your Flask App")
    qr = qrcode.make(otp_uri)
    img = io.BytesIO()
                        -----
    otp_uri = {otp_uri}
    qr = {qr}
    img = {img}
    ----------------------------------------------------------
    """)
    qr.save(img)
    img.seek(0)

    return send_file(img, mimetype="image/png")