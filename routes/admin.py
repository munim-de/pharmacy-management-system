from flask import Blueprint, render_template, Response
from flask_login import login_required
from decorators import role_required
from models import db, Medicine, Sale, SaleDetail, Customer
import csv
import io
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/stats')
@login_required
@role_required(['admin'])
def admin_stats():
    top_meds = db.session.query(
        Medicine.Name,
        func.sum(SaleDetail.Quantity).label('TotalSold')
    ).join(SaleDetail).group_by(Medicine.Name).order_by(func.sum(SaleDetail.Quantity).desc()).limit(5).all()

    daily_sales = db.session.query(
        Sale.SaleDate,
        func.count(Sale.SaleID).label('SalesCount')
    ).group_by(Sale.SaleDate).order_by(Sale.SaleDate.desc()).limit(7).all()

    low_stock = Medicine.query.filter(Medicine.QuantityInStock < 10).all()

    return render_template("admin_stats.html", top_meds=top_meds, daily_sales=daily_sales, low_stock=low_stock)

@admin_bp.route('/admin/report/csv')
@login_required
@role_required(['admin'])
def export_csv():
    sales = db.session.query(Sale.SaleID, Sale.SaleDate, Customer.Name.label('Customer'),
                             Medicine.Name.label('Medicine'), SaleDetail.Quantity).\
            join(SaleDetail, Sale.SaleID == SaleDetail.SaleID).\
            join(Customer, Customer.CustomerID == Sale.CustomerID).\
            join(Medicine, Medicine.MedicineID == SaleDetail.MedicineID).\
            all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['SaleID', 'Date', 'Customer', 'Medicine', 'Quantity'])
    for row in sales:
        writer.writerow([row.SaleID, row.SaleDate, row.Customer, row.Medicine, row.Quantity])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=sales_report.csv'
    return response
