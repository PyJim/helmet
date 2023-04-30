from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                message = 'Logged In Successfully'
                login_user(user, remember=True)
                return redirect(url_for('views.note'))
            else:
                message = 'Incorrect Password, Try Again'
                return render_template('login.html', message=message)
        else:
            message = 'User Does Not Exist, Try Again'
            return render_template('login.html', message=message)

    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()

        if user:
            message = 'User Already Exists'
            return render_template('sign_up.html', message=message)
        elif len(email) < 6:
            message = 'Email Must Be At Least 6 Characters'
            return render_template('sign_up.html', message=message)
        elif len(username) < 4:
            message = 'Username Must Be At Least 4 Characters'
            return render_template('sign_up.html', message=message)
        elif password != confirm_password:
            message = 'Passwords Do Not Match'
            return render_template('sign_up.html', message=message)
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(confirm_password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            message = 'Account Created Successfully'
            login_user(new_user, remember=True)
            return redirect(url_for('views.homepage'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global user
    user = None
    return redirect('/')

