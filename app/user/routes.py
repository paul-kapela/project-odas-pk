from flask import render_template

from app.user import bp

@bp.route('/profile/<username>', methods=['GET'])
def profile():
  return render_template('user/profile.html', title='Profil')