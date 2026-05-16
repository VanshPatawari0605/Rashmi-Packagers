from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# ── Admin user (for login) ──────────────────────────
class Admin(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    from config import Config
    if user_id == 'admin':
        return Admin('admin')
    return None

# ── Enquiry table (saved to database) ───────────────
class Enquiry(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    phone       = db.Column(db.String(15),  nullable=False)
    email       = db.Column(db.String(120), nullable=True)
    product     = db.Column(db.String(100), nullable=False)
    order_type  = db.Column(db.String(20),  nullable=False)  # 'bulk' or 'sample'
    quantity    = db.Column(db.String(50),  nullable=True)
    message     = db.Column(db.Text,        nullable=True)
    submitted_at = db.Column(db.DateTime,   default=datetime.utcnow)

    def __repr__(self):
        return f'<Enquiry {self.name} - {self.product}>'