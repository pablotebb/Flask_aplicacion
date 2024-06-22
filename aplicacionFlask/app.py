from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.secret_key = 'supersecretkey'

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
    nombre = "la empresa"
    
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']
        
        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact2.html')
          
        return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
   
    return render_template('contact2.html', nombre=nombre)
  
@app.route('/register', methods=['GET', 'POST'])
def register():
  nombre = "la empresa"
    
  if request.method == 'POST':
    nombre = request.form['username']
    email = request.form['email']
    contrasena = request.form['password']
        
    if not nombre or not email or not contrasena:
      flash('Todos los campos son obligatorios')
      return render_template('register.html')
          
    return f"Gracias por tu mensaje, {nombre}. Te contactaremos pronto a {email}."
   
  return render_template('register.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
