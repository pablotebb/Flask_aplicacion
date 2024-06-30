> Cuando ejecuto, me da el siguiente error: <br>
> python app8_1.py <br>
> Traceback (most recent call last):
> File "app8_1.py", line 17, in <module>
> import qrcode
> ModuleNotFoundError: No module named 'qrcode'

El error indica que el módulo `qrcode` no está instalado en tu entorno de Python. Debes instalar este módulo para poder generar códigos QR necesarios para la autenticación de dos factores.

### Paso 1: Instalar qrcode

Para instalar `qrcode`, ejecuta el siguiente comando:

```bash
pip install qrcode[pil]
```

Este comando instalará `qrcode` junto con su dependencia `Pillow`, que se utiliza para generar imágenes de códigos QR.

### Paso 2: Verificar la Instalación

Después de instalar el módulo, verifica que la instalación fue exitosa intentando importar el módulo `qrcode` en un script de prueba o en una consola interactiva de Python.

```python
import qrcode

print("qrcode module imported successfully!")
```

### Paso 3: Ejecutar la Aplicación

Una vez que hayas verificado que el módulo `qrcode` está instalado correctamente, vuelve a ejecutar tu aplicación Flask.

```bash
python app8_1.py
```

Si todo está configurado correctamente, la aplicación debería ejecutarse sin problemas. Aquí está el archivo `app.py` completo actualizado para tu referencia:

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.utils import secure_filename
from PIL import Image
import os
import pyotp
import qrcode
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'uploads')

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

s = URLSafeTimedSerializer(app.secret_key)

# Definición del modelo de usuario
class Usuario(UserMixin, db.Model):
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

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas de la aplicación...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado.')
            return render_template('register.html')

        # Crear nuevo usuario
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Enviar correo de verificación
        token = s.dumps(email, salt='email-confirm-salt')
        msg = Message('Confirma tu correo electrónico', sender='your-email@example.com', recipients=[email])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']
        usuario = Usuario.query.filter_by(username=username, password=password).first()

        if usuario and usuario.is_active:
            if pyotp.TOTP(usuario.otp_secret).verify(otp):
                login_user(usuario)
                flash('Has iniciado sesión exitosamente.')
                return redirect(url_for('profile'))
            else:
                flash('Código OTP inválido.')
        elif usuario and not usuario.is_active:
            flash('Tu cuenta no está activada. Por favor, verifica tu correo electrónico.')
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    return render_template('login.html')

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
        image.save(temp_filepath)

        # Guardar la imagen final
        final_filepath = photos.save(temp_filepath)
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')

@app.route('/profile')
@login_required
def profile():
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    return render_template('profile.html', usuario=usuario)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

### Verificación final

1. **Instalación de `qrcode`**: Asegúrate de que el módulo `qrcode` esté instalado correctamente.
2. **Configuración y Verificación de 2FA**: Configura la autenticación de dos factores y verifica que el inicio de sesión requiere un código OTP válido.
3. **Reenvío de Enlace de Verificación**: Regístrate con un nuevo usuario, intenta verificar un enlace expirado y solicita un nuevo enlace.

###
