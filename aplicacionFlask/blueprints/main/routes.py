from flask import Blueprint, flash, render_template, request
from . import main_bp

# main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    nombre = "Pablo"
    print("NOMBRE:", nombre)
    return render_template('index.html', nombre=nombre)

@main_bp.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)
  

@main_bp.route('/contact', methods=['GET', 'POST'])
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
  
  
