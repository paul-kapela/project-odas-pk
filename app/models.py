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
  created_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=False, default=sa.func.now())

  verified_on: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)
  verification_code: so.Mapped[str] = so.mapped_column(sa.String(6), nullable=True)
  last_verification_attempt: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)

  logged_in_on: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)
  tfa_code: so.Mapped[str] = so.mapped_column(sa.String(6), nullable=True)
  last_tfa_attempt: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)

  password_reset_on: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)
  password_reset_code: so.Mapped[str] = so.mapped_column(sa.String(6), nullable=True)
  last_password_reset_attempt: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=True)

  messages: so.WriteOnlyMapped['Message'] = so.relationship(back_populates='author')

  def __repr__(self):
    return f'<User {self.username}>'

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_verify_token(self, expires_in=600):
    return jwt.encode({'verify': self.id, 'exp': expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

  @staticmethod
  def verify_verify_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['verify']
    except Exception:
      return

    return db.session.get(User, id)

  def get_reset_password_token(self, expires_in=600):
    return jwt.encode({'reset_password': self.id, 'exp': expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

  @staticmethod
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
    except Exception:
      return

    return db.session.get(User, id)

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
  created_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=False, default=sa.func.now())

  def __repr__(self):
    return f'<Message {self.title}>'