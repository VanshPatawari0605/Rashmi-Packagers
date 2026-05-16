from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Enquiry, Admin
from config import Config

main = Blueprint('main', __name__)

# ── Home page ────────────────────────────────────────
@main.route('/')
def index():
    return render_template('index.html')

# ── Products page ────────────────────────────────────
@main.route('/products')
def products():
    return render_template('products.html')

# ── About page ───────────────────────────────────────
@main.route('/about')
def about():
    return render_template('about.html')

# ── Enquiry / Place Order ────────────────────────────
@main.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if request.method == 'POST':
        name       = request.form.get('name')
        phone      = request.form.get('phone')
        email      = request.form.get('email')
        product    = request.form.get('product')
        order_type = request.form.get('order_type')
        quantity   = request.form.get('quantity')
        message    = request.form.get('message')

        new_enquiry = Enquiry(
            name       = name,
            phone      = phone,
            email      = email,
            product    = product,
            order_type = order_type,
            quantity   = quantity,
            message    = message
        )
        db.session.add(new_enquiry)
        db.session.commit()

        flash('Your enquiry has been submitted! We will contact you soon.', 'success')
        return redirect(url_for('main.enquiry'))

    return render_template('enquiry.html')

# ── Admin Login ──────────────────────────────────────
@main.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            admin = Admin('admin')
            login_user(admin)
            return redirect(url_for('main.admin'))
        else:
            flash('Wrong username or password.', 'danger')

    return render_template('login.html')

# ── Admin Panel ──────────────────────────────────────
@main.route('/admin')
@login_required
def admin():
    enquiries = Enquiry.query.order_by(Enquiry.submitted_at.desc()).all()
    return render_template('admin.html', enquiries=enquiries)

# ── Admin Logout ─────────────────────────────────────
@main.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ── Delete Enquiry (admin only) ──────────────────────
@main.route('/admin/delete/<int:id>')
@login_required
def delete_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)
    db.session.delete(enquiry)
    db.session.commit()
    return redirect(url_for('main.admin'))