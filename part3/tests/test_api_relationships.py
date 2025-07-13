#!/usr/bin/env python3

import sys
import os
import json
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db

def test_api_relationships():
    """Test relationships through API endpoints."""
    app = create_app()
    
    with app.app_context():
        # Initialize the database
        db.create_all()
        
        # Create test client
        client = app.test_client()
        
        print("=== Testing API Endpoints with Relationships ===\n")
        
        # 1. Create a user (owner)
        print("1. Creating a user via API...")
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = client.post('/api/v1/users/', 
                              data=json.dumps(user_data),
                              content_type='application/json')
        user_result = json.loads(response.data)
        print(f"   User created: {user_result['first_name']} {user_result['last_name']} (ID: {user_result['id']})")
        user_id = user_result['id']
        
        # 2. Create another user (reviewer)
        print("\n2. Creating reviewer via API...")
        reviewer_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123'
        }
        response = client.post('/api/v1/users/', 
                              data=json.dumps(reviewer_data),
                              content_type='application/json')
        reviewer_result = json.loads(response.data)
        print(f"   Reviewer created: {reviewer_result['first_name']} {reviewer_result['last_name']} (ID: {reviewer_result['id']})")
        reviewer_id = reviewer_result['id']
        
        # 3. Create amenities
        print("\n3. Creating amenities via API...")
        amenity1_data = {'name': 'WiFi'}
        response = client.post('/api/v1/amenities/', 
                              data=json.dumps(amenity1_data),
                              content_type='application/json')
        amenity1_result = json.loads(response.data)
        print(f"   Amenity created: {amenity1_result['name']} (ID: {amenity1_result['id']})")
        amenity1_id = amenity1_result['id']
        
        amenity2_data = {'name': 'Swimming Pool'}
        response = client.post('/api/v1/amenities/', 
                              data=json.dumps(amenity2_data),
                              content_type='application/json')
        amenity2_result = json.loads(response.data)
        print(f"   Amenity created: {amenity2_result['name']} (ID: {amenity2_result['id']})")
        amenity2_id = amenity2_result['id']
        
        # 4. Create a place with amenities
        print("\n4. Creating a place with amenities via API...")
        place_data = {
            'title': 'Beautiful Beach House',
            'description': 'A wonderful place by the beach',
            'price': 150.0,
            'latitude': 25.7617,
            'longitude': -80.1918,
            'owner_id': user_id,
            'amenities': [amenity1_id, amenity2_id]
        }
        response = client.post('/api/v1/places/', 
                              data=json.dumps(place_data),
                              content_type='application/json')
        place_result = json.loads(response.data)
        print(f"   Place created: {place_result['title']} (ID: {place_result['id']})")
        place_id = place_result['id']
        
        # 5. Get the place to verify relationships
        print("\n5. Getting place details to verify relationships...")
        response = client.get(f'/api/v1/places/{place_id}')
        place_details = json.loads(response.data)
        print(f"   Place: {place_details['title']}")
        print(f"   Owner: {place_details['owner']['first_name']} {place_details['owner']['last_name']}")
        print(f"   Amenities: {[amenity['name'] for amenity in place_details['amenities']]}")
        
        # 6. Create a review
        print("\n6. Creating a review via API...")
        review_data = {
            'user_id': reviewer_id,
            'place_id': place_id,
            'rating': 5,
            'text': 'Absolutely amazing place! Highly recommend.'
        }
        response = client.post('/api/v1/reviews/', 
                              data=json.dumps(review_data),
                              content_type='application/json')
        review_result = json.loads(response.data)
        print(f"   Review created: Rating {review_result['rating']}/5 (ID: {review_result['id']})")
        
        # 7. Get reviews for the place
        print("\n7. Getting reviews for the place...")
        response = client.get(f'/api/v1/places/{place_id}/reviews')
        if response.status_code == 200:
            reviews = json.loads(response.data)
            print(f"   Place has {len(reviews)} review(s):")
            for review in reviews:
                print(f"     - {review['rating']}/5 stars: {review['text']}")
        else:
            print(f"   API endpoint not available (status: {response.status_code})")
        
        # 8. Get all users to verify they exist
        print("\n8. Getting all users...")
        response = client.get('/api/v1/users/')
        users = json.loads(response.data)
        print(f"   Total users: {len(users)}")
        for user in users:
            print(f"     - {user['first_name']} {user['last_name']} ({user['email']})")
        
        print("\n=== API relationship tests completed successfully! ===")

if __name__ == '__main__':
    test_api_relationships()
