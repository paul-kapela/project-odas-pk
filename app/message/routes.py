from flask import render_template
from flask_login import login_required, current_user

from app.message import bp

@bp.route('/index', methods=['GET'])
def index():
  return render_template('message/index.html', title='Wiadomości')

@bp.route('/messages', methods=['GET'])
@login_required
def messages():
  return render_template('message/messages.html', title='Wiadomości')

@bp.route('/message/', methods=['GET'])
@login_required
def message():
  return render_template('message/message.html', title='Wiadomości')