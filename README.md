# Pharmacy Management System

A full-stack pharmacy app with:
- PostgreSQL + SQLAlchemy
- Flask-based modular backend
- Bootstrap 5 UI
- Role-based login (Admin, Sales, Inventory)
- PDF invoice generation
- CSV monthly reports
- Email/SMS alerts for expiry & stock
- Deployable to Render/Railway

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
