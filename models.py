from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(50), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(255))
    RoleID = db.Column(db.Integer, db.ForeignKey('roles.RoleID'))
    Role = db.relationship('Role')

    def get_id(self):
        return str(self.UserID)

    @property
    def role(self):
        return self.Role.RoleName

class Customer(db.Model):
    __tablename__ = 'customers'
    CustomerID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Phone = db.Column(db.String)
    Email = db.Column(db.String)
    Gender = db.Column(db.String)

class Medicine(db.Model):
    __tablename__ = 'medicines'
    MedicineID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Brand = db.Column(db.String)
    Price = db.Column(db.Float)
    QuantityInStock = db.Column(db.Integer)
    ExpiryDate = db.Column(db.Date)

class Sale(db.Model):
    __tablename__ = 'sales'
    SaleID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'))
    SaleDate = db.Column(db.Date, default=datetime.utcnow)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))

class SaleDetail(db.Model):
    __tablename__ = 'saledetails'
    SaleDetailID = db.Column(db.Integer, primary_key=True)
    SaleID = db.Column(db.Integer, db.ForeignKey('sales.SaleID'))
    MedicineID = db.Column(db.Integer, db.ForeignKey('medicines.MedicineID'))
    Quantity = db.Column(db.Integer)
