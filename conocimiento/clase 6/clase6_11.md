> Y este mi fichero app.py ...

Gracias por compartir el contenido de tu archivo `app.py`. He revisado el código y todo parece estar correctamente configurado para SQLAlchemy y Flask-Migrate. Ahora, vamos a realizar una serie de pasos para asegurarnos de que las migraciones funcionan correctamente.

### Pasos a Seguir:

1. **Verifica que tienes el archivo de configuración de migraciones**:
   Asegúrate de que la carpeta `migrations` contiene un archivo `env.py` que está configurado correctamente para apuntar a tu aplicación Flask y tu base de datos. El contenido debería ser similar a esto:

   ```python
   from __future__ import with_statement
   from alembic import context
   from sqlalchemy import engine_from_config, pool
   from logging.config import fileConfig
   import sys
   import os

   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

   from app import db
   target_metadata = db.metadata

   config = context.config
   fileConfig(config.config_file_name)

   def run_migrations_offline():
       context.configure(
           url=config.get_main_option("sqlalchemy.url"),
           target_metadata=target_metadata,
           literal_binds=True,
           dialect_opts={"paramstyle": "named"},
       )

       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       connectable = engine_from_config(
           config.get_section(config.config_ini_section),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )

       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)

           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():
       run_migrations_offline()
   else:
       run_migrations_online()
   ```

2. **Asegúrate de tener migraciones previas**:
   Asegúrate de haber ejecutado al menos una migración inicial para que Alembic tenga algo con lo que comparar. Si no has hecho esto, puedes intentar:

   ```bash
   flask db init  # Solo si no tienes la carpeta migrations
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

3. **Verifica el estado de la base de datos**:
   Asegúrate de que la base de datos está en el estado esperado antes de realizar cualquier cambio. Puedes hacerlo iniciando una sesión de Python y verificando la existencia de tus tablas:

   ```python
   from app import db
   db.create_all()
   ```

4. **Realiza cambios en el modelo y genera una nueva migración**:
   Después de asegurarte de que tu base de datos está correctamente inicializada, haz un cambio en tu modelo `Usuario`, por ejemplo, agrega un campo nuevo:

   ```python
   class Usuario(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password = db.Column(db.String(120), nullable=False)
       nuevo_campo = db.Column(db.String(120))  # Nuevo campo agregado
   ```

   Luego, ejecuta los comandos de migración:

   ```bash
   flask db migrate -m "Added nuevo_campo to Usuario"
   flask db upgrade
   ```

5. **Comprobar migraciones manualmente**:
   Si los pasos anteriores no funcionan, es posible que haya algún problema con el estado de tu base de datos o la configuración de Alembic. En ese caso, puedes intentar reiniciar el proceso de migraciones:

   ```bash
   rm -rf migrations  # Elimina la carpeta de migraciones (haz un backup antes)
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Conclusión

Siguiendo estos pasos deberías poder solucionar el problema y generar migraciones correctamente. Si después de esto el problema persiste, es posible que necesitemos revisar más detalladamente los archivos de configuración de Alembic o cualquier log adicional que esté proporcionando más detalles del error.
