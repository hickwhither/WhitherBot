from flask import *
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash

from website import db
from website.models import *

import re
valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('views.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user: flash('Username not found.', category='danger')
        elif not check_password_hash(user.password, password): flash('Wrong password.', category='danger')
        else:
            flash('Logged in successfully!', category='success')
            login_user(user)
            return redirect(url_for('views.home'))

    return render_template("user/login.html")

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(gmail=gmail).first(): flash('Gmail existed.', category='danger')
        if User.query.filter_by(username=username).first(): flash('Username existed.', category='danger')
        else:
            user = User(gmail=gmail, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('user/register.html')


