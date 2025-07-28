from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import auth, dashboard, inventory, sales, admin

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register all blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(dashboard.dashboard_bp)
app.register_blueprint(inventory.inventory_bp)
app.register_blueprint(sales.sales_bp)
app.register_blueprint(admin.admin_bp)

if __name__ == '__main__':
    app.run(debug=True)
