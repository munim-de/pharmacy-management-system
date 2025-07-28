from reportlab.pdfgen import canvas
from flask import send_file
import io

@app.route('/invoice/<int:sale_id>')
@login_required
@role_required(['admin', 'salesman'])
def generate_invoice(sale_id):
    db = get_db()
    sale = db.execute('SELECT * FROM Sales WHERE SaleID = ?', (sale_id,)).fetchone()
    customer = db.execute('SELECT * FROM Customers WHERE CustomerID = ?', (sale['CustomerID'],)).fetchone()
    items = db.execute('''
        SELECT Medicines.Name, Medicines.Price, SaleDetails.Quantity
        FROM SaleDetails
        JOIN Medicines ON SaleDetails.MedicineID = Medicines.MedicineID
        WHERE SaleID = ?
    ''', (sale_id,)).fetchall()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Pharmacy Invoice - Sale ID: {sale_id}")
    p.drawString(100, 780, f"Customer: {customer['Name']}")

    y = 750
    total = 0
    for item in items:
        line = f"{item['Name']} - {item['Quantity']} x {item['Price']:.2f}"
        p.drawString(100, y, line)
        total += item['Quantity'] * item['Price']
        y -= 20

    p.drawString(100, y - 20, f"Total: {total:.2f}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{sale_id}.pdf", mimetype='application/pdf')
