> y no se puede encriptar la password?

Sí, puedes cifrar la contraseña antes de almacenarla en el archivo `.env` y luego descifrarla en tu aplicación Flask. Esto agrega una capa adicional de seguridad. Aquí hay un ejemplo de cómo hacerlo utilizando la biblioteca `cryptography` en Python.

### Instalación de la biblioteca `cryptography`

Primero, instala la biblioteca `cryptography`:

```bash
pip install cryptography
```

### Cifrado de la contraseña

1. **Genera una clave de cifrado** (esto solo necesita hacerse una vez y la clave debe almacenarse de forma segura):

   ```python
   from cryptography.fernet import Fernet

   # Genera una clave de cifrado y guárdala en un lugar seguro
   key = Fernet.generate_key()
   print(key.decode())
   ```

   Guarda esta clave de forma segura, ya que la necesitarás para descifrar la contraseña.

2. **Cifra la contraseña** usando la clave generada:

   ```python
   from cryptography.fernet import Fernet

   # Usa la clave generada anteriormente
   key = b'tu_clave_de_cifrado_aquí'
   cipher_suite = Fernet(key)

   # La contraseña que quieres cifrar
   password = b'tu_contraseña'
   encrypted_password = cipher_suite.encrypt(password)
   print(encrypted_password.decode())
   ```

   Guarda `encrypted_password` en tu archivo `.env`.

3. **Configura tu archivo `.env`** para incluir la contraseña cifrada y la clave de cifrado:

   ```plaintext
   ENCRYPTION_KEY=tu_clave_de_cifrado_aquí
   MAIL_PASSWORD_ENCRYPTED=tu_contraseña_cifrada_aquí
   MAIL_USERNAME=tu_correo@hotmail.com
   ```

### Descifrado de la contraseña en tu aplicación Flask

Modifica tu aplicación Flask para descifrar la contraseña antes de usarla:

```python
from flask import Flask
from flask_mail import Mail, Message
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuración del servidor de correo
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')

# Descifrar la contraseña
encryption_key = os.getenv('ENCRYPTION_KEY').encode()
cipher_suite = Fernet(encryption_key)
encrypted_password = os.getenv('MAIL_PASSWORD_ENCRYPTED').encode()
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

app.config['MAIL_PASSWORD'] = decrypted_password

mail = Mail(app)

@app.route("/send-email")
def send_email():
    msg = Message("Hello",
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=["destinatario@example.com"])
    msg.body = "This is a test email sent from a Flask application using Hotmail SMTP server."
    mail.send(msg)
    return "Email sent!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Resumen

1. **Genera una clave de cifrado** y guárdala de forma segura.
2. **Cifra la contraseña** y almacénala en el archivo `.env`.
3. **Descifra la contraseña en tu aplicación Flask** antes de usarla.

Este enfoque asegura que la contraseña no se almacene en texto plano en el archivo `.env`, proporcionando una capa adicional de seguridad.
