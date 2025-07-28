import os

class Config:
    # Secret key for sessions and security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')  # Replace 'devkey' with a secure value in production

    # PostgreSQL database URI (set as DATABASE_URL in Render environment)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///local.db'  # fallback to local DB for development
    )

    # Disable modification tracking to save overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: Show SQL queries in logs (useful for debugging)
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'

    # Optional: Enable debug mode if needed
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
