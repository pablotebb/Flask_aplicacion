> $ python app5_1.py

```
Me da este error:
Traceback (most recent call last):
File "app5.py", line 142, in <module>
db.create_all() # Crear las tablas en la base de datos
File "C:\Users\pablo\anaconda3\lib\site-packages\flask_sqlalchemy\extension.py", line 900, in create_all
self.\_call_for_binds(bind_key, "create_all")
File "C:\Users\pablo\anaconda3\lib\site-packages\flask_sqlalchemy\extension.py", line 871, in \_call_for_binds
engine = self.engines[key]
File "C:\Users\pablo\anaconda3\lib\site-packages\flask_sqlalchemy\extension.py", line 687, in engines
app = current_app.\_get_current_object() # type: ignore[attr-defined]
File "C:\Users\pablo\anaconda3\lib\site-packages\werkzeug\local.py", line 519, in \_get_current_object
raise RuntimeError(unbound_message) from None
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.
(base)
```

El error que estás viendo, "RuntimeError: Working outside of application context", indica que se está intentando utilizar una funcionalidad de Flask (en este caso, la creación de tablas en la base de datos) fuera del contexto de la aplicación Flask.

Para solucionar este problema, necesitas crear un contexto de aplicación antes de llamar a `db.create_all()`. Esto asegura que todas las configuraciones y variables relacionadas con Flask estén disponibles.

### Solución

Envuelve la llamada a `db.create_all()` dentro de un bloque de contexto de aplicación.

Aquí tienes cómo hacerlo:

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Configurar la URI de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Resto del código de la aplicación...

# Decorador para rutas protegidas
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/profile')
@login_required
def profile():
    username = session['username']
    return f"Bienvenido a tu perfil, {username}!"

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

        usuario.password = new_password
        db.session.commit()

        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('profile'))
    return render_template('change_password.html')

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación

1. **Contexto de aplicación**: `with app.app_context():` crea un contexto de aplicación, dentro del cual puedes hacer operaciones relacionadas con la configuración y las extensiones de Flask.
2. **Creación de tablas**: `db.create_all()` se llama dentro de este bloque de contexto, lo que asegura que se ejecuta dentro del contexto de la aplicación Flask.

Intenta ejecutar tu aplicación nuevamente después de realizar estos cambios. Esto debería resolver el problema del contexto de aplicación y permitir que se creen las tablas en la base de datos sin errores.
