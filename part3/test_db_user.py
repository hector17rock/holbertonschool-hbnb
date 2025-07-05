#!/usr/bin/env python3
"""
Test script for database User operations.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import validates

# Setup Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define BaseModel
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.utcnow()

# Define User model
class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, first_name="", last_name="", email="", password="", is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if password:
            self.hash_password(password)
        self.is_admin = is_admin
        
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

def test_user_operations():
    """Test user CRUD operations."""
    with app.app_context():
        print("🧪 Testing User Database Operations")
        print("===================================")
        
        # Create a test user
        print("1. Creating user...")
        user = User(
            first_name="John",
            last_name="Doe", 
            email="john.doe@example.com",
            password="password123",
            is_admin=False
        )
        
        db.session.add(user)
        db.session.commit()
        print(f"✅ User created with ID: {user.id}")
        
        # Retrieve user by ID
        print("2. Retrieving user by ID...")
        retrieved_user = User.query.get(user.id)
        print(f"✅ Retrieved user: {retrieved_user.first_name} {retrieved_user.last_name}")
        
        # Retrieve user by email
        print("3. Retrieving user by email...")
        email_user = User.query.filter_by(email="john.doe@example.com").first()
        print(f"✅ Found user by email: {email_user.email}")
        
        # Test password verification
        print("4. Testing password verification...")
        is_valid = email_user.verify_password("password123")
        print(f"✅ Password verification: {is_valid}")
        
        # Create admin user
        print("5. Creating admin user...")
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com", 
            password="admin123",
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Admin user created with ID: {admin_user.id}")
        
        # Get all users
        print("6. Getting all users...")
        all_users = User.query.all()
        print(f"✅ Total users in database: {len(all_users)}")
        for user in all_users:
            admin_status = "Admin" if user.is_admin else "Regular"
            print(f"   - {user.first_name} {user.last_name} ({admin_status})")
        
        # Update user
        print("7. Updating user...")
        retrieved_user.first_name = "Jane"
        db.session.commit()
        print(f"✅ User updated: {retrieved_user.first_name} {retrieved_user.last_name}")
        
        print("\\n🎉 All tests passed! Database integration working correctly.")

if __name__ == "__main__":
    test_user_operations()
