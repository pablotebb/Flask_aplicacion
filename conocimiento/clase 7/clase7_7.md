### Clase 7: Mejora del Perfil de Usuario

#### Objetivo

- Implementar la funcionalidad para que los usuarios suban fotos de perfil.
- Mostrar la fecha de creación de la cuenta y la foto de perfil en la página de perfil.

#### Temas a cubrir

1. Configuración de `Flask-Uploads` para manejar archivos.
2. Modificación del modelo de usuario para almacenar la ruta de la foto de perfil.
3. Creación de formularios y rutas para subir y mostrar la foto de perfil.

### Configuración de Flask-Uploads

#### Paso 1: Instalar Flask-Uploads

Primero, necesitamos instalar la extensión Flask-Uploads:

```bash
pip install Flask-Uploads
```

#### Paso 2: Configurar Flask-Uploads

Modifiquemos nuestro archivo `app.py` para incluir la configuración de Flask-Uploads.

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

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

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Resto del código de la aplicación...

if __name__ == '__main__':
    app.run(debug=True)
```

### Modificación del Modelo de Usuario

Añadimos los campos `profile_pic` y `created_at` al modelo `Usuario`.

```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Usuario {self.username}>'
```

### Creación de Formularios y Rutas

#### Paso 1: Crear la plantilla `upload_profile_pic.html`

`templates/upload_profile_pic.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Subir Foto de Perfil</title>
  </head>
  <body>
    <h1>Subir Foto de Perfil</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form
      action="/upload_profile_pic"
      method="post"
      enctype="multipart/form-data"
    >
      <label for="profile_pic">Selecciona una foto:</label><br />
      <input type="file" id="profile_pic" name="profile_pic" /><br /><br />
      <input type="submit" value="Subir Foto" />
    </form>
  </body>
</html>
```

#### Paso 2: Crear la ruta `upload_profile_pic` en `app.py`

Añadimos la lógica para manejar la subida de fotos de perfil:

```python
@app.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    if request.method == 'POST' and 'profile_pic' in request.files:
        filename = photos.save(request.files['profile_pic'])
        filepath = photos.path(filename)

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = filename
        db.session.commit()

        flash('Foto de perfil subida exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')
```

#### Paso 3: Modificar la plantilla `profile.html`

Actualizamos la plantilla del perfil para mostrar la foto de perfil y la fecha de creación de la cuenta.

`templates/profile.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Perfil de Usuario</title>
  </head>
  <body>
    <h1>Bienvenido a tu perfil, {{ usuario.username }}!</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %} {% if usuario.profile_pic %}
    <img
      src="{{ url_for('static', filename='uploads/' + usuario.profile_pic) }}"
      alt="Foto de Perfil"
      width="150"
    />
    {% else %}
    <p>No has subido una foto de perfil.</p>
    {% endif %}

    <p>Correo electrónico: {{ usuario.email }}</p>
    <p>
      Fecha de creación de la cuenta: {{ usuario.created_at.strftime('%Y-%m-%d
      %H:%M:%S') }}
    </p>

    <a href="{{ url_for('change_password') }}">Cambiar Contraseña</a><br />
    <a href="{{ url_for('update_profile') }}">Actualizar Perfil</a><br />
    <a href="{{ url_for('upload_profile_pic') }}">Subir Foto de Perfil</a><br />
    <a href="{{ url_for('delete_account') }}">Eliminar Cuenta</a><br />
  </body>
</html>
```

#### Paso 4: Modificar la ruta `profile` en `app.py`

Actualizamos la lógica para pasar el objeto `usuario` a la plantilla de perfil:

```python
@app.route('/profile')
@login_required
def profile():
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    return render_template('profile.html', usuario=usuario)
```

### Verificación final

1. **Subida de foto de perfil**: Inicia sesión con un usuario de prueba, navega a la página de subida de foto de perfil, sube una foto y verifica que se muestra correctamente en la página de perfil.
2. **Fecha de creación de la cuenta**: Verifica que la fecha de creación de la cuenta se muestra correctamente en la página de perfil.

### Conclusión

Con estas mejoras, has añadido funcionalidades avanzadas a tu aplicación Flask, permitiendo a los usuarios personalizar su perfil con fotos y visualizar información importante como la fecha de creación de su cuenta. Esto enriquece la experiencia del usuario y mejora la usabilidad de la aplicación.

### Tarea para los alumnos

1. **Optimización de imágenes**:

   - Implementa la redimensionamiento automático de imágenes para asegurar que las fotos de perfil no sean demasiado grandes.
   - Usa una librería como `Pillow` para manipular las imágenes antes de guardarlas.

2. **Verificación de correo electrónico**:
   - Implementa un sistema de verificación de correo electrónico al registrarse.
   - Envía un correo electrónico de verificación con un enlace para activar la cuenta.

Estas tareas adicionales les ayudarán a seguir mejorando sus habilidades en el desarrollo de aplicaciones web con Flask. ¡Buena suerte y feliz codificación!
