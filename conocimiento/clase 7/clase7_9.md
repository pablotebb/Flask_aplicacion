### Clase 7: Continuación - Mejora del Perfil de Usuario (Optimización y Verificación de Imágenes)

#### Objetivo

- Implementar la redimensionamiento automático de imágenes para asegurar que las fotos de perfil no sean demasiado grandes.
- Usar la librería `Pillow` para manipular las imágenes antes de guardarlas.
- Implementar un sistema de verificación de correo electrónico al registrarse y activar la cuenta mediante un enlace enviado por correo.

### Optimización de Imágenes con Pillow

#### Paso 1: Instalar Pillow

Primero, necesitamos instalar la librería `Pillow` para la manipulación de imágenes:

```bash
pip install Pillow
```

#### Paso 2: Redimensionar Imágenes al Subir

Modifiquemos nuestro archivo `app.py` para incluir la funcionalidad de redimensionamiento de imágenes usando `Pillow`.

```python
from PIL import Image

@app.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    if request.method == 'POST' and 'profile_pic' in request.files:
        file = request.files['profile_pic']
        filename = secure_filename(file.filename)

        # Guardar el archivo temporalmente
        temp_filepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        file.save(temp_filepath)

        # Redimensionar la imagen
        image = Image.open(temp_filepath)
        image.thumbnail((150, 150))
        image.save(temp_filepath)

        # Guardar la imagen final
        final_filepath = photos.save(temp_filepath)
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')
```

### Verificación de Correo Electrónico

#### Paso 1: Modificación del Modelo de Usuario

Añadimos un campo `is_active` para indicar si la cuenta del usuario está activa.

```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'
```

#### Paso 2: Enviar Enlace de Verificación

Añadimos la lógica para enviar un correo electrónico de verificación después del registro.

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado.')
            return render_template('register.html')

        # Crear nuevo usuario
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Enviar correo de verificación
        token = s.dumps(email, salt='email-confirm-salt')
        msg = Message('Confirma tu correo electrónico', sender='your-email@example.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = f'Para activar tu cuenta, haz clic en el siguiente enlace: {link}'
        mail.send(msg)

        flash('Se ha enviado un enlace de verificación a tu correo electrónico.')
        return redirect(url_for('login'))
    return render_template('register.html')
```

#### Paso 3: Confirmar el Enlace de Verificación

Añadimos la lógica para confirmar el enlace de verificación y activar la cuenta del usuario.

```python
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace de verificación ha expirado.')
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.is_active = True
        db.session.commit()
        flash('Tu cuenta ha sido activada exitosamente.')
    else:
        flash('La verificación de correo falló.')
    return redirect(url_for('login'))
```

### Actualización de la Lógica de Inicio de Sesión

Modificamos la ruta de inicio de sesión para verificar si la cuenta del usuario está activa.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username, password=password).first()

        if usuario and usuario.is_active:
            session['username'] = username
            flash('Has iniciado sesión exitosamente.')
            return redirect(url_for('profile'))
        elif usuario and not usuario.is_active:
            flash('Tu cuenta no está activada. Por favor, verifica tu correo electrónico.')
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    return render_template('login.html')
```

### Verificación final

1. **Registro y Verificación de Correo**: Regístrate con un nuevo usuario y verifica que recibes un correo electrónico con el enlace de verificación.
2. **Redimensionamiento de Imágenes**: Sube una imagen de perfil y verifica que se redimensiona correctamente.
3. **Inicio de Sesión**: Intenta iniciar sesión con una cuenta no verificada y verifica que recibes un mensaje adecuado. Luego, verifica la cuenta y asegúrate de que puedas iniciar sesión.

### Conclusión

Con esta implementación, has añadido funcionalidades avanzadas a tu aplicación Flask, mejorando la seguridad y la experiencia del usuario. Ahora los usuarios pueden subir fotos de perfil redimensionadas automáticamente y verificar su cuenta a través de un enlace enviado por correo electrónico.

### Tarea para los alumnos

1. **Manejo de Errores**:

   - Implementa manejo de errores para casos donde el enlace de verificación expira o es inválido.
   - Mejora la experiencia del usuario con mensajes claros y específicos.

2. **Seguridad Adicional**:
   - Implementa la funcionalidad para reenvío del enlace de verificación en caso de que el usuario no reciba el correo.
   - Añade autenticación de dos factores (2FA) para mayor seguridad.

Estas tareas adicionales les ayudarán a seguir mejorando sus habilidades en el desarrollo de aplicaciones web con Flask y asegurar que sus aplicaciones sean seguras y robustas. ¡Buena suerte y feliz codificación!
