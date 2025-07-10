#!/usr/bin/env python3
"""Test script for API endpoints and relationships."""

import requests
import json
import time
import subprocess
import sys
from threading import Thread

BASE_URL = "http://localhost:5001/api/v1"

def start_flask_app():
    """Start the Flask application in the background."""
    try:
        subprocess.Popen([sys.executable, "run.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(3)  # Give the app time to start
        print("Flask app started...")
    except Exception as e:
        print(f"Error starting Flask app: {e}")

def test_api_relationships():
    """Test the API endpoints and relationships."""
    
    print("=== Testing API Relationships ===\n")
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        print(f"Server status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Starting Flask server...")
        start_flask_app()
        try:
            response = requests.get(f"{BASE_URL}/users", timeout=5)
            print(f"Server status after start: {response.status_code}")
        except Exception as e:
            print(f"Could not connect to server: {e}")
            return
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return
    
    # 1. Create a User
    print("\n1. Creating a User via API...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            user = response.json()
            user_id = user.get('id')
            print(f"   Created user: {user.get('first_name')} {user.get('last_name')} (ID: {user_id})")
        else:
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"   Error creating user: {e}")
        return
    
    # 2. Create Amenities
    print("\n2. Creating Amenities via API...")
    amenities_data = [
        {"name": "WiFi"},
        {"name": "Swimming Pool"},
        {"name": "Free Parking"}
    ]
    
    amenity_ids = []
    for amenity_data in amenities_data:
        try:
            response = requests.post(f"{BASE_URL}/amenities", json=amenity_data)
            if response.status_code in [200, 201]:
                amenity = response.json()
                amenity_ids.append(amenity.get('id'))
                print(f"   Created amenity: {amenity.get('name')} (ID: {amenity.get('id')})")
            else:
                print(f"   Error creating amenity: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # 3. Create a Place
    print("\n3. Creating a Place via API...")
    place_data = {
        "title": "Beautiful Beach House",
        "description": "A lovely house by the beach",
        "price": 150.0,
        "latitude": 25.7617,
        "longitude": -80.1918,
        "owner_id": user_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/places", json=place_data)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            place = response.json()
            place_id = place.get('id')
            print(f"   Created place: {place.get('title')} (ID: {place_id})")
        else:
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"   Error creating place: {e}")
        return
    
    # 4. Add Amenities to Place (if endpoint exists)
    print("\n4. Testing Place-Amenity Relationship...")
    for amenity_id in amenity_ids[:2]:  # Add first two amenities
        try:
            response = requests.post(f"{BASE_URL}/places/{place_id}/amenities/{amenity_id}")
            print(f"   Adding amenity to place: {response.status_code}")
        except Exception as e:
            print(f"   Error adding amenity: {e}")
    
    # 5. Create Reviews
    print("\n5. Creating Reviews via API...")
    
    # Create another user for the second review
    user2_data = {
        "first_name": "Jane",
        "last_name": "Smith", 
        "email": "jane.smith@example.com",
        "password": "securepassword456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users", json=user2_data)
        if response.status_code in [200, 201]:
            user2 = response.json()
            user2_id = user2.get('id')
            print(f"   Created second user: {user2.get('first_name')} (ID: {user2_id})")
    except Exception as e:
        print(f"   Error creating second user: {e}")
        user2_id = user_id  # Fallback to first user
    
    # Create reviews
    reviews_data = [
        {
            "text": "Amazing place! Really enjoyed our stay.",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        },
        {
            "text": "Good location but could be cleaner.",
            "rating": 3,
            "user_id": user2_id,
            "place_id": place_id
        }
    ]
    
    for review_data in reviews_data:
        try:
            response = requests.post(f"{BASE_URL}/reviews", json=review_data)
            if response.status_code in [200, 201]:
                review = response.json()
                print(f"   Created review: {review.get('rating')}/5 stars")
            else:
                print(f"   Error creating review: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # 6. Test Relationship Endpoints
    print("\n=== Testing Relationship Retrieval ===")
    
    # Get user's places
    print("\n6a. Getting User's Places...")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            user_details = response.json()
            print(f"   User: {user_details.get('first_name')} {user_details.get('last_name')}")
            # Check if places are included in response
            places = user_details.get('places', [])
            if places:
                print(f"   User owns {len(places)} place(s)")
            else:
                print("   No places data in user response")
        else:
            print(f"   Error getting user: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Get places (should show owner information)
    print("\n6b. Getting Places...")
    try:
        response = requests.get(f"{BASE_URL}/places")
        if response.status_code == 200:
            places = response.json()
            print(f"   Found {len(places)} place(s)")
            for place in places:
                print(f"     - {place.get('title')} (Owner ID: {place.get('owner_id')})")
        else:
            print(f"   Error getting places: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Get place details with reviews
    print("\n6c. Getting Place Reviews...")
    try:
        response = requests.get(f"{BASE_URL}/places/{place_id}")
        if response.status_code == 200:
            place_details = response.json()
            print(f"   Place: {place_details.get('title')}")
            reviews = place_details.get('reviews', [])
            if reviews:
                print(f"   Has {len(reviews)} review(s)")
            else:
                print("   No reviews data in place response")
        else:
            print(f"   Error getting place details: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Get reviews (should show user and place information)
    print("\n6d. Getting Reviews...")
    try:
        response = requests.get(f"{BASE_URL}/reviews")
        if response.status_code == 200:
            reviews = response.json()
            print(f"   Found {len(reviews)} review(s)")
            for review in reviews:
                print(f"     - {review.get('rating')}/5: {review.get('text')[:50]}...")
        else:
            print(f"   Error getting reviews: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== API Relationship Testing Complete ===")

if __name__ == "__main__":
    test_api_relationships()
