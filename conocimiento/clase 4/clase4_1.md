¡Muy bien! Continuemos con nuestro curso de Flask. En esta clase, aprenderemos sobre sesiones y autenticación de usuarios, elementos fundamentales para crear aplicaciones web seguras y personalizadas.

### Clase 4: Sesiones y Autenticación de Usuarios

#### Objetivo

- Introducir el concepto de sesiones en Flask.
- Implementar autenticación de usuarios.
- Proteger rutas con autenticación.

#### Temas a cubrir

1. ¿Qué son las sesiones?
2. Configurar y manejar sesiones en Flask.
3. Crear un sistema básico de autenticación.
4. Proteger rutas usando decoradores.

### ¿Qué son las sesiones?

Las sesiones en Flask permiten almacenar información específica del usuario entre diferentes solicitudes. Esto es útil para mantener datos como la autenticación del usuario.

### Configurar y manejar sesiones en Flask

#### Paso 1: Configurar las sesiones

Para manejar sesiones en Flask, utilizamos el objeto `session` proporcionado por Flask. Necesitamos una `secret_key` para firmar las cookies de la sesión.

Modifiquemos el archivo `app.py` para incluir la configuración de sesión y el sistema de autenticación.

#### Paso 2: Crear el formulario de inicio de sesión

Creemos un archivo `login.html` en el directorio `templates`:

```html
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
```

#### Paso 3: Modificar `app.py` para incluir autenticación

Vamos a añadir una ruta de inicio de sesión (`/login`) y lógica para manejar sesiones.

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Datos de usuario para la autenticación (esto es solo un ejemplo, normalmente se almacenan en una base de datos)
usuarios = {
    "usuario1": "password1",
    "usuario2": "password2"
}

@app.route('/')
def home():
    nombre = "Tu Nombre"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Tu Nombre"
    return render_template('about.html', nombre=nombre)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']

        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact.html')

        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        # Aquí se debe agregar la lógica para guardar los datos del usuario en una base de datos
        return f"Registro exitoso. Bienvenido, {username}!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in usuarios or usuarios[username] != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('home'))

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

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación del código

- **Línea 5**: Creamos un diccionario `usuarios` para almacenar datos de usuario y contraseñas. En una aplicación real, estos datos se almacenarían en una base de datos.
- **Líneas 38-52**: Añadimos la ruta `/login` para manejar el inicio de sesión. Validamos las credenciales del usuario y si son correctas, guardamos el nombre de usuario en la sesión.
- **Líneas 54-57**: Añadimos la ruta `/logout` para cerrar la sesión.
- **Líneas 59-67**: Creamos un decorador `login_required` para proteger rutas que requieren autenticación.
- **Líneas 69-71**: Añadimos la ruta `/profile` que está protegida por el decorador `login_required`.

### Tarea para los alumnos

Ahora, quiero que cada uno de ustedes cree una nueva funcionalidad para cambiar la contraseña del usuario.

#### Requisitos de la tarea

1. Crea una nueva ruta `/change_password` en tu archivo `mi_app.py`.
2. Crea una plantilla llamada `change_password.html` dentro de la carpeta `templates`.
3. En la plantilla `change_password.html`, incluye un formulario con campos para la contraseña actual, la nueva contraseña y la confirmación de la nueva contraseña.
4. Valida que todos los campos estén completos y que la nueva contraseña coincida con la confirmación.
5. Si la validación es exitosa, actualiza la contraseña del usuario (en este caso, actualiza el diccionario `usuarios`).
6. Si la validación falla, muestra un mensaje flash de error.

#### Sugerencia de código para `mi_app.py`

```python
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Datos de usuario para la autenticación (esto es solo un ejemplo, normalmente se almacenan en una base de datos)
usuarios = {
    "usuario1": "password1",
    "usuario2": "password2"
}

@app.route('/')
def home():
    nombre = "Tu Nombre"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Tu Nombre"
    return render_template('about.html', nombre=nombre)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']

        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact.html')

        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        # Aquí se debe agregar la lógica para guardar los datos del usuario en una base de datos
        return f"Registro exitoso. Bienvenido, {username}!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in usuarios or usuarios[username] != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('home'))

# Decorador para rutas protegidas
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
```
