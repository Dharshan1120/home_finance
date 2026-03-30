from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Budget

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/', methods=['GET'])
@jwt_required()
def get_budgets():
    current_user_id = get_jwt_identity()
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    return jsonify([b.to_dict() for b in budgets]), 200

@budgets_bp.route('/', methods=['POST'])
@jwt_required()
def set_budget():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('category') or not data.get('limit'):
        return jsonify({'error': 'Missing required fields: category, limit'}), 400

    category = data['category']
    limit = float(data['limit'])
    
    # Check if a budget for this category already exists
    budget = Budget.query.filter_by(user_id=current_user_id, category=category).first()
    
    if budget:
        budget.limit = limit
    else:
        budget = Budget(user_id=current_user_id, category=category, limit=limit)
        db.session.add(budget)
        
    db.session.commit()
    return jsonify({'message': 'Budget updated', 'budget': budget.to_dict()}), 200
