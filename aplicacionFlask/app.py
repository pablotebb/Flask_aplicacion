from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    nombre = "Pablo"
    return render_template('index.html', nombre=nombre)

@app.route('/about')
def about():
    nombre = "Pablo"
    return render_template('about.html', nombre=nombre)
  
@app.route('/contact')
def contact():
    nombre = "Pablo"
    return render_template('contact.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
