from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Expense, Budget
from sqlalchemy import func
from datetime import datetime, timedelta
from utils import predict_next_month_expenses

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    current_user_id = get_jwt_identity()
    
    # 1. Base query for user's expenses
    expenses_query = Expense.query.filter_by(user_id=current_user_id)
    all_expenses = expenses_query.all()
    
    total_expenses = sum([e.amount for e in all_expenses])
    
    # For simplicity, we just assume a hardcoded or basic total income if no model is there. 
    # Or calculate it from user inputs if we had Income model. We didn't add Income routes yet, so 0.
    total_income = 5000.0 # Mock initial income or add later
    savings = total_income - total_expenses
    
    # 2. Get AI Prediction
    predicted_expenses = predict_next_month_expenses(all_expenses)
    
    # 3. Aggregations for charts
    # Monthly Trends
    monthly_data = db.session.query(
        func.date_format(Expense.date, '%Y-%m').label('month'),
        func.sum(Expense.amount).label('total')
    ).filter(Expense.user_id == current_user_id).group_by('month').order_by('month').all()
    
    monthly_chart = {
        'labels': [m.month for m in monthly_data],
        'data': [float(m.total) for m in monthly_data]
    }
    
    # Category Distribution
    category_data = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(Expense.user_id == current_user_id).group_by(Expense.category).all()
    
    category_chart = {
        'labels': [c.category for c in category_data],
        'data': [float(c.total) for c in category_data]
    }
    
    # 4. Budgets and warnings
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    budget_warnings = []
    
    current_month_start = datetime.utcnow().replace(day=1).date()
    
    for b in budgets:
        # Sum expenses for this category in the current month
        spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user_id,
            Expense.category == b.category,
            Expense.date >= current_month_start
        ).scalar() or 0.0
        
        if spent > b.limit:
            budget_warnings.append({
                'category': b.category,
                'limit': float(b.limit),
                'spent': float(spent)
            })
            
    return jsonify({
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'predicted_expenses': predicted_expenses,
        'monthly_chart': monthly_chart,
        'category_chart': category_chart,
        'budget_warnings': budget_warnings
    }), 200
