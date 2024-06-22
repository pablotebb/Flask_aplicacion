# Además de Flask, importamos la función render_template de flask.
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    nombre = "Pablo"
    # En lugar de devolver texto simple, usamos render_template para renderizar los archivos HTML y pasamos la variable nombre a las plantillas.
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
