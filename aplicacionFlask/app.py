# Importamos request de flask, y flash de flask para mostrar mensajes flash.
from flask import Flask, render_template, request, flash

app = Flask(__name__)
# Establecemos una secret_key necesaria para usar la funcionalidad de mensajes flash.
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    nombre = "Pablo"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)

# Modificamos la ruta /contact para manejar tanto GET como POST usando el parámetro methods.  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    nombre = "la empresa"
    # Si el método de la solicitud es POST, procesamos los datos del formulario. request.form contiene los datos del formulario enviados en una solicitud POST.
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']
        
        # Validamos que todos los campos del formulario estén completos. Si falta algún campo, mostramos un mensaje flash y renderizamos nuevamente la plantilla del formulario.
        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios')
            return render_template('contact2.html')
          
        return f"Gracias por tu mensaje, <b>{nombre}</b>. Te contactaremos pronto a <b>{email}</b>."
    # Si el método de la solicitud es GET, simplemente renderizamos la plantilla contact.html.
    return render_template('contact2.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
