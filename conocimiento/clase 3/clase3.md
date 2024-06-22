¡Perfecto! Continuemos con el curso. Ahora que hemos aprendido a usar plantillas con Jinja2, vamos a avanzar hacia la gestión de formularios y el manejo de datos enviados desde el cliente. Esto es crucial para cualquier aplicación web que interactúe con los usuarios.

### Clase 3: Manejo de Formularios en Flask

#### Objetivo

- Aprender a manejar formularios en Flask.
- Procesar datos enviados por el usuario.
- Validación básica de formularios.

#### Temas a cubrir

1. Métodos HTTP: GET y POST.
2. Procesar formularios usando Flask.
3. Validar datos de formulario.
4. Mostrar mensajes de validación en la plantilla.

### Métodos HTTP: GET y POST

Cuando trabajamos con formularios en aplicaciones web, generalmente usamos dos métodos HTTP principales: GET y POST.

- **GET**: Se utiliza para solicitar datos del servidor. Los datos se envían a través de la URL.
- **POST**: Se utiliza para enviar datos al servidor. Los datos se envían en el cuerpo de la solicitud, lo que es más seguro para enviar información sensible.

### Procesar formularios usando Flask

Vamos a modificar nuestro ejemplo anterior para manejar los datos del formulario de contacto.

#### Paso 1: Modificar la ruta `/contact` para manejar POST

Modifiquemos el archivo `app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

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
        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación del código

- **Línea 3**: Importamos `request` de `flask`.
- **Línea 17**: Modificamos la ruta `/contact` para manejar tanto GET como POST usando el parámetro `methods`.
- **Líneas 18-23**: Si el método de la solicitud es POST, procesamos los datos del formulario. `request.form` contiene los datos del formulario enviados en una solicitud POST.
- **Línea 24**: Si el método de la solicitud es GET, simplemente renderizamos la plantilla `contact.html`.

### Validar datos de formulario

Vamos a agregar una validación básica para asegurarnos de que todos los campos estén completos antes de procesar el formulario.

#### Paso 2: Añadir validación básica

Modifiquemos nuevamente el archivo `app.py`:

```python
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación del código

- **Línea 4**: Importamos `flash` de `flask` para mostrar mensajes flash.
- **Línea 6**: Establecemos una `secret_key` necesaria para usar la funcionalidad de mensajes flash.
- **Líneas 19-23**: Validamos que todos los campos del formulario estén completos. Si falta algún campo, mostramos un mensaje flash y renderizamos nuevamente la plantilla del formulario.

#### Paso 3: Mostrar mensajes flash en la plantilla

Modifiquemos el archivo `contact.html` para mostrar mensajes flash:

```html
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
```

### Explicación del código

- **Líneas 10-17**: Usamos la función `get_flashed_messages` para obtener y mostrar mensajes flash.

### Tarea para los alumnos

Ahora, ustedes van a crear una nueva funcionalidad que permitirá a los usuarios registrarse en la aplicación.

#### Requisitos de la tarea

1. Crea una nueva ruta `/register` en tu archivo `mi_app.py`.
2. Crea una plantilla llamada `register.html` dentro de la carpeta `templates`.
3. En la plantilla `register.html`, incluye un formulario con campos para el nombre de usuario, correo electrónico y contraseña.
4. Valida que todos los campos estén completos en el servidor.
5. Si la validación es exitosa, muestra un mensaje de éxito.
6. Si la validación falla, muestra un mensaje flash de error.

#### Sugerencia de código para `mi_app.py`

```python
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

        return f"Registro exitoso. Bienvenido, {username}!"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### Sugerencia de código para `register.html`

```html
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
```

Asegúrate de que la etiqueta `form` tenga los atributos `action` y `method` configurados adecuadamente. En la próxima clase, exploraremos cómo manejar sesiones y autenticación de usuarios. ¡Buena suerte y feliz codificación!
