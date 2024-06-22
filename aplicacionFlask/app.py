from flask import Flask, render_template, request, flash, redirect, url_for, session
from validar_contrasena import validar_contrasena
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Configurar la URI de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'
      
# Resto del código de la aplicación...

# Decorador para rutas protegidas (para proteger rutas que requieren autenticación)
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    nombre = "Pablo"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']

        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact2.html')

        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact2.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
    
        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')
          
        try:
            validar_contrasena(password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('register.html')

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(f'Registro exitoso. Bienvenido, {username}!')
        return redirect(url_for('profile'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or usuario.password != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('home'))
    return render_template('login.html')
  
# Añadimos la ruta /logout para cerrar la sesión.
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('home'))
  

  
# Añadimos la ruta /profile que está protegida por el decorador login_required.
@app.route('/profile')
@login_required
def profile():
    username = session['username']
    return f"Bienvenido a tu perfil, {username}!"

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario.password != current_password:
            flash('La contraseña actual es incorrecta')
            return render_template('change_password.html')

        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden')
            return render_template('change_password.html')
          
        try:
            validar_contrasena(new_password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('change_password.html')

        usuario.password = new_password
        db.session.commit()

        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('profile'))
    return render_template('change_password.html')
  
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

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


