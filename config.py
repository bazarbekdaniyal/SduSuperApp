"""
SDU SuperApp Application Configuration

Environment Variables:
- SMTP_EMAIL: Email for sending notifications
- SMTP_PASSWORD: App password for SMTP
- SECRET_KEY: Flask secret key
- ADMIN_USERNAME: Admin panel username
- ADMIN_PASSWORD: Admin panel password
"""
import os

# SMTP Configuration (set these in your environment)
SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    DEBUG = False
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    # Admin Panel (set in environment variables for production)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

