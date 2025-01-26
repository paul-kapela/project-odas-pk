import re
import sqlalchemy as sa
from wtforms.validators import ValidationError, StopValidation

from flask_argon2 import check_password_hash

from app import db
from app.models import User

def validate_username_characters(form, field):
  if not re.match(r'^[a-zA-Z0-9]+$', field.data):
    raise ValidationError('Nazwa użytkownika może zawierać tylko litery i cyfry')

def validate_username_free(form, field):
  user = db.session.scalar(sa.select(User).where(User.username == field.data))

  if user is not None:
    raise ValidationError('Podana nazwa użytkownika jest już zajęta')

def validate_email_free(form, field):
  email = db.session.scalar(sa.select(User).where(User.email == field.data))

  if email is not None:
    raise ValidationError('Podany adres e-mail jest już zajęty')

def validate_password_match(form, field):
  if field.data != form.password.data:
    raise ValidationError('Hasła muszą być takie same')

def validate_password_strength(form, field):
  if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!?@#$%^&*(){}\[\]_\-+=])[a-zA-Z\d!?@#$%^&*(){}\[\]_\-+=].{12,}$', field.data):
    raise ValidationError('Hasło nie spełnia wymogów bezpieczeństwa')

def verify_username(form, field):
  user = db.session.scalar(sa.select(User).where(User.username == field.data))

  if user is None:
    raise StopValidation('Nie ma takiego użytkownika')

def verify_password(form, field):
  user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
  hashed_password = user.password_hash

  password = form.password.data

  return check_password_hash(hashed_password, password)