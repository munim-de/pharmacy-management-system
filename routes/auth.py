from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ✅ Add this block at the end for temporary admin creation
@auth_bp.route('/create-admin')
def create_admin():
    # Set your admin credentials
    email = "admin@example.com"
    password = "admin123"
    role = "admin"

    if User.query.filter_by(email=email).first():
        return "Admin already exists."

    hashed_pw = generate_password_hash(password)
    admin_user = User(email=email, password=hashed_pw, role=role)

    db.session.add(admin_user)
    db.session.commit()
    return "Admin user created successfully."
