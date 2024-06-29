from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_uploads import UploadSet, IMAGES


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
photos = UploadSet('photos', IMAGES)

