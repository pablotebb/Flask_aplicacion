Esta es una técnica poderosa para organizar tu código de manera más limpia y estructurada, especialmente en aplicaciones grandes.

### Clase 7: Blueprints y Organización de la Aplicación

#### 1. Introducción a Blueprints

Blueprints en Flask permiten estructurar tu aplicación en componentes más pequeños y manejables. Cada Blueprint puede definir sus propias rutas, vistas, modelos y otros recursos. Esto ayuda a mantener el código organizado y facilita el mantenimiento y la escalabilidad.

#### 2. Modularización de la Aplicación

Vamos a modularizar nuestra aplicación de To-Do List utilizando Blueprints. Primero, vamos a definir la estructura de nuestro proyecto:

```
todo_app/
│
├── app.py
├── extensions.py
├── models.py
├── auth/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       ├── login.html
│       ├── register.html
├── tasks/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── tasks.html
├── templates/
│   └── base.html
└── static/
    └── style.css
```

#### 3. Configuración de Blueprints

Primero, creamos un archivo `extensions.py` para inicializar las extensiones que usaremos en la aplicación:

```python
# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
```

#### 4. Definición de Modelos

En el archivo `models.py`, definimos nuestros modelos:

```python
# models.py

from extensions import db
from flask_login import UserMixin

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
```

#### 5. Creación de Blueprints para Autenticación

En el directorio `auth`, creamos `__init__.py` y `routes.py` para gestionar la autenticación:

```python
# auth/__init__.py

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import routes
```

```python
# auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('tasks.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered and can log in')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
```

#### 6. Creación de Blueprints para las Tareas

En el directorio `tasks`, creamos `__init__.py` y `routes.py` para gestionar las tareas:

```python
# tasks/__init__.py

from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')

from . import routes
```

```python
# tasks/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Task
from extensions import db
from . import tasks_bp

@tasks_bp.route('/')
@login_required
def index():
    tasks = current_user.tasks
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    content = request.form['content']
    due_date = request.form.get('due_date')
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    new_task = Task(content=content, due_date=due_date, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully.')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('tasks.index'))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('tasks.index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('tasks.index'))
    if request.method == 'POST':
        task.content = request.form['content']
        due_date = request.form.get('due_date')
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('tasks.index'))
    return render_template('edit_task.html', task=task)
```

#### 7. Registro de Blueprints en la Aplicación Principal

Finalmente, modificamos `app.py` para registrar los Blueprints:

```python
# app.py

from flask import Flask
from extensions import db, migrate, login_manager
from auth import auth_bp
from tasks import tasks_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp, url_prefix='/tasks')

if __name__ == '__main__':
    app.run(debug=True)
```

#### 8. Plantillas HTML

Asegúrate de que tus plantillas HTML están en las carpetas correctas dentro de `auth/templates` y `tasks/templates`. Aquí hay un ejemplo básico de cómo podrían verse:

- **login.html** en `auth/templates`:

```html
<!-- auth/templates/login.html -->
{% extends 'base.html' %} {% block title %}Login{% endblock %} {% block content
%}
<h1>Login</h1>
<form method="POST">
  <label for="username">Username:</label>
  <input type="text" id="username" name="username" required /><br />
  <label for="password">Password:</label>
  <input type="password" id="password" name="password" required /><br />
  <button type="submit">Login</button>
</form>
{% endblock %}
```

- **register.html** en `auth/templates`:

```html
<!-- auth/templates/register.html -->
{% extends 'base.html' %} {% block title %}Register{% endblock %} {% block
content %}
<h1>Register</h1>
<form method="POST">
  <label for="username">Username:</label>
  <input type="text" id="username" name="username" required /><br />
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required /><br />
  <label for="password">Password:</label>
  <input type="password" id="password" name="password" required /><br />
  <button type="submit">Register</button>
</form>
{% endblock %}
```

- **tasks.html** en `

tasks/templates`:

```html
<!-- tasks/templates/tasks.html -->
{% extends 'base.html' %} {% block title %}My Tasks{% endblock %} {% block
content %}
<h1>My Tasks</h1>
<ul>
  {% for task in tasks %}
  <li>
    {{ task.content }} - Due: {{ task.due_date }}
    <form
      method="POST"
      action="{{ url_for('tasks.toggle_task', task_id=task.id) }}"
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
    <a href="{{ url_for('tasks.edit_task', task_id=task.id) }}">Edit</a>
    <a href="{{ url_for('tasks.delete_task', task_id=task.id) }}">Delete</a>
  </li>
  {% endfor %}
</ul>
<h2>Add New Task</h2>
<form method="POST" action="{{ url_for('tasks.add_task') }}">
  <label for="content">Task:</label>
  <input type="text" id="content" name="content" required />
  <label for="due_date">Due Date:</label>
  <input type="date" id="due_date" name="due_date" />
  <button type="submit">Add Task</button>
</form>
{% endblock %}
```

Con esta estructura, has modularizado tu aplicación de To-Do List utilizando Blueprints, lo que facilita su mantenimiento y escalabilidad. Cada módulo (autenticación y tareas) tiene su propio Blueprint, y estos se registran en la aplicación principal.
