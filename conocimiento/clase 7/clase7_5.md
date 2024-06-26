> Ahora, me da este error: <br>
> TemplateNotFound <br>
> jinja2.exceptions.TemplateNotFound: login.html

El error `TemplateNotFound: login.html` indica que Flask no puede encontrar el archivo `login.html` en la carpeta de plantillas. Asegúrate de que la estructura de tu proyecto incluye una carpeta de plantillas y que el archivo `login.html` está ubicado en la carpeta correcta.

### Estructura del Proyecto

Tu estructura de proyecto debería verse algo así:

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
├── templates/
│   ├── login.html
│   └── home.html  # Otros archivos de plantilla que puedas tener
├── extensions.py
├── models.py
└── validar_contrasena.py
```

### Verificación de Plantillas

Asegúrate de que la carpeta `templates` está en el mismo nivel que `app.py` y contiene el archivo `login.html`.

### Código de `app.py`

En `app.py`, asegúrate de que la aplicación está configurada correctamente para buscar plantillas en la carpeta `templates`:

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

### Ejemplo de `login.html`

Asegúrate de que `login.html` está en la carpeta `templates` y contiene el código HTML necesario. Aquí tienes un ejemplo simple de `login.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login</title>
  </head>
  <body>
    <h1>Login</h1>
    <form method="POST" action="{{ url_for('auth.login') }}">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" />
      <br />
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" />
      <br />
      <button type="submit">Login</button>
    </form>
  </body>
</html>
```

### Reiniciar la Aplicación

Después de asegurarte de que todo está en su lugar, reinicia la aplicación:

```sh
python app.py
```

Luego, ve a la URL `http://127.0.0.1:5000/login` en tu navegador. Si todo está configurado correctamente, deberías ver el formulario de inicio de sesión.

### Solución de Problemas Adicional

Si el problema persiste, verifica lo siguiente:

1. **Rutas de Plantillas:** Asegúrate de que no hay errores tipográficos en el nombre del archivo `login.html`.
2. **Permisos de Archivos:** Verifica los permisos de los archivos para asegurarte de que Flask tiene acceso a la carpeta y archivos de plantillas.
3. **Errores en el Navegador:** Revisa los registros de errores en la consola del navegador y en la consola donde se ejecuta Flask para obtener más detalles.
