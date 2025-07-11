#!/usr/bin/env python3
"""
Comprehensive API endpoint testing script for HBnB application.
This script tests all available API endpoints systematically.
"""

import requests
import json
import time
from app import create_app
from app.models.base_model import db

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://127.0.0.1:5002/api/v1"
    
    print("🚀 Starting API endpoint testing...")
    print("=" * 50)
    
    # Test 1: GET all users (should be empty initially)
    print("\n1. Testing GET /users (should be empty)")
    try:
        response = requests.get(f"{base_url}/users", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /users - PASSED")
    except Exception as e:
        print(f"   ❌ GET /users - FAILED: {e}")
        return False
    
    # Test 2: Create first user (admin)
    print("\n2. Testing POST /users (create first admin user)")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "admin@example.com",
        "password": "password123",
        "is_admin": True
    }
    
    try:
        response = requests.post(f"{base_url}/users", json=user_data, timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 201
        user_id = response.json()['id']
        print(f"   ✅ POST /users - PASSED (User ID: {user_id})")
    except Exception as e:
        print(f"   ❌ POST /users - FAILED: {e}")
        return False
    
    # Test 3: Login to get JWT token
    print("\n3. Testing POST /auth/login")
    login_data = {
        "email": "admin@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=5)
        print(f"   Status Code: {response.status_code}")
        response_data = response.json()
        print(f"   Response: {response_data}")
        assert response.status_code == 200
        access_token = response_data['access_token']
        print("   ✅ POST /auth/login - PASSED")
    except Exception as e:
        print(f"   ❌ POST /auth/login - FAILED: {e}")
        return False
    
    # Test 4: Get user by ID
    print(f"\n4. Testing GET /users/{user_id}")
    try:
        response = requests.get(f"{base_url}/users/{user_id}", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /users/{id} - PASSED")
    except Exception as e:
        print(f"   ❌ GET /users/{user_id} - FAILED: {e}")
        return False
    
    # Test 5: Get all amenities (should be empty)
    print("\n5. Testing GET /amenities")
    try:
        response = requests.get(f"{base_url}/amenities", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /amenities - PASSED")
    except Exception as e:
        print(f"   ❌ GET /amenities - FAILED: {e}")
        return False
    
    # Test 6: Create amenity (requires admin token)
    print("\n6. Testing POST /amenities (create amenity)")
    amenity_data = {
        "name": "WiFi"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{base_url}/amenities", json=amenity_data, headers=headers, timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 201
        amenity_id = response.json()['id']
        print(f"   ✅ POST /amenities - PASSED (Amenity ID: {amenity_id})")
    except Exception as e:
        print(f"   ❌ POST /amenities - FAILED: {e}")
        return False
    
    # Test 7: Get all places (should be empty)
    print("\n7. Testing GET /places")
    try:
        response = requests.get(f"{base_url}/places", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /places - PASSED")
    except Exception as e:
        print(f"   ❌ GET /places - FAILED: {e}")
        return False
    
    # Test 8: Create place (requires authentication)
    print("\n8. Testing POST /places (create place)")
    place_data = {
        "title": "Cozy Apartment",
        "description": "A beautiful apartment in the city center",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "amenities": [amenity_id]
    }
    
    try:
        response = requests.post(f"{base_url}/places", json=place_data, headers=headers, timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 201
        place_id = response.json()['id']
        print(f"   ✅ POST /places - PASSED (Place ID: {place_id})")
    except Exception as e:
        print(f"   ❌ POST /places - FAILED: {e}")
        return False
    
    # Test 9: Get place by ID
    print(f"\n9. Testing GET /places/{place_id}")
    try:
        response = requests.get(f"{base_url}/places/{place_id}", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /places/{id} - PASSED")
    except Exception as e:
        print(f"   ❌ GET /places/{place_id} - FAILED: {e}")
        return False
    
    # Test 10: Get all reviews (should be empty)
    print("\n10. Testing GET /reviews")
    try:
        response = requests.get(f"{base_url}/reviews", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        print("   ✅ GET /reviews - PASSED")
    except Exception as e:
        print(f"   ❌ GET /reviews - FAILED: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All API endpoint tests completed successfully!")
    print("=" * 50)
    return True

def setup_database():
    """Initialize the database tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")

if __name__ == "__main__":
    # First, setup the database
    setup_database()
    
    # Wait a moment for any cleanup
    time.sleep(2)
    
    # Test the API endpoints
    success = test_api_endpoints()
    
    if success:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
