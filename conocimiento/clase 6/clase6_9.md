> Pero después de haber puesto el Modelo en app.py, y hago: <br>
> flask db migrate -m "Creamos Modelo Usuario" <br>
> INFO [alembic.runtime.migration] Context impl SQLiteImpl.
> INFO [alembic.runtime.migration] Will assume non-transactional DDL.
> INFO [alembic.env] No changes in schema detected. <br>
> Que puede estar pasando?

El mensaje "No changes in schema detected" indica que Alembic no detectó ningún cambio en la estructura de la base de datos que requiera una nueva migración. Esto puede suceder por varias razones. Aquí hay algunos pasos que puedes seguir para resolver el problema:

### Verificar la Configuración de Alembic

1. **Asegurarse de que Alembic está configurado correctamente**:

   Asegúrate de que tienes un archivo `alembic.ini` y un directorio de migraciones correctamente configurado. Si no has inicializado Alembic en tu proyecto, hazlo con:

   ```bash
   flask db init
   ```

2. **Verificar la estructura de tu proyecto**:

   Asegúrate de que tu proyecto tenga la siguiente estructura:

   ```
   your_project/
   ├── app.py
   ├── migrations/
   │   ├── alembic.ini
   │   ├── env.py
   │   ├── script.py.mako
   │   └── versions/
   ├── requirements.txt
   └── ...
   ```

### Verificar la Definición del Modelo

3. **Verificar que el modelo está definido correctamente**:

   Asegúrate de que tu modelo está definido correctamente en `app.py` y que `db` es una instancia de `SQLAlchemy` asociada a tu aplicación Flask.

   ```python
   # app.py
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_migrate import Migrate

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
   db = SQLAlchemy(app)
   migrate = Migrate(app, db)

   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       campo1 = db.Column(db.String(128))
       campo2 = db.Column(db.String(128))
       campo3 = db.Column(db.String(128))

   if __name__ == "__main__":
       app.run()
   ```

### Crear la Base de Datos

4. **Crear la base de datos**:

   Antes de correr las migraciones, asegúrate de que la base de datos y las tablas no existen. Si la base de datos ya existe y no se han hecho cambios en el esquema, Alembic no detectará cambios. Puedes crear la base de datos inicial ejecutando el shell de Python:

   ```bash
   flask shell
   ```

   Luego, dentro del shell de Flask, crea las tablas manualmente:

   ```python
   from app import db
   db.create_all()
   ```

### Generar la Migración

5. **Generar la migración**:

   Después de asegurarte de que la base de datos y el modelo están configurados correctamente, intenta generar la migración nuevamente:

   ```bash
   flask db migrate -m "Creamos Modelo Usuario"
   ```

### Solucionar Problemas

6. **Verificar el contenido de `env.py` en el directorio `migrations`**:

   Asegúrate de que `env.py` está configurado para importar y detectar correctamente los modelos. El archivo `env.py` debe tener una sección similar a la siguiente:

   ```python
   from alembic import context
   from sqlalchemy import engine_from_config, pool
   from logging.config import fileConfig
   import sys
   import os

   sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

   from app import db
   target_metadata = db.metadata

   config = context.config
   fileConfig(config.config_file_name)

   def run_migrations_offline():
       context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True)
       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)
           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():
       run_migrations_offline()
   else:
       run_migrations_online()
   ```

### Resumen

1. Asegúrate de que tu archivo `app.py` está configurado correctamente y contiene tu modelo.
2. Inicializa las migraciones si aún no lo has hecho (`flask db init`).
3. Verifica que tu archivo `env.py` en el directorio `migrations` está configurado para detectar los modelos.
4. Crea la base de datos inicial si aún no lo has hecho.
5. Genera la migración con `flask db migrate -m "Creamos Modelo Usuario"`.

Siguiendo estos pasos deberías poder resolver el problema y generar la migración correctamente.
