### Continuación del Curso

Ahora que hemos cubierto las sesiones y autenticación de usuarios, así como la corrección de errores comunes, vamos a continuar con la siguiente parte del curso.

### Clase 5: Manejo de Bases de Datos con SQLAlchemy

#### Objetivo

- Introducir el uso de bases de datos en Flask.
- Configurar SQLAlchemy en una aplicación Flask.
- Definir modelos y realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar).

#### Temas a cubrir

1. Configuración de SQLAlchemy en Flask.
2. Definición de modelos.
3. Realización de operaciones CRUD.

### Configuración de SQLAlchemy en Flask

#### Paso 1: Instalar Flask-SQLAlchemy

Primero, necesitamos instalar la extensión Flask-SQLAlchemy:

```bash
pip install Flask-SQLAlchemy
```

#### Paso 2: Configurar SQLAlchemy

Modifiquemos nuestro archivo `app.py` para incluir la configuración de SQLAlchemy.

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

if __name__ == '__main__':
    db.create_all()  # Crear las tablas en la base de datos
    app.run(debug=True)
```

### Definición de Modelos

Hemos definido un modelo `Usuario` con los campos `id`, `username`, `email` y `password`. Ahora vamos a modificar nuestras rutas para interactuar con la base de datos.

### Realización de operaciones CRUD

#### Registro de Usuarios

Actualicemos la ruta `/register` para guardar los datos de usuario en la base de datos:

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Bienvenido, {username}!')
        return redirect(url_for('login'))
    return render_template('register.html')
```

#### Autenticación de Usuarios

Actualizaremos la ruta `/login` para verificar las credenciales del usuario desde la base de datos:

```python
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
```

#### Cambio de Contraseña

Actualizaremos la ruta `/change_password` para que interactúe con la base de datos:

```python
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
```

### Tarea para los alumnos

Ahora que hemos integrado SQLAlchemy para manejar nuestros datos de usuarios, quiero que implementen las siguientes funcionalidades adicionales:

1. **Ruta para eliminar una cuenta de usuario**:

   - Cree una ruta `/delete_account` que permita a los usuarios eliminar su cuenta.
   - Asegúrese de que la ruta está protegida por el decorador `login_required`.
   - Confirme la eliminación de la cuenta antes de proceder.

2. **Ruta para actualizar el perfil del usuario**:
   - Cree una ruta `/update_profile` que permita a los usuarios actualizar su nombre de usuario y correo electrónico.
   - Asegúrese de que la ruta está protegida por el decorador `login_required`.
   - Valide que el nuevo nombre de usuario y correo electrónico no estén ya en uso.

#### Sugerencia de código para eliminar una cuenta:

```python
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
```

#### Sugerencia de código para actualizar el perfil:

```python
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
```

Con estas tareas adicionales, estarán en camino de crear una aplicación web robusta y bien estructurada utilizando Flask y SQLAlchemy. ¡Buena suerte y feliz codificación!
