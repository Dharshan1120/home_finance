from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Expense
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=current_user_id).order_by(Expense.date.desc()).all()
    return jsonify([exp.to_dict() for exp in expenses]), 200

@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('amount') or not data.get('category') or not data.get('date'):
        return jsonify({'error': 'Missing required fields: amount, category, date'}), 400

    try:
        new_expense = Expense(
            user_id=current_user_id,
            amount=float(data['amount']),
            category=data['category'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            description=data.get('description', '')
        )
        db.session.add(new_expense)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Expense added', 'expense': new_expense.to_dict()}), 201

@expenses_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    current_user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=current_user_id).first()
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404

    data = request.get_json()
    if 'amount' in data:
        expense.amount = float(data['amount'])
    if 'category' in data:
        expense.category = data['category']
    if 'date' in data:
        expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'description' in data:
        expense.description = data['description']

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Expense updated', 'expense': expense.to_dict()}), 200

@expenses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    current_user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=current_user_id).first()
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted'}), 200
