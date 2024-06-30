from sqlite3 import IntegrityError
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import auth_bp
from extensions import db, mail
from models import Usuario
from validar_contrasena import validar_contrasena
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
import datetime
import pyotp
from werkzeug.exceptions import BadRequestKeyError
# import qrcode

# auth_bp = Blueprint('auth', __name__)


print("AUTH ROUTES")
print("auth_bp: ", auth_bp)


s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("LOGIN")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
          otp = request.form['otp']
        except BadRequestKeyError as e:
          otp = ''

        usuario = Usuario.query.filter_by(username=username, password=password).first()

        if usuario and usuario.is_active:
            if pyotp.TOTP(usuario.otp_secret).verify(otp):
                session['username'] = username
                flash('Has iniciado sesión exitosamente.')
                return redirect(url_for('auth.profile'))
            else:
                flash('Código OTP inválido.')
        elif usuario and not usuario.is_active:
            flash('Tu cuenta no está activada. Por favor, verifica tu correo electrónico.')
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
       

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_profile_pic = ""
        user_created_at = datetime.datetime.now()
        user_is_active = True
        user_otp_secret = ""
        
        print("Password: ", password)

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
            flash(e)
            return render_template('register.html')
          
        print("NOMBRE:", username)
        print("CONTRASEÑA:", password)

        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(username=username, email=email, password=password,
        profile_pic=user_profile_pic, created_at= user_created_at, is_active=user_is_active, otp_secret = user_otp_secret)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Enviar correo de verificación
        token = s.dumps(email, salt='email-confirm-salt')
        msg = Message('Confirma tu correo electrónico', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
        link = url_for('auth.confirm_email', token=token, _external=True)
        msg.body = f'Para activar tu cuenta, haz clic en el siguiente enlace: {link}'
        mail.send(msg)
        
        flash('Se ha enviado un enlace de verificación a tu correo electrónico.')
        return redirect(url_for('auth.login'))
       
    return render_template('register.html')


@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace de verificación ha expirado.')
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
  
@auth_bp.route('/resend_verification', methods=['GET', 'POST'])
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


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('main.home'))

@auth_bp.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            print("Dentro de usuario")
            token = s.dumps(email, salt='email-reset-salt')
            print("Token: ", token)
            msg = Message('Restablecer Contraseña', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            print("msg: ", msg)
            link = url_for('auth.reset_token', token=token, _external=True)
            print("link:", link)
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {link}'
            print("msg.body:", msg.body)
            mail.send(msg)
            flash('Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
            return redirect(url_for('auth.login'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.')
            return render_template('reset_request.html')
    return render_template('reset_request.html')

@auth_bp.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        email = s.loads(token, salt='email-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace de restablecimiento ha expirado.')
        return redirect(url_for('auth.reset_request'))

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
            flash(e)
            return render_template('reset_request.html')
        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = new_password
        db.session.commit()

        flash('Tu contraseña ha sido restablecida exitosamente.')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', token=token)
