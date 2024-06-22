### Continuación de la Clase 4

Vamos a continuar con la implementación de la funcionalidad para cambiar la contraseña.

#### Paso 4: Crear el formulario de cambio de contraseña

Creemos un archivo `change_password.html` en el directorio `templates`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Change Password</title>
  </head>
  <body>
    <h1>Cambiar Contraseña</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/change_password" method="post">
      <label for="current_password">Contraseña Actual:</label><br />
      <input
        type="password"
        id="current_password"
        name="current_password"
      /><br />
      <label for="new_password">Nueva Contraseña:</label><br />
      <input type="password" id="new_password" name="new_password" /><br />
      <label for="confirm_password">Confirmar Nueva Contraseña:</label><br />
      <input
        type="password"
        id="confirm_password"
        name="confirm_password"
      /><br /><br />
      <input type="submit" value="Cambiar Contraseña" />
    </form>
  </body>
</html>
```

#### Paso 5: Añadir la lógica de cambio de contraseña en `app.py`

```python
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']

        if usuarios[username] != current_password:
            flash('La contraseña actual es incorrecta')
            return render_template('change_password.html')

        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden')
            return render_template('change_password.html')

        usuarios[username] = new_password
        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('profile'))
    return render_template('change_password.html')
```

### Explicación del código

- **Líneas 74-93**: Añadimos la ruta `/change_password` que maneja la lógica de cambio de contraseña.
  - Validamos que la contraseña actual coincida con la que está almacenada.
  - Verificamos que los campos de la nueva contraseña y la confirmación no estén vacíos.
  - Nos aseguramos de que las nuevas contraseñas coincidan.
  - Actualizamos la contraseña en el diccionario `usuarios` y mostramos un mensaje de éxito.

### Tarea para los alumnos

1. Asegúrense de que la ruta `/change_password` está protegida por el decorador `login_required`.
2. Añadan una validación más robusta para las contraseñas (por ejemplo, longitud mínima, caracteres especiales, etc.).
3. Implementen una funcionalidad adicional para que los usuarios puedan recuperar su contraseña mediante un enlace enviado a su correo electrónico (esto implicará configurar el envío de correos y manejar tokens de recuperación).

---

En la próxima clase, aprenderemos a manejar bases de datos utilizando SQLAlchemy, lo que nos permitirá almacenar usuarios y otros datos de manera más estructurada y persistente. ¡Buena suerte y feliz codificación!
