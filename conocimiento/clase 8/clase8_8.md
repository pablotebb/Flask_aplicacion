### Clase 9: Mejora de la Experiencia del Usuario y Gestión de Perfil

#### Objetivo

- Añadir opciones para que los usuarios puedan desactivar la autenticación de dos factores (2FA).
- Mejorar la experiencia del usuario (UX) añadiendo mensajes más claros y validaciones adicionales.

### Desactivar Autenticación de Dos Factores (2FA)

#### Paso 1: Añadir la Ruta para Desactivar 2FA

Añadimos una ruta para permitir a los usuarios desactivar la autenticación de dos factores.

```python
@app.route('/disable_2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa():
    if request.method == 'POST':
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario:
            usuario.otp_secret = None
            db.session.commit()
            flash('Autenticación de dos factores desactivada exitosamente.')
        return redirect(url_for('profile'))

    return render_template('disable_2fa.html')
```

#### Paso 2: Plantilla `disable_2fa.html`

Creamos una nueva plantilla para la página de desactivación de 2FA.

`templates/disable_2fa.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Desactivar Autenticación de Dos Factores</title>
  </head>
  <body>
    <h1>Desactivar Autenticación de Dos Factores</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/disable_2fa" method="post">
      <input type="submit" value="Desactivar 2FA" />
    </form>
  </body>
</html>
```

### Validaciones Adicionales y Mejora de la UX

#### Paso 1: Validaciones Adicionales en Registro

Añadimos validaciones adicionales para el registro, como la verificación de contraseñas seguras.

```python
from werkzeug.security import generate_password_hash, check_password_hash
import re

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

        # Validar la contraseña
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            flash('La contraseña debe tener al menos 8 caracteres y contener letras, números y caracteres especiales.')
            return render_template('register.html')

        # Crear nuevo usuario con contraseña hasheada
        hashed_password = generate_password_hash(password, method='sha256')
        nuevo_usuario = Usuario(username=username, email=email, password=hashed_password)
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
```

#### Paso 2: Modificaciones en el Inicio de Sesión

Adaptamos la lógica de inicio de sesión para trabajar con contraseñas hasheadas.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and check_password_hash(usuario.password, password) and usuario.is_active:
            if usuario.otp_secret:
                if pyotp.TOTP(usuario.otp_secret).verify(otp):
                    login_user(usuario)
                    flash('Has iniciado sesión exitosamente.')
                    return redirect(url_for('profile'))
                else:
                    flash('Código OTP inválido.')
            else:
                login_user(usuario)
                flash('Has iniciado sesión exitosamente.')
                return redirect(url_for('profile'))
        elif usuario and not usuario.is_active:
            flash('Tu cuenta no está activada. Por favor, verifica tu correo electrónico.')
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    return render_template('login.html')
```

#### Paso 3: Modificar la Plantilla `login.html`

Actualizamos la plantilla de inicio de sesión para incluir condicionalmente el campo OTP.

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
      {% if usuario and usuario.otp_secret %}
      <label for="otp">Código OTP:</label><br />
      <input type="text" id="otp" name="otp" /><br /><br />
      {% endif %}
      <input type="submit" value="Iniciar Sesión" />
    </form>
  </body>
</html>
```

### Verificación final

1. **Desactivar 2FA**: Habilita y desactiva la autenticación de dos factores para verificar la funcionalidad.
2. **Registro**: Intenta registrarte con contraseñas no seguras para comprobar las validaciones.
3. **Inicio de Sesión**: Inicia sesión con y sin autenticación de dos factores para asegurarte de que todo funciona correctamente.

### Conclusión

Estas implementaciones añaden más funcionalidades y mejoran la experiencia del usuario en tu aplicación Flask. Has añadido una opción para desactivar la autenticación de dos factores y mejorado las validaciones y mensajes de error para ofrecer una experiencia más amigable y segura.

### Tarea para los alumnos

1. **Personalización del Perfil**:

   - Añade una sección en el perfil del usuario donde puedan cambiar su contraseña.
   - Permite a los usuarios actualizar su información personal, como nombre de usuario y dirección de correo electrónico.

2. **Notificaciones**:
   - Implementa notificaciones por correo electrónico para cambios importantes, como la desactivación de 2FA o la actualización de información de la cuenta.

Estas tareas adicionales les ayudarán a seguir mejorando sus habilidades en el desarrollo de aplicaciones web seguras y robustas con Flask. ¡Buena suerte y feliz codificación!
