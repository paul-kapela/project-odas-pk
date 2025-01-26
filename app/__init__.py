from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from flask_argon2 import Argon2
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()

argon2 = Argon2()
csrf = CSRFProtect()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)
  mail.init_app(app)

  argon2.init_app(app)
  csrf.init_app(app)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  from app.message import bp as message_bp
  app.register_blueprint(message_bp)

  from app.models import User

  @login.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  return app
