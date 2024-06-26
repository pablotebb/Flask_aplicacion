> En Flask;
> @app.route('/upload_profile_pic', methods=['GET', 'POST'])
> @login_required
> def upload_profile_pic():
> if request.method == 'POST' and 'profile_pic' in request.files:
> file = request.files['profile_pic']
> filename = secure_filename(file.filename)
> Me sale este error:
> TypeError
> TypeError: storage must be a werkzeug.FileStorage

El error `TypeError: storage must be a werkzeug.FileStorage` sugiere que hay un problema con el tipo de archivo que se está pasando a la función `photos.save()`. Es probable que `photos.save()` esté esperando un objeto de tipo `werkzeug.FileStorage`, pero en su lugar está recibiendo una cadena de caracteres que representa la ruta del archivo.

Para solucionar este problema, debes ajustar el flujo de trabajo de tu código. Aquí tienes una versión modificada de tu función `upload_profile_pic` que debería resolver el problema:

1. Guarda el archivo subido temporalmente.
2. Redimensiona la imagen.
3. Vuelve a cargar el archivo redimensionado en un objeto `FileStorage`.
4. Guarda el archivo usando `photos.save()`.

```python
from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image
import os
from io import BytesIO
from werkzeug.datastructures import FileStorage
from yourapp import app, db, photos
from yourapp.models import Usuario

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

        # Guardar la imagen redimensionada en un objeto BytesIO
        image_bytes = BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)

        # Crear un nuevo objeto FileStorage para la imagen redimensionada
        resized_file = FileStorage(image_bytes, filename=filename, content_type=file.content_type)

        # Guardar la imagen final
        final_filepath = photos.save(resized_file)
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        # Actualizar la base de datos con la ruta del archivo final
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')
```

### Explicación de los cambios:

1. **Redimensionado y Guardado en BytesIO**:

   - Después de redimensionar la imagen, en lugar de guardarla directamente en el sistema de archivos, se guarda en un objeto `BytesIO`.

2. **Crear un Nuevo Objeto FileStorage**:
   - Un nuevo objeto `FileStorage` se crea a partir del contenido del `BytesIO`. Esto simula un archivo subido que puede ser manejado correctamente por `photos.save()`.

### Dependencias

Asegúrate de tener instaladas las siguientes dependencias:

- Flask
- Flask-Login
- Werkzeug
- Pillow

Este código debería solucionar el problema y permitir la subida y redimensionado de la foto de perfil correctamente.

> y como se importan esas dependencias?

Para importar las dependencias necesarias para tu aplicación Flask y asegurarte de que todo funcione correctamente, debes asegurarte de tenerlas instaladas y luego importarlas en tu código. Aquí tienes los pasos detallados:

### Instalación de Dependencias

Puedes instalar las dependencias utilizando `pip`. Aquí tienes los comandos para instalar cada una de ellas:

```sh
pip install Flask
pip install Flask-Login
pip install Werkzeug
pip install Pillow
```

### Importación en tu Código

A continuación, debes importar las dependencias necesarias en tu archivo de aplicación Flask. Aquí tienes un ejemplo de cómo hacerlo:

```python
from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image
import os
from io import BytesIO
from werkzeug.datastructures import FileStorage
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from yourapp.models import Usuario  # Asegúrate de que esto apunta al lugar correcto

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'  # Directorio donde se guardarán las imágenes

# Inicializar las extensiones
db = SQLAlchemy(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Tu ruta de subida de foto de perfil
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

        # Guardar la imagen redimensionada en un objeto BytesIO
        image_bytes = BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)

        # Crear un nuevo objeto FileStorage para la imagen redimensionada
        resized_file = FileStorage(image_bytes, filename=filename, content_type=file.content_type)

        # Guardar la imagen final
        final_filepath = photos.save(resized_file)
        os.remove(temp_filepath)  # Eliminar el archivo temporal

        # Actualizar la base de datos con la ruta del archivo final
        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()
        usuario.profile_pic = final_filepath
        db.session.commit()

        flash('Foto de perfil subida y redimensionada exitosamente')
        return redirect(url_for('profile'))
    return render_template('upload_profile_pic.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Explicación de las Importaciones:

- `from flask import Flask, request, redirect, url_for, flash, render_template, session`: Importa los módulos necesarios de Flask.
- `from flask_login import login_required`: Importa el decorador `login_required` para proteger rutas.
- `from werkzeug.utils import secure_filename`: Importa la función para asegurar el nombre del archivo.
- `from PIL import Image`: Importa la librería PIL para manipular imágenes.
- `import os`: Importa el módulo OS para trabajar con el sistema de archivos.
- `from io import BytesIO`: Importa `BytesIO` para manejar archivos en memoria.
- `from werkzeug.datastructures import FileStorage`: Importa `FileStorage` para crear un objeto que simula un archivo subido.
- `from flask_sqlalchemy import SQLAlchemy`: Importa SQLAlchemy para manejar la base de datos.
- `from flask_uploads import UploadSet, IMAGES, configure_uploads`: Importa `flask-uploads` para manejar las subidas de archivos.
- `from yourapp.models import Usuario`: Importa el modelo `Usuario` desde tu aplicación. Asegúrate de que esta importación sea correcta según la estructura de tu proyecto.

### Nota Final

Asegúrate de que la configuración de la base de datos y las rutas de los archivos están correctamente definidas según la estructura de tu proyecto.
