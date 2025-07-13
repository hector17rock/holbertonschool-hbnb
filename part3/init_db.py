#!/usr/bin/env python3
"""
Database initialization script for User model mapping.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User


def init_database():
    """Initialize database with User table"""
    print("Initializing Database...")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully")
            
            # Create a sample admin user
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email="admin@hbnb.com",
                is_admin=True
            )
            admin_user.hash_password("adminpass123")
            
            # Check if admin already exists
            existing_admin = User.query.filter_by(email="admin@hbnb.com").first()
            if not existing_admin:
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created:")
                print(f"   Email: {admin_user.email}")
                print(f"   ID: {admin_user.id}")
                print(f"   Password: adminpass123")
            else:
                print("Admin user already exists")
            
            # Create a sample regular user
            regular_user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                is_admin=False
            )
            regular_user.hash_password("password123")
            
            # Check if regular user already exists
            existing_user = User.query.filter_by(email="john@example.com").first()
            if not existing_user:
                db.session.add(regular_user)
                db.session.commit()
                print("Regular user created:")
                print(f"   Email: {regular_user.email}")
                print(f"   ID: {regular_user.id}")
                print(f"   Password: password123")
            else:
                print("Regular user already exists")
            
            # Show database status
            user_count = User.query.count()
            admin_count = User.query.filter_by(is_admin=True).count()
            regular_count = User.query.filter_by(is_admin=False).count()
            
            print(f"\nDatabase Status:")
            print(f"- Total users: {user_count}")
            print(f"- Admin users: {admin_count}")
            print(f"- Regular users: {regular_count}")
            
            print("\nDatabase initialization completed!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    
    return True


if __name__ == "__main__":
    print("HBnB Database Initialization")
    print("=" * 60)
    
    success = init_database()
    
    if success:
        print("\n" + "=" * 60)
        print("Database ready for testing!")
        print("\nYou can now:")
        print("1. Run the Flask app: python3 run.py")
        print("2. Test API endpoints with cURL or Postman")
        print("3. Run the test script: python3 test_user_model.py")
        
        print("\nSample API tests:")
        print("# Get admin login token:")
        print('curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"email": "admin@hbnb.com", "password": "adminpass123"}\'')
        
        print("\n# Create a new user (admin required):")
        print('curl -X POST "http://127.0.0.1:5000/api/v1/users/" \\')
        print('  -H "Authorization: Bearer <admin_token>" \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com", "password": "password123"}\'')
        
        print("\n# Get all users:")
        print('curl -X GET "http://127.0.0.1:5000/api/v1/users/"')
        
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)
