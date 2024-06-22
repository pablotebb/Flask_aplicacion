from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
  return "¡Hola, Pablo! Bienvenido a tu primera aplicación Flask."

@app.route('/about')
def about():
  return "Esta es la página About de Pablo."

if __name__ == '__main__':
  app.run(debug=True)