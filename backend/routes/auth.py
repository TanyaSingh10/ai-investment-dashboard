from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import Config
from models import db, User, Organization

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    org_name = data.get('org_name')
    
    if not email or not password or not org_name:
        return jsonify({'message': 'Missing email, password, or org_name'}), 400
        
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 409
        
    # Create Organization first
    org = Organization(name=org_name)
    db.session.add(org)
    db.session.flush() # To get org.id
    
    # Create User
    hashed_password = generate_password_hash(password)
    user = User(email=email, password_hash=hashed_password, org_id=org.id)
    db.session.add(user)
    db.session.commit()
    
    # Generate JWT
    token = jwt.encode({
        'user_id': user.id,
        'org_id': org.id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, Config.SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'org_id': org.id
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = jwt.encode({
        'user_id': user.id,
        'org_id': user.org_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, Config.SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'org_id': user.org_id
        }
    }), 200
