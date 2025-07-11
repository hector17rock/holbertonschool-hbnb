#!/usr/bin/env python3
"""
Internal API endpoint testing using Flask test client.
This bypasses network issues and tests the API directly.
"""

import json
from app import create_app
from app.models.base_model import db

def test_api_endpoints():
    """Test all API endpoints using Flask test client"""
    
    # Create app instance
    app = create_app()
    
    # Setup database
    with app.app_context():
        db.drop_all()  # Clean slate for testing
        db.create_all()
        
        # Create a test client
        client = app.test_client()
        
        print("🚀 Starting API endpoint testing...")
        print("=" * 50)
        
        # Test 1: GET all users (should be empty initially)
        print("\n1. Testing GET /api/v1/users (should be empty)")
        response = client.get('/api/v1/users/')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/users - PASSED")
        
        # Test 2: Create first user (admin)
        print("\n2. Testing POST /api/v1/users (create first admin user)")
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "admin@example.com",
            "password": "password123",
            "is_admin": True
        }
        
        response = client.post('/api/v1/users/', 
                              data=json.dumps(user_data),
                              content_type='application/json')
        print(f"   Status Code: {response.status_code}")
        response_data = response.get_json()
        print(f"   Response: {response_data}")
        assert response.status_code == 201
        user_id = response_data['id']
        print(f"   ✅ POST /api/v1/users - PASSED (User ID: {user_id})")
        
        # Test 3: Login to get JWT token
        print("\n3. Testing POST /api/v1/auth/login")
        login_data = {
            "email": "admin@example.com",
            "password": "password123"
        }
        
        response = client.post('/api/v1/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        print(f"   Status Code: {response.status_code}")
        response_data = response.get_json()
        print(f"   Response: {response_data}")
        assert response.status_code == 200
        access_token = response_data['access_token']
        print("   ✅ POST /api/v1/auth/login - PASSED")
        
        # Test 4: Get user by ID
        print(f"\n4. Testing GET /api/v1/users/{user_id}")
        response = client.get(f'/api/v1/users/{user_id}')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/users/{id} - PASSED")
        
        # Test 5: Get all amenities (should be empty)
        print("\n5. Testing GET /api/v1/amenities")
        response = client.get('/api/v1/amenities/')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/amenities - PASSED")
        
        # Test 6: Create amenity (requires admin token)
        print("\n6. Testing POST /api/v1/amenities (create amenity)")
        amenity_data = {
            "name": "WiFi"
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = client.post('/api/v1/amenities/',
                              data=json.dumps(amenity_data),
                              headers=headers)
        print(f"   Status Code: {response.status_code}")
        response_data = response.get_json()
        print(f"   Response: {response_data}")
        assert response.status_code == 201
        amenity_id = response_data['id']
        print(f"   ✅ POST /api/v1/amenities - PASSED (Amenity ID: {amenity_id})")
        
        # Test 7: Get all places (should be empty)
        print("\n7. Testing GET /api/v1/places")
        response = client.get('/api/v1/places/')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/places - PASSED")
        
        # Test 8: Create place (requires authentication)
        print("\n8. Testing POST /api/v1/places (create place)")
        place_data = {
            "title": "Cozy Apartment",
            "description": "A beautiful apartment in the city center",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenities": [amenity_id]
        }
        
        response = client.post('/api/v1/places/',
                              data=json.dumps(place_data),
                              headers=headers)
        print(f"   Status Code: {response.status_code}")
        response_data = response.get_json()
        print(f"   Response: {response_data}")
        assert response.status_code == 201
        place_id = response_data['id']
        print(f"   ✅ POST /api/v1/places - PASSED (Place ID: {place_id})")
        
        # Test 9: Get place by ID
        print(f"\n9. Testing GET /api/v1/places/{place_id}")
        response = client.get(f'/api/v1/places/{place_id}')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/places/{id} - PASSED")
        
        # Test 10: Get all reviews (should be empty)
        print("\n10. Testing GET /api/v1/reviews")
        response = client.get('/api/v1/reviews/')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 200
        print("   ✅ GET /api/v1/reviews - PASSED")
        
        # Test 11: Test Error Case - Get non-existent user
        print("\n11. Testing GET /api/v1/users/non-existent-id (should return 404)")
        response = client.get('/api/v1/users/non-existent-id')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 404
        print("   ✅ GET /api/v1/users/non-existent-id - PASSED (404 as expected)")
        
        # Test 12: Test unauthorized access
        print("\n12. Testing POST /api/v1/amenities without auth (should return 401)")
        response = client.post('/api/v1/amenities/',
                              data=json.dumps({"name": "Pool"}),
                              content_type='application/json')
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        assert response.status_code == 401
        print("   ✅ POST /api/v1/amenities without auth - PASSED (401 as expected)")
        
        print("\n" + "=" * 50)
        print("🎉 All API endpoint tests completed successfully!")
        print("=" * 50)
        
        return True

if __name__ == "__main__":
    try:
        success = test_api_endpoints()
        if success:
            print("\n🎉 All tests passed! Your API is working correctly.")
        else:
            print("\n❌ Some tests failed. Please check the output above.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
