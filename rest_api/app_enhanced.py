from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ========================
# MODELS
# ========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)  # For JWT auth
    api_key = db.Column(db.String(64), unique=True, nullable=True)  # For API key auth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': 'The request was malformed or missing required parameters',
        'status_code': 400
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'error': 'Unprocessable Entity',
        'message': 'The request was well-formed but was unable to be followed due to semantic errors',
        'status_code': 422
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'status_code': 500
    }), 500

# ========================
# UTILITY FUNCTIONS
# ========================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_data(data, required_fields=None):
    """Validate user input data"""
    if required_fields is None:
        required_fields = ['name', 'email']
    
    errors = []
    
    # Check required fields
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is required")
    
    # Validate email format
    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors.append("Invalid email format")
    
    # Validate name length
    if 'name' in data and data['name']:
        if len(data['name']) < 2:
            errors.append("Name must be at least 2 characters long")
        if len(data['name']) > 100:
            errors.append("Name must be less than 100 characters")
    
    return errors

def create_error_response(message, status_code=400, errors=None):
    """Create standardized error response"""
    response = {
        'error': True,
        'message': message,
        'status_code': status_code
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def create_success_response(data=None, message=None, status_code=200, meta=None):
    """Create standardized success response"""
    response = {
        'error': False,
        'status_code': status_code
    }
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    if meta:
        response['meta'] = meta
    return jsonify(response), status_code

# ========================
# AUTHENTICATION HELPERS
# ========================

import secrets

def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)

def check_api_key():
    """Check API key from headers"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None
    
    user = User.query.filter_by(api_key=api_key, is_active=True).first()
    return user

# ========================
# ROUTES
# ========================

@app.route("/")
def home():
    return jsonify({
        'message': 'Enhanced Flask REST API is running 🚀',
        'version': '2.0',
        'features': [
            'Proper HTTP status codes',
            'Input validation',
            'Error handling', 
            'Pagination',
            'SQLite database',
            'JWT authentication',
            'API key authentication'
        ],
        'endpoints': {
            'auth': {
                'register': 'POST /auth/register',
                'login': 'POST /auth/login',
                'generate_api_key': 'POST /auth/api-key'
            },
            'users': {
                'list': 'GET /users',
                'create': 'POST /users',
                'get': 'GET /users/<id>',
                'update': 'PUT /users/<id>',
                'delete': 'DELETE /users/<id>'
            }
        }
    })

# ========================
# AUTHENTICATION ROUTES
# ========================

@app.route("/auth/register", methods=["POST"])
def register():
    """Register a new user with password"""
    try:
        data = request.get_json()
        if not data:
            return create_error_response("Request body must be JSON", 400)
        
        # Validate required fields for registration
        required_fields = ['name', 'email', 'password']
        validation_errors = validate_user_data(data, required_fields)
        
        # Validate password
        if 'password' in data:
            if len(data['password']) < 6:
                validation_errors.append("Password must be at least 6 characters long")
        
        if validation_errors:
            return create_error_response("Validation failed", 422, validation_errors)
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return create_error_response("Email already exists", 422, ["Email must be unique"])
        
        # Create new user with password
        user = User(
            name=data['name'].strip(),
            email=data['email'].lower().strip()
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return create_success_response(
            data={
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            },
            message="User registered successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to register user", 500)

@app.route("/auth/login", methods=["POST"])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        if not data:
            return create_error_response("Request body must be JSON", 400)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return create_error_response("Email and password are required", 400)
        
        # Find user and verify password
        user = User.query.filter_by(email=email.lower().strip(), is_active=True).first()
        if not user or not user.check_password(password):
            return create_error_response("Invalid email or password", 401)
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return create_success_response(
            data={
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            },
            message="Login successful"
        )
        
    except Exception as e:
        return create_error_response("Failed to login", 500)

@app.route("/auth/api-key", methods=["POST"])
@jwt_required()
def generate_user_api_key():
    """Generate API key for authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        # Generate new API key
        api_key = generate_api_key()
        user.api_key = api_key
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return create_success_response(
            data={
                'api_key': api_key,
                'message': 'Use this key in X-API-Key header for authentication'
            },
            message="API key generated successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to generate API key", 500)

# ========================
# PROTECTED ROUTES EXAMPLE
# ========================

@app.route("/auth/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user profile (JWT protected)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        return create_success_response(data=user.to_dict())
        
    except Exception as e:
        return create_error_response("Failed to get profile", 500)

@app.route("/auth/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update current user profile (JWT protected)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        data = request.get_json()
        if not data:
            return create_error_response("Request body must be JSON", 400)
        
        # Validate input
        validation_errors = validate_user_data(data, required_fields=[])
        if validation_errors:
            return create_error_response("Validation failed", 422, validation_errors)
        
        # Check email uniqueness if email is being updated
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return create_error_response("Email already exists", 422, ["Email must be unique"])
        
        # Update user fields
        if 'name' in data:
            user.name = data['name'].strip()
        if 'email' in data:
            user.email = data['email'].lower().strip()
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return create_success_response(
            data=user.to_dict(),
            message="Profile updated successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to update profile", 500)

# GET all users with pagination (supports both JWT and API key auth)
@app.route("/users", methods=["GET"])
def get_users():
    try:
        # Optional authentication - works for both authenticated and unauthenticated requests
        auth_user = None
        
        # Check JWT token
        try:
            from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                auth_user = User.query.get(user_id)
        except:
            pass
        
        # Check API key if no JWT
        if not auth_user:
            auth_user = check_api_key()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            return create_error_response("Page must be greater than 0", 400)
        if per_page < 1 or per_page > 100:
            return create_error_response("Per page must be between 1 and 100", 400)
        
        # Query with pagination
        users_query = User.query.filter_by(is_active=True)
        total = users_query.count()
        users = users_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Create pagination metadata
        meta = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': users.pages,
            'has_next': users.has_next,
            'has_prev': users.has_prev,
            'next_page': users.next_num if users.has_next else None,
            'prev_page': users.prev_num if users.has_prev else None,
            'authenticated': auth_user is not None
        }
        
        return create_success_response(
            data=[user.to_dict() for user in users.items],
            meta=meta
        )
        
    except Exception as e:
        return create_error_response("Failed to retrieve users", 500)

# GET single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        return create_success_response(data=user.to_dict())
        
    except Exception as e:
        return create_error_response("Failed to retrieve user", 500)

# POST create user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return create_error_response("Request body must be JSON", 400)
        
        validation_errors = validate_user_data(data)
        if validation_errors:
            return create_error_response("Validation failed", 422, validation_errors)
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return create_error_response("Email already exists", 422, ["Email must be unique"])
        
        # Create new user
        user = User(
            name=data['name'].strip(),
            email=data['email'].lower().strip()
        )
        
        db.session.add(user)
        db.session.commit()
        
        return create_success_response(
            data=user.to_dict(),
            message="User created successfully",
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to create user", 500)

# PUT update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        data = request.get_json()
        if not data:
            return create_error_response("Request body must be JSON", 400)
        
        # Validate input (name and email are optional for updates)
        validation_errors = validate_user_data(data, required_fields=[])
        if validation_errors:
            return create_error_response("Validation failed", 422, validation_errors)
        
        # Check email uniqueness if email is being updated
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return create_error_response("Email already exists", 422, ["Email must be unique"])
        
        # Update user fields
        if 'name' in data:
            user.name = data['name'].strip()
        if 'email' in data:
            user.email = data['email'].lower().strip()
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return create_success_response(
            data=user.to_dict(),
            message="User updated successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to update user", 500)

# DELETE user (soft delete)
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return create_error_response("User not found", 404)
        
        # Soft delete - mark as inactive instead of removing
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return create_success_response(
            message="User deleted successfully",
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response("Failed to delete user", 500)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)