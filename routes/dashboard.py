from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db, Sale, Medicine

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'salesman':
        sales = Sale.query.filter_by(UserID=current_user.id).order_by(Sale.SaleDate.desc()).all()
    elif current_user.role == 'admin':
        sales = Sale.query.order_by(Sale.SaleDate.desc()).all()
    else:
        sales = []

    low_stock = Medicine.query.filter(Medicine.QuantityInStock < 10).all()

    return render_template('dashboard.html', sales=sales, low_stock=low_stock)
