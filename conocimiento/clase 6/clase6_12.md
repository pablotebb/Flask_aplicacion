> y este es mi fichero env.py...

Gracias por compartir tu archivo `env.py`. Este archivo parece estar configurado correctamente para usar Flask-Migrate con Alembic. A continuación, revisemos los pasos detallados para asegurarnos de que todo esté configurado correctamente y veamos cómo generar y aplicar una nueva migración.

### Pasos para Generar y Aplicar Migraciones

1. **Verificar las dependencias**:
   Asegúrate de que tienes instaladas las dependencias necesarias:

   ```bash
   pip install Flask-Migrate Flask-SQLAlchemy
   ```

2. **Revisar la estructura del proyecto**:
   Asegúrate de que la estructura de tu proyecto está correcta. Basado en tus imágenes, parece que `app.py` y la carpeta `migrations` están en el directorio correcto.

3. **Iniciar las migraciones**:
   Si no lo has hecho ya, inicia las migraciones. Esto solo se hace una vez por proyecto:

   ```bash
   flask db init
   ```

4. **Crear una migración inicial**:
   Genera la migración inicial para la base de datos:

   ```bash
   flask db migrate -m "Initial migration"
   ```

   Si ya has hecho esto y no hay cambios detectados, asegúrate de que el modelo está bien definido y que hay realmente cambios en el esquema de la base de datos que deban ser migrados.

5. **Aplicar las migraciones**:
   Aplica las migraciones generadas a la base de datos:

   ```bash
   flask db upgrade
   ```

6. **Hacer cambios en el modelo**:
   Asegúrate de que has realizado cambios en tu modelo que deben ser reflejados en la base de datos. Por ejemplo, agregar un nuevo campo:

   ```python
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password = db.Column(db.String(120), nullable=False)
       nuevo_campo = db.Column(db.String(120))  # Nuevo campo agregado
   ```

7. **Generar una nueva migración**:
   Después de hacer cambios en el modelo, genera una nueva migración:

   ```bash
   flask db migrate -m "Added nuevo_campo to Usuario"
   ```

   Si todavía recibes el mensaje "No changes in schema detected", asegúrate de que estás trabajando en el entorno virtual correcto y que el modelo ha sido modificado.

8. **Aplicar la nueva migración**:
   Aplica la nueva migración a la base de datos:

   ```bash
   flask db upgrade
   ```

### Solución de Problemas

Si después de seguir estos pasos sigues sin ver cambios en el esquema de la base de datos, considera los siguientes puntos:

- **Entorno virtual**: Asegúrate de que estás trabajando en el entorno virtual correcto.
- **Esquema de base de datos**: Verifica manualmente el esquema de la base de datos para asegurarte de que refleja los cambios esperados.
- **Log de migraciones**: Revisa los logs de Alembic en la carpeta `migrations` para obtener más detalles sobre por qué no se están detectando los cambios.
- **Comprobación manual**: Puedes intentar borrar la base de datos y las migraciones, y luego volver a generar todo desde cero para asegurarte de que el proceso funciona correctamente.

Espero que estos pasos te ayuden a resolver el problema y puedas generar y aplicar las migraciones correctamente. Si tienes alguna pregunta adicional o necesitas más ayuda, no dudes en preguntar.
