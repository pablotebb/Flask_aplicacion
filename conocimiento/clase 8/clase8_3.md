> y luego lo configuras en el fichero .gitignore, para no subir esa variable de entorno? Si es así como se configura?

Sí, es una buena práctica agregar el archivo `.env` al archivo `.gitignore` para asegurarte de que tus credenciales no se suban a tu repositorio de control de versiones. Aquí tienes los pasos para hacerlo:

1. **Crea el archivo `.gitignore`** (si no lo tienes ya) en el directorio raíz de tu proyecto y agrega la línea correspondiente para ignorar el archivo `.env`:

   ```plaintext
   # Ignore the .env file containing environment variables
   .env
   ```

2. **Asegúrate de que el archivo `.env` no se haya añadido previamente a tu repositorio**. Si ya lo has añadido, necesitas eliminarlo del seguimiento del control de versiones con el siguiente comando:

   ```bash
   git rm --cached .env
   ```

3. **Comprueba que el archivo `.gitignore` contiene la línea para ignorar el archivo `.env`**:

   ```plaintext
   # .gitignore

   # Ignore the .env file containing environment variables
   .env
   ```

4. **Comprueba el estado del repositorio para asegurarte de que el archivo `.env` no esté siendo rastreado**:

   ```bash
   git status
   ```

   Debes ver algo como esto si el archivo `.env` está correctamente ignorado:

   ```plaintext
   On branch main
   Your branch is up to date with 'origin/main'.

   Untracked files:
     (use "git add <file>..." to include in what will be committed)
       .env

   nothing added to commit but untracked files present (use "git add" to track)
   ```

5. **Continúa trabajando y haciendo commits en tu proyecto** sin preocuparte de que el archivo `.env` se suba a tu repositorio.

Al seguir estos pasos, tus credenciales y variables sensibles estarán protegidas y no serán expuestas en tu repositorio de código. Aquí tienes un ejemplo de cómo podría verse tu archivo `.gitignore` junto con el archivo `.env`:

- **`.gitignore`**:

  ```plaintext
  # Byte-compiled / optimized / DLL files
  __pycache__/
  *.py[cod]
  *$py.class

  # C extensions
  *.so

  # Distribution / packaging
  .Python
  build/
  develop-eggs/
  dist/
  downloads/
  eggs/
  .eggs/
  lib/
  lib64/
  parts/
  sdist/
  var/
  wheels/
  pip-wheel-metadata/
  share/python-wheels/
  *.egg-info/
  .installed.cfg
  *.egg
  MANIFEST

  # PyInstaller
  #  Usually these files are written by a python script from a template
  #  before PyInstaller builds the exe, so as to inject date/other infos into it.
  *.manifest
  *.spec

  # Installer logs
  pip-log.txt
  pip-delete-this-directory.txt

  # Unit test / coverage reports
  htmlcov/
  .tox/
  .nox/
  .coverage
  .coverage.*
  .cache
  nosetests.xml
  coverage.xml
  *.cover
  .hypothesis/
  .pytest_cache/

  # Translations
  *.mo
  *.pot

  # Django stuff:
  *.log
  local_settings.py
  db.sqlite3
  db.sqlite3-journal

  # Flask stuff:
  instance/
  .webassets-cache

  # Scrapy stuff:
  .scrapy

  # Sphinx documentation
  docs/_build/

  # Jupyter Notebook
  .ipynb_checkpoints

  # IPython
  profile_default/
  ipython_config.py

  # pyenv
  .python-version

  # celery beat schedule file
  celerybeat-schedule

  # dotenv
  .env
  .env.local
  .env.development.local
  .env.test.local
  .env.production.local

  # macOS
  .DS_Store

  # Windows
  thumbs.db
  ehthumbs.db
  ```

- **`.env`**:

  ```plaintext
  MAIL_USERNAME=tu_correo@hotmail.com
  MAIL_PASSWORD=tu_contraseña
  ```

Este enfoque te ayudará a mantener tus credenciales seguras y fuera del repositorio.
