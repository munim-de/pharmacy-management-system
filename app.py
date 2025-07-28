from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Import your routes after app is created
from routes import auth, dashboard, inventory, sales, admin
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(inventory.bp)
app.register_blueprint(sales.bp)
app.register_blueprint(admin.bp)

# Optional: basic health check route
@app.route('/healthz')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run()
