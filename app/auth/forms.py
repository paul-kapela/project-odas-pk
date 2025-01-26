from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from app.auth.validators import validate_username_characters, validate_username_free, validate_email_free, \
  validate_password_strength, validate_password_match, verify_username


class LoginForm(FlaskForm):
  username = StringField('Nazwa użytkownika', validators=[DataRequired(), verify_username])
  password = PasswordField('Hasło', validators=[DataRequired()])
  remember_me = BooleanField('Zapamiętaj mnie')
  submit = SubmitField('Zaloguj')

class TwoFactorForm(FlaskForm):
  code = StringField('Kod', validators=[DataRequired()])
  submit = SubmitField('Potwierdź')

class RegistrationForm(FlaskForm):
  username = StringField('Nazwa użytkownika', validators=[DataRequired(), validate_username_characters, validate_username_free])
  email = StringField('Email', validators=[DataRequired(), Email(), validate_email_free])
  password = PasswordField('Hasło', validators=[DataRequired(), validate_password_strength])
  password_confirm = PasswordField('Powtórz hasło', validators=[DataRequired(), validate_password_match])
  submit = SubmitField('Zarejestruj')

class VerifyForm(FlaskForm):
  code = StringField('Kod', validators=[DataRequired()])
  submit = SubmitField('Potwierdź')