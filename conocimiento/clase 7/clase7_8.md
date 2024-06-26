> Me sale este error:
> python app7*1.py
> Traceback (most recent call last):
> File "app7_1.py", line 5, in <module>
> from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
> File "C:\Users\pablo\anaconda3\lib\site-packages\flask_uploads.py", line 26, in <module>
> from werkzeug import secure_filename, FileStorage
> ImportError: cannot import name 'secure_filename' from 'werkzeug' (C:\Users\pablo\anaconda3\lib\site-packages\werkzeug_init*.py)
> (base)

El error que estás viendo se debe a que la función `secure_filename` ha sido movida en versiones recientes de `werkzeug`. Para solucionar esto, vamos a modificar la importación correspondiente en el archivo `flask_uploads.py`.

### Solución al Error

#### Paso 1: Modificar `flask_uploads.py`

Busca el archivo `flask_uploads.py` en tu instalación de Python. Debería estar en una ruta similar a `C:\Users\pablo\anaconda3\lib\site-packages\flask_uploads.py`.

Abre el archivo y cambia la línea:

```python
from werkzeug import secure_filename, FileStorage
```

a

```python
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```

Este cambio asegura que las importaciones sean correctas para versiones recientes de `werkzeug`.

#### Paso 2: Verificar `app.py`

Asegúrate de que tu archivo `app.py` esté configurado correctamente para las importaciones y configuraciones necesarias.

Aquí está el archivo `app.py` actualizado:

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

# Rutas de la aplicación...

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

@app.route('/profile')
@login_required
def profile():
    username = session['username']
    usuario = Usuario.query.filter_by(username=username).first()
    return render_template('profile.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
```

### Verificación final

1. **Corrección de Importaciones**: Asegúrate de que las importaciones en `flask_uploads.py` estén corregidas y el archivo `app.py` esté configurado correctamente.
2. **Ejecución de la Aplicación**: Intenta ejecutar nuevamente la aplicación con `python app7_1.py`.

Si todavía enfrentas problemas, considera verificar que todas las dependencias estén instaladas correctamente y que la configuración de tu entorno esté en orden.
