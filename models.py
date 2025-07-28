# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ------------------ User Model ------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

# ------------------ Customer Model ------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50))

    def __repr__(self):
        return f"<Customer {self.name}>"

# ------------------ Medicine Model ------------------
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Medicine {self.name}>"

# ------------------ Sale Model ------------------
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    total_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('Customer', backref='sales')
    salesperson = db.relationship('User', backref='sales')

    def __repr__(self):
        return f"<Sale {self.id}>"

# ------------------ SaleDetail Model ------------------
class SaleDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    sale = db.relationship('Sale', backref='details')
    medicine = db.relationship('Medicine', backref='sale_details')

    def __repr__(self):
        return f"<SaleDetail Sale:{self.sale_id} Medicine:{self.medicine_id}>"
