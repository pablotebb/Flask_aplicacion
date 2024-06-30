### Clase 8: Funcionalidad Avanzada y Seguridad

#### Objetivo

- Implementar manejo de errores para enlaces de verificación expirados o inválidos.
- Añadir la funcionalidad para reenvío del enlace de verificación.
- Implementar autenticación de dos factores (2FA).

### Manejo de Errores de Verificación de Correo

#### Paso 1: Modificar la Ruta de Verificación de Correo

Añadimos manejo de errores para el caso donde el enlace de verificación ha expirado o es inválido.

```python
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
```

#### Paso 2: Ruta para Reenvío de Enlace de Verificación

Creamos una nueva ruta para permitir a los usuarios solicitar un nuevo enlace de verificación.

```python
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
```

#### Paso 3: Plantilla `resend_verification.html`

Creamos una nueva plantilla para solicitar el reenvío del enlace de verificación.

`templates/resend_verification.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Reenviar Enlace de Verificación</title>
  </head>
  <body>
    <h1>Reenviar Enlace de Verificación</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/resend_verification" method="post">
      <label for="email">Correo electrónico:</label><br />
      <input type="email" id="email" name="email" required /><br /><br />
      <input type="submit" value="Enviar Enlace" />
    </form>
  </body>
</html>
```

### Autenticación de Dos Factores (2FA)

#### Paso 1: Instalar PyOTP

Primero, necesitamos instalar la librería `pyotp` para manejar la autenticación de dos factores.

```bash
pip install pyotp
```

#### Paso 2: Añadir Campos de 2FA al Modelo de Usuario

Añadimos campos al modelo de usuario para manejar la autenticación de dos factores.

```python
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
```

#### Paso 3: Generar Secretos OTP y QR Codes

Añadimos la lógica para generar secretos OTP y mostrar un QR code para que los usuarios configuren la autenticación de dos factores.

```python
import pyotp
import qrcode
import io

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
```

#### Paso 4: Verificar OTP al Iniciar Sesión

Modificamos la ruta de inicio de sesión para verificar el OTP después de que el usuario ingrese su nombre de usuario y contraseña.

```python
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
```

#### Paso 5: Modificar la Plantilla `login.html`

Actualizamos la plantilla de inicio de sesión para incluir el campo OTP.

`templates/login.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Iniciar Sesión</title>
  </head>
  <body>
    <h1>Iniciar Sesión</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/login" method="post">
      <label for="username">Nombre de Usuario:</label><br />
      <input type="text" id="username" name="username" required /><br /><br />
      <label for="password">Contraseña:</label><br />
      <input
        type="password"
        id="password"
        name="password"
        required
      /><br /><br />
      <label for="otp">Código OTP:</label><br />
      <input type="text" id="otp" name="otp" required /><br /><br />
      <input type="submit" value="Iniciar Sesión" />
    </form>
  </body>
</html>
```

### Verificación final

1. **Reenvío de Enlace de Verificación**: Regístrate con un nuevo usuario, intenta verificar un enlace expirado y solicita un nuevo enlace.
2. **Configuración y Verificación de 2FA**: Configura la autenticación de dos factores y verifica que el inicio de sesión requiere un código OTP válido.

### Conclusión

Con estas implementaciones, has añadido manejo de errores para enlaces de verificación, la posibilidad de reenvío de enlaces y autenticación de dos factores, mejorando significativamente la seguridad y usabilidad de tu aplicación Flask.

### Tarea para los alumnos

1. **Personalización de 2FA**:

   - Permite a los usuarios desactivar la autenticación de dos factores desde su perfil.
   - Añade notificaciones adicionales para alertar a los usuarios cuando se active o desactive la autenticación de dos factores.

2. **Mejoras en la Experiencia del Usuario**:
   - Implementa mensajes de error más detallados y amigables para el usuario.
   - Añade validaciones adicionales en los formularios para mejorar la seguridad y experiencia del usuario.

Estas tareas adicionales les ayudarán a seguir mejorando sus habilidades en el desarrollo de aplicaciones web seguras y robustas con Flask. ¡Buena suerte y feliz codificación!
