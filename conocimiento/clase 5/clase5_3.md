### Continuación del Curso

Ahora que hemos configurado correctamente SQLAlchemy y hemos cubierto las operaciones básicas de registro, inicio de sesión y cambio de contraseña, vamos a continuar con la implementación de las funcionalidades adicionales que mencioné anteriormente: eliminación de cuenta y actualización del perfil del usuario.

### Implementación de la eliminación de cuenta

#### Paso 1: Crear la plantilla `delete_account.html`

Primero, creemos la plantilla que permitirá a los usuarios eliminar su cuenta. Coloca este archivo en el directorio `templates`.

`templates/delete_account.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Eliminar Cuenta</title>
  </head>
  <body>
    <h1>Eliminar Cuenta</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/delete_account" method="post">
      <p>
        ¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede
        deshacer.
      </p>
      <input type="submit" value="Eliminar Cuenta" />
    </form>
  </body>
</html>
```

#### Paso 2: Crear la ruta `delete_account` en `app.py`

Añade la lógica para manejar la eliminación de cuentas en `app.py`:

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

### Implementación de la actualización de perfil

#### Paso 1: Crear la plantilla `update_profile.html`

A continuación, crearemos la plantilla para que los usuarios puedan actualizar su perfil. Coloca este archivo en el directorio `templates`.

`templates/update_profile.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Actualizar Perfil</title>
  </head>
  <body>
    <h1>Actualizar Perfil</h1>

    {% with messages = get_flashed_messages() %} {% if messages %}
    <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %} {% endwith %}

    <form action="/update_profile" method="post">
      <label for="username">Nuevo Nombre de Usuario:</label><br />
      <input type="text" id="username" name="username" /><br />
      <label for="email">Nuevo Correo Electrónico:</label><br />
      <input type="email" id="email" name="email" /><br /><br />
      <input type="submit" value="Actualizar Perfil" />
    </form>
  </body>
</html>
```

#### Paso 2: Crear la ruta `update_profile` en `app.py`

Añade la lógica para manejar la actualización de perfil en `app.py`:

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

### Verificación final

#### Paso 1: Verificar que las nuevas rutas están protegidas

Asegúrate de que las rutas `/delete_account` y `/update_profile` están protegidas por el decorador `login_required`.

#### Paso 2: Pruebas

- **Eliminar cuenta**: Inicia sesión con un usuario de prueba, navega a la página de eliminación de cuenta y elimina la cuenta. Verifica que la cuenta se elimina correctamente y que la sesión se cierra.
- **Actualizar perfil**: Inicia sesión con un usuario de prueba, navega a la página de actualización de perfil, actualiza el nombre de usuario y el correo electrónico. Verifica que los cambios se aplican correctamente y que se actualiza la sesión.

### Conclusión

Con estas funcionalidades adicionales, has mejorado la aplicación Flask para incluir la eliminación de cuentas y la actualización de perfiles de usuario. Estas características son esenciales para una gestión completa de usuarios en una aplicación web.

### Tarea para los alumnos

Para consolidar lo aprendido, implementen las siguientes funcionalidades adicionales:

1. **Restablecimiento de contraseña**:

   - Cree una funcionalidad que permita a los usuarios restablecer su contraseña a través de un correo electrónico.
   - Utilice tokens de restablecimiento y configure el envío de correos electrónicos utilizando `Flask-Mail`.

2. **Perfil de usuario**:
   - Mejore la página de perfil para mostrar más información del usuario, como la fecha de creación de la cuenta.
   - Permita que los usuarios suban una foto de perfil.

Estas tareas les ayudarán a fortalecer su comprensión de Flask y a crear aplicaciones web más completas y funcionales. ¡Buena suerte y feliz codificación!
