from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, logout_user
from models import User
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(Username=username).first()

        if user and check_password_hash(user.Password, password):
            login_user(user)
            flash("Login successful", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect('/')
