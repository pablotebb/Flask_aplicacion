¡Hola a todos y bienvenidos al curso de Flask! Flask es un framework ligero y flexible de Python que facilita la creación de aplicaciones web. En este curso, aprenderemos a construir aplicaciones web usando Flask, comenzando desde lo básico hasta temas más avanzados. Construiremos varias aplicaciones que podrán incluir en su portafolio.

### Clase 1: Introducción a Flask y Primera Aplicación

#### Objetivo

- Introducir Flask y su instalación.
- Crear la primera aplicación web sencilla.

#### Temas a cubrir

1. ¿Qué es Flask?
2. Instalación de Flask.
3. Estructura básica de una aplicación Flask.
4. Crear una ruta y una vista simple.

### ¿Qué es Flask?

Flask es un microframework web para Python basado en Werkzeug y Jinja2. Es llamado "micro" porque no incluye muchas de las características predefinidas de otros frameworks web más grandes, como Django. Esto lo hace flexible y adecuado para proyectos de cualquier tamaño.

### Instalación de Flask

Para instalar Flask, necesitas tener Python y pip (el gestor de paquetes de Python) instalados en tu máquina. Ejecuta el siguiente comando para instalar Flask:

```bash
pip install Flask
```

### Estructura básica de una aplicación Flask

Vamos a empezar con una aplicación muy simple para entender la estructura básica.

1. **Crear la aplicación**:
   Crea un archivo llamado `app.py` y agrega el siguiente código:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola, Mundo! Bienvenidos a Flask."

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación del código

- **Línea 1**: Importamos la clase `Flask` del paquete `flask`.
- **Línea 3**: Creamos una instancia de la clase `Flask`. La instancia `app` será nuestra aplicación.
- **Línea 5**: Usamos el decorador `@app.route('/')` para decirle a Flask que la función `home` debe responder a las solicitudes a la URL raíz (`/`).
- **Línea 6**: La función `home` devuelve un simple mensaje "¡Hola, Mundo!".
- **Línea 8**: Si este script se ejecuta directamente, inicia el servidor de desarrollo de Flask con `debug=True` para que podamos ver los errores de forma más detallada.

### Ejecución de la aplicación

Guarda el archivo y ejecuta el siguiente comando en la terminal para iniciar la aplicación:

```bash
python app.py
```

Abre tu navegador web y ve a `http://127.0.0.1:5000/`. Deberías ver el mensaje "¡Hola, Mundo! Bienvenidos a Flask."

### Tarea para los alumnos

Ahora, cada uno de ustedes va a crear una aplicación Flask similar, pero con algunas variaciones para practicar.

#### Requisitos de la aplicación

1. Crea un nuevo archivo llamado `mi_app.py`.
2. En lugar de "¡Hola, Mundo! Bienvenidos a Flask.", la aplicación debería responder con "¡Hola, [tu nombre]! Bienvenido a tu primera aplicación Flask." en la URL raíz.
3. Agrega una nueva ruta `/about` que responda con el mensaje "Esta es la página About de [tu nombre]."

#### Sugerencia de código

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola, [tu nombre]! Bienvenido a tu primera aplicación Flask."

@app.route('/about')
def about():
    return "Esta es la página About de [tu nombre]."

if __name__ == '__main__':
    app.run(debug=True)
```

Cambia `[tu nombre]` por tu nombre real. Guarda el archivo y ejecútalo usando `python mi_app.py`. Abre tu navegador y verifica las URLs `http://127.0.0.1:5000/` y `http://127.0.0.1:5000/about`.

Con esto, hemos cubierto la introducción a Flask y la creación de una aplicación básica. En la próxima clase, exploraremos cómo trabajar con plantillas usando Jinja2 para crear páginas HTML más dinámicas y complejas. ¡Feliz codificación!
