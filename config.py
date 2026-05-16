import os

class Config:
    SECRET_KEY = 'rashmi-packagers-secret-2025'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'rashmi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin credentials
    ADMIN_USERNAME = 'RP_Admin'
    ADMIN_PASSWORD = 'RP1977'