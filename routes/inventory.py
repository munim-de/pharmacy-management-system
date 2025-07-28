from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from models import db, Medicine
from decorators import role_required

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'inventory_manager'])
def inventory():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = float(request.form['price'])
        qty = int(request.form['quantity'])
        expiry = request.form['expiry']

        new_med = Medicine(Name=name, Brand=brand, Price=price, QuantityInStock=qty, ExpiryDate=expiry)
        db.session.add(new_med)
        db.session.commit()
        return redirect('/inventory')

    medicines = Medicine.query.all()
    return render_template('inventory.html', medicines=medicines)
