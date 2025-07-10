#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy relationships using API calls
"""
import requests
import json

BASE_URL = "http://localhost:5002/api/v1"

def test_user_creation():
    """Test creating a user"""
    print("🧪 Testing User Creation...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "is_admin": True
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_login_and_get_token():
    """Test user login to get JWT token"""
    print("\n🔐 Testing User Login...")
    login_data = {
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def test_create_amenity(token):
    """Test creating an amenity (admin required)"""
    print("\n🏠 Testing Amenity Creation...")
    headers = {"Authorization": f"Bearer {token}"}
    amenity_data = {"name": "WiFi"}
    
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_create_place(token, user_id, amenity_id):
    """Test creating a place (User-Place relationship)"""
    print("\n🏡 Testing Place Creation...")
    headers = {"Authorization": f"Bearer {token}"}
    place_data = {
        "title": "Cozy Beach House",
        "description": "A beautiful beach house with ocean view",
        "price": 150.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user_id,
        "amenities": [amenity_id] if amenity_id else []
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_create_review(token, place_id):
    """Test creating a review (User-Review and Place-Review relationships)"""
    print("\n⭐ Testing Review Creation...")
    headers = {"Authorization": f"Bearer {token}"}
    review_data = {
        "text": "Amazing place! Highly recommended.",
        "rating": 5,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_get_place_details(place_id):
    """Test getting place details to verify relationships"""
    print(f"\n📄 Testing Place Details (ID: {place_id})...")
    response = requests.get(f"{BASE_URL}/places/{place_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        place_data = response.json()
        print(f"Place: {place_data['title']}")
        print(f"Owner: {place_data['owner']['first_name']} {place_data['owner']['last_name']}")
        print(f"Amenities: {[a['name'] for a in place_data['amenities']]}")
    else:
        print(f"Error: {response.json()}")

def test_get_all_reviews():
    """Test getting all reviews to verify relationships"""
    print("\n📝 Testing All Reviews...")
    response = requests.get(f"{BASE_URL}/reviews/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        reviews = response.json()
        for review in reviews:
            print(f"Review: {review['text'][:50]}... (Rating: {review['rating']})")
            print(f"  User ID: {review['user_id']}")
            print(f"  Place ID: {review['place_id']}")
    else:
        print(f"Error: {response.json()}")

def main():
    """Main test function"""
    print("🚀 Starting Relationship Tests")
    print("=" * 50)
    
    # Test 1: Create User
    user = test_user_creation()
    if not user:
        print("❌ User creation failed. Stopping tests.")
        return
    
    user_id = user.get('id')
    print(f"✅ User created with ID: {user_id}")
    
    # Test 2: Login to get token
    token = test_login_and_get_token()
    if not token:
        print("❌ Login failed. Stopping tests.")
        return
    
    print("✅ Login successful. Token obtained.")
    
    # Test 3: Create Amenity
    amenity = test_create_amenity(token)
    amenity_id = amenity.get('id') if amenity else None
    if amenity_id:
        print(f"✅ Amenity created with ID: {amenity_id}")
    else:
        print("⚠️ Amenity creation failed. Continuing without amenities.")
    
    # Test 4: Create Place (tests User-Place relationship)
    place = test_create_place(token, user_id, amenity_id)
    if not place:
        print("❌ Place creation failed. Stopping tests.")
        return
    
    place_id = place.get('id')
    print(f"✅ Place created with ID: {place_id}")
    
    # Test 5: Create Review (tests User-Review and Place-Review relationships)
    review = test_create_review(token, place_id)
    if review:
        review_id = review.get('id')
        print(f"✅ Review created with ID: {review_id}")
    else:
        print("⚠️ Review creation failed.")
    
    # Test 6: Verify relationships by getting place details
    test_get_place_details(place_id)
    
    # Test 7: Verify relationships by getting all reviews
    test_get_all_reviews()
    
    print("\n" + "=" * 50)
    print("🎉 Relationship tests completed!")

if __name__ == "__main__":
    main()
