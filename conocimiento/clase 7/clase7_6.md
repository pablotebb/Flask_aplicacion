```
Me da este fallo:
SMTPDataError
smtplib.SMTPDataError: (554, b'5.2.0 STOREDRV.Submission.Exception:OutboundSpamException; Failed to process message due to a permanent exception with message [BeginDiagnosticData]WASCL UserAction verdict is not None. Actual verdict is Suspend. OutboundSpamException: WASCL UserAction verdict is not None. Actual verdict is Suspend.[EndDiagnosticData] [Hostname=AM8P192MB1009.EURP192.PROD.OUTLOOK.COM]')
```

El error `SMTPDataError: (554, b'5.2.0 STOREDRV.Submission.Exception:OutboundSpamException...` indica que tu correo electrónico fue marcado como spam y no se pudo enviar a través del servidor de Outlook. Esto puede ocurrir por varias razones, como el contenido del mensaje, la configuración de tu cuenta de correo o incluso la reputación del servidor de envío.

### Posibles Soluciones:

1. **Verificar el Contenido del Correo:**
   Asegúrate de que el contenido del correo no contenga elementos que podrían ser considerados spam, como enlaces sospechosos, texto sospechoso o imágenes.

2. **Revisar la Configuración de tu Cuenta:**
   Asegúrate de que tu cuenta de correo no esté restringida o marcada por actividades sospechosas. Esto puede requerir que inicies sesión en tu cuenta de Outlook y revises las alertas de seguridad o restricciones.

3. **Utilizar una Dirección de Correo Electrónico Diferente:**
   Prueba a usar una dirección de correo electrónico diferente, preferiblemente una que no haya tenido problemas de spam anteriormente.

4. **Configurar un Servidor SMTP Diferente:**
   Considera utilizar un servidor SMTP diferente para enviar tus correos, como Gmail, SendGrid, o cualquier otro proveedor de correo electrónico confiable.

### Ejemplo de Configuración para Gmail SMTP:

Asegúrate de tener una cuenta de Gmail y habilitar "Acceso de aplicaciones menos seguras" en tu cuenta de Google:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    # Configuración del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'tu_email@gmail.com'
    smtp_password = 'tu_contraseña'

    # Configuración del mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ejemplo de uso
send_email('destinatario@example.com', 'Asunto del correo', 'Cuerpo del correo')
```

### Configuración de Flask-Mail para Gmail:

Si estás usando Flask-Mail, aquí tienes un ejemplo de configuración para usar Gmail:

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración del servidor SMTP de Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'tu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña'
app.config['MAIL_DEFAULT_SENDER'] = 'tu_email@gmail.com'

mail = Mail(app)

@app.route("/send_email")
def send_email():
    msg = Message("Asunto del correo", recipients=["destinatario@example.com"])
    msg.body = "Cuerpo del correo"
    try:
        mail.send(msg)
        return "Correo enviado exitosamente."
    except Exception as e:
        return f"Error al enviar el correo: {e}"

if __name__ == "__main__":
    app.run(debug=True)
```

Estas configuraciones deberían ayudarte a evitar los problemas con el servidor de correo y permitir que tus correos electrónicos se envíen correctamente. Asegúrate de usar credenciales válidas y de verificar que no haya restricciones en la cuenta de correo que estás usando para enviar los correos.
