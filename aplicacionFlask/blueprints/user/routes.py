from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import user_bp
from extensions import db
from models import Usuario
from validar_contrasena import validar_contrasena

# user_bp = Blueprint('user', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Necesitas iniciar sesión primero')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@user_bp.route('/profile')
@login_required
def profile():
    print("Dentro de profile")
    # username = session['username']
    # return render_template('profile.html', username=username)
    return render_template('profile.html')

@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        username = session['username']
        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario or usuario.password != current_password:
            flash('La contraseña actual no es correcta')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden')
            return render_template('change_password.html')

        try:
            validar_contrasena(new_password)
        except ValueError as e:
            flash(e)
            return render_template('change_password.html')

        usuario.password = new_password
        db.session.commit()

        flash('Contraseña actualizada con éxito')
        return redirect(url_for('user.profile'))
    return render_template('change_password.html')
