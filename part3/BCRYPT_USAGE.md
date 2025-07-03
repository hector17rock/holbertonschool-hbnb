# 🔐 Bcrypt Integration Guide

This guide explains how to use the Flask-Bcrypt plugin in the HBnB application for secure password hashing.

## ✅ Setup Complete

The Bcrypt plugin has been successfully registered in the Flask application:

### In `app/__init__.py`:
```python
from flask_bcrypt import Bcrypt

# Initialize Bcrypt instance
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    
    # ... rest of the application setup
    return app
```

## 🔧 How to Use Bcrypt

### 1. Import the Bcrypt Instance

```python
from app import bcrypt
```

### 2. Hash a Password

```python
# In your User model or service layer
def hash_password(password):
    """Hash a password using Bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Example usage
user_password = "mySecretPassword123"
hashed = hash_password(user_password)
print(hashed)  # $2b$12$...
```

### 3. Verify a Password

```python
# In your authentication logic
def verify_password(stored_hash, provided_password):
    """Verify a password against its hash."""
    return bcrypt.check_password_hash(stored_hash, provided_password)

# Example usage
is_valid = verify_password(stored_hash, user_input_password)
if is_valid:
    print("Authentication successful!")
else:
    print("Invalid password!")
```

## 📝 Integration Examples

### Example 1: User Model Enhancement

```python
# In app/models/user.py
from app import bcrypt

class User:
    def __init__(self, first_name, last_name, email, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if password:
            self.password_hash = self.hash_password(password)
    
    def hash_password(self, password):
        """Hash the user's password."""
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Set a new password for the user."""
        self.password_hash = self.hash_password(password)
```

### Example 2: Authentication Service

```python
# In app/services/auth_service.py
from app import bcrypt
from app.models.user import User

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate a user with email and password."""
        user = User.get_by_email(email)  # Assuming this method exists
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None
    
    @staticmethod
    def register_user(user_data):
        """Register a new user with hashed password."""
        # Hash the password before storing
        if 'password' in user_data:
            user_data['password_hash'] = bcrypt.generate_password_hash(
                user_data['password']
            ).decode('utf-8')
            del user_data['password']  # Remove plain password
        
        return User(**user_data)
```

### Example 3: API Endpoint Usage

```python
# In app/api/v1/auth.py (if you create an auth endpoint)
from flask_restx import Resource, Namespace
from app import bcrypt
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

@api.route('/login')
class Login(Resource):
    def post(self):
        """User login endpoint."""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = facade.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return {'message': 'Login successful', 'user_id': user.id}, 200
        else:
            return {'error': 'Invalid credentials'}, 401

@api.route('/register')
class Register(Resource):
    def post(self):
        """User registration endpoint."""
        data = request.get_json()
        
        # Hash the password
        if 'password' in data:
            data['password_hash'] = bcrypt.generate_password_hash(
                data['password']
            ).decode('utf-8')
            del data['password']
        
        user = facade.create_user(data)
        return {'message': 'User created', 'user_id': user.id}, 201
```

## 🛡️ Security Best Practices

### 1. Never Store Plain Text Passwords
```python
# ❌ DON'T DO THIS
user.password = "plaintext_password"

# ✅ DO THIS
user.password_hash = bcrypt.generate_password_hash("password").decode('utf-8')
```

### 2. Always Use Application Context
```python
# When using Bcrypt outside of request context
with app.app_context():
    hashed = bcrypt.generate_password_hash("password")
```

### 3. Handle Exceptions
```python
def safe_hash_password(password):
    try:
        return bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception as e:
        # Log the error
        print(f"Error hashing password: {e}")
        return None
```

## 🧪 Testing Your Implementation

Run the demo script to test the integration:

```bash
python3 bcrypt_demo.py
```

## 🔗 Available Methods

### `bcrypt.generate_password_hash(password, rounds=12)`
- **Purpose**: Hash a password
- **Returns**: Bytes object (needs `.decode('utf-8')`)
- **Parameters**:
  - `password`: The password to hash
  - `rounds`: Cost factor (default 12, higher = more secure but slower)

### `bcrypt.check_password_hash(hash, password)`
- **Purpose**: Verify a password against its hash
- **Returns**: Boolean (True if password matches)
- **Parameters**:
  - `hash`: The stored password hash
  - `password`: The password to verify

## 📚 Next Steps

1. **Update User Model**: Add password hashing methods
2. **Create Authentication Service**: Implement login/register logic
3. **Add API Endpoints**: Create auth endpoints for login/register
4. **Add Password Validation**: Implement password strength requirements
5. **Add Session Management**: Implement JWT or session-based auth

## 🔧 Dependencies

Make sure these are in your `requirements.txt`:
```
flask
flask-restx
flask-bcrypt
```

Install with:
```bash
pip install -r requirements.txt
```
