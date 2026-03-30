from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@views_bp.route('/login')
def login_view():
    return render_template('auth/login.html')

@views_bp.route('/register')
@views_bp.route('/signup')
def signup_view():
    return render_template('auth/signup.html')

@views_bp.route('/dashboard')
def dashboard_view():
    return render_template('app/dashboard.html')

@views_bp.route('/expenses')
def expenses_view():
    return render_template('app/expenses.html')

@views_bp.route('/budget')
def budget_view():
    return render_template('app/budget.html')
