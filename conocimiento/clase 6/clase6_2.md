```

Si en Flask, haces:

app.py
class Usuario(..) = {
        campo1 = ...
        campo2 = ...
}
....

Consola:
flask db migrate -m "Add User"
flask db upgrade

app.py (modificacion)
class Usuario(..) = {
        campo1 = ...
        campo2 = ...
        campo3 = ...    /* Aplico cambio */
}
....

Consola:
flask db upgrade


app.py (modificacion)
class Usuario(..) = {
        campo1 = ...
        campo2 = ...
        campo3 = ...
}

class Tarea(..) = {
       campo1 = ...
       campo2 =...
....

Consola:
flask db migrate -m "Add Tarea"
flask db upgrade

app.py (modificacion)
class Usuario(..) = {
        campo1 = ...
        campo2 = ...
        campo3 = ...
}

class Tarea(..) = {
       campo1 = ...
       campo2 =...
       campo3 = ...    /* Aplico cambio */
....

Consola:
flask db upgrade

app.py (modificacion)
class Usuario(..) = {
        campo1 = ...
        campo2 = ...
        campo3 = ...
        campo4=...  /* Aplico cambio */
}

class Tarea(..) = {
       campo1 = ...
       campo2 =...
       campo3 = ...
       campo4=...      /* Aplico cambio */
....

Consola:
flask db upgrade

Es correcto?

```

No, el procedimiento que has descrito no es correcto en su totalidad. El comando `flask db upgrade` solo aplica la migración más reciente que ya ha sido generada, no genera una nueva migración automáticamente cuando se detectan cambios en los modelos. Aquí te muestro el procedimiento correcto para manejar migraciones con Flask-Migrate y Alembic:

1. **Primera migración**:

   ```python
   # app.py
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_migrate import Migrate

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
   db = SQLAlchemy(app)
   migrate = Migrate(app, db)

   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
   ```

   **En consola**:

   ```bash
   flask db init  # Solo la primera vez para inicializar la carpeta de migraciones
   flask db migrate -m "Add User"
   flask db upgrade
   ```

2. **Modificación en el modelo Usuario**:

   ```python
   # app.py
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))  # Aplico cambio
   ```

   **En consola**:

   ```bash
   flask db migrate -m "Add campo3 to Usuario"
   flask db upgrade
   ```

3. **Añadiendo el modelo Tarea**:

   ```python
   # app.py
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))

   class Tarea(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
   ```

   **En consola**:

   ```bash
   flask db migrate -m "Add Tarea"
   flask db upgrade
   ```

4. **Modificación en el modelo Tarea**:

   ```python
   # app.py
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))

   class Tarea(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))  # Aplico cambio
   ```

   **En consola**:

   ```bash
   flask db migrate -m "Add campo3 to Tarea"
   flask db upgrade
   ```

5. **Otra modificación en ambos modelos**:

   ```python
   # app.py
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))
       campo4 = db.Column(db.String(128))  # Aplico cambio

   class Tarea(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))
       campo4 = db.Column(db.String(128))  # Aplico cambio
   ```

   **En consola**:

   ```bash
   flask db migrate -m "Add campo4 to Usuario and Tarea"
   flask db upgrade
   ```

Es crucial recordar siempre correr `flask db migrate` para generar una nueva migración cada vez que haces cambios en tus modelos. Luego, aplicar los cambios con `flask db upgrade`. Sin estos pasos, las modificaciones en tus modelos no se reflejarán en la base de datos.
