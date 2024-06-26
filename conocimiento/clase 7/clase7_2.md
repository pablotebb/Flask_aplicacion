```
En Flask, como adaptarías este trozo de código, a Bluprints:
app.js

from flask import Flask, render_template, request, flash, redirect, url_for, session
from validar_contrasena import validar_contrasena
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(**name**)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db' # Configurar la URI de la base de datos
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
app.config['MAIL_TIMEOUT'] = 60 # Aumenta el tiempo de espera a 60 segundos

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

# Definición del modelo de usuario

class Usuario(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(79), unique=True, nullable=False)
email = db.Column(db.String(120), unique=True, nullable=False)
password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'


# Resto del código de la aplicación...

# Decorador para rutas protegidas (para proteger rutas que requieren autenticación)

def login_required(f):
def wrap(*args, \*\*kwargs):
if 'username' not in session:
flash('Necesitas iniciar sesión primero')
return redirect(url_for('login'))
return f(*args, \*\*kwargs)
wrap.**name** = f.**name**
return wrap

@app.route('/')
def home():
nombre = "Pablo"
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
username = request.form['username']
email = request.form['email']
password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        try:
            validar_contrasena(password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('register.html')

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(f'Registro exitoso. Bienvenido, {username}!')
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
username = request.form['username']
password = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or usuario.password != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('home'))
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
link = url_for('reset_token', token=token, \_external=True)
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
username = session['username'] # return f"Bienvenido a tu perfil, {username}!"
return render_template('profile.html', username=username)

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

# Crear las tablas en la base de datos

with app.app_context():
db.create_all()

if **name** == '**main**':
app.run(debug=True)

templates/about.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>About</title>
  </head>
  <body>
    <h1>Esta es la página About de {{ nombre }}.</h1>
  </body>
</html>

templates/change_password.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Change Password</title>
  </head>
  <body>
    <h1>Cambiar Contraseña</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/change_password" method="post">
      <label for="current_password">Contraseña Actual:</label><br />
      <input
        type="password"
        id="current_password"
        name="current_password"
      /><br />
      <label for="new_password">Nueva Contraseña:</label><br />
      <input type="password" id="new_password" name="new_password" /><br />
      <label for="confirm_password">Confirmar Nueva Contraseña:</label><br />
      <input
        type="password"
        id="confirm_password"
        name="confirm_password"
      /><br /><br />
      <input type="submit" value="Cambiar Contraseña" />
    </form>

  </body>
</html>

contact.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Contact</title>
  </head>
  <body>
    <h1>Contacta a {{ nombre }}</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/contact" method="post">
      <label for="name">Nombre:</label><br />
      <input type="text" id="name" name="name" /><br />
      <label for="email">Correo electrónico:</label><br />
      <input type="email" id="email" name="email" /><br />
      <label for="message">Mensaje:</label><br />
      <textarea id="message" name="message"></textarea><br /><br />
      <input type="submit" value="Enviar" />
    </form>

  </body>
</html>

contact2.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Contact</title>
  </head>
  <body>
    <h1>Contacta a {{ nombre }}</h1>

    <!-- Usamos la función get_flashed_messages para obtener y mostrar mensajes flash. -->
    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/contact" method="post">
      <label for="name">Nombre:</label><br />
      <input type="text" id="name" name="name" /><br />
      <label for="email">Correo electrónico:</label><br />
      <input type="email" id="email" name="email" /><br />
      <label for="message">Mensaje:</label><br />
      <textarea id="message" name="message"></textarea><br /><br />
      <input type="submit" value="Enviar" />
    </form>

  </body>
</html>

delete_account.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Eliminar Cuenta</title>
  </head>
  <body>
    <h1>Eliminar Cuenta</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/delete_account" method="post">
      <p>
        ¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede
        deshacer.
      </p>
      <input type="submit" value="Eliminar Cuenta" />
    </form>

  </body>
</html>

index.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
  </head>
  <body>
    <h1>
      ¡Hola, {{ nombre }}! Bienvenido a tu primera aplicación Flask con
      plantillas.
    </h1>
  </body>
</html>

login.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login</title>
  </head>
  <body>
    <h1>Inicio de Sesión</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/login" method="post">
      <label for="username">Nombre de Usuario:</label><br />
      <input type="text" id="username" name="username" /><br />
      <label for="password">Contraseña:</label><br />
      <input type="password" id="password" name="password" /><br /><br />
      <input type="submit" value="Iniciar Sesión" />
    </form>

  </body>
</html>

profile.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Perfil de Usuario</title>
  </head>
  <body>
    <h1>Bienvenido a tu perfil, {{ username }}!</h1>
  </body>
</html>

register.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Register</title>
  </head>
  <body>
    <h1>Registro de Usuario</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/register" method="post">
      <label for="username">Nombre de Usuario:</label><br />
      <input type="text" id="username" name="username" /><br />
      <label for="email">Correo electrónico:</label><br />
      <input type="email" id="email" name="email" /><br />
      <label for="password">Contraseña:</label><br />
      <input type="password" id="password" name="password" /><br /><br />
      <input type="submit" value="Registrar" />
    </form>

  </body>
</html>

reset_request.html

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

update_profile.html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Actualizar Perfil</title>
  </head>
  <body>
    <h1>Actualizar Perfil</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/update_profile" method="post">
      <label for="username">Nuevo Nombre de Usuario:</label><br />
      <input type="text" id="username" name="username" /><br />
      <label for="email">Nuevo Correo Electrónico:</label><br />
      <input type="email" id="email" name="email" /><br /><br />
      <input type="submit" value="Actualizar Perfil" />
    </form>

  </body>
</html>
```

Para adaptar este código a usar Blueprints en Flask, puedes organizar la estructura de tu proyecto de la siguiente manera:

1. Crea un directorio para cada Blueprint.
2. Separa las rutas en diferentes módulos según sus funcionalidades.
3. Define cada Blueprint en su propio archivo.
4. Registra los Blueprints en la aplicación principal.

Aquí tienes un ejemplo de cómo podrías reestructurar tu proyecto.

**Estructura de Directorios:**

```
my_flask_app/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── validate_password.py
├── blueprints/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── user/
│       ├── __init__.py
│       ├── routes.py
├── templates/
│   ├── layout.html
│   └── ...
└── .env
```

**app.py**

```python
from flask import Flask
from config import Config
from extensions import db, migrate, mail
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

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

**config.py**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_MAX_EMAILS = None
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_TIMEOUT = 60  # Aumenta el tiempo de espera a 60 segundos
```

**extensions.py**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
```

**models.py**

```python
from extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(79), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'
```

**blueprints/auth/routes.py**

```python
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from extensions import db
from models import Usuario
from validate_password import validar_contrasena
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

auth_bp = Blueprint('auth', __name__)

s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or usuario.password != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('main.home'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        try:
            validar_contrasena(password)
        except ValueError as e:
            flash(e)
            return render_template('register.html')

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(f'Registro exitoso. Bienvenido, {username}!')
        return redirect(url_for('user.profile'))
    return render_template('register.html')

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
            token = s.dumps(email, salt='email-reset-salt')
            msg = Message('Restablecer Contraseña', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            link = url_for('auth.reset_token', token=token, _external=True)
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {link}'
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
            return render_template('reset_token.html', token=token)

        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = new_password
        db.session.commit()

        flash('Tu contraseña ha sido restablecida exitosamente.')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', token=token)
```

**blueprints/main/routes.py**

```python
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    nombre = "Pablo"
    return render_template('index.html', nombre=nombre)

@main_bp.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)

@main_bp.route('/contact', methods=['GET', 'POST'])
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
```

**blueprints/user/routes.py**

```python
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from extensions import db
from models import Usuario
from validate_password import validar_contrasena

user_bp = Blueprint('user', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@user_bp.route('/profile')
@login_required
def profile():
    username = session['username']
    return render_template('profile.html', username=username)

@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']


        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or usuario.password != current_password:
            flash('La contraseña actual no es correcta')
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
        db.session.commit()

        flash('Contraseña actualizada con éxito')
        return redirect(url_for('user.profile'))
    return render_template('change_password.html')
```

**validate_password.py**

```python
import re

def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not re.search("[a-z]", contrasena):
        raise ValueError("La contraseña debe contener al menos una letra minúscula")
    if not re.search("[A-Z]", contrasena):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula")
    if not re.search("[0-9]", contrasena):
        raise ValueError("La contraseña debe contener al menos un dígito")
    if not re.search("[@#$%^&+=]", contrasena):
        raise ValueError("La contraseña debe contener al menos un carácter especial: @#$%^&+=")
    return True
```

Esta estructura utiliza Blueprints para organizar tu aplicación Flask de manera modular y escalable. Cada módulo contiene sus propias rutas, vistas y plantillas, lo que facilita el mantenimiento y la expansión de tu proyecto.
