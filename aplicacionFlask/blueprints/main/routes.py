from flask import Blueprint, flash, render_template, request
from . import main_bp

# main_bp = Blueprint('main', __name__)


print("____________________MAIN ROUTES _____________________")


@main_bp.route('/')
def home():
   
    print(f"""
    --------------------
    /HOME
    -------------------
    """) 
    
    nombre = "Pablo"
    print(f"""
    ----------------------------------------------------------
    nombre = {nombre}
    ----------------------------------------------------------
    """)
    return render_template('index.html', nombre=nombre)

@main_bp.route('/about')
def about():
  
    print(f"""
    --------------------
    /ABOUT
    -------------------
    """) 
  
    nombre = "Pablo"
    print(f"""
    ----------------------------------------------------------
    nombre = {nombre}
    ----------------------------------------------------------
    """)
    return render_template('about.html', nombre=nombre)
  

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
  
    print(f"""
    --------------------
    /CONTACT
    -------------------
    """) 
  
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']
        
        print(f"""
        --------------------
        nombre =  {nombre}
        email =   {email}
        mensaje = {mensaje}
        -------------------
        """) 

        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact2.html')

        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
    return render_template('contact2.html')
  
  
