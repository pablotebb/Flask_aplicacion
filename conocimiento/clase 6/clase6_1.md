Flask-Migrate es una extensión que utiliza Alembic para manejar las migraciones de bases de datos en Flask a través de SQLAlchemy. Esto permite realizar cambios en el esquema de la base de datos de forma controlada y reversible.

### Clase 6: Migraciones de Bases de Datos

#### 1. Introducción a Flask-Migrate

Flask-Migrate simplifica la gestión de cambios en el esquema de la base de datos al permitirte crear y aplicar migraciones fácilmente. Las migraciones son cambios incrementales en el esquema de la base de datos que se aplican secuencialmente.

#### 2. Instalación de Flask-Migrate

Primero, instalamos Flask-Migrate:

```bash
pip install Flask-Migrate
```

#### 3. Configuración Inicial

Integra Flask-Migrate en tu aplicación Flask. Vamos a modificar el archivo `app.py` para incluir Flask-Migrate y realizar la configuración inicial:

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializar Flask-Migrate
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Definición del modelo de usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Definición del modelo de tarea
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### 4. Creación de Migraciones

Para iniciar la configuración de migraciones, primero debes inicializar Alembic en tu proyecto:

```bash
flask db init
(Nota - Tiene que estar en el directorio, donde este app.py)
```

Este comando creará un directorio `migrations` en tu proyecto, que contendrá todos los archivos de configuración y las migraciones.

#### 5. Crear una Migración

Cuando realices cambios en tus modelos (por ejemplo, añadir un nuevo campo a una tabla), debes crear una nueva migración:

```bash
flask db migrate -m "Descripción del cambio"
```

Este comando generará un archivo de migración en el directorio `migrations` que describirá los cambios en el esquema de la base de datos.

#### 6. Aplicar Migraciones

Para aplicar los cambios en el esquema de la base de datos, usa el siguiente comando:

```bash
flask db upgrade
```

Este comando aplicará todas las migraciones pendientes a la base de datos.

#### 7. Gestión de Cambios en el Esquema de la Base de Datos

Si necesitas revertir una migración (por ejemplo, si una migración introdujo un error), puedes usar:

```bash
flask db downgrade
```

Esto revertirá la última migración aplicada. Si deseas revertir múltiples migraciones, debes especificar la versión a la que deseas volver.

#### Ejemplo Práctico

Vamos a suponer que queremos añadir un campo `due_date` al modelo `Task` para almacenar la fecha de vencimiento de una tarea.

1. **Modificar el Modelo**:

   Modifica la clase `Task` para incluir el nuevo campo:

   ```python
   class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       content = db.Column(db.String(200), nullable=False)
       completed = db.Column(db.Boolean, default=False)
       due_date = db.Column(db.Date, nullable=True)  # Nuevo campo
       user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   ```

2. **Crear y Aplicar la Migración**:

   Ejecuta los siguientes comandos para crear y aplicar la migración:

   ```bash
   flask db migrate -m "Add due_date to Task"
   flask db upgrade
   ```

3. **Actualizar la Plantilla HTML**:

   Actualiza las plantillas para incluir el nuevo campo `due_date` donde sea necesario. Por ejemplo, en `tasks.html`, puedes añadir un campo para ingresar la fecha de vencimiento:

   ```html
   <!-- templates/tasks.html -->
   {% extends 'base.html' %} {% block title %}My Tasks{% endblock %} {% block
   content %}
   <h1>My Tasks</h1>
   <ul>
     {% for task in current_user.tasks %}
     <li>
       {{ task.content }} - Due: {{ task.due_date }}
       <form
         method="POST"
         action="{{ url_for('toggle_task', task_id=task.id) }}"
       >
         <input
           type="checkbox"
           {%
           if
           task.completed
           %}checked{%
           endif
           %}
           onchange="this.form.submit()"
         />
       </form>
       <a href="{{ url_for('edit_task', task_id=task.id) }}">Edit</a>
       <a href="{{ url_for('delete_task', task_id=task.id) }}">Delete</a>
     </li>
     {% endfor %}
   </ul>
   <h2>Add New Task</h2>
   <form method="POST" action="{{ url_for('add_task') }}">
     <label for="content">Task:</label>
     <input type="text" id="content" name="content" required />
     <label for="due_date">Due Date:</label>
     <input type="date" id="due_date" name="due_date" />
     <button type="submit">Add Task</button>
   </form>
   {% endblock %}
   ```

4. **Actualizar la Vista para Manejar el Nuevo Campo**:

   En `app.py`, actualiza la lógica para manejar el nuevo campo `due_date`:

   ```python
   from datetime import datetime
   from flask import Flask, render_template, request, redirect, url_for, flash
   from flask_sqlalchemy import SQLAlchemy
   from flask_migrate import Migrate
   from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
   from werkzeug.security import generate_password_hash, check_password_hash

   app = Flask(__name__)
   app.secret_key = 'supersecretkey'
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

   db = SQLAlchemy(app)
   migrate = Migrate(app, db)
   login_manager = LoginManager(app)
   login_manager.login_view = 'login'

   class User(UserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(100), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password_hash = db.Column(db.String(200), nullable=False)
       tasks = db.relationship('Task', backref='user', lazy=True)

   class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       content = db.Column(db.String(200), nullable=False)
       completed = db.Column(db.Boolean, default=False)
       due_date = db.Column(db.Date, nullable=True)
       user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

   @login_manager.user_loader
   def load_user(user_id):
       return User.query.get(int(user_id))

   @app.route('/')
   @login_required
   def index():
       return render_template('tasks.html')

   @app.route('/add', methods=['POST'])
   @login_required
   def add_task():
       content = request.form.get('content')
       due_date = request.form.get('due_date')
       if due_date:
           due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
       new_task = Task(content=content, due_date=due_date, user_id=current_user.id)
       db.session.add(new_task)
       db.session.commit()
       flash('Task added successfully.')
       return redirect(url_for('index'))

   if __name__ == '__main__':
       app.run(debug=True)
   ```

Con estos pasos, ahora tienes una aplicación Flask que incluye migraciones de bases de datos gestionadas por Flask-Migrate. Puedes seguir añadiendo funcionalidades y realizando cambios en el esquema de la base de datos utilizando migraciones de manera segura y organizada.
