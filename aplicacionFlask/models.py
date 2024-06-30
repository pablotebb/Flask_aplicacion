from extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=False)
    otp_secret = db.Column(db.String(16), nullable=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'
      

