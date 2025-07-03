#!/usr/bin/env python3
"""
Demo script showing how to use Bcrypt in the HBnB application.

This script demonstrates:
1. How to import and use the bcrypt instance
2. Password hashing
3. Password verification
4. Integration with the Flask application context
"""

from app import create_app, bcrypt
import config

def demo_bcrypt_usage():
    """Demonstrate Bcrypt functionality within the Flask app context."""
    
    # Create the Flask application
    app = create_app(config.DevelopmentConfig)
    
    print("🔐 HBnB Bcrypt Integration Demo")
    print("=" * 40)
    
    # Work within application context
    with app.app_context():
        # Example passwords to hash
        test_passwords = [
            "user123",
            "mySecurePassword!",
            "admin2024"
        ]
        
        print("\n📝 Hashing passwords:")
        hashed_passwords = []
        
        for password in test_passwords:
            # Hash the password
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            hashed_passwords.append((password, hashed))
            print(f"  Original: '{password}'")
            print(f"  Hashed:   {hashed}")
            print()
        
        print("\n✅ Verifying passwords:")
        for original, hashed in hashed_passwords:
            # Verify the password
            is_valid = bcrypt.check_password_hash(hashed, original)
            status = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"  '{original}' → {status}")
        
        print("\n❌ Testing with wrong passwords:")
        for original, hashed in hashed_passwords[:2]:  # Test first 2
            # Test with wrong password
            wrong_password = original + "_wrong"
            is_valid = bcrypt.check_password_hash(hashed, wrong_password)
            status = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"  '{wrong_password}' → {status}")

def demo_user_registration_flow():
    """Demonstrate a typical user registration flow with password hashing."""
    
    app = create_app(config.DevelopmentConfig)
    
    print("\n👤 User Registration Flow Demo")
    print("=" * 40)
    
    with app.app_context():
        # Simulate user registration data
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "password": "mySecretPassword123"
        }
        
        print(f"📋 User registration data:")
        print(f"  Name: {user_data['first_name']} {user_data['last_name']}")
        print(f"  Email: {user_data['email']}")
        print(f"  Password: {'*' * len(user_data['password'])}")
        
        # Hash the password (as you would in the User model or service)
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        
        print(f"\n🔐 Password hashed:")
        print(f"  Hash: {hashed_password}")
        
        # Simulate login verification
        print(f"\n🔑 Login verification:")
        login_password = "mySecretPassword123"  # User enters this
        is_authenticated = bcrypt.check_password_hash(hashed_password, login_password)
        
        print(f"  Entered password: {'*' * len(login_password)}")
        print(f"  Authentication: {'✅ SUCCESS' if is_authenticated else '❌ FAILED'}")

if __name__ == "__main__":
    try:
        demo_bcrypt_usage()
        demo_user_registration_flow()
        print("\n🎉 Bcrypt integration working perfectly!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure flask-bcrypt is installed: pip install flask-bcrypt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
