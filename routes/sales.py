from flask import Blueprint, render_template, request, redirect, send_file
from flask_login import login_required, current_user
from models import db, Sale, SaleDetail, Medicine, Customer
from decorators import role_required
from datetime import datetime
import io
from reportlab.pdfgen import canvas

bp = Blueprint('sales', __name__)

@bp.route('/sales', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'salesman'])
def sales():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        medicine_id = request.form['medicine_id']
        quantity = int(request.form['quantity'])

        new_sale = Sale(CustomerID=customer_id, SaleDate=datetime.now(), UserID=current_user.id)
        db.session.add(new_sale)
        db.session.commit()

        sale_detail = SaleDetail(SaleID=new_sale.SaleID, MedicineID=medicine_id, Quantity=quantity)
        db.session.add(sale_detail)

        # Update stock
        medicine = Medicine.query.get(medicine_id)
        medicine.QuantityInStock -= quantity
        db.session.commit()

        return redirect(f'/invoice/{new_sale.SaleID}')

    medicines = Medicine.query.all()
    return render_template('sales.html', medicines=medicines)

@bp.route('/invoice/<int:sale_id>')
@login_required
@role_required(['admin', 'salesman'])
def generate_invoice(sale_id):
    sale = Sale.query.get(sale_id)
    customer = Customer.query.get(sale.CustomerID)
    items = db.session.query(Medicine.Name, Medicine.Price, SaleDetail.Quantity).\
        join(SaleDetail, Medicine.MedicineID == SaleDetail.MedicineID).\
        filter(SaleDetail.SaleID == sale_id).all()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Pharmacy Invoice - Sale ID: {sale.SaleID}")
    p.drawString(100, 780, f"Customer: {customer.Name}")

    y = 750
    total = 0
    for item in items:
        p.drawString(100, y, f"{item.Name} - {item.Quantity} x {item.Price}")
        total += item.Quantity * item.Price
        y -= 20

    p.drawString(100, y - 20, f"Total: {total}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{sale_id}.pdf", mimetype='application/pdf')
