### Clase 6: Restablecimiento de Contraseña

#### Objetivo

- Implementar la funcionalidad de restablecimiento de contraseña en la aplicación Flask.
- Utilizar `Flask-Mail` para enviar correos electrónicos con un enlace de restablecimiento de contraseña.

#### Temas a cubrir

1. Configuración de `Flask-Mail`.
2. Generación de tokens de restablecimiento de contraseña.
3. Envío de correos electrónicos.
4. Creación de formularios para solicitar y restablecer la contraseña.

### Configuración de Flask-Mail

#### Paso 1: Instalar Flask-Mail

Primero, necesitamos instalar la extensión Flask-Mail:

```bash
pip install Flask-Mail
```

#### Paso 2: Configurar Flask-Mail

Modifiquemos nuestro archivo `app.py` para incluir la configuración de Flask-Mail.

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

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

db = SQLAlchemy(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

# Definición del modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Resto del código de la aplicación...

if __name__ == '__main__':
    app.run(debug=True)
```

### Generación de Tokens de Restablecimiento de Contraseña

Usaremos `itsdangerous` para generar tokens seguros que expiren después de un tiempo determinado.

### Envío de Correos Electrónicos

Vamos a crear las rutas para solicitar el restablecimiento de contraseña y para manejar el enlace de restablecimiento.

#### Paso 1: Crear la plantilla `reset_request.html`

`templates/reset_request.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Restablecer Contraseña</title>
  </head>
  <body>
    <h1>Restablecer Contraseña</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/reset_request" method="post">
      <label for="email">Correo Electrónico:</label><br />
      <input type="email" id="email" name="email" /><br /><br />
      <input type="submit" value="Enviar Enlace de Restablecimiento" />
    </form>
  </body>
</html>
```

#### Paso 2: Crear la ruta `reset_request` en `app.py`

Añadimos la lógica para manejar la solicitud de restablecimiento de contraseña:

```python
@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            token = s.dumps(email, salt='email-reset-salt')
            msg = Message('Restablecer Contraseña', sender='your-email@example.com', recipients=[email])
            link = url_for('reset_token', token=token, _external=True)
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {link}'
            mail.send(msg)
            flash('Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
            return redirect(url_for('login'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.')
            return render_template('reset_request.html')
    return render_template('reset_request.html')
```

#### Paso 3: Crear la plantilla `reset_token.html`

`templates/reset_token.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Restablecer Contraseña</title>
  </head>
  <body>
    <h1>Restablecer Contraseña</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/reset_token/{{ token }}" method="post">
      <label for="new_password">Nueva Contraseña:</label><br />
      <input type="password" id="new_password" name="new_password" /><br />
      <label for="confirm_password">Confirmar Nueva Contraseña:</label><br />
      <input
        type="password"
        id="confirm_password"
        name="confirm_password"
      /><br /><br />
      <input type="submit" value="Restablecer Contraseña" />
    </form>
  </body>
</html>
```

#### Paso 4: Crear la ruta `reset_token` en `app.py`

Añadimos la lógica para manejar el enlace de restablecimiento de contraseña:

```python
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

        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = new_password
        db.session.commit()

        flash('Tu contraseña ha sido restablecida exitosamente.')
        return redirect(url_for('login'))

    return render_template('reset_token.html', token=token)
```

### Verificación final

1. **Solicitud de restablecimiento**: Prueba la solicitud de restablecimiento de contraseña proporcionando un correo electrónico válido. Verifica que se envía un correo electrónico con el enlace de restablecimiento.
2. **Restablecimiento de contraseña**: Haz clic en el enlace de restablecimiento de contraseña, proporciona una nueva contraseña y verifica que se actualiza correctamente.

### Conclusión

Con esta implementación, has añadido una funcionalidad crítica de seguridad a tu aplicación Flask: la capacidad de restablecer contraseñas a través de correos electrónicos. Esta funcionalidad es fundamental para cualquier aplicación que maneje datos de usuario sensibles.

### Tarea para los alumnos

1. **Mejora del perfil de usuario**:

   - Implementa la subida de fotos de perfil utilizando `Flask-Uploads` o una librería similar.
   - Mejora la página de perfil para mostrar la fecha de creación de la cuenta y la foto de perfil.

2. **Verificación de correo electrónico**:
   - Implementa un sistema de verificación de correo electrónico al registrarse.
   - Envía un correo electrónico de verificación con un enlace para activar la cuenta.

Estas tareas les ayudarán a profundizar en la implementación de características de seguridad y manejo de usuarios en Flask. ¡Buena suerte y feliz codificación!
