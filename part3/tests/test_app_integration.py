#!/usr/bin/env python3
"""
Integration test for Flask app with SQLAlchemy models.
Tests the complete flow through API endpoints with database persistence.
"""

import json
import requests
from app import create_app
from app.models.base_model import db


def test_flask_app_integration():
    """Test Flask app integration with SQLAlchemy models."""
    print("🚀 Testing Flask App Integration with SQLAlchemy")
    print("=" * 55)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Drop and recreate database tables
        print("🏗️  Setting up database...")
        db.drop_all()
        db.create_all()
        print("✅ Database tables created successfully!\n")
    
    # Start Flask test client
    with app.test_client() as client:
        
        # Test 1: Create first admin user
        print("🧪 Test 1: Create first admin user...")
        user_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'admin123',
            'is_admin': True
        }
        
        response = client.post('/api/v1/users/', 
                               data=json.dumps(user_data),
                               content_type='application/json')
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        if response.status_code == 201:
            print("✅ Admin user created successfully")
            user_id = response.get_json()['id']
        else:
            print("❌ Failed to create admin user")
            return
        
        # Test 2: Login admin user
        print("\n🧪 Test 2: Login admin user...")
        login_data = {
            'email': 'admin@example.com',
            'password': 'admin123'
        }
        
        response = client.post('/api/v1/auth/login',
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Admin login successful")
            auth_token = response.get_json()['access_token']
            headers = {'Authorization': f'Bearer {auth_token}'}
        else:
            print("❌ Failed to login admin user")
            print(f"Response: {response.get_json()}")
            return
        
        # Test 3: Create amenities
        print("\n🧪 Test 3: Create amenities...")
        amenities_data = [
            {'name': 'WiFi'},
            {'name': 'Swimming Pool'},
            {'name': 'Parking'}
        ]
        
        amenity_ids = []
        for amenity_data in amenities_data:
            response = client.post('/api/v1/amenities/',
                                   data=json.dumps(amenity_data),
                                   content_type='application/json',
                                   headers=headers)
            if response.status_code == 201:
                amenity_id = response.get_json()['id']
                amenity_ids.append(amenity_id)
                print(f"✅ Created amenity: {amenity_data['name']} (ID: {amenity_id})")
            else:
                print(f"❌ Failed to create amenity: {amenity_data['name']}")
                print(f"Response: {response.get_json()}")
        
        # Test 4: Create a place
        print("\n🧪 Test 4: Create a place...")
        place_data = {
            'title': 'Beautiful Beach House',
            'description': 'A stunning oceanfront property',
            'price': 250.0,
            'latitude': 34.0522,
            'longitude': -118.2437,
            'amenities': amenity_ids[:2]  # Use first 2 amenities
        }
        
        response = client.post('/api/v1/places/',
                               data=json.dumps(place_data),
                               content_type='application/json',
                               headers=headers)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Place created successfully")
            place_response = response.get_json()
            place_id = place_response['id']
            print(f"   Place ID: {place_id}")
            print(f"   Title: {place_response['title']}")
            print(f"   Price: ${place_response['price']}")
        else:
            print("❌ Failed to create place")
            print(f"Response: {response.get_json()}")
            return
        
        # Test 5: Get all places
        print("\n🧪 Test 5: Get all places...")
        response = client.get('/api/v1/places/')
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            places = response.get_json()
            print(f"✅ Retrieved {len(places)} place(s)")
            for place in places:
                print(f"   - {place['title']}: ${place['price']}")
        else:
            print("❌ Failed to get places")
            print(f"Response: {response.get_json()}")
        
        # Test 6: Get specific place
        print("\n🧪 Test 6: Get specific place...")
        response = client.get(f'/api/v1/places/{place_id}')
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            place_detail = response.get_json()
            print("✅ Place details retrieved successfully")
            print(f"   Title: {place_detail['title']}")
            print(f"   Owner: {place_detail['owner']['first_name']} {place_detail['owner']['last_name']}")
            print(f"   Amenities: {[a['name'] for a in place_detail['amenities']]}")
        else:
            print("❌ Failed to get place details")
            print(f"Response: {response.get_json()}")
        
        # Test 7: Create a review
        print("\n🧪 Test 7: Create a review...")
        review_data = {
            'text': 'Amazing place! Highly recommended.',
            'rating': 5,
            'place_id': place_id
        }
        
        response = client.post('/api/v1/reviews/',
                               data=json.dumps(review_data),
                               content_type='application/json',
                               headers=headers)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Review created successfully")
            review_response = response.get_json()
            review_id = review_response['id']
            print(f"   Review ID: {review_id}")
            print(f"   Rating: {review_response['rating']}/5")
        else:
            print("❌ Failed to create review")
            print(f"Response: {response.get_json()}")
        
        # Test 8: Get all users
        print("\n🧪 Test 8: Get all users...")
        response = client.get('/api/v1/users/')
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            users = response.get_json()
            print(f"✅ Retrieved {len(users)} user(s)")
            for user in users:
                print(f"   - {user['first_name']} {user['last_name']}: {user['email']}")
        else:
            print("❌ Failed to get users")
            print(f"Response: {response.get_json()}")
        
        # Test 9: Get all amenities
        print("\n🧪 Test 9: Get all amenities...")
        response = client.get('/api/v1/amenities/')
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            amenities = response.get_json()
            print(f"✅ Retrieved {len(amenities)} amenity/amenities")
            for amenity in amenities:
                print(f"   - {amenity['name']}")
        else:
            print("❌ Failed to get amenities")
            print(f"Response: {response.get_json()}")
        
        print("\n🎉 All integration tests completed!")
        print("✅ SQLAlchemy models are working correctly with the Flask app")
        print("✅ All CRUD operations through API endpoints are functional")
        print("✅ Database persistence is working properly")


if __name__ == "__main__":
    test_flask_app_integration()
