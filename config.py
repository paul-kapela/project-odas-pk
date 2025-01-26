import os
from datetime import timedelta

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'the-numbers-mason-what-do-they-mean'

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('TRACK_MODIFICATIONS') or False

  MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
  MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND') is not None
  MAIL_DEBUG = os.environ.get('MAIL_DEBUG') is not None
  ADMINS = os.environ.get('ADMINS') or ['chirp@chirp.pl']

  ARGON_MEMORY_COST = 2 ** 16
  ARGON2_TIME_COST = 4
  ARGON2_PARALLELISM = 2

  RESEND_COOLDOWN = timedelta(minutes=os.environ.get('RESEND_COOLDOWN') or 300)