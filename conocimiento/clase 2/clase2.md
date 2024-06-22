¡Excelente! Vamos a continuar con el desarrollo de nuestras habilidades en Flask. Ahora que han creado su primera aplicación básica, es momento de introducir conceptos más avanzados.

### Clase 2: Plantillas con Jinja2

#### Objetivo

- Introducir el motor de plantillas Jinja2.
- Crear y renderizar plantillas HTML.
- Pasar datos desde Flask a las plantillas.

#### Temas a cubrir

1. ¿Qué es Jinja2?
2. Crear plantillas HTML.
3. Renderizar plantillas en Flask.
4. Pasar datos a las plantillas.

### ¿Qué es Jinja2?

Jinja2 es un motor de plantillas para Python que se integra perfectamente con Flask. Permite generar HTML dinámico desde el servidor, utilizando variables, bucles, y estructuras de control en las plantillas.

### Crear plantillas HTML

Vamos a estructurar nuestra aplicación para usar plantillas. La estructura de nuestra aplicación será la siguiente:

```
mi_app/
│
├── templates/
│   ├── index.html
│   └── about.html
├── app.py
```

#### Paso 1: Crear el directorio de plantillas

Dentro de tu directorio de proyecto, crea una carpeta llamada `templates`.

#### Paso 2: Crear plantillas HTML

Dentro de la carpeta `templates`, crea un archivo llamado `index.html` y agrega el siguiente código:

```html
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
```

Luego, crea otro archivo llamado `about.html`:

```html
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
```

### Renderizar plantillas en Flask

Modificaremos nuestro archivo `app.py` para renderizar estas plantillas en lugar de devolver texto simple.

#### Paso 3: Modificar `app.py`

Aquí está el nuevo contenido de `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    nombre = "Tu Nombre"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Tu Nombre"
    return render_template('about.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación del código

- **Línea 1**: Además de `Flask`, importamos la función `render_template` de `flask`.
- **Línea 5 y 10**: En lugar de devolver texto simple, usamos `render_template` para renderizar los archivos HTML y pasamos la variable `nombre` a las plantillas.

### Ejecución de la aplicación

Guarda todos los archivos y ejecuta de nuevo la aplicación con `python app.py`. Visita las URLs `http://127.0.0.1:5000/` y `http://127.0.0.1:5000/about` para ver las plantillas renderizadas.

### Tarea para los alumnos

Ahora, quiero que ustedes creen una nueva ruta y plantilla:

#### Requisitos de la tarea

1. Agrega una nueva ruta `/contact` en tu archivo `mi_app.py`.
2. Crea una plantilla llamada `contact.html` dentro de la carpeta `templates`.
3. En la plantilla `contact.html`, incluye un formulario simple con campos para el nombre, correo electrónico y mensaje.
4. Renderiza la plantilla `contact.html` desde la nueva ruta `/contact`.

#### Sugerencia de código para `mi_app.py`

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    nombre = "Tu Nombre"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Tu Nombre"
    return render_template('about.html', nombre=nombre)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### Sugerencia de código para `contact.html`

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
    <form action="#" method="post">
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

Asegúrate de que la etiqueta `form` tenga los atributos `action` y `method` configurados adecuadamente, aunque por ahora solo estamos creando la estructura HTML.

En la próxima clase, veremos cómo manejar formularios y datos enviados desde el cliente usando Flask. ¡Buena suerte y feliz codificación!
