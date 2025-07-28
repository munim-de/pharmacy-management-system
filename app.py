from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Import your models here so Flask-Login can find User
from models import User

# Setup LoginManager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from routes import auth, dashboard, inventory, sales, admin
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(admin.bp)

    return app

# Gunicorn entry point
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
