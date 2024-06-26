```
Cuando uso:
routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import auth_bp
from extensions import db, mail
from models import Usuario
from validar_contrasena import validar_contrasena
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

auth_bp = Blueprint('auth', **name**)

print("AUTH ROUTES")
print("auth_bp: ", auth_bp)

s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
print("LOGIN")
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

...
Y lo ejecuto, y luego voy al navegador, no me entra en login (no sale el template).
Visualiza en consola:
print("AUTH ROUTES")
print("auth_bp: ", auth_bp)
pero no visualiza en consola:
print("LOGIN")
```

El problema podría estar en cómo se están registrando los Blueprints en tu aplicación principal. Asegúrate de que estás registrando el Blueprint `auth_bp` correctamente en `app.py`.

Vamos a revisar y ajustar tu estructura de archivos y la forma en que se están importando y registrando los Blueprints.

### Estructura del proyecto

Primero, asegúrate de que tu estructura de archivos sea similar a esta:

```
aplicacionFlask/
│
├── app.py
├── blueprints/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── user/
│       ├── __init__.py
│       └── routes.py
├── extensions.py
├── models.py
└── validar_contrasena.py
```

### Código de `app.py`

En `app.py`, debes asegurarte de que estás importando y registrando correctamente todos los Blueprints:

```python
from flask import Flask
from extensions import db, mail
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

### Código de `blueprints/auth/__init__.py`

En `blueprints/auth/__init__.py`, asegúrate de crear el Blueprint y registrar las rutas desde `routes.py`:

```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes  # Importa las rutas para registrarlas en el Blueprint
```

### Código de `blueprints/auth/routes.py`

En `blueprints/auth/routes.py`, asegúrate de que estás utilizando el Blueprint `auth_bp` definido en `__init__.py`:

```python
from flask import render_template, request, flash, redirect, url_for, session
from . import auth_bp  # Importa el Blueprint desde el módulo actual
from extensions import db, mail
from models import Usuario
from validar_contrasena import validar_contrasena
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("LOGIN")  # Este mensaje debería aparecer cuando accedas a /login
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
```

### Otros Blueprints

Asegúrate de que los otros Blueprints (`main` y `user`) estén configurados de manera similar:

**blueprints/main/**init**.py**

```python
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import routes
```

**blueprints/user/**init**.py**

```python
from flask import Blueprint

user_bp = Blueprint('user', __name__)

from . import routes
```

### Verificación

Después de hacer estos cambios, ejecuta tu aplicación nuevamente:

```sh
python app.py
```

Luego, ve a la URL `http://127.0.0.1:5000/login` en tu navegador. Si todo está configurado correctamente, deberías ver el mensaje "LOGIN" en la consola cuando accedas a esta ruta.

Si el problema persiste, asegúrate de revisar los registros de errores en la consola y en el navegador para obtener más información sobre posibles problemas.
