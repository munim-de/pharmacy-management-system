# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# -------------------- User Model --------------------
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, sales, etc.

    def __repr__(self):
        return f"<User {self.email}>"

# -------------------- Medicine Model --------------------
class Medicine(db.Model):
    __tablename__ = 'medicine'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Medicine {self.name}>"

# -------------------- Sale Model --------------------
class Sale(db.Model):
    __tablename__ = 'sale'

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    medicine = db.relationship('Medicine', backref='sales')
    salesperson = db.relationship('User', backref='sales')

    def __repr__(self):
        return f"<Sale {self.id}>"

# -------------------- InventoryLog Model (optional) --------------------
class InventoryLog(db.Model):
    __tablename__ = 'inventory_log'

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    change = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200))

    medicine = db.relationship('Medicine', backref='inventory_logs')

    def __repr__(self):
        return f"<InventoryLog {self.id}>"
