from flask import current_app, render_template

from app.email import send_email

def send_tfa_token_email(user):
  code = user.get_tfa_token()

  send_email('Chirp - potwierdź logowanie',
             sender=current_app.config['ADMINS'][0],
             recipients=[user.email],
             text_body=render_template('email/2fa.txt', user=user, code=code))

def send_verify_token_email(user):
  code = user.get_verify_token()

  send_email('Chirp - zweryfikuj swoje konto',
             sender=current_app.config['ADMINS'][0],
             recipients=[user.email],
             text_body=render_template('email/verify.txt', user=user, code=code))

def send_password_reset_token_email(user):
  code = user.get_reset_password_token()

  send_email('Chirp - zresetuj swoje hasło',
             sender=current_app.config['ADMINS'][0],
             recipients=[user.email],
             text_body=render_template('email/reset_password.txt', user=user, code=code))