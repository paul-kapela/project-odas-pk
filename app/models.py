import secrets
from datetime import datetime
from typing import Optional

import jwt
import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app
from flask_argon2 import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(320), unique=True, index=True)
  password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
  created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.now())

  verified_on: so.Mapped[Optional[datetime]] = so.mapped_column()
  verify_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6))
  last_verify_attempt: so.Mapped[Optional[datetime]] = so.mapped_column()

  logged_in_on: so.Mapped[Optional[datetime]] = so.mapped_column()
  tfa_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6))
  last_tfa_attempt: so.Mapped[Optional[datetime]] = so.mapped_column()

  password_reset_on: so.Mapped[Optional[datetime]] = so.mapped_column()
  password_reset_code: so.Mapped[Optional[str]] = so.mapped_column(sa.String(6))
  last_password_reset_attempt: so.Mapped[Optional[datetime]] = so.mapped_column()

  messages: so.WriteOnlyMapped['Message'] = so.relationship(back_populates='author')

  def __repr__(self):
    return f'<User {self.username}>'

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_verify_token(self):
    token_life = current_app.config['TOKEN_LIFE']

    if self.last_verify_attempt is None or (datetime.now() - self.last_verify_attempt) > token_life:
      code = str(secrets.choice(range(100000, 999999)))

      self.verify_code = code
      self.last_verify_attempt = datetime.now()

      db.session.commit()

      return self.verify_code

    return None

  def verify_verify_token(self, token):
    if self.last_verify_attempt is None:
      return False

    token_life = current_app.config['TOKEN_LIFE']

    if (datetime.now() - self.last_verify_attempt) > token_life:
      return False

    if self.verify_code != token:
      return False

    self.verified_on = datetime.now()
    self.verify_code = None
    self.last_verify_attempt = None

    db.session.commit()

    return True

  def get_tfa_token(self):
    token_life = current_app.config['TOKEN_LIFE']

    if self.last_tfa_attempt is None or (datetime.now() - self.last_tfa_attempt) > token_life:
      code = str(secrets.choice(range(100000, 999999)))

      self.tfa_code = code
      self.last_tfa_attempt = datetime.now()

      db.session.commit()

      return self.tfa_code

    return None

  def verify_tfa_token(self, token):
    if self.last_tfa_attempt is None:
      return False

    token_life = current_app.config['TOKEN_LIFE']

    if (datetime.now() - self.last_tfa_attempt) > token_life:
      return False

    if self.tfa_code != token:
      return False

    self.tfa_code = None
    self.last_tfa_attempt = None

    db.session.commit()

    return True

  def get_reset_password_token(self):
    token_life = current_app.config['TOKEN_LIFE']

    if self.last_password_reset_attempt is None or (datetime.now() - self.last_password_reset_attempt) > token_life:
      code = str(secrets.choice(range(100000, 999999)))

      self.password_reset_code = code
      self.last_password_reset_attempt = datetime.now()

      db.session.commit()

      return self.password_reset_code

    return None

  def verify_reset_password_token(self, token):
    if self.last_password_reset_attempt is None:
      return False

    token_life = current_app.config['TOKEN_LIFE']

    if (datetime.now() - self.last_password_reset_attempt) > token_life:
      return False

    if self.password_reset_code != token:
      return False

    self.password_reset_code = None
    self.last_password_reset_attempt = None

    return True

#class Session(db.Model):
#  id: so.Mapped[int] = so.mapped_column(primary_key=True)
#  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), nullable=False, index=True)
#
#  created_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=False, default=sa.func.now())
#  last_used_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)


class Message(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  title: so.Mapped[str] = so.mapped_column(sa.String(128))
  content: so.Mapped[str] = so.mapped_column(sa.String(20000))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  author: so.Mapped[User] = so.relationship(User, back_populates='messages')
  created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.now())

  def __repr__(self):
    return f'<Message {self.title}>'