from flask import Flask, render_template, request, flash, redirect, url_for, session
from validar_contrasena import validar_contrasena
# from recuperar_contrasena import recuperar_contrasena



app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Datos de usuario para la autenticación (esto es solo un ejemplo, normalmente se almacenan en una base de datos)
usuarios = {
    "usuario1": "password1",
    "usuario2": "password2"
}

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
        
        try:
            validar_contrasena(password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('register.html')


        if not username or not email or not password:
            flash('Todos los campos son obligatorios')
            return render_template('register.html')

        # Aquí se debe agregar la lógica para guardar los datos del usuario en una base de datos (en este caso los meteriamos en un diccionario)
        
        return f"Registro exitoso. Bienvenido, {username}!"
    return render_template('register.html')

# Añadimos la ruta /login para manejar el inicio de sesión. Validamos las credenciales del usuario y si son correctas, guardamos el nombre de usuario en la sesión.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
  
        # Validamos las credenciales del usuario y si son correctas
        if username not in usuarios or usuarios[username] != password:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('login.html')

        # guardamos el nombre de usuario en la sesión
        session['username'] = username
        flash('Inicio de sesión exitoso')
        return redirect(url_for('home'))
    return render_template('login.html')
  

  
# Decorador para rutas protegidas (para proteger rutas que requieren autenticación)
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
  
# Añadimos la ruta /logout para cerrar la sesión.
@app.route('/logout')
@login_required
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
  
# Añadimos la ruta /change_password que maneja la lógica de cambio de contraseña.  
# Nos aseguramos de que la ruta /change_password está protegida por el decorador login_required.
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']

        # Validamos que la contraseña actual coincida con la que está almacenada.
        if usuarios[username] != current_password:
            flash('La contraseña actual es incorrecta')
            return render_template('change_password.html')
        

        # Verificamos que los campos de la nueva contraseña y la confirmación no estén vacíos.
        if not new_password or not confirm_password:
            flash('Todos los campos son obligatorios')
            return render_template('change_password.html')
       

        # Nos aseguramos de que las nuevas contraseñas coincidan
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden')
            return render_template('change_password.html')
          
           
        try:
            validar_contrasena(new_password)
        except ValueError as e:
            # Mostrar mensaje de error al usuario
            flash(e)
            return render_template('change_password.html')

        # Actualizamos la contraseña en el diccionario usuarios y mostramos un mensaje de éxito.
        usuarios[username] = new_password
        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('logout'))
    return render_template('change_password.html')


# @app.route('/recuperar_contrasena', methods=['GET', 'POST'])
# def recuperar_contrasena(request):
#     if request.method == 'POST':
#         correo_electronico = request.form['correo_electronico']
#         return recuperar_contrasena(correo_electronico)
#     else:
#         return render_template('recuperar_contrasena.html')


# @app.route('/recuperar_contrasena/<token>', methods=['GET', 'POST'])
# def recuperar_contrasena_token(token):
#   try:
#     user_id, _ = URLSafeTimedSignature(app.config['SECRET_KEY']).validate(token)
#     user = User.query.get(user_id)
#   except:
#     flash('El token de recuperación es inválido o ha expirado.')
#     return redirect(url_for('login'))

#   if request.method == 'POST':
#     nueva_contrasena = request.form['nueva_contrasena']
#     # Cambiar la contraseña del usuario en la base de datos
#     flash('Contraseña actualizada correctamente.')
#     return redirect(url_for('login'))
#   else:
#     return render_template('recuperar_contrasena.html')




if __name__ == '__main__':
    app.run(debug=True)
