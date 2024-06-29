import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_MAX_EMAILS = None
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_TIMEOUT = 60  # Aumenta el tiempo de espera a 60 segundos
    UPLOADED_PHOTOS_DEST = 'static/uploads'