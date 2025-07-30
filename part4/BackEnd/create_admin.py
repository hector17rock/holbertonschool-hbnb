#!/usr/bin/env python3
"""
Script to create an admin user for testing admin endpoints.
This script bypasses the API restrictions to create a user with admin privileges.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import facade

def create_admin_user():
    """Create an admin user for testing"""
    
    admin_data = {
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': 'adminpass123',
        'is_admin': True
    }
    
    try:
        # Check if admin already exists
        existing_admin = facade.get_user_by_email(admin_data['email'])
        if existing_admin:
            print(f"Admin user already exists with email: {admin_data['email']}")
            print(f"Admin user ID: {existing_admin.id}")
            return existing_admin
        
        # Create admin user
        admin_user = facade.create_user(admin_data)
        print(f"Admin user created successfully!")
        print(f"Email: {admin_user.email}")
        print(f"ID: {admin_user.id}")
        print(f"Is Admin: {admin_user.is_admin}")
        
        return admin_user
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return None

def create_regular_user():
    """Create a regular user for testing"""
    
    user_data = {
        'first_name': 'Regular',
        'last_name': 'User',
        'email': 'user@example.com',
        'password': 'userpass123',
        'is_admin': False
    }
    
    try:
        # Check if user already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            print(f"Regular user already exists with email: {user_data['email']}")
            print(f"Regular user ID: {existing_user.id}")
            return existing_user
        
        # Create regular user
        regular_user = facade.create_user(user_data)
        print(f"Regular user created successfully!")
        print(f"Email: {regular_user.email}")
        print(f"ID: {regular_user.id}")
        print(f"Is Admin: {regular_user.is_admin}")
        
        return regular_user
        
    except Exception as e:
        print(f"Error creating regular user: {e}")
        return None

if __name__ == "__main__":
    print("Creating test users...")
    print("=" * 50)
    
    # Create admin user
    admin_user = create_admin_user()
    print()
    
    # Create regular user
    regular_user = create_regular_user()
    print()
    
    if admin_user and regular_user:
        print("Test users created successfully!")
        print("=" * 50)
        print("To get admin token, use:")
        print(f'curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"email": "{admin_user.email}", "password": "adminpass123"}}\'')
        print()
        print("To get regular user token, use:")
        print(f'curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"email": "{regular_user.email}", "password": "userpass123"}}\'')
    else:
        print("Failed to create test users!")
        sys.exit(1)
