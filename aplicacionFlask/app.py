# Importamos la clase Flask del paquete flask.
from flask import Flask

# Creamos una instancia de la clase Flask. La instancia app será nuestra aplicación.
app = Flask(__name__)

# Usamos el decorador @app.route('/') para decirle a Flask que la función home debe responder a las solicitudes a la URL raíz (/).
@app.route('/')
def home():
    #  La función home devuelve un simple mensaje "¡Hola, Mundo!".
    return "¡Hola, Mundo! Bienvenidos a Flask."

if __name__ == '__main__':
    #  Si este script se ejecuta directamente, inicia el servidor de desarrollo de Flask con debug=True para que podamos ver los errores de forma más detallada.
    app.run(debug=True)
