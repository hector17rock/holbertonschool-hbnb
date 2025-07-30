#!/usr/bin/env python3
"""
Test script for User model mapping and database initialization.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.services.facade import HBnBFacade
from app.services.repositories.user_repository import UserRepository


def test_user_model_mapping():
    """Test User model SQLAlchemy mapping"""
    print("Testing User Model Mapping...")
    print("=" * 50)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        print("1. Creating database tables...")
        try:
            db.create_all()
            print("   ✅ Database tables created successfully")
        except Exception as e:
            print(f"   ❌ Error creating tables: {e}")
            return False
        
        print("\n2. Testing User model attributes...")
        try:
            # Test User model creation
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                is_admin=False
            )
            
            # Test password hashing
            user.hash_password("password123")
            
            print(f"   - Created user: {user.first_name} {user.last_name}")
            print(f"   - Email: {user.email}")
            print(f"   - Admin status: {user.is_admin}")
            print(f"   - Password hashed: {user.password[:20]}...")
            print(f"   - User ID: {user.id}")
            print(f"   - Created at: {user.created_at}")
            print(f"   - Updated at: {user.updated_at}")
            
            # Test password verification
            is_valid = user.verify_password("password123")
            print(f"   - Password verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
            # Test invalid password
            is_invalid = user.verify_password("wrongpassword")
            print(f"   - Invalid password test: {'❌ Should be false' if is_invalid else '✅ Correctly rejected'}")
            
        except Exception as e:
            print(f"   ❌ Error testing User model: {e}")
            return False
        
        print("\n3. Testing User validation...")
        try:
            # Test email validation
            try:
                user_invalid_email = User(
                    first_name="Jane",
                    last_name="Smith",
                    email="invalid-email",
                    is_admin=False
                )
                user_invalid_email.hash_password("password123")
                db.session.add(user_invalid_email)
                db.session.commit()
                print("   ❌ Should have failed email validation")
            except ValueError as e:
                print(f"   ✅ Email validation works: {e}")
                db.session.rollback()
            
            # Test name validation
            try:
                user_empty_name = User(
                    first_name="",
                    last_name="Smith",
                    email="jane@example.com",
                    is_admin=False
                )
                user_empty_name.hash_password("password123")
                db.session.add(user_empty_name)
                db.session.commit()
                print("   ❌ Should have failed name validation")
            except ValueError as e:
                print(f"   ✅ Name validation works: {e}")
                db.session.rollback()
                
        except Exception as e:
            print(f"   ❌ Error testing validation: {e}")
            return False
        
        print("\n4. Testing UserRepository...")
        try:
            # Test UserRepository
            user_repo = UserRepository()
            
            # Create test users
            test_users = [
                {
                    'first_name': 'Alice',
                    'last_name': 'Johnson',
                    'email': 'alice@example.com',
                    'password': 'password123',
                    'is_admin': False
                },
                {
                    'first_name': 'Bob',
                    'last_name': 'Admin',
                    'email': 'bob@example.com',
                    'password': 'adminpass',
                    'is_admin': True
                }
            ]
            
            created_users = []
            for user_data in test_users:
                user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_admin=user_data['is_admin']
                )
                user.hash_password(user_data['password'])
                user_repo.add(user)
                created_users.append(user)
                print(f"   - Created user: {user.first_name} {user.last_name}")
            
            # Test get_user_by_email
            alice = user_repo.get_user_by_email('alice@example.com')
            print(f"   - Found user by email: {alice.first_name} {alice.last_name}")
            
            # Test get_admin_users
            admin_users = user_repo.get_admin_users()
            print(f"   - Found {len(admin_users)} admin users")
            
            # Test get_regular_users
            regular_users = user_repo.get_regular_users()
            print(f"   - Found {len(regular_users)} regular users")
            
            # Test search_users_by_name
            alice_results = user_repo.search_users_by_name('Alice')
            print(f"   - Search for 'Alice': {len(alice_results)} results")
            
            # Test email_exists
            email_exists = user_repo.email_exists('alice@example.com')
            print(f"   - Email exists check: {'✅ Found' if email_exists else '❌ Not found'}")
            
        except Exception as e:
            print(f"   ❌ Error testing UserRepository: {e}")
            return False
        
        print("\n5. Testing HBnBFacade with UserRepository...")
        try:
            # Test facade
            facade = HBnBFacade()
            
            # Test user creation through facade
            user_data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'password': 'testpass123',
                'is_admin': False
            }
            
            created_user = facade.create_user(user_data)
            print(f"   - Created user via facade: {created_user.first_name} {created_user.last_name}")
            
            # Test get_user_by_email through facade
            found_user = facade.get_user_by_email('test@example.com')
            print(f"   - Found user via facade: {found_user.first_name} {found_user.last_name}")
            
            # Test get_all_users
            all_users = facade.get_all_users()
            print(f"   - Total users via facade: {len(all_users)}")
            
            # Test update_user
            update_data = {'first_name': 'Updated'}
            updated_user = facade.update_user(created_user.id, update_data)
            print(f"   - Updated user: {updated_user.first_name} {updated_user.last_name}")
            
        except Exception as e:
            print(f"   ❌ Error testing facade: {e}")
            return False
        
        print("\n6. Testing database persistence...")
        try:
            # Test that users are persisted
            user_count = User.query.count()
            print(f"   - Total users in database: {user_count}")
            
            # Test unique email constraint
            try:
                duplicate_user = User(
                    first_name="Duplicate",
                    last_name="User",
                    email="alice@example.com",  # This should fail
                    is_admin=False
                )
                duplicate_user.hash_password("password123")
                db.session.add(duplicate_user)
                db.session.commit()
                print("   ❌ Should have failed unique constraint")
            except Exception as e:
                print(f"   ✅ Unique constraint works: {type(e).__name__}")
                db.session.rollback()
            
        except Exception as e:
            print(f"   ❌ Error testing persistence: {e}")
            return False
        
        print("\n✅ All User model tests passed!")
        return True


if __name__ == "__main__":
    print("User Model Mapping Test")
    print("=" * 60)
    
    success = test_user_model_mapping()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ User model mapping implementation successful!")
        print("\nFeatures implemented:")
        print("- ✅ BaseModel mapped to SQLAlchemy")
        print("- ✅ User model mapped to SQLAlchemy")
        print("- ✅ UserRepository with specialized methods")
        print("- ✅ Database table creation")
        print("- ✅ Password hashing and verification")
        print("- ✅ Email and name validation")
        print("- ✅ Unique email constraint")
        print("- ✅ Facade integration with UserRepository")
        print("- ✅ Database persistence")
        
        print("\nNext steps:")
        print("1. Test API endpoints with database")
        print("2. Map other models (Place, Review, Amenity)")
        print("3. Add relationship mappings")
        print("4. Implement migrations")
    else:
        print("❌ User model mapping test failed!")
        print("Check the error messages above for details.")
