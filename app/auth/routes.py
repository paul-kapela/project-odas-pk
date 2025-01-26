from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user

from app import db
from app.models import User

from app.auth import bp
from app.auth.forms import LoginForm, TwoFactorForm, RegistrationForm, VerifyForm
from app.auth.email import send_verify_token_email, send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()

    if user is None or not user.verify_password(form.password.data):
      flash('Nieprawidłowy adres email lub hasło', 'danger')
      return redirect(url_for('auth.login'))

    login_user(user) #, remember=form.remember_me.data)

    return redirect(url_for('auth.two_factor_auth'))

  return render_template('auth/login.html', title='Logowanie', form=form)

@bp.route('/2fa', methods=['GET', 'POST'])
def two_factor_auth():
  form = TwoFactorForm()

  return render_template('auth/2fa.html', title='Autoryzacja dwuetapowa', form=form)

@bp.route('/logout')
def logout():
  logout_user()

  return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = RegistrationForm()

  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)

    db.session.add(user)
    db.session.commit()

    flash('Rejestracja przebiegła pomyślnie! Prosimy o zweryfikowanie adresu e-mail.', 'success')

    return redirect(url_for('auth.verify'))

  return render_template('auth/register.html', title='Rejestracja', form=form)

@bp.route('/verify', methods=['GET', 'POST'])
def verify():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = VerifyForm()

  if form.validate_on_submit():

    pass

  return render_template('auth/verify.html', title='Weryfikacja', form=form)

@bp.route('/resend-verify', methods=['GET', 'POST'])
def resend_verify():
  email = request.form.get('email')

  user = User.query.filter_by(email=email).first()

  if user is None:
    return jsonify({"error": "Nieznany użytkownik"}), 404

  now = datetime.now()